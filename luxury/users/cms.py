from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .filters import UserFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .serializers import UserSerializer
from django.db.models import Q
from .forms import *
from django.http import HttpResponse
from home.models import Settings
import csv
from io import StringIO
from datetime import datetime, timedelta

from home.tasks import email_notification


@login_required
def export_csv_customers(request):
    resp = HttpResponse(content_type="text/csv")
    writer = csv.writer(resp)
    writer.writerow(["Full Name", "Email", "Phone"])
    users = User.objects.filter(is_superadmin=False)
    for u in users.values_list("full_name", "email", "phone"):
        writer.writerow(u)
    resp["Content-Disposition"] = 'attachment; filename="customers.csv"'
    return resp


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def users(request):
    all_users = User.objects.filter(is_superadmin=True).order_by("-created")
    filters = UserFilter(request.GET, queryset=all_users)
    filtered_users = filters.qs
    paginator = Paginator(filtered_users, 30)
    page = request.GET.get("page")
    paged_users = paginator.get_page(page)
    return render(
        request, "cms/users/index.html", {"users": paged_users, "filters": filters}
    )


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def customers(request):
    sort = request.GET.get("sort") or "-created"
    all_users = User.objects.filter(is_superadmin=False).order_by(sort)
    filters = UserFilter(request.GET, queryset=all_users)
    filtered_users = filters.qs
    paginator = Paginator(filtered_users, 30)
    page = request.GET.get("page")
    paged_users = paginator.get_page(page)
    return render(
        request, "cms/users/customers.html", {"users": paged_users, "filters": filters}
    )


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            password = form.cleaned_data["password"]
            is_superadmin = form.cleaned_data["is_superadmin"]
            if is_superadmin:
                User.objects.create_superuser(
                    full_name=full_name, email=email, phone=phone, password=password
                )
            else:
                User.objects.create_user(
                    full_name=full_name, email=email, phone=phone, password=password
                )
            return redirect("cms_users")
        else:
            messages.error(request, form.errors)
            return render(request, "cms/users/add.html", {"form": form})
    else:
        form = UserForm(None)
        return render(request, "cms/users/add.html", {"form": form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return redirect("cms_users")
    if request.method == "POST":
        form = EditUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            if user.is_superadmin:
                return redirect("cms_users")
            else:
                return redirect("cms_customers")
        else:
            messages.error(request, form.errors)
            return render(request, "cms/users/edit.html", {"form": form, "id": id})
    else:
        form = EditUserForm(instance=user)
        return render(request, "cms/users/edit.html", {"form": form, "id": id})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_customer(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return redirect("cms_users")
    if request.method == "POST":
        form = EditCustomerForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            if user.is_superadmin:
                return redirect("cms_users")
            else:
                return redirect("cms_customers")
        else:
            messages.error(request, form.errors)
            return render(
                request, "cms/users/customer_edit.html", {"form": form, "id": id}
            )
    else:
        form = EditCustomerForm(instance=user)
        return render(request, "cms/users/customer_edit.html", {"form": form, "id": id})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def change_password(request, id):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.")
        else:
            user = get_object_or_404(User, id=id)
            user.set_password(confirm_password)
            user.save()
            return redirect("cms_users")
    return render(request, "cms/users/change_password.html")


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_user(request, id):
    try:
        usr = User.objects.get(id=id)
        if usr.is_superadmin:
            if User.objects.filter(is_superadmin=True).count() <= 1:
                messages.error(request, "Cannot delete the only super admin.")
            else:
                usr.email = f"{usr.email}-{usr.id}"
                usr.save()
                User.objects.filter(id=id).delete()
        else:
            usr.email = f"{usr.email}-{usr.id}"
            usr.save()
            User.objects.filter(id=id).delete()
    except User.DoesNotExist:
        pass
    return redirect("cms_users")


def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("cms_home")
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, "cms/users/login.html")


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out.")
    return redirect("cms_login")


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
            message = render_to_string("users/reset_email_password.html", context)
            email_notification(subject, message, [email])
            messages.success(
                request, "Password reset mail has been sent to your email address."
            )
            return redirect("cms_login")
        else:
            messages.error(request, "User does not exist.")
            return redirect("forgot_password")
    return render(request, "cms/users/forgot_password.html")


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your password.")
        return redirect("cms_reset_password")
    else:
        messages.error(request, "The link is expired.")
        return redirect("cms_login")


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
            return redirect("cms_login")
        else:
            messages.error(request, "Passwords do not match.")
            return redirect("cms_reset_password")
    else:
        return render(request, "cms/users/reset_password.html")


@api_view(["GET"])
def api_users(request):
    all_users = User.objects.filter(is_superadmin=False, is_admin=False)
    paginator = PageNumberPagination()
    paginator.page_size = 15
    users_pages = paginator.paginate_queryset(all_users, request)
    serializer = UserSerializer(users_pages, many=True)
    if serializer:
        return Response(
            {
                "status": True,
                "data": serializer.data,
                "prev": paginator.get_previous_link(),
                "next": paginator.get_next_link(),
            }
        )
    else:
        return Response({"status": False, "errors": serializer.errors})


@api_view(["GET"])
def cron_new_customers(request):
    try:
        customers = (
            User.objects.filter(is_superadmin=False)
            .filter(Q(created__date__gte=datetime.now() - timedelta(hours=24)))
            .order_by("-created")
        )  # .filter(Q(created__date__gte=datetime.now() - timedelta(hours=24)))
        # if carts.count() <= 0:
        #     return Response({'status': False, 'msg': 'No orphan carts'})
        csvfile = StringIO()
        writer = csv.writer(csvfile)
        writer.writerow(["Full Name", "Email", "Phone", "Status"])
        for item in customers.values_list("full_name", "email", "phone", "is_active"):
            writer.writerow(item)
        mail_subject = "New Customers"
        message = render_to_string("cms/users/cron_customers_mail.html")
        go_email = Settings.objects.all().first().email
        attachment = {
            "filename": "carts.csv",
            "content": csvfile.getvalue(),
            "mimetype": "text/csv",
        }
        email_notification(mail_subject, message, [go_email], [attachment])
        return Response({"status": True})
    except Exception as e:
        return Response({"status": False, "error": f"{e}"})
