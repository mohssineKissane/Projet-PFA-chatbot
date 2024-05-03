from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Cart, Order, Product, OrderItem
from django.contrib.auth.decorators import login_required
import random
# Create your views here.


@login_required(login_url='loginpage')
def index(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)
    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.selling_price * item.product_qty
    context = {'cartitems': cartitems, 'total_price': total_price}
    return render(request, "store/checkout.html", context)


@login_required(login_url='loginpage')
def placeorder(request):
    if request.method == 'POST':
        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.Lname = request.POST.get('Lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.postalcode = request.POST.get('postalcode')

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price += item.product.selling_price * item.product_qty

        neworder.total_price = cart_total_price
        neworder.save()

        for item in cart:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )
            item.product.quantity -= item.product_qty
            item.product.save()

        cart.delete()
        messages.success(request, "Your order has been placed successfully")
        return redirect('listorder')


def listorder(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, "store/order.html", context)
