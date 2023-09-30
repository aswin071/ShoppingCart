from django.urls import path
from .import views

urlpatterns = [
    path("",views.signup, name="signup"),
    path("login/",views.user_login, name="login"),
    path("home",views.index, name="home"),
    path("logout/",views.user_logout, name="logout"),
    path("products/",views.ProductPage, name="products"),
    path("addproduct/", views.addProduct, name="addproduct"),
    path('<int:id>/deleteProduct/', views.deleteProduct, name="deleteProduct"),
    path('<int:id>/editProduct/', views.editProduct, name='editProduct'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
]
