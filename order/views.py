from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string

# Create your views here.
from order.models import ShopCart, ShopCartForm, OrderForm, OrderProduct, Order
from product.models import Category, Product
from user.models import UserProfile


@login_required(login_url='/login')
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    checkproduct = ShopCart.objects.filter(product_id=id)
    if checkproduct:
        control = 1
    else:
        control = 0

        if request.method == 'POST':
            form = ShopCartForm(request.POST)
            if form.is_valid():
                if control == 1:
                    data = ShopCart.objects.get(product_id=id)
                    data.quantity += form.cleaned_data['quantity']
                    data.save()
                else:
                    data = ShopCart()
                    data.user_id = current_user.id
                    data.product_id = id
                    data.quantity = form.cleaned_data['quantity']
                    data.save()
            messages.success(request, 'SuccessFully added to Cart')
            return HttpResponseRedirect(url)

        else:
            if control == 1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += 1
                data.save()
            else:
                data= ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = 1
                data.save()
                messages.success(request, 'SuccessFully added to Cart')
                return HttpResponseRedirect(url)


def cart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        # return HttpResponse(str(total))

    context = {
        'category': category,
        'shopcart': shopcart,
        'total': total,
    }
    return render(request, 'cart.html', context)

def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, 'Your Item deleted from ShopCart')
    return HttpResponseRedirect('/cart')


def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    total = 0
    for rs in schopcart:
        total += rs.product.price * rs.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        # return HttpResponse(str(total))
        if form.is_valid():

            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            schopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in schopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                data.product_id = rs.product_id   
                data.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request, 'Your Order has been completed. Thank You')
            return render(request, 'Order_Completed.html', {'ordercode':ordercode, 'category':category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form =OrderForm()
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)

    context = {'category': category,'schopcart': schopcart,'total': total,'profile': profile,'form':form}
    return render(request, 'order_form.html', context)


def ordercompleted(request):
    return render(request, 'order_completed.html')