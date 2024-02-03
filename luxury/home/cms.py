from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from campaigns.models import *
from django.contrib import messages
from .forms import SettingsForm
from home.models import Settings
from orders.models import Order
from users.models import User
from datetime import datetime, date, timedelta



@login_required
@user_passes_test(lambda user: user.is_superadmin)
def home(request):
    now = datetime.now()
    seven_days = date.today() - timedelta(days=7)
    all_orders = Order.objects.count()
    monthly_orders = Order.objects.filter(created__month=now.month).count()
    yearly_orders = Order.objects.filter(created__year=now.year).count()
    weekly_orders = Order.objects.filter(created__gte=seven_days).count()
    all_customers = User.objects.filter(is_superadmin=False).count()
    monthly_customers = User.objects.filter(created__month=now.month, is_superadmin=False).count()
    yearly_customers = User.objects.filter(created__year=now.year, is_superadmin=False).count()
    weekly_customers = User.objects.filter(created__gte=seven_days, is_superadmin=False).count()
    context = {'all_orders': all_orders, 'weekly_orders': weekly_orders, 'monthly_orders': monthly_orders, 'yearly_orders': yearly_orders,
               'all_customers': all_customers, 'monthly_customers': monthly_customers, 'yearly_customers': yearly_customers, 
               'weekly_customers': weekly_customers}
    return render(request, 'cms/home/index.html', context)


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def send_message(request):
    return render(request, 'cms/messages/send.html')


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def settings(request):
    obj = Settings.objects.all()
    return render(request, 'cms/settings/index.html', {'settings': obj})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def change_settings(request):
    if Settings.objects.all().count() <= 0:
        if request.method == 'POST':
            form = SettingsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('cms_settings')
            else:
                messages.error(request, form.errors)
                return render(request, 'cms/settings/add.html', {'form': form})        
        else:
            form = SettingsForm(None)
            return render(request, 'cms/settings/add.html', {'form': form})
    else:   
        try:
            setting = Settings.objects.all()[0]
        except Settings.DoesNotExist:
            return redirect('cms_settings')
        if request.method == 'POST':
            form = SettingsForm(request.POST, instance=setting)
            if form.is_valid():
                form.save()
                return redirect('cms_settings')
            else:
                messages.error(request, form.errors)
                return render(request, 'cms/settings/edit.html', {'form': form})        
        else:
            form = SettingsForm(instance=setting)
            return render(request, 'cms/settings/edit.html', {'form': form})