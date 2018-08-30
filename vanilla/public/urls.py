from django.conf.urls import include
from django.conf.urls import url


urlpatterns = [
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^account/', include('vanilla.public.account.urls')),
]
