''' For registering database '''
# Run : python manage.py makemigrations --> python manage.py migrate

from django.db import models
from django.contrib.auth.models import User
from django.db.models import prefetch_related_objects


# Create your models here.
class Customer(models.Model):
    # Relating the 'Customer' model to the 'User' model via one-to-one relationship i.e.,
    # one object of 'Customer' model is linked to any but only one object of the 'User' model
    user = models.OneToOneField(to=User, related_name="customer", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(upload_to='product_images', blank=True, null=True, default=None)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.transaction_id)

    def total_price_of_all_orderitems_in_order(self):
        # This will give a list of all the 'OrderItem' objects which are related to this particular 'Order'.
        total_ordered_items = self.orderitem_set.all()

        # this will give a list of prices of all the ordered items in the given order.
        price_list = [order_item.ordered_item_price() for order_item in total_ordered_items]
        total_price = sum(price_list)
        return total_price

    def total_num_of_products_in_order(self):
        total_ordered_items = self.orderitem_set.all()
        total_items = sum([item.quantity for item in total_ordered_items])
        return total_items

    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()

        for i in order_items:
            if i.product.digital == False:
                shipping = True
        return shipping


class OrderItem(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(to=Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def ordered_item_price(self):
        total_price = self.quantity * self.product.price
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(to=Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    pin_code = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    stata = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class ProductDetails(models.Model):
    product = models.OneToOneField(to=Product, related_name="product_details", on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title





