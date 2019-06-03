from django.conf.urls import include, url


urlpatterns = [
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^account/', include('main.public.account.urls')),
]
