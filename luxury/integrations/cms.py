
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import IntegrationForm
from .models import Integration

@login_required
@user_passes_test(lambda user: user.is_superadmin)
def list_integrations(request):
    integrations = Integration.objects.all()

    return render(request, 'cms/integrations/list.html', {'integrations': integrations})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_integration(request):
    if request.method == 'POST':
        form = IntegrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('cms_integrations'))
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/integrations/add.html', {'form': form})        
    else:
        form = IntegrationForm()
        return render(request, 'cms/integrations/add.html', {'form': form})
    

@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_integration(request, pk):
    try:
        integration = Integration.objects.get(pk=pk)
    except Integration.DoesNotExist:
        return redirect(reverse('cms_integrations'))

    if request.method == 'POST':
        form = IntegrationForm(request.POST, instance=integration)
        if form.is_valid():
            form.save()
            return redirect(reverse('cms_integrations'))
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/integrations/edit.html', {'form': form})        
    else:
        form = IntegrationForm(instance=integration)
        return render(request, 'cms/integrations/edit.html', {'form': form})
    
    
@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_integration(request, pk):
    try:
        Integration.objects.filter(pk=pk).delete()
    except Integration.DoesNotExist:
        return redirect(reverse('cms_integrations'))

    return redirect(reverse('cms_integrations'))
