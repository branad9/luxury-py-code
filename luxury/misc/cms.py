from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from pathlib import Path

from .forms import RobotsForm

def robots(request):
    robots_file_path = settings.BASE_DIR / 'robots.txt'
    Path(robots_file_path).touch(exist_ok=True)

    if request.method == 'POST':
        form = RobotsForm(request.POST)
        if form.is_valid():
            with open(robots_file_path, 'w') as file:
                content = file.write(form.cleaned_data['content'])

            return redirect(reverse('cms_misc_robots'))
        else:
            return render(request, 'cms/robots.html', {'form': form})

    with open(robots_file_path) as file:
        content = file.read()

    form = RobotsForm(initial={'content': content})
    return render(request, 'cms/robots.html', {'form': form})


