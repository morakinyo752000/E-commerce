from django.urls import path
from home import views
from order import views as OrderViews
from user import views as UserViews

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<int:id>/<slug:slug>', views.category_products, name='category_products'),
    path('search/', views.search, name='search'),
    path('search_auto', views.search_auto, name='search_auto'),
    path('product/<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('cart/', OrderViews.cart, name='cart'),
    path('login/', UserViews.login_form, name='login_form'),
    path('signup/', UserViews.signup_form, name='signup_form'),
    path('logout/', UserViews.logout_func, name='logout_func'),
    path('user/', UserViews.user, name='user'),
    path('faq/', UserViews.faq, name='faq'),

]