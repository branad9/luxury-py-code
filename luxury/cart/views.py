from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cart.models import CartItem
from users.models import Address
from .serializers import *
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q
from datetime import timedelta, datetime
from io import StringIO
from home.models import Settings
import csv
import json

from home.tasks import email_notification


@login_required(login_url="login")
def cart(request):
    user_phone = request.user.phone
    if user_phone is None:
        check_phone = False
    else:
        check_phone = True
    address = Address.objects.filter(user=request.user, default=True)
    return render(
        request,
        "web/cart.html",
        {"check_phone": json.dumps(check_phone), "address": address},
    )


@api_view(["GET"])
@login_required(login_url="login")
def get_cart(request):
    items = CartItem.objects.filter(user=request.user)
    serializer = ReadCartItemSerializer(items, many=True)
    if serializer:
        return Response({"status": True, "data": serializer.data})
    else:
        return Response({"status": False, "errors": serializer.errors})


@api_view(["POST"])
@login_required(login_url="login")
def delete_cart(request):
    cart_id = request.POST.get("cart_id")
    try:
        CartItem.objects.filter(id=cart_id).delete()
        return Response(
            {"status": True, "success": {"Mesage": "Cartitem deleted successfully."}}
        )
    except CartItem.DoesNotExist:
        return Response({"status": False, "errors": {"Error": "Cartitem not found."}})


@api_view(["POST"])
@login_required(login_url="login")
def change_cart(request):
    product = request.POST.get("product")
    variation = request.POST.get("variation")
    total = request.POST.get("total")
    qty = request.POST.get("qty")
    if variation != "0":
        data = {
            "user": request.user.id,
            "product": product,
            "variation": variation,
            "total": total,
            "qty": qty,
        }
        cart_item = CartItem.objects.filter(
            user=request.user, product_id=product, variation_id=variation
        )
    else:
        data = {"user": request.user.id, "product": product, "total": total, "qty": qty}
        cart_item = CartItem.objects.filter(user=request.user, product_id=product)
    if cart_item.exists():
        serializer = CartItemSerializer(cart_item[0], partial=True, data=data)
    else:
        serializer = CartItemSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": True})
    else:
        return Response({"status": False, "errors": serializer.errors})


@api_view(["GET"])
def cron_orphan_carts(request):
    try:
        # carts = CartItem.objects.filter(Q(created__date=datetime.now()))
        carts = CartItem.objects.filter(
            Q(created__date__gte=datetime.now() - timedelta(hours=24))
        )
        # if carts.count() <= 0:
        #     return Response({'status': False, 'msg': 'No orphan carts'})
        csvfile = StringIO()
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Product", "Qty", "Total"])
        for item in carts.values_list(
            "user__full_name", "product__name", "qty", "total"
        ):
            writer.writerow(item)
        mail_subject = "Orphan Carts"
        message = render_to_string("web/cron_mail.html")
        send_email = Settings.objects.all().first().email
        attachment = {
            "filename": "carts.csv",
            "content": csvfile.getvalue(),
            "mimetype": "text/csv",
        }
        email_notification(mail_subject, message, [send_email], [attachment])
        return Response({"status": True})
    except Exception as e:
        return Response({"status": False, "error": f"{e}"})
