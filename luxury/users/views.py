from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import User, Wishlist
from orders.models import Order
from .serializers import *
from .forms import RegisterForm
from cart.cms import api_send_msg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Prefetch
import math, random
import json

from home.models import Settings
from home.tasks import email_notification


def generate_otp():
    digits = "0123456789"
    otp = ""
    for i in range(6):
        otp += digits[math.floor(random.random() * 10)]
    return otp


code = generate_otp()


@login_required
def verify_phone(request):
    verify_type = request.session.get("verify_type", "phone")
    if request.method == "POST":
        if "phone_form" in request.POST:
            phone = request.POST["phone"]
            request.session["user_phone"] = phone
            request.session["verify_type"] = "otp"
            verify_type = request.session.get("verify_type", "phone")
            otp = api_send_msg(phone, f"The OTP for verification is {code}.")
            messages.success(request, "Please check Whatsapp for OTP verification.")
        if "otp_form" in request.POST:
            otp = request.POST["otp"]
            if otp == code:
                user = request.user
                user.phone = request.session.get("user_phone", None)
                user.save()
                del request.session["user_phone"]
                del request.session["verify_type"]
                return redirect("cart")
            else:
                messages.error(request, "Incorrect OTP. Failed to verify phone number.")
    return render(request, "web/verify_phone.html", {"verify_type": verify_type})


def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid login credentials")
    return render(request, "web/login.html")


