# for creating superuser : 'python manage.py createsuperuser'

from django.contrib import admin
from . import models


# In order to register models into django -admin  you have to do the following.
# After registration, you can create or delete new objects from those models in Django-admin
admin.site.register(models.Customer)
admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.ShippingAddress)
admin.site.register(models.ProductDetails)



