from django.conf.urls.defaults import *

urlpatterns = patterns('apply_linkedin.django.views',
    
    url(r'process_application/$', 'process_application', name='apply_linkedin.process_application'),
    
)