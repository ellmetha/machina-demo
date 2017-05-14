from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^parameters/edit/', views.UserAccountParametersUpdateView.as_view(), name='parameters'),
    url(r'^password/edit/', views.UserPasswordUpdateView.as_view(), name='password'),
    url(r'^register/', views.UserCreateView.as_view(), name='register'),
    url(r'^unregister/', views.UserDeleteView.as_view(), name='unregister'),
]
