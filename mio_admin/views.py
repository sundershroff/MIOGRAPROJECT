from django.shortcuts import render,redirect
from pymongo import MongoClient
from api.models import *
from mio_admin.models import *
import requests
from django.contrib.auth.models import User,auth
import random
from api import delivery_extension
from django.core.files.storage import FileSystemStorage
from django.views.decorators.cache import never_cache
from cryptography.fernet import Fernet
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.decorators import api_view
import os
from django.conf import settings
from datetime import date
# Generate a key
key = Fernet.generate_key()

# Create a cipher suite
cipher_suite = Fernet(key)

client = MongoClient('localhost', 27017)
all_image_url = "http://127.0.0.1:3000/"
# Create your views here.
# @never_cache
def decimal(amount):
    if type(amount) is float:
        # Convert the decimal number to a string
        decimal_string = str(amount)

        # Find the index of the decimal point
        decimal_point_index = decimal_string.index('.')

        # Get the decimal value with the last two digits
        decimal_last_two_digits = decimal_string[:decimal_point_index + 3]
        return decimal_last_two_digits
    else:
        return amount

def login_hub(request):
    error = ""
    if request.method == "POST":
        print(request.POST)
        if "admin" in request.POST:
            try:
                username1 = request.POST['username']
                password = request.POST['password']
                username = User.objects.get(username = username1)
                user = auth.authenticate(request,username = username1,password = password)
                if user is not None:
                    auth.login(request,user)
                    # Encrypt the string
                    # plaintext = username1.encode()
                    # cipher_text = cipher_suite.encrypt(plaintext)
                    # print(type(cipher_text))
                    return redirect(f"/admin_index/{username1}")
                else:
                    error = "Password is Wrong"
            except:
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(request,username = "admin",password = "12345")
                if user is not None:
                    auth.login(request,user)
                    if admin_CustomUser.objects.filter(username = username).exists() == True:
                        print("user exixts")
                        if admin_CustomUser.objects.filter(username = username,password = password).exists() == True:
                            print(admin_CustomUser.objects.get(username = username).access_priveleges)
                            return redirect(f"/admin_index/{username}")
                        else:
                            error = "Password is Wrong"
                    else:
                        error = "User Does'nt Exixts"
                        
        elif "hub" in request.POST:
            username1 = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(request,username = "hub",password = "12345")
            if user is not None:
                auth.login(request,user)
                if Hub_CustomUser.objects.filter(username = username1).exists() == True:
                    print("user exixts")
                    if Hub_CustomUser.objects.filter(username = username1,password = password).exists() == True:
                        return redirect(f"/hub/dashboard/{Hub_CustomUser.objects.get(username = username1).hub}")
                    else:
                        error = "Password is Wrong"
            else:
                error = "User Does'nt Exixts"
            
    context = {
        'error':error
    }
    return render(request,"admin_loginpage.html",context)

def logout(request):
    auth.logout(request)
    return redirect("/admin/")

def index(request,access_priveleges):
    x = date.today()
    print(x)
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    #delivery man 
    region_area = "REGION"
    delivery_online = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True") | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True")
    delivery_without_emerged = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False) | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False)
    delivery_offline = deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True") | deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True")
    quick_delivery = Delivery_model.objects.filter(delivery_type = "quick",approve_status = "True") | Delivery_model.objects.filter(delivery_type = "Quick",approve_status = "True")
    if request.method == "POST":
        print(request.POST)
        if "region_select" in request.POST:
            if request.POST['region_select'] == "nagercoil":
                region_area = request.POST['region_select']
                quick_delivery = Delivery_model.objects.filter(region = "nagercoil",delivery_type = "quick",approve_status = "True") | Delivery_model.objects.filter(region = "nagercoil",delivery_type = "Quick",approve_status = "True")
                delivery_without_emerged = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False,deliveryperson__region = region_area) | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False,deliveryperson__region = region_area)
                delivery_online = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area ) | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area )
                delivery_offline = deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area ) | deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area )

            elif request.POST['region_select'] == "kanniyakumari":
                region_area = request.POST['region_select']
                quick_delivery = Delivery_model.objects.filter(region = "kanniyakumari",delivery_type = "quick",approve_status = "True")    
                delivery_without_emerged = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False,deliveryperson__region = region_area) | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False,deliveryperson__region = region_area)
                delivery_online = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area ) | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area )
                delivery_offline = deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area ) | deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area )

            elif request.POST['region_select'] == "thuckalay":
                region_area = request.POST['region_select']
                quick_delivery = Delivery_model.objects.filter(region = "thuckalay",delivery_type = "quick",approve_status = "True")
                delivery_without_emerged = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False,deliveryperson__region = region_area) | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False,deliveryperson__region = region_area)
                delivery_online = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area ) | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area )
                delivery_offline = deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area ) | deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area )

            elif request.POST['region_select'] == "marthandam":
                region_area = request.POST['region_select']
                quick_delivery = Delivery_model.objects.filter(region = "marthandam",delivery_type = "quick",approve_status = "True")
                delivery_without_emerged = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False,deliveryperson__region = region_area) | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False,deliveryperson__region = region_area)
                delivery_online = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area ) | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area )
                delivery_offline = deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area ) | deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area )

            elif request.POST['region_select'] == "karungal":
                region_area = request.POST['region_select']
                quick_delivery = Delivery_model.objects.filter(region = "karungal",delivery_type = "quick",approve_status = "True")
                delivery_without_emerged = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False,deliveryperson__region = region_area) | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False,deliveryperson__region = region_area)
                delivery_online = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area ) | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area )
                delivery_offline = deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area ) | deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area )

            elif request.POST['region_select'] == "nithiravilai":
                region_area = request.POST['region_select']
                quick_delivery = Delivery_model.objects.filter(region = "nithiravilai",delivery_type = "quick",approve_status = "True")
                delivery_without_emerged = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False,deliveryperson__region = region_area) | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__emergency=False,deliveryperson__region = region_area)
                delivery_online = deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area ) | deliverylogintable_model.objects.filter(status = 1,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area )
                delivery_offline = deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area ) | deliverylogintable_model.objects.filter(status = 0,today_date = x,deliveryperson__delivery_type = "Quick",deliveryperson__approve_status = "True",deliveryperson__region = region_area )
        elif "work_assign" in request.POST:
            print(request.POST)
            order_data = (Product_Ordermodel.objects.filter(deliveryperson__uid = request.POST['emerged_partner'],status="order-confirmed")
                            | 
                          Product_Ordermodel.objects.filter(status="order-picked")
                                                           )
            print(order_data)
            for x in order_data:
                delivery_details = Delivery_model.objects.get(uid = request.POST['work_assign'])
                update_order_work = Product_Ordermodel.objects.get(order_id = x.order_id)
                update_order_work.deliveryperson = delivery_details
                update_order_work.save()
                print("work assign succesfully")
            
    context = {
        'region_area':region_area,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
        'quick_delivery':quick_delivery,
        'delivery_online':delivery_online,
        'delivery_offline':delivery_offline,
        'delivery_without_emerged':delivery_without_emerged,
    }
    
    return render(request,'admin_index.html',context)

