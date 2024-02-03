from django.urls import path

from . import cms

cms_patterns = [
    path('cms/misc/robots/', cms.robots, name='cms_misc_robots')
]

urlpatterns = [
    
]

urlpatterns += cms_patterns