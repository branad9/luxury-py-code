from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
from cart.models import CartItem
from .serializers import *
from users.models import Address
from django.template.loader import render_to_string
from rest_framework.pagination import PageNumberPagination
from home.models import Settings
from home.tasks import email_notification


@login_required
def ordered(request):
    return render(request, "web/ordered.html")


@api_view(["POST"])
@login_required
def place_order(request):
    user = request.user
    total = request.POST.get("total")
    cart_items = CartItem.objects.filter(user=user)
    def_add = Address.objects.filter(user=request.user, default=True)
    if def_add.count() <= 0:
        return Response(
            {
                "status": False,
                "no_address": True,
                "errors": "Please select delivery address",
            }
        )
    items = []
    for ci in cart_items:
        if ci.variation is not None:
            variation_id = ci.variation.id
        else:
            variation_id = None
        items.append(
            {
                "product": ci.product.id,
                "variation": variation_id,
                "qty": ci.qty,
                "price": ci.total,
            }
        )
    data = {
        "user": user.id,
        "order_total": total,
        "delivery_charges": 0,
        "status": "Ordered",
        "items": items,
    }
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        obj = serializer.save()
        obj.order_number = f"ORD-{obj.id}"
        obj.save()
        cart_items.delete()
        # send mail to customer and admin
        context = {"user": request.user, "order": obj}
        message = render_to_string("web/order_mail.html", context, request)
        go_email = Settings.objects.all().first().email
        email_notification("Order Placed Successfully.", message, [request.user.email])

        message_admin = render_to_string("web/order_mail_admin.html", context, request)
        email_notification(
            "New Order Placed.", message_admin, [go_email]
        )
        cart_items.delete()
        return Response({"status": True})
    else:
        return Response({"status": False, "errors": serializer.errors})


@api_view(["GET"])
@login_required
def all_orders(request):
    orders = Order.objects.filter(user=request.user)
    paginator = PageNumberPagination()
    paginator.page_size = 3
    order_pages = paginator.paginate_queryset(orders, request)
    serializer = ReadOrderSerializer(order_pages, many=True)
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


@api_view(["POST"])
@login_required
def cancel_order(request):
    order_id = request.POST.get("order_id")
    cancellationReason = request.POST.get("cancellationReason")
    try:
        order = Order.objects.get(id=order_id)
        order.status = "Cancelled"
        order.cancelled_by = request.user
        order.cancellationReason = cancellationReason
        order.save()
        return Response({"status": True})
    except Order.DoesNotExist:
        return Response({"status": False})
