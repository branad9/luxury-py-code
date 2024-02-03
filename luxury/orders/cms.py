from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import *
from .forms import OrderForm
from django.http import HttpResponse
import csv
from django.template.loader import render_to_string
from django.conf import settings


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def export_csv_orders(request):
    resp = HttpResponse(content_type="text/csv")
    writer = csv.writer(resp)
    writer.writerow(["User", "Order No", "Total", "Status"])
    orders = Order.objects.all()
    for ord in orders.values_list(
        "user__full_name", "order_number", "order_total", "status"
    ):
        writer.writerow(ord)
    resp["Content-Disposition"] = 'attachment; filename="orders.csv"'
    return resp


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def orders(request):
    sort = request.GET.get("sort") or "-created"
    all_orders = Order.objects.order_by(sort)
    paginator = Paginator(all_orders, 30)
    page = request.GET.get("page")
    paged_orders = paginator.get_page(page)
    return render(request, "cms/orders.html", {"orders": paged_orders})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_order(request, id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return redirect("cms_orders")
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            if form.cleaned_data["status"] == "Cancelled":
                order.cancelled_by = request.user
            else:
                order.cancelled_by = None
                order.cancellation_reason = None
            order.save()
            return redirect("cms_orders")
        else:
            messages.error(request, form.errors)
            return render(
                request, "cms/edit-order.html", {"form": form, "order": order}
            )
    else:
        form = OrderForm(instance=order)
        return render(request, "cms/edit-order.html", {"form": form, "order": order})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def order_items(request, oid):
    order = get_object_or_404(Order, id=oid)
    items = OrderItem.objects.filter(order_id=oid).select_related(
        "product", "variation"
    )
    paginator = Paginator(items, 30)
    page = request.GET.get("page")
    paged_items = paginator.get_page(page)
    return render(
        request, "cms/order-items.html", {"order": order, "order_items": paged_items}
    )


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def user_details(request, uid):
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        user = None
    return render(request, "cms/modals/user-details.html", {"user": user})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_order(request, id):
    try:
        order = Order.objects.get(id=id)
        order.delete()
    except Order.DoesNotExist:
        pass
    return redirect("cms_orders")
