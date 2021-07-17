from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import CookieCart,cartData
# Create your views here.

def home(request):
    products = Product.objects.all
    data = cartData(request)
    items = data['items']
    order = data['order']
    context = {
        'items' : items,
        'order':order,
        'products':products,
    }
    return render(request,'store/store.html',context)

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']

    context = {
        'items' : items,
        'order':order
    }

    return render(request,'store/cart.html',context)


def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    context = {
        'items' : items,
        'order':order
    }
    return render(request,'store/checkout.html',context)

def updatacart(request):
    data = json.loads(request.body)
    productid = data['productid']
    action = data['action']

    # print(action)
    # print(productid)

    customer = request.user.customer
    product = Product.objects.get(id=productid)
    order,created = Order.objects.get_or_create(customer=customer,completed=False)
    orderitem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderitem.quantity += 1
    elif action == 'remove':
        orderitem.quantity -= 1

    orderitem.save()
    if orderitem.quantity == 0:
        orderitem.delete()

    return JsonResponse("added to cart",safe=False)

def contact_us(request):
    return render(request,'store/contact-us.html')

def about_us(request):
    return render(request,'store/about.html')

def orderprocess(request):
    transaction_id = datetime.datetime.now().timestamp()
    # order,created = Order.objects.get_or_create(customer=customer,completed=False)
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,completed=False)
        
    else:
        name = data['form']['name']
        email = data['form']['InputEmail']
        cookie = CookieCart(request)

        customer,created = Customer.objects.get_or_create(name=name,email=email) 
        customer.name = name
        customer.save()
        order = Order.objects.create(customer=customer,completed=False)
        items = cookie['items']

        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            orderitem = OrderItem.objects.create(
                product=product,
                quantity=item['quantity'],
                order=order
            )
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.completed = True
    order.save()

    if order.shipping == True:
        Shipping.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['country'],
            country=data['shipping']['state'],
            zipcode=data['shipping']['zip'],
        )
    return JsonResponse('Order Placed',safe=False)