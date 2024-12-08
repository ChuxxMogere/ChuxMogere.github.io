"""
URL configuration for marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LogoutView
from django.urls import path

from market import views
from market.views import profile_view

urlpatterns = [

    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('buyer_dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('farmer_dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('delete_product/<int:id>/',views.delete_product, name='delete_product'),
    path('product_detail/<int:id>/',views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_item/<int:id>/', views.update_cart_item, name='update_cart_item'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('order_success/', views.order_success, name='order_success'),
    path('weather_updates/',views.weather_updates, name='weather_updates'),
    path('profile/', profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('farmer_notifications/', views.farmer_notifications, name='farmer_notifications'),



]