import json
from .models import *


def cookie_cart(request):
    items = []
    cart_price = 0
    total_items = 0
    shipping = False

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    # Here 'i' will be the key of the dictionary 'cart' which will contain productId
    for i in cart:
        try:
            total_items += cart[i]['quantity']

            product = Product.objects.get(id=i)
            price = product.price * cart[i]['quantity']

            cart_price += price

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image': product.image,
                },
                'quantity': cart[i]['quantity'],
                'ordered_item_price': price,
            }
            items.append(item)

            if product.digital == False:
                shipping = True
        except:
            pass

    context = {
        'items': items,
        'cart_price': cart_price,
        'total_items': total_items,
        'shipping': shipping,
    }
    return context


def cart_data(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        # It gives all the 'OrderItem' objects which are linked to a particular 'Order' with many-to-one relation
        items = order.orderitem_set.all()

        cart_price = order.total_price_of_all_orderitems_in_order()
        total_items = order.total_num_of_products_in_order()
        shipping = order.shipping()

    # For Guest user(non logged-in user) :-
    else:
        cookie_data = cookie_cart(request)

        items = cookie_data["items"]
        cart_price = cookie_data["cart_price"]
        total_items = cookie_data["total_items"]
        shipping = cookie_data["shipping"]

    context = {'items': items,
               'cart_price': cart_price,
               'total_products': total_items,
               'shipping': shipping}
    return context

