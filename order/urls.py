from django.urls import path
from order import views


urlpatterns = [
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderproduct/', views.orderproduct, name='orderproduct'),
    path('ordercompleted/', views.ordercompleted, name='ordercompleted'),

]