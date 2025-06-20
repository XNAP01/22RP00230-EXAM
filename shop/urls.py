from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.order_history, name='order_history'),
    path('signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('category/<str:category_name>/', views.products_by_category, name='products_by_category'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
]
