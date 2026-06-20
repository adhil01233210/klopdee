from django.urls import path

from.import views
urlpatterns=[
    path('',views.index,name='home'),
    path('index/',views.index,name='index'),
    path('io/',views.index,name='io'),
    path('home/',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('add_product/', views.add_product, name='add_product'),
    path('add-product/', views.add_product, name='add_product'),
    path('product_list/', views.product_list, name='product_list'),
    path('my_products/', views.my_products, name='my_products'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/',views.delete_product, name='delete_product'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/increase/<int:pk>/',views.increase_quantity,name='increase_quantity'),
    path('cart/decrease/<int:pk>/', views.decrease_quantity, name='decrease_quantity'),
    path( 'cart/remove/<int:pk>/',views.remove_from_cart,name='remove_from_cart'),
    path('my_cart/', views.cart, name='my_cart'),
]
