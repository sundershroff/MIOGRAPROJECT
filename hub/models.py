from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from datetime import datetime
from api.models import *
# Create your models here.
class product_arrive(models.Model):
    order = models.ForeignKey(Product_Ordermodel,on_delete=models.CASCADE,null=True)
    product_picked = models.BooleanField(default=0)
    product_picked_date = models.DateTimeField(null=True)
    product_arrived = models.BooleanField(default=0)
    product_arrived_date = models.DateTimeField(null=True)
    delivery_person = models.ForeignKey(Delivery_model,on_delete=models.CASCADE,null=True)
    product_arrived_to_me = models.BooleanField(default=0)
    product_arrived_to_me_date = models.DateTimeField(null=True)
    
    def save(self, *args, **kwargs):
            if self.product_picked == "1" and not self.product_picked_date:
                self.product_picked_date = timezone.now().date()
            if self.product_arrived == "1" and not self.product_arrived_date:
                self.product_arrived_date = timezone.now().date()
            if self.product_arrived_to_me == "1" and not self.product_arrived_to_me_date:
                self.product_arrived_to_me_date = timezone.now().date()
            super().save(*args, **kwargs)
        
class product_return(models.Model):
    order = models.ForeignKey(Product_Ordermodel,on_delete=models.CASCADE,null=True)
    product_arrived = models.BooleanField(default=0)
    product_arrived_date = models.DateTimeField(null=True)
    delivery_person = models.ForeignKey(Delivery_model,on_delete=models.CASCADE,null=True)
    product_arrived_to_me = models.BooleanField(default=0)
    product_arrived_to_me_date = models.DateTimeField(null=True)
    out_of_delivery = models.TextField(null=True)
    out_of_delivery_date = models.DateTimeField(null=True)
    
    def save(self, *args, **kwargs):
            if self.product_arrived == "1" and not self.product_arrived_date:
                self.product_arrived_date = timezone.now().date()
            if self.product_arrived_to_me == "1" and not self.product_arrived_to_me_date:
                self.product_arrived_to_me_date = timezone.now().date()
            if self.out_of_delivery == "1" and not self.out_of_delivery_date:
                self.out_of_delivery_date = timezone.now().date()
            super().save(*args, **kwargs)
    