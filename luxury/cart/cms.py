from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages
from cart.models import CartItem
from .serializers import *
import requests
import json
import csv



def api_send_msg(number, msg):
    header = {"Content-Type": "application/json"}
    payload = {
                "app": {
                    "id": "917208128600",
                    "time": 1656040106,
                    "data": {
                        "recipient": {
                            "id": f"91{number}"
                        },
                        "message": [
                            {
                                "time": 1656040106,
                                "type": "text",
                                "value": msg
                            }
                        ]
                    }
                }
            }
    resp = requests.post("https://whapi.io/api/send", headers=header, data=json.dumps(payload))
    return resp.status_code


@login_required
def export_csv_cart(request):
    resp = HttpResponse(content_type='text/csv')
    writer = csv.writer(resp)
    writer.writerow(['User', 'Product', 'Qty', 'Total'])
    items = CartItem.objects.all()
    for item in items.values_list('user__full_name', 'product__name', 'qty', 'total'):
        writer.writerow(item)
    resp['Content-Disposition'] = 'attachment; filename="carts.csv"'
    return resp


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def cart(request):
    sort = request.GET.get('sort') or '-created'
    items = CartItem.objects.order_by(sort)
    paginator = Paginator(items, 30)
    page = request.GET.get('page')
    paged_items = paginator.get_page(page)
    return render(request, 'cms/cart.html', {'items': paged_items})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def send_msg(request, uid):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=uid)
            if user.phone is None:
                messages.error(request, f'{user} has not verified phone number.')
                return redirect('cms_cart')
            msg =  request.POST.get('message')    
            text = api_send_msg(user.phone, msg)
            if text >= 200 and text <= 299:
                 messages.success(request, 'Message sent successfully.')
            else:    
                 messages.error(request, 'Something went wrong while sending message.')
        except User.DoesNotExist:
            pass
        return redirect('cms_cart')    
    else:            
        return render(request, 'cms/modals/send-msg.html', {'uid': uid})
        
        
@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_cart(request, id):
    try:
        cart = CartItem.objects.get(id=id)
        cart.delete()
    except CartItem.DoesNotExist:
        pass    
    return redirect('cms_cart')
    
    
    
    
    
