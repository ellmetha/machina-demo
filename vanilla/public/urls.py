from django.conf.urls import include
from django.conf.urls import url

from .account.urls import urlpatterns as account_urlpatterns


urlpatterns = [
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^account/', include(account_urlpatterns, 'account')),
]
