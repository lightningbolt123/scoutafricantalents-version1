from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.store_view, name='store'),
    path('payment-successful/', views.payment_successful, name='payment-successful'),
    path('check-out/', views.checkout, name='check-out'),
    path('payment-canceled/', views.payment_canceled, name='payment-canceled'),
    re_path(r'^(?P<id>[\w-]+)/$', views.subscribe, name='subscribe'),

]