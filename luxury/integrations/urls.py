from . import cms
from django.urls import path


cms_patterns = [
    path('cms/integrations/', cms.list_integrations, name='cms_integrations'),
    path('cms/integrations/add/', cms.add_integration, name='cms_add_integration'),
    path('cms/integrations/<int:pk>/edit/', cms.edit_integration, name='cms_edit_integration'),
    path('cms/integrations/<int:pk>/delete/', cms.delete_integration, name='cms_delete_integration'),
]

urlpatterns = [
    
]
    
urlpatterns += cms_patterns