def register(request):
    if request.method == "POST":
        fm = RegisterForm(request.POST)
        if User.objects.filter(email=fm.data["email"]).exists():
            messages.error(request, "This email is already registered")
            return redirect("register")
        if fm.data["password"] != fm.data["confirm_password"]:
            messages.error(request, "Password and confirm pasword do not match.")
            return redirect("register")
        if fm.is_valid():
            full_name = fm.cleaned_data["full_name"]
            email = fm.cleaned_data["email"]
            password = fm.cleaned_data["password"]
            user = User.objects.create_user(
                full_name=full_name, email=email, password=password
            )
            # User Activation through email
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string(
                "web/verify_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            email_notification(mail_subject, message, [email])

            # Email notificaiton to admin
            setting = Settings.objects.first()

            mail_subject = "New User Registered"
            message = render_to_string(
                "emails/user_registration_notification.html", {"user": user}
            )
            email_notification(mail_subject, message, [setting.email])

            messages.success(
                request, "Please activate your account from the link sent on the mail."
            )
            return redirect("/user/login?command=verification&email=" + email)
    else:
        fm = RegisterForm()
    return render(request, "web/register.html", {"form": fm})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations, your account is activated")
        return redirect("login")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("register")


@login_required(login_url="login")
def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out.")
    return redirect("login")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # reset password email
            current_site = get_current_site(request)
            subject = "Reset your password"
            context = {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            }
            message = render_to_string("web/reset_email_password.html", context)
            email_notification(subject, message, [email])
            messages.success(
                request, "Password reset mail has been sent to your email address."
            )
            return redirect("login")
        else:
            messages.error(request, "User does not exist.")
            return redirect("forgot_password")
    return render(request, "web/forgot_password.html")


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your password.")
        return redirect("reset_password")
    else:
        messages.error(request, "The link is expired.")
        return redirect("login")


def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            uid = request.session.get("uid")
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful.")
            return redirect("login")
        else:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password")
    else:
        return render(request, "web/reset_password.html")


@login_required(login_url="login")
def wishlist(request):
    return render(request, "web/wishlist.html")


@api_view(["GET"])
@login_required(login_url="login")
def get_wishlist(request):
    list = Wishlist.objects.filter(user=request.user)
    serializer = ReadWishlistSerializer(list, many=True)
    if serializer:
        return Response({"status": True, "data": serializer.data})
    else:
        return Response({"status": False, "errors": serializer.errors})


@api_view(["POST"])
@login_required(login_url="login")
def add_wishlist(request):
    product = request.POST.get("product")
    variation = request.POST.get("variation")
    if variation != "0":
        data = {"user": request.user.id, "product": product, "variation": variation}
        list = Wishlist.objects.filter(
            user=request.user, product_id=product, variation_id=variation
        )
    else:
        data = {"user": request.user.id, "product": product}
        list = Wishlist.objects.filter(user=request.user, product_id=product)
    if list.exists():
        return Response({"status": True})
    serializer = WishlistSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": True})
    else:
        return Response({"status": False, "errors": serializer.errors})


@api_view(["POST"])
@login_required(login_url="login")
def delete_wishlist(request):
    try:
        wid = request.POST.get("wid")
        Wishlist.objects.filter(id=wid).delete()
        return Response(
            {"status": True, "success": {"Message": "Wishlist deleted successfully."}}
        )
    except Wishlist.DoesNotExist:
        return Response({"status": False, "errors": {"Error": "Wishlist not found."}})


@login_required(login_url="login")
def user_dashboard(request):
    # orders = Order.objects.filter(user=request.user).prefetch_related('orderitems', 'orderitems__product', 'orderitems__product__images')
    orders = Order.objects.filter(user=request.user).prefetch_related(
        "orderitems",
        "orderitems__product",
        Prefetch(
            "orderitems__product__images",
            queryset=ProductImage.objects.filter(default=True),
        ),
    )
    return render(request, "web/dashboard.html", {"orders": orders})


@api_view(["GET"])
@login_required(login_url="login")
def api_get_addresses(request):
    list = Address.objects.filter(user=request.user)
    serializer = AddressSerializer(list, many=True)
    if serializer:
        return Response({"status": True, "data": serializer.data})
    else:
        return Response({"status": False, "errors": serializer.errors})


@api_view(["GET"])
@login_required(login_url="login")
def api_address_details(request):
    aid = request.GET.get("aid")
    try:
        address = Address.objects.get(id=aid)
        serializer = AddressSerializer(instance=address)
        return Response({"status": True, "data": serializer.data})
    except Address.DoesNotExist:
        return Response({"status": False, "errors": "Address not found"})


@api_view(["POST"])
@login_required(login_url="login")
def api_address_change_default(request):
    aid = request.POST.get("aid")
    try:
        Address.objects.filter(user=request.user).update(default=False)
        address = Address.objects.get(id=aid)
        address.default = True
        address.save()
        return Response({"status": True, "errors": "Address defaulted"})
    except Address.DoesNotExist:
        return Response({"status": False, "errors": "Address not found"})


@api_view(["POST"])
@login_required(login_url="login")
def api_add_address(request):
    json_address = request.POST.get("address")
    address = json.loads(json_address)
    print(f"adding address {address}")
    data = {
        "user": request.user.id,
        "type": address["type"],
        "address": address["address"],
        "locality": address["locality"],
        "city": address["city"],
        "pincode": address["pincode"],
    }
    serializer = AddressSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": True})
    else:
        return Response({"status": False, "errors": serializer.errors})


@api_view(["POST"])
@login_required(login_url="login")
def api_edit_address(request):
    json_address = request.POST.get("address")
    resp_address = json.loads(json_address)
    aid = resp_address["id"]
    try:
        address = Address.objects.get(id=aid)
    except Address.DoesNotExist:
        return Response({"status": False, "errors": "Address not found"})
    data = {
        "user": request.user.id,
        "type": resp_address["type"],
        "address": resp_address["address"],
        "locality": resp_address["locality"],
        "city": resp_address["city"],
        "pincode": resp_address["pincode"],
    }
    serializer = AddressSerializer(address, partial=True, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": True})
    else:
        return Response({"status": False, "errors": serializer.errors})


@api_view(["POST"])
@login_required(login_url="login")
def api_delete_address(request):
    aid = request.POST.get("aid")
    try:
        Address.objects.filter(id=aid).delete()
        return Response(
            {"status": True, "success": {"Message": "Address deleted successfully."}}
        )
    except Wishlist.DoesNotExist:
        return Response({"status": False, "errors": {"Error": "Address not found."}})
