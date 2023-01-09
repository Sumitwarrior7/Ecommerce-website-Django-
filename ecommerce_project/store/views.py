import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *
from .sumit import cookie_cart, cart_data


# Create your views here.
def user_register(request):
    registration_form = UserRegisterForm()   # Blank registration form :-
    registered = False

    # After user filled the registration form :-
    if request.method == "POST":
        # Filled registration form :-
        inputted_registration_form = UserRegisterForm(request.POST)

        if inputted_registration_form.is_valid():
            registered = True

            # There is no need for hashing :-
            # user_password = inputted_registration_form.cleaned_data['password']
            # hashed_password = make_password(password=user_password, salt="Sumit1234567890", hasher="default")

            # Creating a User with the given registration form data :-
            registered_user = User.objects.create_user(username=inputted_registration_form.cleaned_data['username'],
                                                       password=inputted_registration_form.cleaned_data['password'],
                                                       first_name=inputted_registration_form.cleaned_data['first_name'],
                                                       last_name=inputted_registration_form.cleaned_data['last_name'],
                                                       email=inputted_registration_form.cleaned_data['email'])
            registered_user.save()  # Saving the new User into the database

            # Creating a new customer with the registered user :-
            registered_customer = Customer(user=registered_user,
                                           name=inputted_registration_form.cleaned_data['username'],
                                           email=inputted_registration_form.cleaned_data['email'])
            registered_customer.save()   # Saving the new Customer into the database

            # Logging-In the new user :-
            login(request, registered_user)

            return redirect(to=store)
        else:
            print("Not valid")
            return redirect(to=store)

    return render(request, 'store/register.html', context={'registration_form': registration_form})


def user_login(request):
    if request.method == 'POST':
        inputted_login_form = UserLoginForm(request.POST)

        if inputted_login_form.is_valid():
            inputted_email = inputted_login_form.cleaned_data['email']
            inputted_password = inputted_login_form.cleaned_data['password']

            try:
                login_user = User.objects.get(email=inputted_email)
                login_username = login_user.username

                # Django's default authentication works with 'username' and 'password' only
                user_authentication = authenticate(request, username=login_username, password=inputted_password)
                if user_authentication is not None:
                    print('login successful')
                    login(request, login_user)
                    return redirect(to=store)
                else:
                    print('Password Incorrect')

            except ObjectDoesNotExist:
                print('User not exist!!')

    login_form = UserLoginForm()

    return render(request, 'store/login.html', context={'login_form': login_form})


def user_logout(request):
    logout(request)
    return redirect(to=store)


def store(request):
    all_products = Product.objects.all().values()

    context = {'products': all_products}
    return render(request, "store/store.html", context)


def cart(request):
    sumit_data = cart_data(request)

    context = {
        'items': sumit_data['items'],
        'cart_price': sumit_data['cart_price'],
        'total_products': sumit_data['total_products'],
    }
    return render(request, "store/cart.html", context)


def checkout(request):
    sumit_data = cart_data(request)

    context = {
        'items': sumit_data['items'],
        'cart_price': sumit_data['cart_price'],
        'total_products': sumit_data['total_products'],
        'shipping': sumit_data['shipping'],
    }

    return render(request, "store/checkout.html", context)


# When 'add to cart' button of any product is clicked , function given below is triggered :-
def update_item(request):
    data = json.loads(request.body)

    # The "product_id" & "action", we are getting from the function triggered in 'main.js' on clicking 'add to cart' button
    product_id = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # When user clicks on a particular product's "add to cart" button, then it checks whether the the user's order
    # already have that particular product or not. If it has , then it will be given to 'order_item' but if not, then
    # that particular orderitem-object will be created and then given to 'order_item'
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        order_item.quantity += 1
    elif action == "remove":
        order_item.quantity -= 1
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse("Item was added", safe=False)


# For updating item in product view page under dynamic routing :-
def update_item_by_view(request, productid):
    data = json.loads(request.body)

    # The "product_id" & "action", we are getting from the function triggered in 'main.js' on clicking 'add to cart' button
    product_id = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # When user clicks on a particular product's "add to cart" button, then it checks whether the the user's order
    # already have that particular product or not. If it has , then it will be given to 'order_item' but if not, then
    # that particular orderitem-object will be created and then given to 'order_item'
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        order_item.quantity += 1
    elif action == "remove":
        order_item.quantity -= 1
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse("Item was added", safe=False)


def view_product(request, productid):
    product = Product.objects.get(id=productid)
    product_details = ProductDetails.objects.get(product=product)
    print("chutiyapa")

    data_of_cart = cart_data(request)
    order_items = data_of_cart['items']

    product_quantity = None
    for item in order_items:
        if request.user.is_authenticated:
            print('Auth')
            item_id = int(item.product.id)

            if item_id == int(productid):
                product_quantity = item.quantity
        else:
            print('Not auth')
            item_id = int(item['product']['id'])

            if item_id == int(productid):
                product_quantity = item['quantity']

    if product_quantity is None:
        product_quantity = 0

    context = {
        'brand_name': product_details.brand_name,
        'title': product_details.title,
        'description': product_details.description,
        'product_id': product.id,
        'price': product.price,
        'image': product.image,
        'quantity': product_quantity,
    }
    return render(request, "store/product_view.html", context=context)


def product_search(request):
    user_query = request.POST['input-query']

    user_queried_products = Product.objects.filter(name__icontains=user_query).values()

    queried_names_list = [n for n in user_queried_products]

    # List of the ids of all the products having their names containing searched query
    queried_product_id_list = [p['id'] for p in queried_names_list]
    print('thas')
    print(queried_product_id_list)

    if len(queried_product_id_list) == 0:
        print('No results')
        no_results = True
        search_results_list = []
    else:
        no_results = False
        search_results_list = []
        for prod_id in queried_product_id_list:
            id_product = Product.objects.get(id=prod_id)

            id_product_img = id_product.image
            id_product_name = id_product.name
            id_product_price = id_product.price

            id_product_details = ProductDetails.objects.get(product=id_product)
            id_product_title = id_product_details.title

            search_card_details_dict = {
                'product_id': prod_id,
                'product_img': id_product_img,
                'product_name': id_product_name,
                'product_title': id_product_title,
                'product_price': id_product_price,
            }
            search_results_list.append(search_card_details_dict)

    context = {
        'search_results': search_results_list,
        'no_results': no_results,
    }
    return render(request, 'store/search_results.html', context=context)


