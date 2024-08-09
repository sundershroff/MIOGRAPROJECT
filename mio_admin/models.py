from django.db import models
from django.contrib.auth.models import AbstractUser,Permission
from django.contrib.auth.models import User,auth
from api.models import *

class admin_CustomUser(models.Model):
    username=models.TextField(null=True)
    name=models.TextField(null=True)
    email=models.EmailField(null=True)
    password=models.TextField(null=True)
    phonenumber=models.TextField(null=True)
    access_priveleges = models.JSONField(null=True)
    
class Hub_CustomUser(models.Model):
    username=models.TextField(null=True)
    name=models.TextField(null=True)
    email=models.EmailField(null=True)
    password=models.TextField(null=True)
    phonenumber=models.TextField(null=True)
    hub = models.TextField(null=True)
    door_no = models.TextField(null=True)
    street = models.TextField(null=True)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    country = models.TextField(null=True)

    
class comission_Editing(models.Model):
    per_km = models.IntegerField(null = True)
    incentive = models.IntegerField(null = True)
    normal_delivery_commision = models.IntegerField(null = True)
    
class business_commision(models.Model):
    commission =models.TextField(null=True)
    gst = models.TextField(null=True)
        
class banner(models.Model):
    category =models.TextField(null=True)
    banner1 = models.ImageField(upload_to="banner",null=True)
    banner2 = models.ImageField(upload_to="banner",null=True)
    banner_list1 = models.JSONField(null=True)
    banner_list2 = models.JSONField(null=True)
    ad1 = models.ImageField(upload_to="banner",null=True)
    ad2 = models.ImageField(upload_to="banner",null=True)
    
class zone(models.Model):
    zone =models.TextField(null=True)
    pincode = models.JSONField(null = True)
    
class shutdown(models.Model):
    shopping = models.BooleanField(null=True,default=0)
    food = models.BooleanField(null=True,default=0)
    fresh_cuts = models.BooleanField(null=True,default=0)
    daily_mio = models.BooleanField(null=True,default=0)
    pharmacy = models.BooleanField(null=True,default=0)
    d_original = models.BooleanField(null=True,default=0)
    jewellery = models.BooleanField(null=True,default=0)
    used_products = models.BooleanField(null=True,default=0)
    cod = models.BooleanField(null=True,default=0)
    online_payment = models.BooleanField(null=True,default=0)
    
class hsn_code(models.Model):
    hsn_code = models.TextField(null=True)
    goods = models.TextField(null=True)
    gst = models.TextField(null=True)

class admin_to_business_payment(models.Model):
    balance_amount = models.FloatField(default=0)
    paid_amount = models.FloatField(default=0)
    seller = models.TextField(null=True)
    order = models.ForeignKey(Product_Ordermodel, on_delete=models.CASCADE,null=True)