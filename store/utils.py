from .models import *
import json

def CookieCart(request):
    try:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        
        items = []
        order = {
            'get_cart_total': 0,
            'get_item_total' : 0,
            'shipping':False,
        }

        for i in cart:
            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']
            order['get_item_total'] += cart[i]['quantity']
            order['get_cart_total'] += total

            item = {
                'product' : {
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        
    except:
        pass

    return {'items':items,'order':order}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,completed=False)
        items = order.orderitem_set.all()
    else:
        cookiedata = CookieCart(request)
        items = cookiedata['items']
        order = cookiedata['order']
    
    return {'order':order,'items':items}