def dashboard(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    #shopping
    order_data_shopping = Product_Ordermodel.objects.filter(category_data = "shopping",payment_type="cod")
    shop_data_payment = admin_to_business_payment.objects.filter(order__shop_id__category = "shopping")
    #delivery payment
    shopping_delivery_total = 0
    shopping_delivery_received = 0
    for x in order_data_shopping:
        shopping_delivery_total += float(x.total_amount)
        shopping_delivery_received += float(x.float_cash)
    shopping_total = decimal(shopping_delivery_total)
    shopping_to_be_received = decimal(shopping_delivery_received)
    received_shopping = float(shopping_total)-float(shopping_to_be_received)
    shopping_received = decimal(received_shopping)
    #seller payment
    shopping_calc_total = 0
    shopping_calc_balance = 0
    shopping_calc_paid = 0
    for y in shop_data_payment:
        shopping_calc_total += float(y.balance_amount) + float(y.paid_amount)
        shopping_calc_balance += float(y.balance_amount)
        shopping_calc_paid += float(y.paid_amount)
    shopping_total = decimal(shopping_calc_total)
    shopping_balance = decimal(shopping_calc_balance)
    shopping_paid = decimal(shopping_calc_paid)
#food
    order_data_food = Product_Ordermodel.objects.filter(category_data = "food",payment_type="cod")
    food_data_payment = admin_to_business_payment.objects.filter(order__food_id__category = "food")
    #delivery payment
    food_delivery_total = 0
    food_delivery_received = 0
    for x in order_data_food:
        food_delivery_total += float(x.total_amount)
        food_delivery_received += float(x.float_cash)
    food_total = decimal(food_delivery_total)
    print(food_total)
    food_to_be_received = decimal(food_delivery_received)
    received_food = float(food_total)-float(food_to_be_received)
    food_received = decimal(received_food)
    print(f"food received",{food_received})
    #seller payment
    food_calc_total = 0
    food_calc_balance = 0
    food_calc_paid = 0
    for y in food_data_payment:
        food_calc_total += float(y.balance_amount) + float(y.paid_amount)
        food_calc_balance += float(y.balance_amount)
        food_calc_paid += float(y.paid_amount)
    food_total = decimal(food_calc_total)
    food_balance = decimal(food_calc_balance)
    food_paid = decimal(food_calc_paid)
#fresh cuts
    order_data_fresh = Product_Ordermodel.objects.filter(category_data = "fresh_cuts",payment_type="cod")
    fresh_data_payment = admin_to_business_payment.objects.filter(order__fresh_id__category = "fresh_cuts")
    #delivery payment
    fresh_delivery_total = 0
    fresh_delivery_received = 0
    for x in order_data_fresh:
        fresh_delivery_total += float(x.total_amount)
        fresh_delivery_received += float(x.float_cash)
    fresh_total = decimal(fresh_delivery_total)
    print(fresh_total)
    fresh_to_be_received = decimal(fresh_delivery_received)
    received_fresh = float(fresh_total)-float(fresh_to_be_received)
    fresh_received = decimal(received_fresh)
    print(f"fresh received",{fresh_received})
    #seller payment
    fresh_calc_total = 0
    fresh_calc_balance = 0
    fresh_calc_paid = 0
    for y in fresh_data_payment:
        fresh_calc_total += float(y.balance_amount) + float(y.paid_amount)
        fresh_calc_balance += float(y.balance_amount)
        fresh_calc_paid += float(y.paid_amount)
    fresh_total = decimal(fresh_calc_total)
    fresh_balance = decimal(fresh_calc_balance)
    fresh_paid = decimal(fresh_calc_paid)
#daily mio
    order_data_dailymio = Product_Ordermodel.objects.filter(category_data = "daily_mio",payment_type="cod")
    dailymio_data_payment = admin_to_business_payment.objects.filter(order__dmio_id__category = "daily_mio")
    #delivery payment
    dailymio_delivery_total = 0
    dailymio_delivery_received = 0
    for x in order_data_dailymio:
        dailymio_delivery_total += float(x.total_amount)
        dailymio_delivery_received += float(x.float_cash)
    dailymio_total = decimal(dailymio_delivery_total)
    print(dailymio_total)
    dailymio_to_be_received = decimal(dailymio_delivery_received)
    received_dailymio = float(dailymio_total)-float(dailymio_to_be_received)
    dailymio_received = decimal(received_dailymio)
    print(f"dailymio received",{dailymio_received})
    #seller payment
    dailymio_calc_total = 0
    dailymio_calc_balance = 0
    dailymio_calc_paid = 0
    for y in dailymio_data_payment:
        dailymio_calc_total += float(y.balance_amount) + float(y.paid_amount)
        dailymio_calc_balance += float(y.balance_amount)
        dailymio_calc_paid += float(y.paid_amount)
    dailymio_total = decimal(dailymio_calc_total)
    dailymio_balance = decimal(dailymio_calc_balance)
    dailymio_paid = decimal(dailymio_calc_paid)
#pharmacy
    order_data_pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy",payment_type="cod")
    pharmacy_data_payment = admin_to_business_payment.objects.filter(order__pharm_id__category = "pharmacy")
    #delivery payment
    pharmacy_delivery_total = 0
    pharmacy_delivery_received = 0
    for x in order_data_pharmacy:
        pharmacy_delivery_total += float(x.total_amount)
        pharmacy_delivery_received += float(x.float_cash)
    pharmacy_total = decimal(pharmacy_delivery_total)
    print(pharmacy_total)
    pharmacy_to_be_received = decimal(pharmacy_delivery_received)
    received_pharmacy = float(pharmacy_total)-float(pharmacy_to_be_received)
    pharmacy_received = decimal(received_pharmacy)
    print(f"pharmacy received",{pharmacy_received})
    #seller payment
    pharmacy_calc_total = 0
    pharmacy_calc_balance = 0
    pharmacy_calc_paid = 0
    for y in pharmacy_data_payment:
        pharmacy_calc_total += float(y.balance_amount) + float(y.paid_amount)
        pharmacy_calc_balance += float(y.balance_amount)
        pharmacy_calc_paid += float(y.paid_amount)
    pharmacy_total = decimal(pharmacy_calc_total)
    pharmacy_balance = decimal(pharmacy_calc_balance)
    pharmacy_paid = decimal(pharmacy_calc_paid)
#d original
    order_data_doriginal = Product_Ordermodel.objects.filter(category_data = "d_original",payment_type="cod")
    doriginal_data_payment = admin_to_business_payment.objects.filter(order__d_id__category = "d_original")
    #delivery payment
    doriginal_delivery_total = 0
    doriginal_delivery_received = 0
    for x in order_data_doriginal:
        doriginal_delivery_total += float(x.total_amount)
        doriginal_delivery_received += float(x.float_cash)
    doriginal_total = decimal(doriginal_delivery_total)
    print(doriginal_total)
    doriginal_to_be_received = decimal(doriginal_delivery_received)
    received_doriginal = float(doriginal_total)-float(doriginal_to_be_received)
    doriginal_received = decimal(received_doriginal)
    print(f"doriginal received",{doriginal_received})
    #seller payment
    doriginal_calc_total = 0
    doriginal_calc_balance = 0
    doriginal_calc_paid = 0
    for y in doriginal_data_payment:
        doriginal_calc_total += float(y.balance_amount) + float(y.paid_amount)
        doriginal_calc_balance += float(y.balance_amount)
        doriginal_calc_paid += float(y.paid_amount)
    doriginal_total = decimal(doriginal_calc_total)
    doriginal_balance = decimal(doriginal_calc_balance)
    doriginal_paid = decimal(doriginal_calc_paid)
#jewellery
    order_data_jewellery = Product_Ordermodel.objects.filter(category_data = "jewellery",payment_type="cod")
    jewellery_data_payment = admin_to_business_payment.objects.filter(order__jewel_id__category = "jewellery")
    #delivery payment
    jewellery_delivery_total = 0
    jewellery_delivery_received = 0
    for x in order_data_jewellery:
        jewellery_delivery_total += float(x.total_amount)
        jewellery_delivery_received += float(x.float_cash)
    jewellery_total = decimal(jewellery_delivery_total)
    print(jewellery_total)
    jewellery_to_be_received = decimal(jewellery_delivery_received)
    received_jewellery = float(jewellery_total)-float(jewellery_to_be_received)
    jewellery_received = decimal(received_jewellery)
    print(f"jewellery received",{jewellery_received})
    #seller payment
    jewellery_calc_total = 0
    jewellery_calc_balance = 0
    jewellery_calc_paid = 0
    for y in jewellery_data_payment:
        jewellery_calc_total += float(y.balance_amount) + float(y.paid_amount)
        jewellery_calc_balance += float(y.balance_amount)
        jewellery_calc_paid += float(y.paid_amount)
    jewellery_total = decimal(jewellery_calc_total)
    jewellery_balance = decimal(jewellery_calc_balance)
    jewellery_paid = decimal(jewellery_calc_paid)



    context = {
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
        #shopping
        'shopping_delivery_total':shopping_total,
        'shopping_to_be_received':shopping_to_be_received,
        'shopping_received':shopping_received,
        'shopping_total':shopping_total,
        'shopping_balance':shopping_balance,
        'shopping_paid':shopping_paid,
        #food
        'food_delivery_total':food_total,
        'food_to_be_received':food_to_be_received,
        'food_received':food_received,
        'food_total':food_total,
        'food_balance':food_balance,
        'food_paid':food_paid,
        #fresh_cuts
        'fresh_delivery_total':fresh_total,
        'fresh_to_be_received':fresh_to_be_received,
        'fresh_received':fresh_received,
        'fresh_total':fresh_total,
        'fresh_balance':fresh_balance,
        'fresh_paid':fresh_paid,
        #daily_mio
        'dailymio_delivery_total':dailymio_total,
        'dailymio_to_be_received':dailymio_to_be_received,
        'dailymio_received':dailymio_received,
        'dailymio_total':dailymio_total,
        'dailymio_balance':dailymio_balance,
        'dailymio_paid':dailymio_paid,
        #pharmacy
        'pharmacy_delivery_total':pharmacy_total,
        'pharmacy_to_be_received':pharmacy_to_be_received,
        'pharmacy_received':pharmacy_received,
        'pharmacy_total':pharmacy_total,
        'pharmacy_balance':pharmacy_balance,
        'pharmacy_paid':pharmacy_paid,
        #d original
        'doriginal_delivery_total':doriginal_total,
        'doriginal_to_be_received':doriginal_to_be_received,
        'doriginal_received':doriginal_received,
        'doriginal_total':doriginal_total,
        'doriginal_balance':doriginal_balance,
        'doriginal_paid':doriginal_paid,
        #jewellery
        'jewellery_delivery_total':jewellery_total,
        'jewellery_to_be_received':jewellery_to_be_received,
        'jewellery_received':jewellery_received,
        'jewellery_total':jewellery_total,
        'jewellery_balance':jewellery_balance,
        'jewellery_paid':jewellery_paid,
    }
    return render(request,'admin_dashboard.html',context)

def product_details(request,access_priveleges):
    today_date = date.today()
    # print(x)
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    region_area = "REGION"
    shopping = shoppingmodel.objects.filter(category = "shopping")
    food = foodmodel.objects.filter(category = "food")
    fresh_cuts = freshcutsmodel.objects.filter(category = "fresh_cuts")
    daily_mio = dailymio_model.objects.filter(category = "daily_mio")
    pharmacy = pharmacy_model.objects.filter(category = "pharmacy")
    d_original = d_originalmodel.objects.filter(category = "d_original")
    jewellery = jewellerymodel.objects.filter(category = "jewellery")
    #today sales amount
    today_sales = Product_Ordermodel.objects.filter(order_date = today_date)
    today_sales_amount = 0
    admin_commision = 0
    for x in today_sales: 
        today_sales_amount += float(x.total_amount)
    if type(today_sales_amount) is float:
        # Convert the decimal number to a string
        decimal_string = str(today_sales_amount)

        # Find the index of the decimal point
        decimal_point_index = decimal_string.index('.')

        # Get the decimal value with the last two digits
        decimal_last_two_digits = decimal_string[:decimal_point_index + 3]
    else:
        decimal_last_two_digits = today_sales_amount
    #admin commision    
    for y in today_sales: 
        print(int(y.admin_commission_amount))
        print(float(y.total_amount) / int(y.admin_commission_amount))
        admin_commision += float(y.total_amount) / int(y.admin_commission_amount)
    if type(admin_commision) is float:
        # Convert the decimal number to a string
        decimal_string = str(admin_commision)

        # Find the index of the decimal point
        decimal_point_index = decimal_string.index('.')

        # Get the decimal value with the last two digits
        decimal_last_two_digits_commision = decimal_string[:decimal_point_index + 3]
    else:
        decimal_last_two_digits_commision = admin_commision
    if request.method == "POST":
        if "region_select" in request.POST:
            print(today_date)
            region_area = request.POST['region_select']
            #today sales count
            today_sales = Product_Ordermodel.objects.filter(order_date = today_date,region=region_area)
            today_sales_amount = 0
            admin_commision = 0
            for x in today_sales: 
                # print(float(x.total_amount))
                today_sales_amount += float(x.total_amount)
            print(today_sales_amount)
            if type(today_sales_amount) is float:
                # Convert the decimal number to a string
                decimal_string = str(today_sales_amount)

                # Find the index of the decimal point
                decimal_point_index = decimal_string.index('.')

                # Get the decimal value with the last two digits
                decimal_last_two_digits = decimal_string[:decimal_point_index + 3]
            else:
                decimal_last_two_digits = today_sales_amount
                print("notfloat")
            
            #admin commision    
            for y in today_sales: 
                print("hello")
                print(y.total_amount)
                print(int(y.admin_commission_amount))
                print(float(y.total_amount) / int(y.admin_commission_amount))
                admin_commision += float(y.total_amount) / int(y.admin_commission_amount)
            if type(admin_commision) is float:
                # Convert the decimal number to a string
                decimal_string = str(admin_commision)

                # Find the index of the decimal point
                decimal_point_index = decimal_string.index('.')

                # Get the decimal value with the last two digits
                decimal_last_two_digits_commision = decimal_string[:decimal_point_index + 3] 
            else:
                decimal_last_two_digits_commision = admin_commision
                

            if request.POST['region_select'] == "nagercoil":   
                #shopping
                shopping = shoppingmodel.objects.filter(region = "nagercoil",category = "shopping")
                #foods
                food = foodmodel.objects.filter(region = "nagercoil",category = "food")
                #fresh_cuts
                fresh_cuts = freshcutsmodel.objects.filter(region = "nagercoil",category = "fresh_cuts")
                #daily_mio
                daily_mio = dailymio_model.objects.filter(region = "nagercoil",category = "daily_mio")
                #pharmacy
                pharmacy = pharmacy_model.objects.filter(region = "nagercoil",category = "pharmacy")
                #d_original
                d_original = d_originalmodel.objects.filter(region = "nagercoil",category = "d_original")
                #jwellery
                jewellery = jewellerymodel.objects.filter(region = "nagercoil",category = "jewellery")

            elif request.POST['region_select'] == "kanniyakumari":
                #shopping
                shopping = shoppingmodel.objects.filter(region = "kanniyakumari",category = "shopping")
                #foods
                food = foodmodel.objects.filter(region = "kanniyakumari",category = "food")
                #fresh_cuts
                fresh_cuts = freshcutsmodel.objects.filter(region = "kanniyakumari",category = "fresh_cuts")
                #daily_mio
                daily_mio = dailymio_model.objects.filter(region = "kanniyakumari",category = "daily_mio")
                #pharmacy
                pharmacy = pharmacy_model.objects.filter(region = "kanniyakumari",category = "pharmacy")
                #d_original
                d_original = d_originalmodel.objects.filter(region = "kanniyakumari",category = "d_original")
                #jwellery
                jewellery = jewellerymodel.objects.filter(region = "kanniyakumari",category = "jewellery")
        
            elif request.POST['region_select'] == "thuckalay":
                #shopping
                shopping = shoppingmodel.objects.filter(region = "thuckalay",category = "shopping")
                #foods
                food = foodmodel.objects.filter(region = "thuckalay",category = "food")
                #fresh_cuts
                fresh_cuts = freshcutsmodel.objects.filter(region = "thuckalay",category = "fresh_cuts")
                #daily_mio
                daily_mio = dailymio_model.objects.filter(region = "thuckalay",category = "daily_mio")
                #pharmacy
                pharmacy = pharmacy_model.objects.filter(region = "thuckalay",category = "pharmacy")
                #d_original
                d_original = d_originalmodel.objects.filter(region = "thuckalay",category = "d_original")
                #jwellery
                jewellery = jewellerymodel.objects.filter(region = "thuckalay",category = "jewellery")
            
            elif request.POST['region_select'] == "marthandam":
                #shopping
                shopping = shoppingmodel.objects.filter(region = "marthandam",category = "shopping")
                #foods
                food = foodmodel.objects.filter(region = "marthandam",category = "food")
                #fresh_cuts
                fresh_cuts = freshcutsmodel.objects.filter(region = "marthandam",category = "fresh_cuts")
                #daily_mio
                daily_mio = dailymio_model.objects.filter(region = "marthandam",category = "daily_mio")
                #pharmacy
                pharmacy = pharmacy_model.objects.filter(region = "marthandam",category = "pharmacy")
                #d_original
                d_original = d_originalmodel.objects.filter(region = "marthandam",category = "d_original")
                #jwellery
                jewellery = jewellerymodel.objects.filter(region = "marthandam",category = "jewellery")
            
            elif request.POST['region_select'] == "karungal":
                #shopping
                shopping = shoppingmodel.objects.filter(region = "karungal",category = "shopping")
                #foods
                food = foodmodel.objects.filter(region = "karungal",category = "food")
                #fresh_cuts
                fresh_cuts = freshcutsmodel.objects.filter(region = "karungal",category = "fresh_cuts")
                #daily_mio
                daily_mio = dailymio_model.objects.filter(region = "karungal",category = "daily_mio")
                #pharmacy
                pharmacy = pharmacy_model.objects.filter(region = "karungal",category = "pharmacy")
                #d_original
                d_original = d_originalmodel.objects.filter(region = "karungal",category = "d_original")
                #jwellery
                jewellery = jewellerymodel.objects.filter(region = "karungal",category = "jewellery")
            
            elif request.POST['region_select'] == "nithiravilai":
                #shopping
                shopping = shoppingmodel.objects.filter(region = "nithiravilai",category = "shopping")
                #foods
                food = foodmodel.objects.filter(region = "nithiravilai",category = "food")
                #fresh_cuts
                fresh_cuts = freshcutsmodel.objects.filter(region = "nithiravilai",category = "fresh_cuts")
                #daily_mio
                daily_mio = dailymio_model.objects.filter(region = "nithiravilai",category = "daily_mio")
                #pharmacy
                pharmacy = pharmacy_model.objects.filter(region = "nithiravilai",category = "pharmacy")
                #d_original
                d_original = d_originalmodel.objects.filter(region = "nithiravilai",category = "d_original")
                #jwellery
                jewellery = jewellerymodel.objects.filter(region = "nithiravilai",category = "jewellery")

    context = {
        'region_area' : region_area,
        "shopping":shopping,
        'food':food,
        'fresh_cuts':fresh_cuts,
        'daily_mio':daily_mio,
        'pharmacy':pharmacy,
        'd_original':d_original,
        'jewellery':jewellery,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
        'today_sales_amount':decimal_last_two_digits,
        'admin_commision':decimal_last_two_digits_commision,
    }
    
    return render(request,'admin_product_details.html',context)

def single_store_details(request,category,id,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    payment = admin_to_business_payment.objects.get(seller = id)
    if category == "shopping":
        data = shoppingmodel.objects.get(shop_id  = id)
    elif category == "food":
        data = foodmodel.objects.get(food_id = id)
    elif category == "fresh_cuts":
        data = freshcutsmodel.objects.get(fresh_id = id)
    elif category == "daily_mio":
        data = dailymio_model.objects.get(dmio_id = id)
    elif category == "pharmacy":
        data = pharmacy_model.objects.get(pharm_id = id)
    elif category == "d_original":
        data = d_originalmodel.objects.get(d_id = id)
    elif category == "jewellery":
        data = jewellerymodel.objects.get(jewel_id = id)
 
    context = {
        'data':data,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
        'order_data':payment.balance_amount,
        'paid_data':payment.paid_amount,
    }
    
    return render(request,"single_store_details.html",context)

def order_details(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    region_area = "REGION"
    shopping = Product_Ordermodel.objects.filter(category_data = "shopping")
    food = Product_Ordermodel.objects.filter(category_data = "food")
    fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts")
    daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio")  
    pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy")  
    d_original = Product_Ordermodel.objects.filter(category_data = "d_original")
    jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery")
    if request.method == "POST":
        print(request.POST)
        if "region_select" in request.POST:
            region_area = request.POST['region_select']    
            if request.POST['region_select'] == "nagercoil":
                shopping = Product_Ordermodel.objects.filter(category_data = "shopping",region = "nagercoil")
                food = Product_Ordermodel.objects.filter(category_data = "food",region = "nagercoil")
                fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts",region = "nagercoil")
                daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio",region = "nagercoil")  
                pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy",region = "nagercoil")  
                d_original = Product_Ordermodel.objects.filter(category_data = "d_original",region = "nagercoil")
                jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery",region = "nagercoil")
            elif request.POST['region_select'] == "kanniyakumari":
                shopping = Product_Ordermodel.objects.filter(category_data = "shopping",region = "kanniyakumari")
                food = Product_Ordermodel.objects.filter(category_data = "food",region = "kanniyakumari")
                fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts",region = "kanniyakumari")
                daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio",region = "kanniyakumari")  
                pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy",region = "kanniyakumari")  
                d_original = Product_Ordermodel.objects.filter(category_data = "d_original",region = "kanniyakumari")
                jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery",region = "kanniyakumari")
        
            elif request.POST['region_select'] == "thuckalay":
                shopping = Product_Ordermodel.objects.filter(category_data = "shopping",region = "thuckalay")
                food = Product_Ordermodel.objects.filter(category_data = "food",region = "thuckalay")
                fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts",region = "thuckalay")
                daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio",region = "thuckalay")  
                pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy",region = "thuckalay")  
                d_original = Product_Ordermodel.objects.filter(category_data = "d_original",region = "thuckalay")
                jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery",region = "thuckalay")
            
            elif request.POST['region_select'] == "marthandam":
                shopping = Product_Ordermodel.objects.filter(category_data = "shopping",region = "marthandam")
                food = Product_Ordermodel.objects.filter(category_data = "food",region = "marthandam")
                fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts",region = "marthandam")
                daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio",region = "marthandam")  
                pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy",region = "marthandam")  
                d_original = Product_Ordermodel.objects.filter(category_data = "d_original",region = "marthandam")
                jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery",region = "marthandam")
            
            elif request.POST['region_select'] == "karungal":
                shopping = Product_Ordermodel.objects.filter(category_data = "shopping",region = "karungal")
                food = Product_Ordermodel.objects.filter(category_data = "food",region = "karungal")
                fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts",region = "karungal")
                daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio",region = "karungal")  
                pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy",region = "karungal")  
                d_original = Product_Ordermodel.objects.filter(category_data = "d_original",region = "karungal")
                jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery",region = "karungal")
            
            elif request.POST['region_select'] == "nithiravilai":
                shopping = Product_Ordermodel.objects.filter(category_data = "shopping",region = "nithiravilai")
                food = Product_Ordermodel.objects.filter(category_data = "food",region = "nithiravilai")
                fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts",region = "nithiravilai")
                daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio",region = "nithiravilai")  
                pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy",region = "nithiravilai")  
                d_original = Product_Ordermodel.objects.filter(category_data = "d_original",region = "nithiravilai")
                jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery",region = "nithiravilai")
    context = {
        'region_area':region_area,
        'shopping':shopping,
        'food':food,
        'fresh_cuts':fresh_cuts,
        'daily_mio':daily_mio,
        'pharmacy':pharmacy,
        'd_original':d_original,
        'jwellery':jwellery,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }
    
    return render(request,'admin_orderlist.html',context)

def bannerr(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    shopping = banner.objects.get(id = 1)
    food = banner.objects.get(id = 2)
    fresh_cuts = banner.objects.get(id = 3)
    daily_mio = banner.objects.get(id = 4)
    pharmacy = banner.objects.get(id = 5)
    d_original = banner.objects.get(id = 6)
    jewellery = banner.objects.get(id = 7)
    context = {
        'shopping':shopping,
        'food':food,
        'fresh_cuts':fresh_cuts,
        'daily_mio':daily_mio,
        'pharmacy':pharmacy,
        'd_original':d_original,
        'jewellery':jewellery,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
        
    }
    
    if request.method == "POST":
        print(request.FILES)
        if "banner" in request.POST:
            data = banner.objects.get(id = request.POST['banner'])
            if "banner1" in request.FILES:
                data.banner1 = request.FILES['banner1']
            if "banner2" in request.FILES:
                data.banner2 = request.FILES['banner2']
        elif "ad" in request.POST:
            data = banner.objects.get(id = request.POST['ad'])
            if "ad1" in request.FILES:
                data.ad1 = request.FILES['ad1']
            if "ad2" in request.FILES:
                data.ad2 = request.FILES['ad2']
        data.save()
        return redirect(f"/admin_banner/{authenticate.username}")
    return render(request,'admin_banner.html',context)

def customer_service(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    seller = ""
    product = ""
    business = ""
    if request.method == "POST":
        if "seller" in request.POST:
            if shoppingmodel.objects.filter(shop_id = request.POST['seller_id']).exists() == True:
                seller = shoppingmodel.objects.filter(shop_id = request.POST['seller_id'])
            elif foodmodel.objects.filter(food_id = request.POST['seller_id']).exists() == True:
                seller = foodmodel.objects.filter(food_id = request.POST['seller_id'])
            elif freshcutsmodel.objects.filter(fresh_id = request.POST['seller_id']).exists() == True:
                seller = freshcutsmodel.objects.filter(fresh_id = request.POST['seller_id'])
            elif dailymio_model.objects.filter(dmio_id = request.POST['seller_id']).exists() == True:
                seller = dailymio_model.objects.filter(dmio_id = request.POST['seller_id'])
            elif pharmacy_model.objects.filter(pharm_id = request.POST['seller_id']).exists() == True:
                seller = pharmacy_model.objects.filter(pharm_id = request.POST['seller_id'])
            elif d_originalmodel.objects.filter(d_id = request.POST['seller_id']).exists() == True:
                seller = d_originalmodel.objects.filter(d_id = request.POST['seller_id'])
            elif jewellerymodel.objects.filter(jewel_id = request.POST['seller_id']).exists() == True:
                seller = jewellerymodel.objects.filter(jewel_id = request.POST['seller_id'])
            else:
                seller = "Seller Not Available"
            print(seller)
        elif "product" in request.POST:
            if shop_productsmodel.objects.filter(product_id = request.POST['product_id']).exists() == True:
                product = shop_productsmodel.objects.filter(product_id = request.POST['product_id'])
            elif food_productsmodel.objects.filter(product_id = request.POST['product_id']).exists() == True:
                product = food_productsmodel.objects.filter(product_id = request.POST['product_id'])
            elif fresh_productsmodel.objects.filter(product_id = request.POST['product_id']).exists() == True:
                product = fresh_productsmodel.objects.filter(product_id = request.POST['product_id'])
            elif dmio_productsmodel.objects.filter(product_id = request.POST['product_id']).exists() == True:
                product = dmio_productsmodel.objects.filter(product_id = request.POST['product_id'])
            elif pharmacy_productsmodel.objects.filter(product_id = request.POST['product_id']).exists() == True:
                product = pharmacy_productsmodel.objects.filter(product_id = request.POST['product_id'])
            elif d_original_productsmodel.objects.filter(product_id = request.POST['product_id']).exists() == True:
                product = d_original_productsmodel.objects.filter(product_id = request.POST['product_id'])
            elif jewel_productsmodel.objects.filter(product_id = request.POST['product_id']).exists() == True:
                product = jewel_productsmodel.objects.filter(product_id = request.POST['product_id'])
            else:
                product = "Product Not Available"
        elif "business" in request.POST:
            print("business")
            try:
                business = Businessmodel.objects.filter(uid = request.POST['business_id'])
            except:
                business = "User Not Available"
            print(business)

    context = {
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
        'seller':seller,
        'product':product,
        'business':business,
    }
    return render(request,'admin_customer_service.html',context)

def product_appaoval(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    region_area = "REGION"
    #shopping
    shop_product = shop_productsmodel.objects.all()
    shop_product_length = shop_productsmodel.objects.filter(status = "False")
    #foods
    food_product = food_productsmodel.objects.all()
    food_product_length = food_productsmodel.objects.filter(status = "False")
    #fresh_cuts
    fresh_cuts = fresh_productsmodel.objects.all()
    fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False")
    #daily_mio
    daily_mio = dmio_productsmodel.objects.all()
    daily_mio_length = dmio_productsmodel.objects.filter(status = "False")
    #pharmacy
    pharmacy = pharmacy_productsmodel.objects.all()
    pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False")
    #d_original
    d_original = d_original_productsmodel.objects.all()
    d_original_length = d_original_productsmodel.objects.filter(status = "False")
    #jwellery
    jwellery = jewel_productsmodel.objects.all()
    jwellery_length = jewel_productsmodel.objects.filter(status = "False")
    if request.method == "POST":
        print(request.POST)
        if "region_select" in request.POST:
            region_area = request.POST['region_select']
            if request.POST['region_select'] == "nagercoil":
                #shopping
                shop_product = shop_productsmodel.objects.filter(region = "nagercoil")
                shop_product_length = shop_productsmodel.objects.filter(status = "False" , region = "nagercoil")
                #foods
                food_product = food_productsmodel.objects.filter(region = "nagercoil")
                food_product_length = food_productsmodel.objects.filter(status = "False" , region = "nagercoil")
                #fresh_cuts
                fresh_cuts = fresh_productsmodel.objects.filter(region = "nagercoil")
                fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False" , region = "nagercoil")
                #daily_mio
                daily_mio = dmio_productsmodel.objects.filter(region = "nagercoil")
                daily_mio_length = dmio_productsmodel.objects.filter(status = "False" , region = "nagercoil")
                #pharmacy
                pharmacy = pharmacy_productsmodel.objects.filter(region = "nagercoil")
                pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False" , region = "nagercoil")
                #d_original
                d_original = d_original_productsmodel.objects.filter(region = "nagercoil")
                d_original_length = d_original_productsmodel.objects.filter(status = "False" , region = "nagercoil")
                #jwellery
                jwellery = jewel_productsmodel.objects.filter(region = "nagercoil")
                jwellery_length = jewel_productsmodel.objects.filter(status = "False" , region = "nagercoil")
        
            elif request.POST['region_select'] == "kanniyakumari":
                #shopping
                shop_product = shop_productsmodel.objects.filter(region = "kanniyakumari")
                shop_product_length = shop_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
                #foods
                food_product = food_productsmodel.objects.filter(region = "kanniyakumari")
                food_product_length = food_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
                #fresh_cuts
                fresh_cuts = fresh_productsmodel.objects.filter(region = "kanniyakumari")
                fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
                #daily_mio
                daily_mio = dmio_productsmodel.objects.filter(region = "kanniyakumari")
                daily_mio_length = dmio_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
                #pharmacy
                pharmacy = pharmacy_productsmodel.objects.filter(region = "kanniyakumari")
                pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
                #d_original
                d_original = d_original_productsmodel.objects.filter(region = "kanniyakumari")
                d_original_length = d_original_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
                #jwellery
                jwellery = jewel_productsmodel.objects.filter(region = "kanniyakumari")
                jwellery_length = jewel_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
        
            elif request.POST['region_select'] == "thuckalay":
                #shopping
                    shop_product = shop_productsmodel.objects.filter(region = "thuckalay")
                    shop_product_length = shop_productsmodel.objects.filter(status = "False" , region = "thuckalay")
                    #foods
                    food_product = food_productsmodel.objects.filter(region = "thuckalay")
                    food_product_length = food_productsmodel.objects.filter(status = "False" , region = "thuckalay")
                    #fresh_cuts
                    fresh_cuts = fresh_productsmodel.objects.filter(region = "thuckalay")
                    fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False" , region = "thuckalay")
                    #daily_mio
                    daily_mio = dmio_productsmodel.objects.filter(region = "thuckalay")
                    daily_mio_length = dmio_productsmodel.objects.filter(status = "False" , region = "thuckalay")
                    #pharmacy
                    pharmacy = pharmacy_productsmodel.objects.filter(region = "thuckalay")
                    pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False" , region = "thuckalay")
                    #d_original
                    d_original = d_original_productsmodel.objects.filter(region = "thuckalay")
                    d_original_length = d_original_productsmodel.objects.filter(status = "False" , region = "thuckalay")
                    #jwellery
                    jwellery = jewel_productsmodel.objects.filter(region = "thuckalay")
                    jwellery_length = jewel_productsmodel.objects.filter(status = "False" , region = "thuckalay")
            
            elif request.POST['region_select'] == "marthandam":
                #shopping
                    shop_product = shop_productsmodel.objects.filter(region = "marthandam")
                    shop_product_length = shop_productsmodel.objects.filter(status = "False" , region = "marthandam")
                    #foods
                    food_product = food_productsmodel.objects.filter(region = "marthandam")
                    food_product_length = food_productsmodel.objects.filter(status = "False" , region = "marthandam")
                    #fresh_cuts
                    fresh_cuts = fresh_productsmodel.objects.filter(region = "marthandam")
                    fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False" , region = "marthandam")
                    #daily_mio
                    daily_mio = dmio_productsmodel.objects.filter(region = "marthandam")
                    daily_mio_length = dmio_productsmodel.objects.filter(status = "False" , region = "marthandam")
                    #pharmacy
                    pharmacy = pharmacy_productsmodel.objects.filter(region = "marthandam")
                    pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False" , region = "marthandam")
                    #d_original
                    d_original = d_original_productsmodel.objects.filter(region = "marthandam")
                    d_original_length = d_original_productsmodel.objects.filter(status = "False" , region = "marthandam")
                    #jwellery
                    jwellery = jewel_productsmodel.objects.filter(region = "marthandam")
                    jwellery_length = jewel_productsmodel.objects.filter(status = "False" , region = "marthandam")
            
            elif request.POST['region_select'] == "karungal":
                #shopping
                    shop_product = shop_productsmodel.objects.filter(region = "karungal")
                    shop_product_length = shop_productsmodel.objects.filter(status = "False" , region = "karungal")
                    #foods
                    food_product = food_productsmodel.objects.filter(region = "karungal")
                    food_product_length = food_productsmodel.objects.filter(status = "False" , region = "karungal")
                    #fresh_cuts
                    fresh_cuts = fresh_productsmodel.objects.filter(region = "karungal")
                    fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False" , region = "karungal")
                    #daily_mio
                    daily_mio = dmio_productsmodel.objects.filter(region = "karungal")
                    daily_mio_length = dmio_productsmodel.objects.filter(status = "False" , region = "karungal")
                    #pharmacy
                    pharmacy = pharmacy_productsmodel.objects.filter(region = "karungal")
                    pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False" , region = "karungal")
                    #d_original
                    d_original = d_original_productsmodel.objects.filter(region = "karungal")
                    d_original_length = d_original_productsmodel.objects.filter(status = "False" , region = "karungal")
                    #jwellery
                    jwellery = jewel_productsmodel.objects.filter(region = "karungal")
                    jwellery_length = jewel_productsmodel.objects.filter(status = "False" , region = "karungal")
            
            elif request.POST['region_select'] == "nithiravilai":
                #shopping
                    shop_product = shop_productsmodel.objects.filter(region = "nithiravilai")
                    shop_product_length = shop_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
                    #foods
                    food_product = food_productsmodel.objects.filter(region = "nithiravilai")
                    food_product_length = food_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
                    #fresh_cuts
                    fresh_cuts = fresh_productsmodel.objects.filter(region = "nithiravilai")
                    fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
                    #daily_mio
                    daily_mio = dmio_productsmodel.objects.filter(region = "nithiravilai")
                    daily_mio_length = dmio_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
                    #pharmacy
                    pharmacy = pharmacy_productsmodel.objects.filter(region = "nithiravilai")
                    pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
                    #d_original
                    d_original = d_original_productsmodel.objects.filter(region = "nithiravilai")
                    d_original_length = d_original_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
                    #jwellery
                    jwellery = jewel_productsmodel.objects.filter(region = "nithiravilai")
                    jwellery_length = jewel_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
            
        else:
            productid = request.POST['product_id']
            status = request.POST['status']
            category = request.POST['category']
            if category == "shopping":
                if status == "True":
                    update = shop_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = shop_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            elif category == "food":
                if status == "True":
                    update = food_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = food_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            elif category == "fresh_cuts":
                if status == "True":
                    update = fresh_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = fresh_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            elif category == "daily_mio":
                if status == "True":
                    update = dmio_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = dmio_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            elif category == "pharmacy":
                if status == "True":
                    update = pharmacy_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = pharmacy_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            elif category == "d_original":
                if status == "True":
                    update = d_original_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = d_original_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            elif category == "jewellery":
                if status == "True":
                    update = jewel_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = jewel_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            print("update successfully")
    context = {
        'region_area':region_area,
        'shopping':shop_product,
        'shop_product_length':shop_product_length,
        "food_product":food_product,
        'food_product_length':food_product_length,
        'fresh_cuts':fresh_cuts,
        'fresh_cuts_length':fresh_cuts_length,
        'daily_mio':daily_mio,
        'daily_mio_length':daily_mio_length,
        'pharmacy':pharmacy,
        'pharmacy_length':pharmacy_length,
        'd_original':d_original,
        'd_original_length':d_original_length,
        'jwellery':jwellery,
        'jwellery_length':jwellery_length,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
        
        
    }   
    

    return render(request,'admin_product_appaoval.html',context)

def edit_product(request,product_id,category,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    print(category)
    if "shopping" == category:
        product = shop_productsmodel.objects.get(product_id = product_id)
        for_custom_description = shop_productsmodel.objects.get(product_id = product_id)
        shop_id = product.shop_id
        print(type(product.product['other_images']))
        print(product.product['other_images'])
    elif "food" == category:
        product = food_productsmodel.objects.get(product_id = product_id)
        for_custom_description = food_productsmodel.objects.get(product_id = product_id)
        shop_id = product.food_id
    elif "fresh_cuts" == category:
        product = fresh_productsmodel.objects.get(product_id = product_id)
        for_custom_description = fresh_productsmodel.objects.get(product_id = product_id)
        shop_id = product.fresh_id
    elif "daily_mio" == category:
        product = dmio_productsmodel.objects.get(product_id = product_id)
        for_custom_description = dmio_productsmodel.objects.get(product_id = product_id)
        shop_id = product.dmio_id

    elif "pharmacy" == category:
        product = pharmacy_productsmodel.objects.get(product_id = product_id)
        for_custom_description = pharmacy_productsmodel.objects.get(product_id = product_id)
        shop_id = product.dmio_id

    elif "d_original" == category:
        product = d_original_productsmodel.objects.get(product_id = product_id)
        for_custom_description = d_original_productsmodel.objects.get(product_id = product_id)
        shop_id = product.d_id
    elif "jewellery" == category:
        product = jewel_productsmodel.objects.get(product_id = product_id)
        for_custom_description = jewel_productsmodel.objects.get(product_id = product_id)
        shop_id = product.jewel_id


    custom_description = for_custom_description.product
    try:
        custom_description.pop("name")
    except:
        pass
    try:
        custom_description.pop("brand")
    except:
        pass
    try:
        custom_description.pop("actual_price")
    except:
        pass
    try:
        custom_description.pop("discount_price")
    except:
        pass
    try:
        custom_description.pop("status")
    except:
        pass
    try:
        custom_description.pop("category")
    except:
        pass
    try:
        custom_description.pop("subcategory")
    except:
        pass
    try:
        custom_description.pop("shop_id")
    except:
        pass
    try:
        custom_description.pop("product_id")
    except:
        pass
    try:
        custom_description.pop("primary_image")
    except:
        pass
    try:
        custom_description.pop("other_images")
    except:
        pass
    try:
        custom_description.pop("selling_price")
    except:
        pass
    try:
        custom_description.pop("reason")
    except:
        pass
    try:
        custom_description.pop("delivery_type")
    except:
        pass
        
    # print(custom_description)
    context = {
        "shop_product":product,
        "custom_description":custom_description,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }
    
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        print(product.category)
        print(request.POST.getlist('key'))
        print(request.POST.getlist('value'))
        for_product = dict(request.POST)
        for_product.pop("csrfmiddlewaretoken")
        try:
            for_product.pop("key")
        except:
            pass
        try:
            for_product.pop("value")
        except:
            pass
        #add custome discription
        new_data={}
        for x,y in zip(request.POST.getlist('key'),request.POST.getlist('value')):
            new_data[x] = y.split()
        print(new_data)
        for_product.update(new_data)
        print(for_product)
        #image saving
        fs = FileSystemStorage()
        #primary image
        if "primary_image" in request.FILES:
            filepath = os.path.join(settings.MEDIA_ROOT, product.product['primary_image'][29:])
            print(product.product['primary_image'][29:])
            print(filepath)
            if os.path.exists(filepath):
                print("in")
                os.remove(filepath)
                primary_image = str(request.FILES['primary_image']).replace(" ", "_")
                primary_image_path = fs.save(f"api/shop_products/{shop_id}/primary_image/"+primary_image, request.FILES['primary_image'])
                primary_image_paths = all_image_url+fs.url(primary_image_path)
        else:
            primary_image_paths = product.product['primary_image']
        print(primary_image_paths)
        #other image
        if "other_images" in request.FILES:
            old_image = product.product['other_images']
            other_image_image = str(request.FILES['other_images']).replace(" ", "_")
            other_image_path = fs.save(f"api/shop_products/{shop_id}/other_images/"+other_image_image, request.FILES['other_images'])
            other_imagelist = all_image_url+fs.url(other_image_path)
            old_image.append(other_imagelist)
            # for i in product.product['other_images']:
            #     print(i)
            #     filepath = os.path.join(settings.MEDIA_ROOT, i[29:])
            #     print(filepath)
            #     if os.path.exists(filepath):
            #         print("in")
            #         os.remove(filepath)
            # other_image = []
            # other_imagelist = []
            # for sav in request.FILES.getlist('other_images'):
            #     ot = fs.save(f"api/shop_products/{shop_id}/other_images/"+str(sav).replace(" ","_"), sav) 
            #     other_image.append(str(ot))
                    
            #     print(other_image)
            #     for iname in other_image:
            #         other_images_path = iname
            #         other_imagelist.append(all_image_url+fs.url(other_images_path))
        else:
            other_imagelist = product.product['other_images']
        print(other_imagelist)
        cleaned_data_dict ={key:value[0] if isinstance(value,list) and len(value)==1 else value for key,value in for_product.items()}
        # cleaned_data_dict.pop("other_images")
        cleaned_data_dict['primary_image'] = primary_image_paths
        cleaned_data_dict['other_images'] = old_image
        print(cleaned_data_dict)
        #save
        product.category = request.POST['category']
        product.category = request.POST['category']
        product.subcategory = request.POST['subcategory']
        if "subcategory1" in request.POST:
            product.subcategory1 = request.POST['subcategory1']
        product.product = cleaned_data_dict
        product.save()
        print("update successfully")
        return redirect(f"/admin/edit_product/{product_id}/{product.category}/{access_priveleges}")
    return render(request,'product_edit.html',context)

def delete_other_image(request,product_id,position,access_priveleges):
    data = shop_productsmodel.objects.get(product_id = product_id)
    data1 = data.product['other_images']
    data1.pop(int(position))
    print(data1)
    return redirect(f"/admin/edit_product/{product_id}/{data.category}/{access_priveleges}")
def hub_details(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    hub= zone.objects.all()
    if request.method == "POST":
        print(request.POST)
        create = Hub_CustomUser.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            username = request.POST['username'],
            password = request.POST['password'],
            phonenumber = request.POST['phonenumber'],
            hub = request.POST['hub'],
            door_no = request.POST['door_no'],
            street = request.POST['street'],
            city = request.POST['city'],
            state = request.POST['state'],
            country = request.POST['country']
        )
        create.save()
        return redirect(f"/admin_hub_menu1/{authenticate.username}")
    context = {
        'hub':hub,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }
    return render(request,'admin_hub_details.html',context)

def hub_menu1(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    region_area = "REGION"
    data = Hub_CustomUser.objects.all()
    
    
    if request.method == "POST":
        if "region_select" in request.POST:
            region_area = request.POST['region_select']
            if request.POST['region_select'] == "nagercoil":
               data = Hub_CustomUser.objects.filter(hub = "nagercoil")
        
            elif request.POST['region_select'] == "kanniyakumari":
                data = Hub_CustomUser.objects.filter(hub = "kanniyakumari")
            elif request.POST['region_select'] == "thuckalay":
                data = Hub_CustomUser.objects.filter(hub = "thuckalay")
            elif request.POST['region_select'] == "marthandam":
                data = Hub_CustomUser.objects.filter(hub = "marthandam")
            elif request.POST['region_select'] == "karungal":
                data = Hub_CustomUser.objects.filter(hub = "karungal")            
            elif request.POST['region_select'] == "nithiravilai":
                data = Hub_CustomUser.objects.filter(hub = "nithiravilai")
        else:
            dele = Hub_CustomUser.objects.get(id  = request.POST['delete'])
            dele.delete()
            return redirect(f"/admin_hub_menu1/{authenticate.username}")
    context = {
        'region_area':region_area,
        'data':data,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }
    return render(request,'admin_hub_menu1.html',context)

def hub_update(request,id,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    data = Hub_CustomUser.objects.get(id = id)
    context={
        'data':data,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }
    
    if request.method == "POST":
        data.name = request.POST['name']
        data.email = request.POST['email']
        data.username = request.POST['username']
        data.password = request.POST['password']
        data.phonenumber = request.POST['phonenumber']
        data.hub = request.POST['hub']
        data.door_no = request.POST['door_no']
        data.street = request.POST['street']
        data.city = request.POST['city']
        data.state = request.POST['state']
        data.country = request.POST['country']
        data.save()
        return redirect(f"/admin_hub_menu1/{authenticate.username}")
    return render(request,"hub_user_update.html",context)



def user_add(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    if request.method == "POST":
        print(request.POST)
        create = admin_CustomUser.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            username = request.POST['username'],
            password = request.POST['password'],
            phonenumber = request.POST['phonenumber'],
            access_priveleges = str(request.POST.getlist('access_priveleges'))
        )
        create.save()
        return redirect(f"/admin_user_menu/{authenticate.username}")
    context = {
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }
    return render(request,'admin_usar_add.html',context)

def user_menu(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    data1 = User.objects.all()
    data = admin_CustomUser.objects.all()
    context = {
        'data':data,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }
    
    if request.method == "POST":
        dele = admin_CustomUser.objects.get(id  = request.POST['delete'])
        dele.delete()
        return redirect(f"/admin_user_menu/{authenticate.username}")
    return render(request,'admin_user_menu.html',context)


def user_update(request,id,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    data = admin_CustomUser.objects.get(id = id)
    context={
        'data':data,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }
    
    if request.method == "POST":
        data.name = request.POST['name']
        data.email = request.POST['email']
        data.username = request.POST['username']
        data.password = request.POST['password']
        data.phonenumber = request.POST['phonenumber']
        data.access_priveleges = request.POST.getlist('access_priveleges')
        data.save()
        return redirect(f"/admin_user_menu/{authenticate.username}")
    return render(request,"admin_user_update.html",context)

def customer(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    data = End_Usermodel.objects.all()
    context = {
        'data':data,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }
    
    return render(request,'customer_menu.html',context)

def delivery_boy_add(request,add,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    try:
        data = Delivery_model.objects.get(uid = add)
        context = {
        'data':data,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
        }
      
        print(data.phone_number)
    except:
        context = {
            'authenticate':authenticate,
            'access_priveleges':authenticate.access_priveleges,
        }

    
    if request.POST:
        print(request.POST)
        print(request.FILES)
        if "phone_number" in request.POST:
            print("value arrived")
            if Delivery_model.objects.filter(phone_number = request.POST['phone_number']).exists() == True:
                context['error'] = "Phone Number Already Exists"
            else:
                global phone_number
                phone_number = request.POST['phone_number']
                global pin
                pin = random.randint(1000,9999)
                print(pin)
                url = "https://www.fast2sms.com/dev/bulkV2"

                payload = f"variables_values={pin}&route=otp&numbers={request.POST['phone_number']}"
                headers = {
                    'authorization': "ngpY1A5PqHfF0IE7SzsceVhBM6OmtjQxbRr9KCiwL2aGJoD8vkALKMNP8Sfp6Tk3Csouw427rDFga0Ox",
                    'Content-Type': "application/x-www-form-urlencoded",
                    'Cache-Control': "no-cache",
                    }

                response = requests.request("POST", url, data=payload, headers=headers)

                print(response.text)
                # Service Route Success Response:
                {
                    "return": True,
                    "request_id": "lwdtp7cjyqxvfe9",
                    "message": [
                        "Message sent successfully"
                    ]
                }
        elif "otp" in request.POST:
            print(pin)
            print(request.POST.getlist("otp"))
            user_pin = ""
            for x in request.POST.getlist("otp"):
                user_pin += x
            print(user_pin)
            if pin ==  int(user_pin):
                print("pin match")
                generate_uid = delivery_extension.id_generate()
                create = Delivery_model.objects.create(
                    uid = generate_uid,
                    otp = user_pin,
                    phone_number = phone_number,
                   
                )
                create.save()
                return redirect(f"/admin/delivery_boy_add/{generate_uid}/{authenticate.username}")
            else:
                error1 = "Invalid OTP"
                print(error1)
                context['error1'] = error1

        else:
            if Delivery_model.objects.filter(email = request.POST['email']).exists() == True:
                context['error'] = "Email Already Exists"
            else:
                data1 = Delivery_model.objects.get(uid = add)
                fs = FileSystemStorage()
         
                profile_picture = str(request.FILES['profile_picture']).replace(" ", "_")
                profile_picturepath = fs.save(f"api/delivery/profile_picture/"+profile_picture, request.FILES['profile_picture'])
                bank_passbok_pic = str(request.FILES['bank_passbok_pic']).replace(" ", "_")
                bank_passbok_pic_path = fs.save(f"api/delivery/bank_passbok_pic/"+bank_passbok_pic, request.FILES['bank_passbok_pic'])
                aadhar_pic = str(request.FILES['aadhar_pic']).replace(" ", "_")
                aadhar_pic_path = fs.save(f"api/delivery/aadhar_pic/"+aadhar_pic, request.FILES['aadhar_pic'])
                pan_pic = str(request.FILES['pan_pic']).replace(" ", "_")
                pan_pic_path = fs.save(f"api/delivery/pan_pic/"+pan_pic, request.FILES['pan_pic'])
                drlicence_pic = str(request.FILES['drlicence_pic']).replace(" ", "_")
                drlicence_pic_path = fs.save(f"api/delivery/drlicence_pic/"+drlicence_pic, request.FILES['drlicence_pic'])

            
                profile_picturepaths = all_image_url+fs.url(profile_picturepath)
                bank_passbok_pic_paths = all_image_url+fs.url(bank_passbok_pic_path)
                aadhar_pic_paths = all_image_url+fs.url(aadhar_pic_path)
                pan_pic_paths = all_image_url+fs.url(pan_pic_path)
                drlicence_pic_paths = all_image_url+fs.url(drlicence_pic_path)
                data1.name = request.POST["name"]
                data1.wp_number = request.POST["wp_number"]
                data1.email = request.POST["email"]
                data1.aadhar_number = request.POST["aadhar_number"]
                data1.driving_licensenum = request.POST["driving_licensenum"]
                data1.pan_number = request.POST["pan_number"]
                data1.profile_picture = profile_picturepaths
                data1.bank_name = request.POST["bank_name"]
                data1.acc_number = request.POST["acc_number"]
                data1.name_asper_passbook = request.POST["name_asper_passbook"]
                
                data1.ifsc_code = request.POST["ifsc_code"]
                data1.bank_passbok_pic = bank_passbok_pic_paths
                data1.aadhar_pic = aadhar_pic_paths
                data1.pan_pic = pan_pic_paths
                data1.drlicence_pic = drlicence_pic_paths
                data1.delivery_type = request.POST["delivery_type"]
                data1.region = request.POST["region"]
                data1.approve_status = "False"
                data1.save()
                print("Update Successfully")
                return redirect(f"/admin/delivery_boy_manage/{authenticate.username}")
                # datas = {
                        # 'name':request.data["name"],
                        # 'wp_number': request.data['wp_number'],
                        # 'email': request.data["email"],
                        # 'aadhar_number':request.data['aadhar_number'],                    
                        # 'driving_licensenum':request.data['driving_licensenum'],
                        # 'pan_number':request.data['pan_number'],                    
                        # 'profile_picture':profile_picturepaths,
                        # 'bank_name':request.data['bank_name'],
                        # 'acc_number':request.data['acc_number'],
                        # 'name_asper_passbook':request.data['name_asper_passbook'],
                        # 'ifsc_code':request.data['ifsc_code'],
                        # 'bank_passbok_pic':bank_passbok_pic_paths,
                        # 'aadhar_pic':aadhar_pic_paths,
                        # 'pan_pic':pan_pic_paths,
                        # 'drlicence_pic':drlicence_pic_paths,
                        # 'delivery_type':request.data['delivery_type'],
                        # 'region':request.data['region'],
                       
                # }

                
        # product={}
        # for x in dict(request.POST):
        #     print(x)
        #     product[x] = dict(request.POST)[x][0]
        # print(product)
        # Response = requests.post("http://127.0.0.1:3000/delivery_person_signup/",data = request.POST,files=request.FILES)
        # print(Response)
        # print(Response.status_code)
        # if Response.status_code == 200:
        #     return redirect("/admin/delivery_boy_manage/")
        # elif Response.status_code == 302:
        #     error = "Email Id Already Existed"
    return render(request,'deliveryboy_add.html',context)

def delivery_otp(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    error1 = ""
    if request.method == "POST":
        print(request.POST)
        
        # return redirect("/admin/delivery_boy_add/add")
    context = {
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }
    return render(request,'delivery_otp.html',context)


def delivery_boy_manage(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    region_area = "REGION"
    data  = Delivery_model.objects.all()
    

    if request.method == "POST":
        if "region_select" in request.POST:
            region_area = request.POST['region_select']
            data  = Delivery_model.objects.filter(region = request.POST['region_select'])
            # if request.POST['region_select'] == "nagercoil":
            #     data  = Delivery_model.objects.filter(region = request.POST['region_select'])
            # elif request.POST['region_select'] == "kanniyakumari":
            #     data  = Delivery_model.objects.filter(region = request.POST['region_select'])     
            # elif request.POST['region_select'] == "thuckalay":
            #     data = Delivery_model.objects.filter(region = request.POST['region_select'])            
            # elif request.POST['region_select'] == "marthandam":
            #     data  = Delivery_model.objects.filter(region = request.POST['region_select'])
            # elif request.POST['region_select'] == "karungal":
            #     data  = Delivery_model.objects.filter(region = request.POST['region_select'])      
            # elif request.POST['region_select'] == "nithiravilai":
            #     data  = Delivery_model.objects.filter(region = request.POST['region_select'])

        else:
            print(request.POST)
            update_data = Delivery_model.objects.get(uid = request.POST['uid'])
            update_data.approve_status = request.POST['status']
            update_data.save()
    context = {
        'region_area' : region_area,
        'data':data,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }
    return render(request,'deliverboy_menu.html',context)

def delivery_boy_single(request,id,access_priveleges):
    
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    data = Delivery_model.objects.get(uid = id)
    delivery_history = Product_Ordermodel.objects.filter(deliveryperson__uid = id)
    paid_amount = 0
    for i in delivery_history:
        print(i.float_cash)
        paid_amount += float(i.float_cash)
    if type(paid_amount) is float:
        # Convert the decimal number to a string
        decimal_string = str(paid_amount)

        # Find the index of the decimal point
        decimal_point_index = decimal_string.index('.')

        # Get the decimal value with the last two digits
        decimal_last_two_digits = decimal_string[:decimal_point_index + 3]
    else:
        decimal_last_two_digits = paid_amount
    print(decimal_last_two_digits)
    total_amount = 0
    for j in delivery_history:
        print(j.total_amount)
        total_amount += float(j.total_amount)
    balance_amount = total_amount - paid_amount
    if type(balance_amount) is float:
                # Convert the decimal number to a string
                decimal_string = str(balance_amount)

                # Find the index of the decimal point
                decimal_point_index = decimal_string.index('.')

                # Get the decimal value with the last two digits
                decimal_last_two_digits_balance = decimal_string[:decimal_point_index + 3]
    else:
        decimal_last_two_digits_balance = balance_amount
    context={
        'data':data,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
        'delivery_history':delivery_history,
        'paid_amount':decimal_last_two_digits,
        'balance_amount':decimal_last_two_digits_balance,
    }
      
    return render(request,'deliverboy_single.html',context)

def delivery_Commision(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    data = comission_Editing.objects.get(id = 1)
    context = {
        'data':data,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }
    
    if request.method == "POST":
        data.per_km = request.POST['per_km']
        data.incentive = request.POST['incentive']
        data.normal_delivery_commision = request.POST['normal_delivery_commision']
        data.save()
        return redirect(f"/admin/delivery_Commision/{authenticate.username}")
    return render(request,'delivery_commision.html',context)

def business_Commision(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    data = business_commision.objects.get(id = 1)
    context = {
        'data':data,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }
    
    if request.method == "POST":
        data.commission = request.POST['commission']
        data.gst = request.POST['gst']
        data.save()
        return redirect(f"/admin/business_Commision/{authenticate.username}")

    return render(request,'business_commsion.html',context)


def shutdownnn(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    data = shutdown.objects.get(id = 1)
    if request.method == "POST":
        print(request.POST)
        shutdownn = shutdown.objects.get(id = 1)
        if "shopping" in request.POST:
            shutdownn.shopping = request.POST['shopping']
            shutdownn.save()
        elif "food" in request.POST:
            shutdownn.food = request.POST['food']
            shutdownn.save()
        elif "fresh_cuts" in request.POST:
            shutdownn.fresh_cuts = request.POST['fresh_cuts']
            shutdownn.save()
        elif "daily_mio" in request.POST:
            shutdownn.daily_mio = request.POST['daily_mio']
            shutdownn.save()
        elif "pharmacy" in request.POST:
            shutdownn.pharmacy = request.POST['pharmacy']
            shutdownn.save()
        elif "d_original" in request.POST:
            shutdownn.d_original = request.POST['d_original']
            shutdownn.save()
        elif "jewellery" in request.POST:
            shutdownn.jewellery = request.POST['jewellery']
            shutdownn.save()
        return redirect(f"/admin/shutdown/{authenticate.username}")
        
    context = {
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
        'data':data
    }
    return render(request,'showdown.html',context)

def zonee(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    data = zone.objects.all()
    context = {
        'zone':data,
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
    }

    if request.method == "POST":
        print(request.POST)
        if "create" in request.POST:
            create = zone.objects.create(
                zone = request.POST['zone'].lower()
            )
            create.save()
        elif "add_zone" in request.POST:
            
            add = zone.objects.get(zone = request.POST['zone'])
            try:
                pincodee=add.pincode
                pincodee.append(request.POST['pincode'])
            except:
                pincodee = []
                pincodee.append(request.POST['pincode'])
            
            print(pincodee)
            add.pincode = pincodee
            add.save()
        elif "delete_pincode" in request.POST:
            deletepincode = zone.objects.get(zone = request.POST['delete_pincode'])
            pincode = deletepincode.pincode
            pincode.remove(request.POST['pincode'])
            deletepincode.pincode = pincode
            deletepincode.save()
        elif "delete_zone" in request.POST:
            deletezone = zone.objects.get(zone = request.POST['delete_zone'])
            print(deletezone)
            deletezone.delete()
        return redirect(f"/admin/zone/{authenticate.username}")
    return render(request,'zone.html',context)

def hsn(request,access_priveleges):
    try:
        authenticate = User.objects.get(username = access_priveleges)
    except:
        authenticate = admin_CustomUser.objects.get(username = access_priveleges)
    data = hsn_code.objects.all()
    context = {
        'authenticate':authenticate,
        'access_priveleges':authenticate.access_priveleges,
        'data':data,
    }
    if request.method == "POST":
        if 'filter' in request.POST:
            pass
        elif "add" in request.POST:
            print(request.POST)
            create = hsn_code.objects.create(
                hsn_code = request.POST['hsn_code'],
                goods = request.POST['goods'],
                gst = request.POST['gst']
            )
            create.save()
        elif "delete" in request.POST:
            delete = hsn_code.objects.get(id = request.POST['delete'])
            delete.delete()
        elif "edit" in request.POST:
            edit = hsn_code.objects.get(id = request.POST['edit'])
            edit.hsn_code = request.POST['hsn_code']
            edit.goods = request.POST['goods']
            edit.gst = request.POST['gst']
            edit.save()
        return redirect(f"/admin/hsn/{authenticate.username}")
    return render(request,'hsn.html',context)

@api_view(['GET'])
def get_shutdown(request):
    data = shutdown.objects.filter(id = 1).values()
    return Response(data,status=status.HTTP_200_OK)

@api_view(['POST'])
def hsn_verification(request,hsn_codee):
    if request.method == "POST":
        if hsn_code.objects.filter(hsn_code = hsn_codee).exists() == True:
            data = hsn_code.objects.get(hsn_code = hsn_codee)
            return Response({'result': 'valid key', 'gst': data.gst[0]},status=status.HTTP_200_OK)
        else:
            return Response({'result':'Invalid key'},status=status.HTTP_404_NOT_FOUND)
  
  
@api_view(['POST']) 
def emergency(request,uid):
    try:
        if request.method == "POST":
            print(uid)
            print(request.data['emergency'])
            data = Delivery_model.objects.get(uid = uid)
            data.emergency = int(request.data['emergency'])
            data.save()
            return Response("emergency",status=status.HTTP_200_OK)
    except:
        return Response("error",status=status.HTTP_400_BAD_REQUEST) 



