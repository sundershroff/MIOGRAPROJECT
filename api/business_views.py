from django.shortcuts import render,get_object_or_404
from api.models import Businessmodel,shoppingmodel,jewellerymodel,foodmodel,freshcutsmodel,pharmacy_model,d_originalmodel,dailymio_model
from api import business_serializers,end_user_serializers
from bson import ObjectId    
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework import status,generics
from django.core.files.storage import FileSystemStorage
from api import business_extension
from rest_framework.decorators import api_view
from api import models
import json
import datetime
from django.http import JsonResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from pymongo import MongoClient
from bson.json_util import dumps,loads
from django.db.models import Sum,Avg
from django.utils import timezone
import datetime
from django.db import transaction
from django.db.models import Q
from mio_admin.models import business_commision,zone
from geopy.distance import geodesic
from mio_admin.models import comission_Editing,zone
import requests

jsondec = json.decoder.JSONDecoder()
all_image_url = "https://miogra.clovion.org/"
x = datetime.datetime.now()

from django.db import transaction

def send_notification(registration_ids, message_title, message_desc):
    for x in registration_ids:
        fcm_api = "AAAAwN1-l3g:APA91bF58TyTj5cEDKz6qpeltmumxQEnzh9xwDN9A9QXLcNEzdAJGY1DrURU9xFOqOpdBA0SMyYd7MrAxtmYp4iWVBHuPhICBZHLFoLj9x6-tQicyMVUWwnM_0KYESKY7kxHqXS2C3P3"
        url = "https://fcm.googleapis.com/fcm/send"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": 'key=' + fcm_api
        }
    
        payload = {
            "registration_ids": [x],
            "priority": "high",
            "notification": {
                "body": message_desc, 
                "title": message_title,
                "image": "https://miogra.clovion.org//static/assets/images/logo/Miogra_logo.png",
                "icon": "https://miogra.clovion.org//static/assets/images/logo/Miogra_logo.png",
            }
        }

        try:
            result = requests.post(url, data=json.dumps(payload), headers=headers)
            print(result.status_code)
            print(result.text) 
    
            with transaction.atomic():  # Ensure atomic transaction
                # Save notification to the database
                sender_id=models.Businessmodel.objects.get(device_id=registration_ids)
                print(sender_id)
                notification = models.Notification.objects.create(
                    notify_id=business_extension.id_generate(),
                    recipient=registration_ids, 
                    message_title=message_title,
                    message_desc=message_desc,
                    sender_id=sender_id.uid,
    
                )
                notification.save()

        except requests.exceptions.RequestException as e:
            print("Failed to send notification:", e)


# send_notification("dShDvq88TLGL6C6BIbJunp:APA91bEYthyTG2otBBcmnmHzh9AMeGrpatBuRy2aFgv3SCqa3evPhs5CZVsMvhWrm03AwXI8Q-rVKZljiLD9hM7xfhcx0Q-qXMQMg1Cl989SY4zUCBG8vfSBEyOF9_mt1v9e1oKpKVPs" , 'you have got a text message' , 'deliveryperson order accepted')

def deliverysend_notification(message_title, message_desc):
    fcm_api = "AAAAbIibZeo:APA91bEHlJFNQjqRjMjX2N-YfgDAjOU_fXdt8HkQiQYhOYbGcv9B6MqGykeaG7zQVdrMOEQrOGckrUwKbl4XWdEOboEY9uDUSALHdzbpdW-DJbUxlVzCG_ayQJIPJfAnEPcCeKX86sqg"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key=' + fcm_api
    }

    delivery = models.deliverylogintable_model.objects.filter(status=True, delivery_type="Quick") | models.deliverylogintable_model.objects.filter(status=True, delivery_type="quick")
    for delivery_person in delivery:
        registration_id = jsondec.decode(delivery_person.deliveryperson.device_id)
        for x in registration_id:
            payload = {
                "registration_ids": [x],
                "priority": "high",
                "notification": {
                    "body": message_desc,
                    "title": message_title,
                    "image": "https://miogra.clovion.org//static/assets/images/logo/Miogra_logo.pnghttps://miogra.clovion.org//static/assets/images/logo/Miogra_logo.png",
                    "icon": "https://miogra.clovion.org//static/assets/images/logo/Miogra_logo.png",
                }
            }
            result = requests.post(url, data=json.dumps(payload), headers=headers)
            print(result.status_code)
            print(result.json())
            try:
                
    
                with transaction.atomic():  # Ensure atomic transaction
                    # Save notification to the database
                    sender_id = models.Delivery_model.objects.get(uid = delivery_person.deliveryperson.uid)
                    notification = models.Notification.objects.create(
                        notify_id=business_extension.id_generate(),
                        recipient=registration_id,
                        message_title=message_title,
                        message_desc=message_desc,
                        sender_id=sender_id.uid,
                    )
                    notification.save()
                    print("saved")

            except requests.exceptions.RequestException as e:
                print("Failed to send notification:", e)

def deliverysend_notification_pickup(registration_id,message_title, message_desc,uid):
    fcm_api = "AAAAbIibZeo:APA91bEHlJFNQjqRjMjX2N-YfgDAjOU_fXdt8HkQiQYhOYbGcv9B6MqGykeaG7zQVdrMOEQrOGckrUwKbl4XWdEOboEY9uDUSALHdzbpdW-DJbUxlVzCG_ayQJIPJfAnEPcCeKX86sqg"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key=' + fcm_api
    }


    for x in registration_id:
        payload = {
            "registration_ids": [x],
            "priority": "high",
            "notification": {
                "body": message_desc,
                "title": message_title,
                "image": "https://miogra.clovion.org//static/assets/images/logo/Miogra_logo.pnghttps://miogra.clovion.org//static/assets/images/logo/Miogra_logo.png",
                "icon": "https://miogra.clovion.org//static/assets/images/logo/Miogra_logo.png",
            }
        }
        try:
            result = requests.post(url, data=json.dumps(payload), headers=headers)
            print(result.status_code)
            print(result.json())

            with transaction.atomic():  # Ensure atomic transaction
                # Save notification to the database
                sender_id = models.Delivery_model.objects.get(uid=uid)
                notification = models.Notification.objects.create(
                    notify_id=business_extension.id_generate(),
                    recipient=registration_id,
                    message_title=message_title,
                    message_desc=message_desc,
                    sender_id=sender_id.uid,
                )
                notification.save()

        except requests.exceptions.RequestException as e:
            print("Failed to send notification:", e)



# def deliverysend_notification(message_title , message_desc):
#     fcm_api = "AAAAbIibZeo:APA91bEHlJFNQjqRjMjX2N-YfgDAjOU_fXdt8HkQiQYhOYbGcv9B6MqGykeaG7zQVdrMOEQrOGckrUwKbl4XWdEOboEY9uDUSALHdzbpdW-DJbUxlVzCG_ayQJIPJfAnEPcCeKX86sqg"
#     url = "https://fcm.googleapis.com/fcm/send"
    
#     headers = {
#     "Content-Type":"application/json",
#     "Authorization": 'key='+fcm_api
#     }    
#     ex_registration_ids=[]
#     delivery = models.deliverylogintable_model.objects.filter(status=True,delivery_type= "Quick")
#     for i in delivery:
#         ex_registration_ids.append((i.deliveryperson.device_id))

#     print(ex_registration_ids)
#     for x in ex_registration_ids:

#         payload = {
#             "registration_ids" :x,
#             "priority" : "high",
#             "notification" : {
#                 "body" : message_desc,
#                 "title" : message_title,
#                 "image" : "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
#                 "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",
                
#             }
#         }
#         try:
#             result = requests.post(url,  data=json.dumps(payload), headers=headers )
#             print(result.status_code)
#             print(result.json())
#             with transaction.atomic():  # Ensure atomic transaction
#                 # Save notification to the database

#                 sender_id=models.Delivery_model.objects.get(device_id=x)
#                 print(sender_id)
#                 notification = models.Notification.objects.create(
#                     notify_id=business_extension.id_generate(),
#                     recipient=x, 
#                     message_title=message_title,
#                     message_desc=message_desc,
#                     sender_id=sender_id.uid,

#                 )
#                 notification.save()

#         except requests.exceptions.RequestException as e:
#             print("Failed to send notification:", e)

# send_notification('hii' , 'hello world')


@api_view(['POST'])
def business_signup(request):
    try:
        try:
            if business_extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                global datas
                x = datetime.datetime.now()
                datas = {
                    'uid': business_extension.id_generate(),
                    'otp': business_extension.otp_generate(),
                    'full_name':request.data["full_name"],
                    'email': request.data["email"],
                    'phone_number': request.data["phone_number"],
                    'password': request.data["password"],
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year),
                    'device_id':request.data.getlist("device_id"),
                }
                print(datas)
                dataserializer = business_serializers.SignupSerializer(data=datas)
                print(dataserializer)
                print(datas['uid'])
                if dataserializer.is_valid():
                    print("valid")
                
                    print("Valid Data")
                    business_extension.send_mail(datas['email'], datas['otp'])
                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def business_otp(request):
    if int(datas['otp']) == int(request.data['user_otp']):
        user = business_serializers.SignupSerializer(data=datas, partial=True)
        
        if user.is_valid():
            user.save()
            return Response(datas['uid'], status=status.HTTP_200_OK)
        else:
            return Response({"Cannot Verify OTP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"Wrong OTP"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def business_signin(request):
    try:
       
        try:
            if business_extension.validate_email(request.data['email']):
                if business_extension.verify_user(request.data['email'], request.data['password']):
                        if business_extension.get_user_id(request.data['email']):
                            data = Businessmodel.objects.get(email = request.data['email'])
                            if data.status == True:
                                print(request.data['device_id'])
                                if request.data['device_id'] not in data.device_id:
                                    print("new")
                                    print(type(data.device_id))
                                    print(data.device_id)
                                    print(type(request.data['device_id']))
                                    data.device_id.append(request.data['device_id'])
                                    data.save()
                                    
                                return Response(business_extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
                            else:
                                return Response({"Your Blocked By Admin"}, status=status.HTTP_403_FORBIDDEN)
                        else:
                            return Response({"Didn't Completed OTP Verification"}, status=status.HTTP_401_UNAUTHORIZED)

                else:
                    return Response({"Password Is Incorrect"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"User Dosn't Exits"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def resend_otp(request,id):

    try:
        try:
            new_otp = business_extension.otp_generate()
            user = Businessmodel.objects.get(uid=id)
            email = user.email 
            print(f"Email: {email}")
            business_extension.send_mail(email, new_otp)
            user.otp = new_otp
            user.save()
            return Response({"New OTP": new_otp, "Email": email}, status=status.HTTP_200_OK)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def my_accounts_data(request,id):
    if request.method == 'GET':
       allDataa = Businessmodel.objects.filter(uid=id)
       alldataserializer = business_serializers.BusinessSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data[0], status=status.HTTP_200_OK)

@api_view(['POST'])
def forget_password(request):

    try:
        try:
            print(request.POST)
            if business_extension.validate_email(request.data['email']):
                Data = Businessmodel.objects.get(email=request.data['email'])

                data1={
                    'email':request.data['email'],
                    'password':request.data['password']
                }
                print(data1)
                basicdetailsserializer = business_serializers.forget_password_serializer(instance=Data, data=data1,partial=True)
                if basicdetailsserializer.is_valid():
                    basicdetailsserializer.save()
                    print("Valid Data")
                    return Response("password updated", status=status.HTTP_200_OK)                        
                else:
                    return Response({"Password Is Incorrect"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"User Dosn't Exits"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def business_profile_picture(request,id):
    try:
        print(request.FILES['profile_picture'])
        fs = FileSystemStorage()
        userdata = Businessmodel.objects.get(uid=id)
        
        profile_picture = str(request.FILES['profile_picture']).replace(" ", "_")
     
        print(id)
        path = fs.save(f"api/business/{id}/profile_picture/"+profile_picture, request.FILES['profile_picture'])
        full_path = all_image_url+fs.url(path)
        print(full_path)

        data = {          
            'profile_picture': full_path
           
        }

        print(data)
        basicdetailsserializer = business_serializers.profile_picture_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def business_profile_update(request, id):
    print(request.POST)
    print(f" profile_picture:{request.FILES}")
    fs = FileSystemStorage()
    userdata = models.Businessmodel.objects.get(uid=id)
    print(userdata)
    datas = Businessmodel.objects.filter(uid=id).values()[0]
    # print(datas)
    if "profile_picture" in request.FILES:
        profile_picture = str(request.FILES['profile_picture']).replace(" ", "_")
        path = fs.save(f"api/business/{id}/profile_picture/" + profile_picture, request.FILES['profile_picture'])
        full_path = all_image_url + fs.url(path)
        print(full_path)
    else:
        full_path = datas['profile_picture']
    print("valid")

    profile_update = Businessmodel.objects.get(uid=id)
    profile_update.phone_number = request.data.get('phone_number', profile_update.phone_number)
    profile_update.profile_picture = full_path
    profile_update.save()
    return Response(id, status=status.HTTP_200_OK)

    # data = {
    #     'phone_number': request.POST['phone_number'],
    #     'profile_picture': full_path
    # }

    # print(data)
    # basicdetailsserializer = business_serializers.update_acc_serializer(
    #     instance=userdata, data=data, partial=True)
    # if basicdetailsserializer.is_valid():
    #     basicdetailsserializer.save()
    #     print("Valid Data")
    #     return Response(id, status=status.HTTP_200_OK)
    # else:
    #     return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)



# shop_dashboard



@api_view(['GET'])
def shop_total_revenue(request, id):
    print(id)
    if request.method == 'GET':
        total_revenue = models.Product_Ordermodel.objects.filter(shop_id_id__shop_id=id,status="delivered").aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0

        shop = models.shoppingmodel.objects.get(shop_id=id)
        shop.total_revenue = total_revenue
        shop.save()

        # notification_data = {

        #     "registration_ids": ["dShDvq88TLGL6C6BIbJunp:APA91bEYthyTG2otBBcmnmHzh9AMeGrpatBuRy2aFgv3SCqa3evPhs5CZVsMvhWrm03AwXI8Q-rVKZljiLD9hM7xfhcx0Q-qXMQMg1Cl989SY4zUCBG8vfSBEyOF9_mt1v9e1oKpKVPs"],
        #     "message_title": "You have got a text message",
        #     "message_desc": "Delivery person order accepted"
        # }
        # send_notification(**notification_data)
 
        return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)
    else:
        return Response("Shop order not found", status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['GET'])
# def shop_total_revenue(request,id):
#     print(id)
#     if request.method == 'GET':

#         total_revenue = models.Product_Ordermodel.objects.filter(shop_id_id__shop_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
#         # print(total_revenue)
#         shop = models.shoppingmodel.objects.get(shop_id=id)
#         shop.total_revenue = total_revenue
#         shop.save()
#         notification_data = {
#                 "message_title": "you have got a text message",
#                 "message_desc": "deliveryperson order accepted"
#             }
#         send_notification("dShDvq88TLGL6C6BIbJunp:APA91bEYthyTG2otBBcmnmHzh9AMeGrpatBuRy2aFgv3SCqa3evPhs5CZVsMvhWrm03AwXI8Q-rVKZljiLD9hM7xfhcx0Q-qXMQMg1Cl989SY4zUCBG8vfSBEyOF9_mt1v9e1oKpKVPs" ,"you have got a text message","deliveryperson order accepted")

#         return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)
#     else:
#         return Response("shop_ordernot found",status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def shop_mon_revenue(request, id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        monthly_revenue = models.Product_Ordermodel.objects.filter(shop_id_id__shop_id=id,status="delivered", order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
        shop = models.shoppingmodel.objects.get(shop_id=id)
        shop.monthly_revenue = monthly_revenue
        shop.save()
        return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)
    else:
        return Response("shop_ordernot found",status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def shop_orderstatus(request,id):
    if request.method == 'GET':

        shop = models.Product_Ordermodel.objects.filter(shop_id_id__shop_id=id).first()
        # if not shop:
            # return Response(data={'error': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.Product_Ordermodel.objects.filter(shop_id_id__shop_id=id, status='delivered').count()
        cancelled_count = models.Product_Ordermodel.objects.filter(shop_id_id__shop_id=id, status='return').count()
        on_process_count = models.Product_Ordermodel.objects.filter(shop_id_id__shop_id=id, status='ready_to_pickup').count()
        delivered_count = delivered_count if delivered_count else 0
        cancelled_count = cancelled_count if cancelled_count else 0
        on_process_count = on_process_count if on_process_count else 0
        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
    else:
        return Response("shop_ordernot found",status=status.HTTP_400_BAD_REQUEST)








@api_view(["POST"])
def update_product_order_status_reject(request, id, product_id, order_id):
    try:
        business = models.Businessmodel.objects.get(uid=id)
        print(business.uid)
        try:
            product_order = models.Product_Ordermodel.objects.get(business__uid=business.uid, product_id=product_id, order_id=order_id)
            # Delete the order
            product_order.delete()
            return Response("Order deleted successfully", status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("Product order not found", status=status.HTTP_404_NOT_FOUND)
    except models.Businessmodel.DoesNotExist:
        return Response("Business not found", status=status.HTTP_404_NOT_FOUND)



@api_view(["POST"])
def update_product_order_status_accept(request,id,product_id,order_id):
    try:
        business = models.Businessmodel.objects.get(uid=id)
        print(business.uid)

        product_orders = models.Product_Ordermodel.objects.filter(business__uid=business.uid, product_id=product_id, order_id=order_id)
        print(product_orders)

        if product_orders.exists():
            for product_order in product_orders:
                # Update the status field with the new value
                product_order.status = "accepted"
                product_order.save()
            print(order_id)
            if product_order.delivery_type == "Quick":
                end_user= models.Product_Ordermodel.objects.get(order_id=order_id)
                end_user_location = (end_user.end_user.latitude, end_user.end_user.longitude)
                print(end_user_location)
                # shop
                shops=models.Product_Ordermodel.objects.get(order_id=order_id)
                if shops.food_id != None:
                    shop_location = (shops.food_id.latitude, shops.food_id.longitude)
                    print(shop_location)
                elif shops.fresh_id != None:
                    shop_location = (shops.fresh_id.latitude, shops.fresh_id.longitude)
                    print(shop_location)
                elif shops.dmio_id !=None:
                    shop_location = (shops.dmio_id.latitude, shops.dmio_id.longitude)
                    print(shop_location)
                elif shops.pharm_id != None:
                    shop_location = (shops.pharm_id.latitude, shops.pharm_id.longitude)
                    print(shop_location)

                distance = geodesic(shop_location, end_user_location).kilometers
                print(distance)
                deliverydistance=float(distance)
                delivery_distance = "{:.2f}".format(deliverydistance)
                print(delivery_distance)
                
                shops.distance=delivery_distance
                shops.save()
                admin_data = comission_Editing.objects.get(id=1)  
                per_km = (admin_data.per_km)  
                incentive =(admin_data.incentive)
                admin_commision=business_commision.objects.get(id=1)
                commission=admin_commision.commission
                shops.admin_commission_amount=commission
                total_amount=per_km*distance
                shops.incentive=incentive
                shops.order_total=int(total_amount)
                shops.save()
                notification_data = {
                    "message_title": "You have got a text message",
                    "message_desc": "New order arrived"
                }
                message_title = "You have got a text message"
                message_desc = "New order arrived"

                deliverysend_notification(message_title,message_desc)
                return Response("Status updated successfully", status=status.HTTP_200_OK)
            elif product_order.delivery_type == "Normal":
                shops=models.Product_Ordermodel.objects.get(order_id=order_id)
                print(shops)
                admin_data = comission_Editing.objects.get(id=1)
                admin_commision=business_commision.objects.get(id=1)
                commission=admin_commision.commission
                shops.admin_commission_amount=commission
                incentive =(admin_data.normal_delivery_commision)
                shops.incentive=incentive
                shops.order_total=incentive
                shops.save()
                return Response("Status updated successfully", status=status.HTTP_200_OK)

        else:
            return Response("Product order not found", status=status.HTTP_404_NOT_FOUND)
    except:
        return Response("Product order not found", status=status.HTTP_404_NOT_FOUND)



@api_view(["POST"])
def business_status_pickedUp(request,order_id):
    try:
        pro=get_object_or_404(models.Product_Ordermodel,order_id=order_id)
        data = models.Product_Ordermodel.objects.get(order_id=order_id)
        print(data)
        pro.status = "ready_to_pickup"  
        pro.save()
        message_title = "Your order is Ready to pick up"
        message_desc = "Hurry Up"
        print(data.deliveryperson.device_id)
        deliverysend_notification_pickup(jsondec.decode(data.deliveryperson.device_id),message_title,message_desc,data.deliveryperson.uid)
# jsondec.decode
        return Response({"order_id":order_id},status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def business_order_dispatch(request,order_id):
    try:
        pro=get_object_or_404(models.Product_Ordermodel,order_id=order_id)
        
        pro.status= "order_dispatch"
        pro.save()
        return Response({"order_id":order_id},status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

# shopping 
@api_view(['POST'])
def shopping(request,id):
    if request.method == "POST":
        print(request.POST)
        pincode = request.POST['pincode']

        data1 = zone.objects.all()
        print(data1)
        get_zone = None  # Initialize get_zone variable

        for x in data1:
            print(x)
            if x.pincode is not None and pincode in x.pincode:
                get_zone = x.zone
                print(get_zone)
                break  # Once the zone is found, exit the loop

        print(get_zone)  # Check if zone is retrieved correctly
        # print(request.data)
        # print(request.FILES)
        fs = FileSystemStorage()
        aadhar = str(request.FILES['aadhar']).replace(" ", "_")
        aadhar_path = fs.save(f"api/shopping/{id}/aahar/"+aadhar, request.FILES['aadhar'])
        pan_file = str(request.FILES['pan_file']).replace(" ", "_")
        pan_file_path = fs.save(f"api/shopping/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
        profile = str(request.FILES['profile']).replace(" ", "_")
        profile_path = fs.save(f"api/shopping/{id}/profile/"+profile, request.FILES['profile'])
        bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
        bank_passbook_path = fs.save(f"api/shopping/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
        gst_file = str(request.FILES['gst_file']).replace(" ", "_")
        gst_file_path = fs.save(f"api/shopping/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

        aadhar_paths = all_image_url+fs.url(aadhar_path)
        pan_file_paths = all_image_url+fs.url(pan_file_path)
        profile_paths = all_image_url+fs.url(profile_path)
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
        gst_file_paths = all_image_url+fs.url(gst_file_path)
        x = datetime.datetime.now()
        shopping_id=business_extension.shop_id_generate()
        while True:
            if id == shopping_id:
                shopping_id=business_extension.shop_id_generate()
            else:
                break
        



        data = {
            'Business_id': id,
            'shop_id': shopping_id,
            'seller_name': request.POST['seller_name'],
            'business_name': request.POST['business_name'],
            'pan_number': request.POST['pan_number'],
            'gst': request.POST['gst'],
            'contact': request.POST['contact'],
            'alternate_contact': request.POST['alternate_contact'],
            'door_number' : request.POST['door_number'],
            'street_name' : request.POST['street_name'],
            'area' : request.POST['area'],
            'region' : get_zone,
            'pincode': request.POST['pincode'],
            'aadhar_number' : request.POST['aadhar_number'],
            # 'pin_your_location': request.POST['pin_your_location'],           
            'name': request.POST['name'],           
            'account_number':request.POST['account_number'],
            'ifsc_code':request.POST['ifsc_code'],
            'upi_id':request.POST['upi_id'],
            'gpay_number':request.POST['gpay_number'],
            'aadhar':aadhar_paths,
            'pan_file': pan_file_paths,
            'profile': profile_paths,
            'bank_passbook': bank_passbook_paths,
            'gst_file': gst_file_paths,
            'category':"shopping",
            'latitude':request.POST['latitude'],
            'longitude':request.POST['longitude'],
            }

        
        print(data)
        basicdetailsserializer = business_serializers.shopping_serializer(data=data)
        print(basicdetailsserializer)
        if basicdetailsserializer.is_valid():
                basicdetailsserializer.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
        else:
            print("serializer prblm")
            return Response("you are out of region", status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def shopping_alldata(request):
    if request.method == "GET":
        data = shoppingmodel.objects.all()
        serializer = business_serializers.shopping_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def my_shopping_data(request,id):
    if request.method == "GET":
        data = shoppingmodel.objects.get(shop_id=id)
        serializer = business_serializers.shopping_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def business_shopping_data(request,id):
    if request.method == "GET":
        data = shoppingmodel.objects.filter(Business_id=id)
        serializer = business_serializers.shopping_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def get_allproducts_order(request, id, prostatus):
    if request.method == "GET":

        if prostatus == "ready_to_pickup":
            if models.Product_Ordermodel.objects.filter(shop_id__shop_id=id).exists():
                data = models.Product_Ordermodel.objects.filter(shop_id__shop_id=id,
                                                                status__in=["ready_to_pickup", "order_dispatch",
                                                                            "shipped"])
                alldataserializer = end_user_serializers.product_orderlistSerializer(data, many=True)
                return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

            elif models.Product_Ordermodel.objects.filter(d_id__d_id=id).exists():
                data = models.Product_Ordermodel.objects.filter(d_id__d_id=id,
                                                                status__in=["ready_to_pickup", "order_dispatch",
                                                                            "delivered"],payment_status = "")
                alldataserializer = end_user_serializers.product_orderlistSerializer(data, many=True)
                return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


            elif models.Product_Ordermodel.objects.filter(jewel_id__jewel_id=id).exists():
                data = models.Product_Ordermodel.objects.filter(jewel_id__jewel_id=id,
                                                                status__in=["ready_to_pickup", "order_dispatch",
                                                                            "delivered"],payment_status = "")
                alldataserializer = end_user_serializers.product_orderlistSerializer(data, many=True)
                return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
        elif prostatus == "payment_settled":
            print(prostatus == "payment_settled")
            if models.Product_Ordermodel.objects.filter(shop_id__shop_id=id).exists():
                data = models.Product_Ordermodel.objects.filter(shop_id__shop_id=id,
                                                                status="delivered", payment_status=prostatus)
                alldataserializer = end_user_serializers.product_orderlistSerializer(data, many=True)
                return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
            elif models.Product_Ordermodel.objects.filter(d_id__d_id=id).exists():
                data = models.Product_Ordermodel.objects.filter(d_id__d_id=id,status="delivered", payment_status=prostatus)
                alldataserializer = end_user_serializers.product_orderlistSerializer(data, many=True)
                return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
            elif models.Product_Ordermodel.objects.filter(jewel_id__jewel_id=id).exists():
                data = models.Product_Ordermodel.objects.filter(jewel_id__jewel_id=id,status="delivered", payment_status=prostatus)
                alldataserializer = end_user_serializers.product_orderlistSerializer(data, many=True)
                return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

        else:
            if models.Product_Ordermodel.objects.filter(shop_id__shop_id=id).exists():
                data = models.Product_Ordermodel.objects.filter(shop_id__shop_id=id, status=prostatus)
                alldataserializer = end_user_serializers.product_orderlistSerializer(data, many=True)
                return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
            elif models.Product_Ordermodel.objects.filter(food_id__food_id=id).exists():
                data = models.Product_Ordermodel.objects.filter(food_id__food_id=id, status=prostatus)
                alldataserializer = end_user_serializers.product_orderlistSerializer(data, many=True)
                return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
            elif models.Product_Ordermodel.objects.filter(fresh_id__fresh_id=id).exists():
                data = models.Product_Ordermodel.objects.filter(fresh_id__fresh_id=id, status=prostatus)
                alldataserializer = end_user_serializers.product_orderlistSerializer(data, many=True)
                return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
            elif models.Product_Ordermodel.objects.filter(dmio_id__dmio_id=id).exists():
                data = models.Product_Ordermodel.objects.filter(dmio_id__dmio_id=id, status=prostatus)
                alldataserializer = end_user_serializers.product_orderlistSerializer(data, many=True)
                return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
            elif models.Product_Ordermodel.objects.filter(jewel_id__jewel_id=id).exists():
                data = models.Product_Ordermodel.objects.filter(jewel_id__jewel_id=id, status=prostatus)
                alldataserializer = end_user_serializers.product_orderlistSerializer(data, many=True)
                return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
            elif models.Product_Ordermodel.objects.filter(d_id__d_id=id).exists():
                data = models.Product_Ordermodel.objects.filter(d_id__d_id=id, status=prostatus)
                alldataserializer = end_user_serializers.product_orderlistSerializer(data, many=True)
                return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
            elif models.Product_Ordermodel.objects.filter(pharm_id__pharm_id=id).exists():
                data = models.Product_Ordermodel.objects.filter(pharm_id__pharm_id=id, status=prostatus)
                alldataserializer = end_user_serializers.product_orderlistSerializer(data, many=True)
                return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
            else:
                return Response("order not found", status=status.HTTP_403_FORBIDDEN)

    else:
        return Response("product found", status=status.HTTP_404_NOT_FOUND)    

@api_view(["POST"])
def shopping_update(request,id,shop_id):
    try:
        # Instantiate FileSystemStorage
        fs = FileSystemStorage()
        
        # Retrieve existing shopping data
        shop_data = shoppingmodel.objects.get(Business_id=id, shop_id=shop_id)
        shop_datas = shoppingmodel.objects.filter(Business_id=id, shop_id=shop_id).values()[0]

        # Handle file uploads
        if "aadhar" in request.FILES:
            aadhar = request.FILES['aadhar']
            aadhar_path = fs.save(f"api/shopping/{id}/aadhar/{aadhar.name}", aadhar)
            aadhar_paths =all_image_url+fs.url(aadhar_path)
        else:
            aadhar_paths = shop_datas["aadhar"]

        if "pan_file" in request.FILES:
            pan_file = request.FILES["pan_file"]
            pan_file_path = fs.save(f"api/shopping/{id}/pan_file/{pan_file.name}", pan_file)
            pan_file_paths = all_image_url+fs.url(pan_file_path)
        else:
            pan_file_paths = shop_datas["pan_file"]

        if "profile" in request.FILES:
            profile = request.FILES["profile"]
            profile_path = fs.save(f"api/shopping/{id}/profile/{profile.name}", profile)
            profile_paths = all_image_url+fs.url(profile_path)
        else:
            profile_paths = shop_datas["profile"]

        if "bank_passbook" in request.FILES:
            bank_passbook = request.FILES["bank_passbook"]
            bank_passbook_path = fs.save(f"api/shopping/{id}/bank_passbook/{bank_passbook.name}", bank_passbook)
            bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
        else:
            bank_passbook_paths = shop_datas["bank_passbook"]

        if "gst_file" in request.FILES:
            gst_file = request.FILES["gst_file"]
            gst_file_path = fs.save(f"api/shopping/{id}/gst_file/{gst_file.name}", gst_file)
            gst_file_paths = all_image_url+fs.url(gst_file_path)
        else:
            gst_file_paths = shop_datas["gst_file"]
        
        # Update other fields

        shop_data = shoppingmodel.objects.get(Business_id=id, shop_id=shop_id)
        shop_data.seller_name = request.data.get('seller_name', shop_data.seller_name)
        shop_data.business_name = request.data.get('business_name', shop_data.business_name)
        shop_data.pan_number = request.data.get('pan_number', shop_data.pan_number)
        shop_data.gst = request.data.get('gst', shop_data.gst)
        shop_data.contact = request.data.get('contact', shop_data.contact)
        shop_data.alternate_contact = request.data.get('alternate_contact', shop_data.alternate_contact)
        shop_data.door_number = request.data.get('door_number', shop_data.door_number)
        shop_data.street_name = request.data.get('street_name', shop_data.street_name)
        shop_data.area = request.data.get('area', shop_data.area)
        shop_data.region = request.data.get('region', shop_data.region)
        shop_data.pincode = request.data.get('pincode', shop_data.pincode)
        shop_data.aadhar_number = request.data.get('aadhar_number', shop_data.aadhar_number)
        # shop_data.pin_your_location = request.data.get('pin_your_location', shop_data.pin_your_location)
        shop_data.name = request.data.get('name', shop_data.name)
        shop_data.account_number = request.data.get('account_number', shop_data.account_number)
        shop_data.ifsc_code = request.data.get('ifsc_code', shop_data.ifsc_code)
        shop_data.upi_id = request.data.get('upi_id', shop_data.upi_id)
        shop_data.gpay_number = request.data.get('gpay_number', shop_data.gpay_number)
        shop_data.latitude = request.data.get('latitude', shop_data.latitude)
        shop_data.longitude = request.data.get('longitude', shop_data.longitude)
        # Update other fields similarly

        # Save changes
        shop_data.aadhar = aadhar_paths
        shop_data.pan_file = pan_file_paths
        shop_data.profile = profile_paths
        shop_data.bank_passbook = bank_passbook_paths
        shop_data.gst_file = gst_file_paths
        shop_data.save()

        return Response(id, status=status.HTTP_200_OK)
    except:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def shop_products(request, id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break

    # add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_products/{id}/primary_image/" + primary_image,
                                 request.FILES['primary_image'])
    primary_image_paths = all_image_url + fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    print(request.FILES.getlist('other_images'))
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_products/{id}/other_images/" + str(sav).replace(" ", "_"), sav)
        other_image.append(str(ot).replace(" ", "_"))

    print(other_image)
    for iname in other_image:
        other_images_path = iname
        other_imagelist.append(all_image_url + fs.url(other_images_path))
    print(other_imagelist)
    print("hbhgduy............................")
    admin_data = business_commision.objects.get(id=1)
    commission = float(admin_data.commission)
    gst = int(request.POST["gst"])

    actualprice = int(request.POST["actual_price"])
    discountprice = int(request.POST["discount_price"])

    # sellingprice = actualprice - discountprice
    sellingprice = discountprice
    commission_amount = sellingprice + ((commission / 100) * sellingprice)

    selling_price = commission_amount + ((gst / 100) * commission_amount)

    shop_products = dict(request.data)

    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    # shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = int(selling_price)
    print(f"{shop_products}")
    cleaned_data_dict = {key: value[0] if isinstance(value, list) and len(value) == 1 else value for key, value in
                         shop_products.items()}
    cleaned_data_dict ['other_images'] = other_imagelist
    
    global shop_product_data
    shop_product_data = {
        'shop_id': id,
        'product_id': product_id,
        'status': False,
        'category': request.data['category'],
        'subcategory': request.data['subcategory'],
        'product': cleaned_data_dict
    }
    # shopping_product = models.shop_productsmodel(**shop_product_data)
    print(f"my datas {shop_product_data}")
    try:
        # shopping_product.save()
        print("Data saved successfully")
        return Response({'discount': cleaned_data_dict['discount_price'], 'selling_price': int(selling_price)},
                        status=status.HTTP_200_OK)
    except Exception as e:
        print("Error while saving data:", e)
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def shop_product_save(request, id):
    print(type(shop_product_data["shop_id"]))
    print(type(id))
    print(shop_product_data["shop_id"])
    if shop_product_data["shop_id"] == id:
        print("is working")
        new_shop_product = models.shop_productsmodel(**shop_product_data)
        new_shop_product.save()
        return Response({"Data saved successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"Data saved unsuccessfully"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def shop_get_subcategoryproducts(request, id, subcategory):
    if request.method == "GET":
        # Filter products based on shop_id and category
        data = models.shop_productsmodel.objects.filter(shop_id=id, subcategory=subcategory)
        alldataserializer = business_serializers.shop_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def shop_get_products(request,id):
    if request.method == "GET":
        data= models.shop_productsmodel.objects.filter(shop_id=id)
        alldataserializer= business_serializers.shop_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)







@api_view(['POST',"GET"])
def product_status_golivePause(request,id,business_status):
    if request.method == "GET":
        if models.shop_productsmodel.objects.filter(shop_id=id).exists():
            data = models.shop_productsmodel.objects.filter(shop_id=id,business_status=business_status)
            serializer = business_serializers.shop_productlistserializer(data, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif models.jewel_productsmodel.objects.filter(jewel_id=id).exists():
            data = models.jewel_productsmodel.objects.filter(jewel_id=id,business_status=business_status)
            serializer = business_serializers.jewel_productlistserializer(data, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif models.food_productsmodel.objects.filter(food_id=id).exists():
            data = models.food_productsmodel.objects.filter(food_id=id,business_status=business_status)
            serializer = business_serializers.food_productlistserializer(data, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif models.fresh_productsmodel.objects.filter(fresh_id=id).exists():
            data = models.fresh_productsmodel.objects.filter(fresh_id=id,business_status=business_status)
            serializer = business_serializers.fresh_productlistserializer(data, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif models.dmio_productsmodel.objects.filter(dmio_id=id).exists():
            data = models.dmio_productsmodel.objects.filter(dmio_id=id,business_status=business_status)
            serializer = business_serializers.dmio_productlistserializer(data, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif models.pharmacy_productsmodel.objects.filter(pharm_id=id).exists():
            data = models.pharmacy_productsmodel.objects.filter(pharm_id=id,business_status=business_status)
            serializer = business_serializers.pharmacy_productlistserializer(data, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif models.d_original_productsmodel.objects.filter(d_id=id).exists():
            data = models.d_original_productsmodel.objects.filter(d_id=id,business_status=business_status)
            serializer = business_serializers.d_original_productlistserializer(data, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
            # Assuming you're passing the product ID to update and the new status in the request data

            product_id = request.data.get('product_id')
            new_status = business_status
            try:
                if models.shop_productsmodel.objects.filter(product_id=product_id, shop_id=id).exists():
                    product = models.shop_productsmodel.objects.get(product_id=product_id, shop_id=id)
                elif models.jewel_productsmodel.objects.filter(product_id=product_id,jewel_id=id).exists():
                    product = models.jewel_productsmodel.objects.get(product_id=product_id,jewel_id=id)
                elif models.food_productsmodel.objects.filter(product_id=product_id,food_id=id).exists():
                    product=models.food_productsmodel.objects.get(product_id=product_id,food_id=id)
                elif models.fresh_productsmodel.objects.filter(product_id=product_id,fresh_id=id).exists():
                    product=models.fresh_productsmodel.objects.get(product_id=product_id,fresh_id=id)
                elif models.dmio_productsmodel.objects.filter(product_id=product_id,dmio_id=id).exists():
                    product=models.dmio_productsmodel.objects.get(product_id=product_id,dmio_id=id)
                elif models.pharmacy_productsmodel.objects.filter(product_id=product_id,pharm_id=id).exists():
                    product=models.pharmacy_productsmodel.objects.get(product_id=product_id,pharm_id=id)
                elif models.d_original_productsmodel.objects.filter(product_id=product_id,d_id=id).exists():
                    product=models.d_original_productsmodel.objects.get(product_id=product_id,d_id=id)

            except models.shop_productsmodel.DoesNotExist:
                return Response({"message": "Product not found for this shop"}, status=status.HTTP_404_NOT_FOUND)
            product.business_status= new_status
            product.save()
            # Update the status


            return Response({"message": "Product status updated successfully"}, status=status.HTTP_200_OK)

 


@api_view(['GET'])
def shop_get_my_product(request,id,product_id):

    if request.method == "GET":
        # Filter products based on shop_id and category
        data = models.shop_productsmodel.objects.filter(shop_id=id, product_id=product_id)
        alldataserializer = business_serializers.shop_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

 

@api_view(['POST'])
def shop_delete_product(request,id,product_id):
    shop_product = get_object_or_404(models.shop_productsmodel, shop_id=id, product_id=product_id)
    shop_product.delete()
    return Response(id,status=status.HTTP_200_OK)


@api_view(['POST'])
def shop_imgupdate_product(request, id, product_id,index_value):
    try:
        if request.method == "POST":
            fs = FileSystemStorage()
            data = models.shop_productsmodel.objects.get(shop_id=id, product_id=product_id)
            shop_pro=data.product.get("other_images")
            product_img=data.product
            print(shop_pro)
            index_value = int(index_value)
            if index_value < 0 or index_value >= len(shop_pro):
                return Response({"error": "Invalid index value"}, status=status.HTTP_400_BAD_REQUEST)
            if index_value == int(index_value):
                other_images = str(request.FILES['other_images']).replace(" ", "_")
                other_images_path = fs.save(f"api/shop_products/{id}/other_images/" + other_images,
                                            request.FILES['other_images'])
                other_images_paths = all_image_url + fs.url(other_images_path)
                print(other_images_paths)
                shop_pro[index_value] = other_images_paths
                product_img["other_images"] =shop_pro
                data.product=product_img  #replacejson
                data.save()

            return Response({"message": "Image Updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Index value mismatch"}, status=status.HTTP_400_BAD_REQUEST)
            
    except models.shop_productsmodel.DoesNotExist:
        return Response({"error": "Shop product not found"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def shop_update_product(request, id, product_id):
    print(request.data)
    shop_products = dict(request.POST)
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_products/{id}/primary_image/" + primary_image,
                                     request.FILES['primary_image'])
        primary_image_paths = all_image_url + fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths
    except:
        pass

    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_products/{id}/other_images/" + str(sav).replace(" ", "_"), sav)
            other_image.append(str(ot).replace(" ", "_"))

            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url + fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass

    try:
        shop_product_instance = models.shop_productsmodel.objects.get(shop_id=id, product_id=product_id)
        existing_product_data = shop_product_instance.product

        # Updating product field with new data
        new_product_data = dict(request.POST)
        # shop_products = dict(request.POST)
        shop_products["other_images"] = shop_product_instance.product['other_images']
        print(shop_products)
        cleaned_data_dict = {key: value[0] if isinstance(value, list) and len(value) == 1 else value for key, value in
                             shop_products.items()}

        # existing_product_data.update(cleaned_data_dict)

        # Saving changes to the SQLite table
        with transaction.atomic():
            # Updating only the product field
            shop_product_instance.product = cleaned_data_dict
            shop_product_instance.category = request.data['category']
            shop_product_instance.subcategory = request.data['subcategory']
            shop_product_instance.save()

        return Response(id, status=status.HTTP_200_OK)
    except models.shop_productsmodel.DoesNotExist:
        return Response({"error": "Shop product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST","GET"])
def shop_productorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.Product_Ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data)
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
        
        if pro_data:
            
            alldata = []
            for product_id in pro_data:
                proget = models.shop_productsmodel.objects.filter(product_id=product_id)
                alldata.extend(proget)
            
            serializer = business_serializers.delivered_productlistserializer(alldata, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
          
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)




# jewels_dashboard
    
@api_view(['GET'])
def jewel_total_revenue(request,id):
    if request.method == 'GET':
        if models.Product_Ordermodel.objects.filter(jewel_id_id__jewel_id=id).exists():
            total_revenue = models.Product_Ordermodel.objects.filter(jewel_id_id__jewel_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
            print(total_revenue)
            jewel = models.jewellerymodel.objects.get(jewel_id=id)
            jewel.total_revenue = total_revenue
            jewel.save()
            return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)
        else:
            return Response(data={'total_revenue': 0}, status=status.HTTP_200_OK)


@api_view(['GET'])
def jewel_mon_revenue(request,id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        if models.Product_Ordermodel.objects.filter(jewel_id_id__jewel_id=id).exists():
            monthly_revenue = models.Product_Ordermodel.objects.filter(jewel_id_id__jewel_id=id, order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
            jewel = models.jewellerymodel.objects.get(jewel_id=id)
            jewel.monthly_revenue = monthly_revenue
            jewel.save()
            return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)
        else:
            return Response(data={'monthly_revenue': 0}, status=status.HTTP_200_OK)


@api_view(['GET'])
def jewel_orderstatus(request,id):
    if request.method == 'GET':

        jewel = models.Product_Ordermodel.objects.filter(jewel_id_id__jewel_id=id).first()
        # if not jewel:
        #     return Response(data={'error': 'jewel not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.Product_Ordermodel.objects.filter(jewel_id_id__jewel_id=id, status='delivered').count()
        cancelled_count = models.Product_Ordermodel.objects.filter(jewel_id_id__jewel_id=id, status='cancelled').count()
        on_process_count = models.Product_Ordermodel.objects.filter(jewel_id_id__jewel_id=id, status='on_process').count()

        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

    else:
        return Response("shop_ordernot found",status=status.HTTP_400_BAD_REQUEST)


# jewellery
@api_view(['POST'])
def jewellery(request,id):
    if request.method == "POST":
        print(request.POST)
        
        
        pincode = request.POST['pincode']

        data1 = zone.objects.all()
        print(data1)
        get_zone = None  # Initialize get_zone variable

        for x in data1:
            print(x)
            if x.pincode is not None and pincode in x.pincode:
                get_zone = x.zone
                print(get_zone)
                break  # Once the zone is found, exit the loop

        print(get_zone)  # Check if zone is retrieved correctly
        # print(request.data)
        # print(request.FILES)
        fs = FileSystemStorage()
        aadhar = str(request.FILES['aadhar']).replace(" ", "_")
        aadhar_path = fs.save(f"api/jewellery/{id}/aahar/"+aadhar, request.FILES['aadhar'])
        pan_file = str(request.FILES['pan_file']).replace(" ", "_")
        pan_file_path = fs.save(f"api/jewellery/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
        profile = str(request.FILES['profile']).replace(" ", "_")
        profile_path = fs.save(f"api/jewellery/{id}/profile/"+profile, request.FILES['profile'])
        bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
        bank_passbook_path = fs.save(f"api/jewellery/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
        gst_file = str(request.FILES['gst_file']).replace(" ", "_")
        gst_file_path = fs.save(f"api/jewellery/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

        aadhar_paths = all_image_url+fs.url(aadhar_path)
        pan_file_paths = all_image_url+fs.url(pan_file_path)
        profile_paths = all_image_url+fs.url(profile_path)
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
        gst_file_paths = all_image_url+fs.url(gst_file_path)
        x = datetime.datetime.now()
        jewels_id=business_extension.jewel_id_generate()
        while True:
            if id == jewels_id:
                jewels_id=business_extension.jewel_id_generate()
            else:
                break

        data = {
            'Business_id': id,
            'jewel_id': jewels_id,
            'seller_name': request.POST['seller_name'],
            'business_name': request.POST['business_name'],
            'pan_number': request.POST['pan_number'],
            'gst': request.POST['gst'],
            'contact': request.POST['contact'],
            'alternate_contact': request.POST['alternate_contact'],
            'pincode': request.POST['pincode'],
            'aadhar_number' : request.POST['aadhar_number'],
            'door_number' : request.POST['door_number'],
            'street_name' : request.POST['street_name'],
            'area' : request.POST['area'],
            'region' : get_zone,
            # 'pin_your_location': request.POST['pin_your_location'],           
            'name': request.POST['name'],           
            'account_number':request.POST['account_number'],
            'ifsc_code':request.POST['ifsc_code'],
            'upi_id':request.POST['upi_id'],
            'gpay_number':request.POST['gpay_number'],
            'aadhar':aadhar_paths,
            'pan_file': pan_file_paths,
            'profile': profile_paths,
            'bank_passbook': bank_passbook_paths,
            'gst_file': gst_file_paths,
            'category':"jewellery",
            'latitude':request.POST['latitude'],
            'longitude':request.POST['longitude'],
            

            }

        print(data)
        basicdetailsserializer = business_serializers.jewellery_serializer(data=data)
        
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            print("serializer prblm")
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def jewellery_alldata(request):
    if request.method == "GET":
        data = jewellerymodel.objects.all()
        serializer = business_serializers.jewellery_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
@api_view(['GET'])
def my_jewellery_data(request,id):
    if request.method == "GET":
        data = jewellerymodel.objects.get(jewel_id=id)
        print(data)
        serializer = business_serializers.jewellery_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def business_jewellery_data(request,id):
    if request.method == "GET":
        data = jewellerymodel.objects.filter(Business_id=id)
        serializer = business_serializers.jewellery_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


@api_view(["POST"])
def jewellery_update(request,id,jewel_id):
    try:

        # Instantiate FileSystemStorage
        fs = FileSystemStorage()
        
        # Retrieve existing jewellery data
        jewel_data = jewellerymodel.objects.get(Business_id=id, jewel_id=jewel_id)
        jewel_datas = jewellerymodel.objects.filter(Business_id=id, jewel_id=jewel_id).values()[0]

        # Handle file uploads
        if "aadhar" in request.FILES:
            aadhar = request.FILES['aadhar']
            aadhar_path = fs.save(f"api/jewellery/{id}/aadhar/{aadhar.name}", aadhar)
            aadhar_paths = all_image_url+fs.url(aadhar_path)
        else:
            aadhar_paths = jewel_datas["aadhar"]

        if "pan_file" in request.FILES:
            pan_file = request.FILES["pan_file"]
            pan_file_path = fs.save(f"api/jewellery/{id}/pan_file/{pan_file.name}", pan_file)
            pan_file_paths = all_image_url+fs.url(pan_file_path)
        else:
            pan_file_paths = jewel_datas["pan_file"]

        if "profile" in request.FILES:
            profile = request.FILES["profile"]
            profile_path = fs.save(f"api/jewellery/{id}/profile/{profile.name}", profile)
            profile_paths = all_image_url+fs.url(profile_path)
        else:
            profile_paths = jewel_datas["profile"]

        if "bank_passbook" in request.FILES:
            bank_passbook = request.FILES["bank_passbook"]
            bank_passbook_path = fs.save(f"api/jewellery/{id}/bank_passbook/{bank_passbook.name}", bank_passbook)
            bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
        else:
            bank_passbook_paths = jewel_datas["bank_passbook"]

        if "gst_file" in request.FILES:
            gst_file = request.FILES["gst_file"]
            gst_file_path = fs.save(f"api/jewellery/{id}/gst_file/{gst_file.name}", gst_file)
            gst_file_paths = all_image_url+fs.url(gst_file_path)
        else:
            gst_file_paths = jewel_datas["gst_file"]
        
        # Update other fields
     
        jewel_data = jewellerymodel.objects.get(Business_id=id, jewel_id=jewel_id)
        jewel_data.seller_name = request.data.get('seller_name', jewel_data.seller_name)
        jewel_data.business_name = request.data.get('business_name', jewel_data.business_name)
        jewel_data.pan_number = request.data.get('pan_number', jewel_data.pan_number)
        jewel_data.gst = request.data.get('gst', jewel_data.gst)
        jewel_data.contact = request.data.get('contact', jewel_data.contact)
        jewel_data.alternate_contact = request.data.get('alternate_contact', jewel_data.alternate_contact)
        jewel_data.door_number = request.data.get('door_number', jewel_data.door_number)
        jewel_data.street_name = request.data.get('street_name', jewel_data.street_name)
        jewel_data.area = request.data.get('area', jewel_data.area)
        jewel_data.region = request.data.get('region', jewel_data.region)
        jewel_data.pincode = request.data.get('pincode', jewel_data.pincode)
        jewel_data.aadhar_number = request.data.get('aadhar_number', jewel_data.aadhar_number)
        # jewel_data.pin_your_location = request.data.get('pin_your_location', jewel_data.pin_your_location)
        jewel_data.name = request.data.get('name', jewel_data.name)
        jewel_data.account_number = request.data.get('account_number', jewel_data.account_number)
        jewel_data.ifsc_code = request.data.get('ifsc_code', jewel_data.ifsc_code)
        jewel_data.upi_id = request.data.get('upi_id', jewel_data.upi_id)
        jewel_data.gpay_number = request.data.get('gpay_number', jewel_data.gpay_number)
        jewel_data.latitude = request.data.get('latitude', jewel_data.latitude)
        jewel_data.longitude = request.data.get('longitude', jewel_data.longitude)
        # Update other fields similarly

        # Save changes
        jewel_data.aadhar = aadhar_paths
        jewel_data.pan_file = pan_file_paths
        jewel_data.profile = profile_paths
        jewel_data.bank_passbook = bank_passbook_paths
        jewel_data.gst_file = gst_file_paths
        jewel_data.save()

        return Response(id, status=status.HTTP_200_OK)
    except:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

# jewellery products 

# jewel products    

@api_view(['POST'])
def jewel_products(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
  
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/jewel_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/jewel_products/{id}/other_images/"+str(sav).replace(" ", "_"), sav) 
        other_image.append(str(ot).replace(" ","_"))
            
    print(other_image)
    for iname in other_image:
        other_images_path = iname
        other_imagelist.append(all_image_url+fs.url(other_images_path))

    
    admin_data = business_commision.objects.get(id=1)  
    commission = float(admin_data.commission)  
    gst =   int(request.POST["gst"])
    
    actualprice = int(request.POST["actual_price"])
    discountprice = int(request.POST["discount_price"])

    # sellingprice = actualprice - discountprice
    sellingprice = discountprice
    commission_amount = sellingprice + ((commission / 100) * sellingprice)

    selling_price = commission_amount + ((gst / 100) * commission_amount)
   
    jewel_products = dict(request.POST)
    jewel_products['jewel_id'] = id
    jewel_products['product_id'] = product_id
    jewel_products['primary_image'] = primary_image_paths
    # jewel_products['other_images'] = other_imagelist
    jewel_products['selling_price'] = int(selling_price)
    print(jewel_products)
    cleaned_data_dict ={key:value[0] if isinstance(value,list) and len(value)==1 else value for key,value in jewel_products.items()}

    cleaned_data_dict ['other_images'] = other_imagelist

    global data
    data= {
        'jewel_id' : id,
        'product_id' : product_id,
        'status':False,
        'category':request.POST['category'],
        'subcategory':request.POST['subcategory'],
        'product':cleaned_data_dict
        
    }
    print(data)
    try:
        # shopping_product.save()
        print("Data saved successfully")
        return Response({'discount': cleaned_data_dict['discount_price'], 'selling_price': int(selling_price)},
                        status=status.HTTP_200_OK)
    except Exception as e:
        print("Error while saving data:", e)
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def jewel_product_save(request, id):
    print(type(data["jewel_id"]))
    print(type(id))
    print(data["jewel_id"])
    if data["jewel_id"] == id:
        print("is working")
        new_shop_product = models.jewel_productsmodel(**data)
        new_shop_product.save()
        return Response({"Data saved successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"Data saved unsuccessfully"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def jewel_get_subcategoryproducts(request, id, subcategory):
    if request.method == "GET":
        # Filter products based on jewel_id and category
        data = models.jewel_productsmodel.objects.filter(jewel_id=id, subcategory=subcategory)
        alldataserializer = business_serializers.jewel_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def jewel_get_products(request,id):
    if request.method == "GET":
        data= models.jewel_productsmodel.objects.filter(jewel_id=id)
        alldataserializer= business_serializers.jewel_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def jewel_get_my_product(request,id,product_id):

    if request.method == "GET":
        # Filter products based on jewel_id and category
        data = models.jewel_productsmodel.objects.filter(jewel_id=id, product_id=product_id)
        alldataserializer = business_serializers.jewel_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def jewel_delete_product(request,id,product_id):
 
    jewel_product = get_object_or_404(models.jewel_productsmodel, jewel_id=id, product_id=product_id)
    jewel_product.delete()
    return Response(id,status=status.HTTP_200_OK)


@api_view(['POST'])
def jewel_update_product(request,id,product_id):
    print(request.data)
    jewel_products = dict(request.POST)

    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/jewel_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        jewel_products['primary_image'] = primary_image_paths
    except:
        # shop_pro=collection.find_one({"jewel_id": id,"product_id":product_id})
        # primary_image_paths=shop_pro.get("primary_image")
        # jewel_products['primary_image'] = primary_image_paths
        pass
        
    
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/jewel_products/{id}/other_images/"+str(sav).replace(" ", "_"), sav)
            other_image.append(str(ot).replace(" ","_"))
                
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
        jewel_products['other_images'] = other_imagelist

    except:
        pass

    try:

        jewel_product_instance = models.jewel_productsmodel.objects.get(jewel_id=id, product_id=product_id)

        
        existing_product_data = jewel_product_instance.product
        jewel_products["other_images"] = jewel_product_instance.product['other_images']
        cleaned_data_dict = {key: value[0] if isinstance(value, list) and len(value) == 1 else value for key, value in
                            jewel_products.items()}
        # existing_product_data.update(cleaned_data_dict)
        
        # Saving changes to the SQLite table
        with transaction.atomic():
            
            # Updating only the product field
            jewel_product_instance.product = cleaned_data_dict
            jewel_product_instance.category = request.data['category']
            jewel_product_instance.subcategory = request.data['subcategory']
            jewel_product_instance.save()
            # cleaned_data_dict ={key:value[0] if isinstance(value,list) and len(value)==1 else value for key,value in new_product_data.items()}
            # print(cleaned_data_dict)
            # jewel_product_instance.product = cleaned_data_dict

            jewel_product_instance.save()
        return Response(id, status=status.HTTP_200_OK)
    except models.jewel_productsmodel.DoesNotExist:
        return Response({"error": "jewel product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def jewel_imgupdate_product(request,id,product_id,index_value):
    try:
        if request.method == "POST":
            fs = FileSystemStorage()
            data = models.jewel_productsmodel.objects.get(jewel_id=id, product_id=product_id)
            jewel_pro=data.product.get("other_images")
            product_img=data.product
            print(jewel_pro)
            index_value = int(index_value)
            if index_value < 0 or index_value >= len(jewel_pro):
                return Response({"error": "Invalid index value"}, status=status.HTTP_400_BAD_REQUEST)
            if index_value == int(index_value):
                other_images = str(request.FILES['other_images']).replace(" ", "_")
                other_images_path = fs.save(f"api/jewel_products/{id}/other_images/" + other_images,
                                            request.FILES['other_images'])
                other_images_paths = all_image_url + fs.url(other_images_path)
                print(other_images_paths)
                jewel_pro[index_value] = other_images_paths
                product_img["other_images"] =jewel_pro
                data.product=product_img  #replacejson
                data.save()

            return Response({"message": "Image Updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Index value mismatch"}, status=status.HTTP_400_BAD_REQUEST)
            
    except models.jewel_productsmodel.DoesNotExist:
        return Response({"error": "Shop product not found"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST","GET"])
def jewel_productorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.Product_Ordermodel.objects.filter(Q(jewel_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data)
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
        
        if pro_data:
            
            alldata = []
            for product_id in pro_data:
                proget = models.jewel_productsmodel.objects.filter(product_id=product_id)
                alldata.extend(proget)
            
            serializer = business_serializers.delivered_productlistserializer(alldata, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
          

        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)




# food dashboard
    
@api_view(['GET'])
def food_total_revenue(request,id):
    if request.method == 'GET':
        if models.Product_Ordermodel.objects.filter(food_id_id__food_id=id).exists():
            total_revenue = models.Product_Ordermodel.objects.filter(food_id_id__food_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
            print(total_revenue)
            food = models.foodmodel.objects.get(food_id=id)
            food.total_revenue = total_revenue
            food.save()
            return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)
        else:
            return Response(data={'total_revenue': 0}, status=status.HTTP_200_OK)

    else:
        return Response("shop_ordernot found",status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def food_mon_revenue(request, id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        if models.Product_Ordermodel.objects.filter(food_id_id__food_id=id).exists():
            monthly_revenue = models.Product_Ordermodel.objects.filter(food_id_id__food_id=id, order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
            food = models.foodmodel.objects.get(food_id=id)
            food.monthly_revenue = monthly_revenue
            food.save()
            return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)
        else:
            return Response(data={'monthly_revenue': 0},status=status.HTTP_200_OK)
    else:
        return Response("shop_ordernot found",status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def food_orderstatus(request,id):
    if request.method == 'GET':

        food = models.Product_Ordermodel.objects.filter(food_id_id__food_id=id).first()
        # if not food:
        #     return Response(data={'error': 'food not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.Product_Ordermodel.objects.filter(food_id_id__food_id=id, status='delivered').count()
        cancelled_count = models.Product_Ordermodel.objects.filter(food_id_id__food_id=id, status='cancelled').count()
        on_process_count = models.Product_Ordermodel.objects.filter(food_id_id__food_id=id, status='on_process').count()

        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
    else:
        return Response("shop_ordernot found",status=status.HTTP_400_BAD_REQUEST)

#foodview  
@api_view(['POST'])
def food(request,id):
    if request.method == "POST":
        print(request.POST)
        pincode = request.POST['pincode']

        data1 = zone.objects.all()
        print(data1)
        get_zone = None  # Initialize get_zone variable

        for x in data1:
            print(x)
            if x.pincode is not None and pincode in x.pincode:
                get_zone = x.zone
                print(get_zone)
                break  # Once the zone is found, exit the loop

        print(get_zone)  # Check if zone is retrieved correctly
        # print(request.data)
        # print(request.FILES)
        fs = FileSystemStorage()
        aadhar = str(request.FILES['aadhar']).replace(" ", "_")
        aadhar_path = fs.save(f"api/food/{id}/aahar/"+aadhar, request.FILES['aadhar'])
        pan_file = str(request.FILES['pan_file']).replace(" ", "_")
        pan_file_path = fs.save(f"api/food/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
        profile = str(request.FILES['profile']).replace(" ", "_")
        profile_path = fs.save(f"api/food/{id}/profile/"+profile, request.FILES['profile'])
        bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
        bank_passbook_path = fs.save(f"api/food/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
        gst_file = str(request.FILES['gst_file']).replace(" ", "_")
        gst_file_path = fs.save(f"api/food/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

        aadhar_paths = all_image_url+fs.url(aadhar_path)
        pan_file_paths = all_image_url+fs.url(pan_file_path)
        profile_paths = all_image_url+fs.url(profile_path)
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
        gst_file_paths = all_image_url+fs.url(gst_file_path)
        x = datetime.datetime.now()
        foods_id=business_extension.food_id_generate()
        while True:
            if id == foods_id:
                foods_id=business_extension.food_id_generate()
            else:
                break

        data = {
            'Business_id': id,
            'food_id': foods_id,
            'seller_name': request.POST['seller_name'],
            'business_name': request.POST['business_name'],
            'pan_number': request.POST['pan_number'],
            'gst': request.POST['gst'],
            'contact': request.POST['contact'],
            'alternate_contact': request.POST['alternate_contact'],
            'pincode': request.POST['pincode'],
            'aadhar_number' : request.POST['aadhar_number'],
            'door_number' : request.POST['door_number'],
            'street_name' : request.POST['street_name'],
            'area' : request.POST['area'],
            'fssa':request.POST['fssa'],
            'region':get_zone,
            # 'pin_your_location': request.POST['pin_your_location'],           
            'name': request.POST['name'],           
            'account_number':request.POST['account_number'],
            'ifsc_code':request.POST['ifsc_code'],
            'upi_id':request.POST['upi_id'],
            'gpay_number':request.POST['gpay_number'],
            'aadhar':aadhar_paths,
            'pan_file': pan_file_paths,
            'profile': profile_paths,
            'bank_passbook': bank_passbook_paths,
            'gst_file': gst_file_paths,
            'category':"food",
            'latitude':request.POST['latitude'],
            'longitude':request.POST['longitude'],

            }

        print(data)
        basicdetailsserializer = business_serializers.food_serializer(data=data)
        
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            print("serializer prblm")
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def food_alldata(request):
    if request.method == "GET":
        data = foodmodel.objects.all()
        serializer = business_serializers.food_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def my_food_data(request,id):
    if request.method == "GET":
        data = foodmodel.objects.get(food_id=id)
        print(data)
        serializer = business_serializers.food_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def business_food_data(request,id):
    if request.method == "GET":
        data = foodmodel.objects.filter(Business_id=id)
        serializer = business_serializers.food_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


@api_view(["POST"])
def food_update(request,id,food_id):
    try:

        # Instantiate FileSystemStorage
        fs = FileSystemStorage()
        
        # Retrieve existing food data
        food_data = foodmodel.objects.get(Business_id=id, food_id=food_id)
        food_datas = foodmodel.objects.filter(Business_id=id, food_id=food_id).values()[0]

        # Handle file uploads
        if "aadhar" in request.FILES:
            aadhar = request.FILES['aadhar']
            aadhar_path = fs.save(f"api/food/{id}/aadhar/{aadhar.name}", aadhar)
            aadhar_paths = all_image_url+fs.url(aadhar_path)
        else:
            aadhar_paths = food_datas["aadhar"]

        if "pan_file" in request.FILES:
            pan_file = request.FILES["pan_file"]
            pan_file_path = fs.save(f"api/food/{id}/pan_file/{pan_file.name}", pan_file)
            pan_file_paths = all_image_url+fs.url(pan_file_path)
        else:
            pan_file_paths = food_datas["pan_file"]

        if "profile" in request.FILES:
            profile = request.FILES["profile"]
            profile_path = fs.save(f"api/food/{id}/profile/{profile.name}", profile)
            profile_paths = all_image_url+fs.url(profile_path)
        else:
            profile_paths = food_datas["profile"]

        if "bank_passbook" in request.FILES:
            bank_passbook = request.FILES["bank_passbook"]
            bank_passbook_path = fs.save(f"api/food/{id}/bank_passbook/{bank_passbook.name}", bank_passbook)
            bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
        else:
            bank_passbook_paths = food_datas["bank_passbook"]

        if "gst_file" in request.FILES:
            gst_file = request.FILES["gst_file"]
            gst_file_path = fs.save(f"api/food/{id}/gst_file/{gst_file.name}", gst_file)
            gst_file_paths = all_image_url+fs.url(gst_file_path)
        else:
            gst_file_paths = food_datas["gst_file"]
        
        # Update other fields
     
        food_data = foodmodel.objects.get(Business_id=id, food_id=food_id)
        food_data.seller_name = request.data.get('seller_name', food_data.seller_name)
        food_data.business_name = request.data.get('business_name', food_data.business_name)
        food_data.pan_number = request.data.get('pan_number', food_data.pan_number)
        food_data.gst = request.data.get('gst', food_data.gst)
        food_data.contact = request.data.get('contact', food_data.contact)
        food_data.alternate_contact = request.data.get('alternate_contact', food_data.alternate_contact)
        food_data.door_number = request.data.get('door_number', food_data.door_number)
        food_data.street_name = request.data.get('street_name', food_data.street_name)
        food_data.area = request.data.get('area', food_data.area)
        food_data.fssa = request.data.get('fssa', food_data.fssa)
        food_data.region = request.data.get('region', food_data.region)
        food_data.pincode = request.data.get('pincode', food_data.pincode)
        food_data.aadhar_number = request.data.get('aadhar_number', food_data.aadhar_number)
        # food_data.pin_your_location = request.data.get('pin_your_location', food_data.pin_your_location)
        food_data.name = request.data.get('name', food_data.name)
        food_data.account_number = request.data.get('account_number', food_data.account_number)
        food_data.ifsc_code = request.data.get('ifsc_code', food_data.ifsc_code)
        food_data.upi_id = request.data.get('upi_id', food_data.upi_id)
        food_data.gpay_number = request.data.get('gpay_number', food_data.gpay_number)
        food_data.latitude = request.data.get('latitude', food_data.latitude)
        food_data.longitude = request.data.get('longitude', food_data.longitude)
        # Update other fields similarly

        # Save changes
        food_data.aadhar = aadhar_paths
        food_data.pan_file = pan_file_paths
        food_data.profile = profile_paths
        food_data.bank_passbook = bank_passbook_paths
        food_data.gst_file = gst_file_paths
        food_data.save()

        return Response(id, status=status.HTTP_200_OK)
    except:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(["POST"])    
def add_review_restaurant(request, id):
    products = models.food_productsmodel.objects.filter(food_id=id)
    total_rating = 0
    total_reviews = 0
    for product in products:
        reviews = models.Reviews.objects.filter(food_product=product)
        product_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        if product_rating is not None:
            total_rating += product_rating
            total_reviews += 1
    if total_reviews > 0:
        average_rating = total_rating / total_reviews
    else:
        average_rating = 0 
   
    shop = models.foodmodel.objects.get(food_id=id)
    shop.rating = int(average_rating)
    shop.save()
    return Response(id, status=status.HTTP_200_OK)


# food products
@api_view(['POST'])
def food_products(request,id):
    # Generate a unique product ID
    product_id = business_extension.product_id_generate()
    
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
        
    # Save primary image
    fs = FileSystemStorage()
    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    
    # Save other images
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_products/{id}/other_images/"+str(sav).replace(" ", "_"), sav) 
        other_image.append(str(ot).replace(" ","_"))
    for iname in other_image:
        other_images_path = iname
        other_imagelist.append(all_image_url+fs.url(other_images_path))
 
    # Retrieve commission and GST from admin data
    admin_data = business_commision.objects.get(id=1)  
    commission = float(admin_data.commission)  
    gst =   int(request.POST["gst"])
    
    # Calculate selling price
    actualprice = int(request.POST["actual_price"])
    discountprice = int(request.POST["discount_price"])
    sellingprice = discountprice
    # sellingprice = actualprice - discountprice
    commission_amount = sellingprice + ((commission / 100) * sellingprice)
    selling_price = commission_amount + ((gst / 100) * commission_amount)
   
    # Prepare food product data
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    # food_products['other_images'] = other_imagelist
    food_products['selling_price'] = int(selling_price)
    print(food_products)
    # Clean data and prepare for serialization
    cleaned_data_dict ={key:value[0] if isinstance(value,list) and len(value)==1 else value for key,value in food_products.items()}
    print(cleaned_data_dict)
    cleaned_data_dict ['other_images'] = other_imagelist

    global food_products_data
    food_products_data= {
        'food_id' : id,
        'product_id' : product_id,
        'status':False,
        'category':request.POST['category'],
        'subcategory':request.POST['subcategory'],
        'product':cleaned_data_dict,
    }

    # Save data to the database
    # new_food_product = models.food_productsmodel(**food_products_data)
    try:
        # new_food_product.save()
        print("Data saved successfully")
        return Response({'discount': cleaned_data_dict['discount_price'], 'selling_price': int(selling_price)},
                        status=status.HTTP_200_OK)
    except Exception as e:
        print("Error while saving data:", e)
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)



@api_view(['POST'])
def food_product_save(request,id):
    print(type(food_products_data["food_id"]))
    print(type(id))
    print(food_products_data["food_id"])
    if food_products_data["food_id"] == id:
        print("is working")
        new_food_product = models.food_productsmodel(**food_products_data)
        new_food_product.save()
        return Response({"Data saved successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"Data saved unsuccessfully"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def food_get_subcategoryproducts(request, id, subcategory):
    if request.method == "GET":
        # Filter products based on food_id and category
        data = models.food_productsmodel.objects.filter(food_id=id, subcategory=subcategory)
        alldataserializer = business_serializers.food_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def food_get_products(request,id):
    if request.method == "GET":
        data= models.food_productsmodel.objects.filter(food_id=id)
        alldataserializer= business_serializers.food_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def food_get_my_product(request,id,product_id):

    if request.method == "GET":
        # Filter products based on food_id and category
        data = models.food_productsmodel.objects.filter(food_id=id, product_id=product_id)
        alldataserializer = business_serializers.food_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

 

@api_view(['POST'])
def food_delete_product(request,id,product_id):

    food_product = get_object_or_404(models.food_productsmodel, food_id=id, product_id=product_id)
    food_product.delete()
    return Response(id,status=status.HTTP_200_OK)




@api_view(['POST'])
def food_update_product(request,id,product_id):

    food_products = dict(request.POST)
  
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths
    except:
        # food_pro=collection.find_one({"food_id": id,"product_id":product_id})
        # primary_image_paths=food_pro.get("primary_image")
        # food_products['primary_image'] = primary_image_paths
        pass
        
    
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_products/{id}/other_images/"+str(sav).replace(" ", "_"), sav)
            other_image.append(str(ot).replace(" ","_"))
                
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist

    except:
        pass
    try:
        food_product_instance = models.food_productsmodel.objects.get(food_id=id, product_id=product_id)
        
        existing_product_data = food_product_instance.product
        
        # Updating product field with new data
        food_products["other_images"] = food_product_instance.product['other_images']
        cleaned_data_dict = {key: value[0] if isinstance(value, list) and len(value) == 1 else value for key, value in
                            food_products.items()}

        # existing_product_data.update(cleaned_data_dict)
     
        
        # Saving changes to the SQLite table
        with transaction.atomic():
            # Updating only the product field
            food_product_instance.product = cleaned_data_dict
            food_product_instance.category = request.data['category']
            food_product_instance.subcategory = request.data['subcategory']
            food_product_instance.save()
        
        return Response(id, status=status.HTTP_200_OK)
    except models.food_productsmodel.DoesNotExist:
        return Response({"error": "Shop product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def food_imgupdate_product(request, id, product_id,index_value):
    try:
        if request.method == "POST":
            fs = FileSystemStorage()
            data = models.food_productsmodel.objects.get(food_id=id, product_id=product_id)
            food_pro=data.product.get("other_images")
            product_img=data.product
            print(food_pro)
            index_value = int(index_value)
            if index_value < 0 or index_value >= len(food_pro):
                return Response({"error": "Invalid index value"}, status=status.HTTP_400_BAD_REQUEST)
            if index_value == int(index_value):
                other_images = str(request.FILES['other_images']).replace(" ", "_")
                other_images_path = fs.save(f"api/food_products/{id}/other_images/" + other_images,
                                            request.FILES['other_images'])
                other_images_paths = all_image_url + fs.url(other_images_path)
                print(other_images_paths)
                food_pro[index_value] = other_images_paths
                product_img["other_images"] =food_pro
                data.product=product_img  #replacejson
                data.save()

            return Response({"message": "Image Updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Index value mismatch"}, status=status.HTTP_400_BAD_REQUEST)
            
    except models.food_productsmodel.DoesNotExist:
        return Response({"error": "Shop product not found"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST","GET"])
def food_productorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.Product_Ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data)
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
        
        if pro_data:
            
            alldata = []
            for product_id in pro_data:
                proget = models.food_productsmodel.objects.filter(product_id=product_id)
                alldata.extend(proget)
            
            serializer = business_serializers.delivered_productlistserializer(alldata, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
          

        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)



# freshcuts

@api_view(['GET'])
def fresh_total_revenue(request, id):

    if request.method == 'GET':
        if models.Product_Ordermodel.objects.filter(fresh_id_id__fresh_id=id).exists():
            total_revenue = models.Product_Ordermodel.objects.filter(fresh_id_id__fresh_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
            print(total_revenue)
            fresh = models.freshcutsmodel.objects.get(fresh_id=id)
            fresh.total_revenue = total_revenue
            fresh.save()
            return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)
        else:
            return Response(data={'total_revenue': 0}, status=status.HTTP_200_OK)
  

@api_view(['GET'])
def fresh_mon_revenue(request, id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        if models.Product_Ordermodel.objects.filter(fresh_id_id__fresh_id=id).exists():
            monthly_revenue = models.Product_Ordermodel.objects.filter(fresh_id_id__fresh_id=id, order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
            fresh = models.freshcutsmodel.objects.get(fresh_id=id)
            fresh.monthly_revenue = monthly_revenue
            fresh.save()
            return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)
        else:
            return Response(data={'monthly_revenue': 0}, status=status.HTTP_200_OK)
   

@api_view(['GET'])
def fresh_orderstatus(request,id):
    if request.method == 'GET':

        shop = models.Product_Ordermodel.objects.filter(fresh_id_id__fresh_id=id).first()
        # if not shop:
        #     return Response(data={'error': 'fresh not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.Product_Ordermodel.objects.filter(fresh_id_id__fresh_id=id, status='delivered').count()
        cancelled_count = models.Product_Ordermodel.objects.filter(fresh_id_id__fresh_id=id, status='cancelled').count()
        on_process_count = models.Product_Ordermodel.objects.filter(fresh_id_id__fresh_id=id, status='on_process').count()

        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
    else:
        return Response("shop_ordernot found",status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def freshcuts(request,id):
    if request.method == "POST":
        print(request.POST)
        pincode = request.POST['pincode']

        data1 = zone.objects.all()
        print(data1)
        get_zone = None  # Initialize get_zone variable

        for x in data1:
            print(x)
            if x.pincode is not None and pincode in x.pincode:
                get_zone = x.zone
                print(get_zone)
                break  # Once the zone is found, exit the loop

        print(get_zone)  # Check if zone is retrieved correctly
        # print(request.data)
        # print(request.FILES)
        fs = FileSystemStorage()
        aadhar = str(request.FILES['aadhar']).replace(" ", "_")
        aadhar_path = fs.save(f"api/freshcuts/{id}/aahar/"+aadhar, request.FILES['aadhar'])
        pan_file = str(request.FILES['pan_file']).replace(" ", "_")
        pan_file_path = fs.save(f"api/freshcuts/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
        profile = str(request.FILES['profile']).replace(" ", "_")
        profile_path = fs.save(f"api/freshcuts/{id}/profile/"+profile, request.FILES['profile'])
        bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
        bank_passbook_path = fs.save(f"api/freshcuts/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
        gst_file = str(request.FILES['gst_file']).replace(" ", "_")
        gst_file_path = fs.save(f"api/freshcuts/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

        aadhar_paths = all_image_url+fs.url(aadhar_path)
        pan_file_paths = all_image_url+fs.url(pan_file_path)
        profile_paths = all_image_url+fs.url(profile_path)
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
        gst_file_paths = all_image_url+fs.url(gst_file_path)
        x = datetime.datetime.now()
        freshcuts_id=business_extension.fresh_id_generate()
        while True:
            if id == freshcuts_id:
                freshcuts_id=business_extension.fresh_id_generate()
            else:
                break

        data = {
            'Business_id': id,
            'fresh_id': freshcuts_id,
            'seller_name': request.POST['seller_name'],
            'business_name': request.POST['business_name'],
            'pan_number': request.POST['pan_number'],
            'gst': request.POST['gst'],
            'contact': request.POST['contact'],
            'alternate_contact': request.POST['alternate_contact'],
            'pincode': request.POST['pincode'],
            'aadhar_number' : request.POST['aadhar_number'],
            'door_number' : request.POST['door_number'],
            'street_name' : request.POST['street_name'],
            'area' : request.POST['area'],        
            'fssa':request.POST['fssa'],
            'region':get_zone,
            # 'pin_your_location': request.POST['pin_your_location'],           
            'name': request.POST['name'],           
            'account_number':request.POST['account_number'],
            'ifsc_code':request.POST['ifsc_code'],
            'upi_id':request.POST['upi_id'],
            'gpay_number':request.POST['gpay_number'],
            'aadhar':aadhar_paths,
            'pan_file': pan_file_paths,
            'profile': profile_paths,
            'bank_passbook': bank_passbook_paths,
            'gst_file': gst_file_paths,
            'category':"fresh_cuts",
            'latitude':request.POST['latitude'],
            'longitude':request.POST['longitude'],

            }

        print(data)
        print("sunder")
        basicdetailsserializer = business_serializers.freshcuts_serializer(data=data)
        
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            print("serializer prblm")
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def freshcuts_alldata(request):
    if request.method == "GET":
        data = freshcutsmodel.objects.all()
        serializer = business_serializers.freshcuts_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def my_freshcuts_data(request,id):
    if request.method == "GET":
        data = freshcutsmodel.objects.get(fresh_id=id)
        print(data)
        serializer = business_serializers.freshcuts_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def business_freshcuts_data(request,id):
    if request.method == "GET":
        data = freshcutsmodel.objects.filter(Business_id=id)
        serializer = business_serializers.freshcuts_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


@api_view(["POST"])
def freshcuts_update(request,id,fresh_id):
    try:

        # Instantiate FileSystemStorage
        fs = FileSystemStorage()
        
        # Retrieve existing freshcuts data
        freshcuts_data = freshcutsmodel.objects.get(Business_id=id, fresh_id=fresh_id)
        freshcuts_datas = freshcutsmodel.objects.filter(Business_id=id, fresh_id=fresh_id).values()[0]

        # Handle file uploads
        if "aadhar" in request.FILES:
            aadhar = request.FILES['aadhar']
            aadhar_path = fs.save(f"api/freshcuts/{id}/aadhar/{aadhar.name}", aadhar)
            aadhar_paths = fs.url(aadhar_path)
        else:
            aadhar_paths = freshcuts_datas["aadhar"]

        if "pan_file" in request.FILES:
            pan_file = request.FILES["pan_file"]
            pan_file_path = fs.save(f"api/freshcuts/{id}/pan_file/{pan_file.name}", pan_file)
            pan_file_paths = fs.url(pan_file_path)
        else:
            pan_file_paths = freshcuts_datas["pan_file"]

        if "profile" in request.FILES:
            profile = request.FILES["profile"]
            profile_path = fs.save(f"api/freshcuts/{id}/profile/{profile.name}", profile)
            profile_paths = fs.url(profile_path)
        else:
            profile_paths = freshcuts_datas["profile"]

        if "bank_passbook" in request.FILES:
            bank_passbook = request.FILES["bank_passbook"]
            bank_passbook_path = fs.save(f"api/freshcuts/{id}/bank_passbook/{bank_passbook.name}", bank_passbook)
            bank_passbook_paths = fs.url(bank_passbook_path)
        else:
            bank_passbook_paths = freshcuts_datas["bank_passbook"]

        if "gst_file" in request.FILES:
            gst_file = request.FILES["gst_file"]
            gst_file_path = fs.save(f"api/freshcuts/{id}/gst_file/{gst_file.name}", gst_file)
            gst_file_paths = fs.url(gst_file_path)
        else:
            gst_file_paths = freshcuts_datas["gst_file"]
        
        # Update other fields
     
        freshcuts_data = freshcutsmodel.objects.get(Business_id=id, fresh_id=fresh_id)
        freshcuts_data.seller_name = request.data.get('seller_name', freshcuts_data.seller_name)
        freshcuts_data.business_name = request.data.get('business_name', freshcuts_data.business_name)
        freshcuts_data.pan_number = request.data.get('pan_number', freshcuts_data.pan_number)
        freshcuts_data.gst = request.data.get('gst', freshcuts_data.gst)
        freshcuts_data.contact = request.data.get('contact', freshcuts_data.contact)
        freshcuts_data.alternate_contact = request.data.get('alternate_contact', freshcuts_data.alternate_contact)
        freshcuts_data.door_number = request.data.get('door_number', freshcuts_data.door_number)
        freshcuts_data.street_name = request.data.get('street_name', freshcuts_data.street_name)
        freshcuts_data.area = request.data.get('area', freshcuts_data.area)
        freshcuts_data.fssa = request.data.get('fssa', freshcuts_data.fssa)
        freshcuts_data.region = request.data.get('region', freshcuts_data.region)
        freshcuts_data.pincode = request.data.get('pincode', freshcuts_data.pincode)
        freshcuts_data.aadhar_number = request.data.get('aadhar_number', freshcuts_data.aadhar_number)
        # freshcuts_data.pin_your_location = request.data.get('pin_your_location', freshcuts_data.pin_your_location)
        freshcuts_data.name = request.data.get('name', freshcuts_data.name)
        freshcuts_data.account_number = request.data.get('account_number', freshcuts_data.account_number)
        freshcuts_data.ifsc_code = request.data.get('ifsc_code', freshcuts_data.ifsc_code)
        freshcuts_data.upi_id = request.data.get('upi_id', freshcuts_data.upi_id)
        freshcuts_data.gpay_number = request.data.get('gpay_number', freshcuts_data.gpay_number)
        freshcuts_data.latitude = request.data.get('latitude', freshcuts_data.latitude)
        freshcuts_data.longitude = request.data.get('longitude', freshcuts_data.longitude)
        # Update other fields similarly

        # Save changes
        freshcuts_data.aadhar = aadhar_paths
        freshcuts_data.pan_file = pan_file_paths
        freshcuts_data.profile = profile_paths
        freshcuts_data.bank_passbook = bank_passbook_paths
        freshcuts_data.gst_file = gst_file_paths
        freshcuts_data.save()

        return Response(id, status=status.HTTP_200_OK)
    except:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    
# fresh products    
@api_view(['POST'])
def fresh_products(request, id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
   
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/fresh_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/fresh_products/{id}/other_images/"+str(sav).replace(" ", "_"), sav) 
        other_image.append(str(ot).replace(" ","_"))
            
    print(other_image)
    for iname in other_image:
        other_images_path = iname
        other_imagelist.append(all_image_url+fs.url(other_images_path))

    
    admin_data = business_commision.objects.get(id=1)  
    commission = float(admin_data.commission)  
    gst =   int(request.POST["gst"])
    
    actualprice = int(request.POST["actual_price"])
    discountprice = int(request.POST["discount_price"])

    # sellingprice = actualprice - discountprice
    sellingprice = discountprice
    commission_amount = sellingprice + ((commission / 100) * sellingprice)

    selling_price = commission_amount + ((gst / 100) * commission_amount)
   
    fresh_products = dict(request.POST)
    fresh_products['fresh_id'] = id
    fresh_products['product_id'] = product_id
    fresh_products['primary_image'] = primary_image_paths
    # fresh_products['other_images'] = other_imagelist
    fresh_products['selling_price'] = int(selling_price)
    print(fresh_products)
    cleaned_data_dict ={key:value[0] if isinstance(value,list) and len(value)==1 else value for key,value in fresh_products.items()}
    cleaned_data_dict ['other_images'] = other_imagelist
   
    global data
    data= {
        'fresh_id' : id,
        'product_id' : product_id,
        'status':False,
        'category':request.POST['category'],
        'subcategory':request.POST['subcategory'],
        'product':cleaned_data_dict
        
    }
    print(data)
    try:
        # shopping_product.save()
        print("Data saved successfully")
        print("dd")
        return Response({'discount': cleaned_data_dict['discount_price'], 'selling_price': int(selling_price)},
                        status=status.HTTP_200_OK)
    except Exception as e:
        print("Error while saving data:", e)
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def fresh_product_save(request, id):
    print(type(data["fresh_id"]))
    print(type(id))
    print(data["fresh_id"])
    if data["fresh_id"] == id:
        print("is working")
        new_shop_product = models.fresh_productsmodel(**data)
        new_shop_product.save()
        return Response({"Data saved successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"Data saved unsuccessfully"}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
def fresh_get_subcategoryproducts(request,id, subcategory):
    if request.method == "GET":
        # Filter products based on fresh_id and category
        data = models.fresh_productsmodel.objects.filter(fresh_id=id, subcategory=subcategory)
        alldataserializer = business_serializers.fresh_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def fresh_get_products(request,id):
    if request.method == "GET":
        data= models.fresh_productsmodel.objects.filter(fresh_id=id)
        alldataserializer= business_serializers.fresh_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def fresh_get_my_product(request,id,product_id):

    if request.method == "GET":
        # Filter products based on fresh_id and category
        data = models.fresh_productsmodel.objects.filter(fresh_id=id, product_id=product_id)
        alldataserializer = business_serializers.fresh_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

 
@api_view(['POST'])
def fresh_delete_product(request,id,product_id):
   
    fresh_product = get_object_or_404(models.fresh_productsmodel, fresh_id=id, product_id=product_id)

    fresh_product.delete()
    return Response(id,status=status.HTTP_200_OK)

@api_view(['POST'])
def fresh_update_product(request,id,product_id):

    fresh_products = dict(request.POST)

    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/fresh_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        fresh_products['primary_image'] = primary_image_paths
    except:
        # fresh_pro=collection.find_one({"fresh_id": id,"product_id":product_id})
        # primary_image_paths=fresh_pro.get("primary_image")
        # fresh_products['primary_image'] = primary_image_paths
        pass
        
    
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/fresh_products/{id}/other_images/"+str(sav).replace(" ", "_"), sav)
            other_image.append(str(ot).replace(" ","_"))
                
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
        fresh_products['other_images'] = other_imagelist

    except:
        pass
 
    try:
        fresh_product_instance = models.fresh_productsmodel.objects.get(fresh_id=id, product_id=product_id)
        
        existing_product_data = fresh_product_instance.product
        
        # Updating product field with new data
        fresh_products["other_images"] = fresh_product_instance.product['other_images']
        cleaned_data_dict = {key: value[0] if isinstance(value, list) and len(value) == 1 else value for key, value in
                             fresh_products.items()}

        # existing_product_data.update(cleaned_data_dict)
        
        # Saving changes to the SQLite table
        with transaction.atomic():
            # Updating only the product field
            fresh_product_instance.product = cleaned_data_dict
            fresh_product_instance.category = request.data['category']
            fresh_product_instance.subcategory = request.data['subcategory']
            fresh_product_instance.save()
        
        return Response(id, status=status.HTTP_200_OK)
    except models.fresh_productsmodel.DoesNotExist:
        return Response({"error": "fresh product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def fresh_imgupdate_product(request,id,product_id,index_value):
    try:
        if request.method == "POST":
            fs = FileSystemStorage()
            data = models.fresh_productsmodel.objects.get(fresh_id=id, product_id=product_id)
            fresh_pro=data.product.get("other_images")
            product_img=data.product
            print(fresh_pro)
            index_value = int(index_value)
            if index_value < 0 or index_value >= len(fresh_pro):
                return Response({"error": "Invalid index value"}, status=status.HTTP_400_BAD_REQUEST)
            if index_value == int(index_value):
                other_images = str(request.FILES['other_images']).replace(" ", "_")
                other_images_path = fs.save(f"api/fresh_products/{id}/other_images/" + other_images,
                                            request.FILES['other_images'])
                other_images_paths = all_image_url + fs.url(other_images_path)
                print(other_images_paths)
                fresh_pro[index_value] = other_images_paths
                product_img["other_images"] =fresh_pro
                data.product=product_img  #replacejson
                data.save()

            return Response({"message": "Image Updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Index value mismatch"}, status=status.HTTP_400_BAD_REQUEST)
            
    except models.fresh_productsmodel.DoesNotExist:
        return Response({"error": "Shop product not found"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST","GET"])
def fresh_productorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.Product_Ordermodel.objects.filter(Q(fresh_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data)
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
        
        if pro_data:
            
            alldata = []
            for product_id in pro_data:
                proget = models.fresh_productsmodel.objects.filter(product_id=product_id)
                alldata.extend(proget)
            
            serializer = business_serializers.delivered_productlistserializer(alldata, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
          

        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)



# dailymio_dashboard
    
@api_view(['GET'])
def dmio_total_revenue(request, id):
    if request.method == 'GET':
        if models.Product_Ordermodel.objects.filter(dmio_id_id__dmio_id=id).exists():
            total_revenue = models.Product_Ordermodel.objects.filter(dmio_id_id__dmio_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
            print(total_revenue)
            dmio = models.dailymio_model.objects.get(dmio_id=id)
            dmio.total_revenue = total_revenue
            dmio.save()
            return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)
        else:
            return Response(data={'total_revenue': 0}, status=status.HTTP_200_OK)



@api_view(['GET'])
def dmio_mon_revenue(request, id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        if models.Product_Ordermodel.objects.filter(dmio_id_id__dmio_id=id).exists():
            monthly_revenue = models.Product_Ordermodel.objects.filter(dmio_id_id__dmio_id=id, order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
            dmio = models.dailymio_model.objects.get(dmio_id=id)
            dmio.monthly_revenue = monthly_revenue
            dmio.save()
            return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)
        else:
            return Response(data={'monthly_revenue': 0}, status=status.HTTP_200_OK)



@api_view(['GET'])
def dmio_orderstatus(request,id):
    if request.method == 'GET':

        dmio = models.Product_Ordermodel.objects.filter(dmio_id_id__dmio_id=id).first()
        # if not dmio:
        #     return Response(data={'error': 'dmio not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.Product_Ordermodel.objects.filter(dmio_id_id__dmio_id=id, status='delivered').count()
        cancelled_count = models.Product_Ordermodel.objects.filter(dmio_id_id__dmio_id=id, status='cancelled').count()
        on_process_count = models.Product_Ordermodel.objects.filter(dmio_id_id__dmio_id=id, status='on_process').count()

        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
    else:
        return Response("shop_ordernot found",status=status.HTTP_400_BAD_REQUEST)

# dailymio_model

@api_view(['POST'])
def dailymio(request,id):
    if request.method == "POST":
        print(request.POST)
        pincode = request.POST['pincode']

        data1 = zone.objects.all()
        print(data1)
        get_zone = None  # Initialize get_zone variable

        for x in data1:
            print(x)
            if x.pincode is not None and pincode in x.pincode:
                get_zone = x.zone
                print(get_zone)
                break  # Once the zone is found, exit the loop

        print(get_zone)  # Check if zone is retrieved correctly
        
        # print(request.data)
        # print(request.FILES)
        fs = FileSystemStorage()
        aadhar = str(request.FILES['aadhar']).replace(" ", "_")
        aadhar_path = fs.save(f"api/dailymio/{id}/aahar/"+aadhar, request.FILES['aadhar'])
        pan_file = str(request.FILES['pan_file']).replace(" ", "_")
        pan_file_path = fs.save(f"api/dailymio/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
        profile = str(request.FILES['profile']).replace(" ", "_")
        profile_path = fs.save(f"api/dailymio/{id}/profile/"+profile, request.FILES['profile'])
        bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
        bank_passbook_path = fs.save(f"api/dailymio/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
        gst_file = str(request.FILES['gst_file']).replace(" ", "_")
        gst_file_path = fs.save(f"api/dailymio/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

        aadhar_paths = all_image_url+fs.url(aadhar_path)
        pan_file_paths = all_image_url+fs.url(pan_file_path)
        profile_paths = all_image_url+fs.url(profile_path)
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
        gst_file_paths = all_image_url+fs.url(gst_file_path)
        x = datetime.datetime.now()
        dmio_id=business_extension.dmio_id_generate()
        while True:
            if id == dmio_id:
                dmio_id=business_extension.dmio_id_generate()
            else:
                break

        data = {
            'Business_id': id,
            'dmio_id':dmio_id,
            'seller_name': request.POST['seller_name'],
            'business_name': request.POST['business_name'],
            'pan_number': request.POST['pan_number'],
            'gst': request.POST['gst'],
            'contact': request.POST['contact'],
            'alternate_contact': request.POST['alternate_contact'],
            'pincode': request.POST['pincode'],
            'aadhar_number' : request.POST['aadhar_number'],
            'door_number' : request.POST['door_number'],
            'street_name' : request.POST['street_name'],
            'area' : request.POST['area'],        
            'fssa':request.POST['fssa'],
            'region':get_zone,
            # 'pin_your_location': request.POST['pin_your_location'],           
            'name': request.POST['name'],           
            'account_number':request.POST['account_number'],
            'ifsc_code':request.POST['ifsc_code'],
            'upi_id':request.POST['upi_id'],
            'gpay_number':request.POST['gpay_number'],
            'aadhar':aadhar_paths,
            'pan_file': pan_file_paths,
            'profile': profile_paths,
            'bank_passbook': bank_passbook_paths,
            'gst_file': gst_file_paths,
            'category':"daily_mio",
            'latitude':request.POST['latitude'],
            'longitude':request.POST['longitude'],
            }

        print(data)
        basicdetailsserializer = business_serializers.dailymio_serializer(data=data)
        
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            print("serializer prblm")
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

    else:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dailymio_alldata(request):
    if request.method == "GET":
        data = dailymio_model.objects.all()
        serializer = business_serializers.dailymio_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def my_dailymio_data(request,id):
    if request.method == "GET":
        data = dailymio_model.objects.get(dmio_id=id)
        print(data)
        serializer = business_serializers.dailymio_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def business_dailymio_data(request,id):
    if request.method == "GET":
        data = dailymio_model.objects.filter(Business_id=id)
        serializer = business_serializers.dailymio_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
def dailymio_update(request,id,dmio_id):
    try:

        # Instantiate FileSystemStorage
        fs = FileSystemStorage()
        
        # Retrieve existing dailymio data
        dailymio_data = dailymio_model.objects.get(Business_id=id, dmio_id=dmio_id)
        dailymio_datas = dailymio_model.objects.filter(Business_id=id, dmio_id=dmio_id).values()[0]

        # Handle file uploads
        if "aadhar" in request.FILES:
            aadhar = request.FILES['aadhar']
            aadhar_path = fs.save(f"api/dailymio/{id}/aadhar/{aadhar.name}", aadhar)
            aadhar_paths = all_image_url+fs.url(aadhar_path)
        else:
            aadhar_paths = dailymio_datas["aadhar"]

        if "pan_file" in request.FILES:
            pan_file = request.FILES["pan_file"]
            pan_file_path = fs.save(f"api/dailymio/{id}/pan_file/{pan_file.name}", pan_file)
            pan_file_paths = all_image_url+fs.url(pan_file_path)
        else:
            pan_file_paths = dailymio_datas["pan_file"]

        if "profile" in request.FILES:
            profile = request.FILES["profile"]
            profile_path = fs.save(f"api/dailymio/{id}/profile/{profile.name}", profile)
            profile_paths = all_image_url+fs.url(profile_path)
        else:
            profile_paths = dailymio_datas["profile"]

        if "bank_passbook" in request.FILES:
            bank_passbook = request.FILES["bank_passbook"]
            bank_passbook_path = fs.save(f"api/dailymio/{id}/bank_passbook/{bank_passbook.name}", bank_passbook)
            bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
        else:
            bank_passbook_paths = dailymio_datas["bank_passbook"]

        if "gst_file" in request.FILES:
            gst_file = request.FILES["gst_file"]
            gst_file_path = fs.save(f"api/dailymio/{id}/gst_file/{gst_file.name}", gst_file)
            gst_file_paths = all_image_url+fs.url(gst_file_path)
        else:
            gst_file_paths = dailymio_datas["gst_file"]
        
        # Update other fields
     
        dailymio_data = dailymio_model.objects.get(Business_id=id, dmio_id=dmio_id)
        dailymio_data.seller_name = request.data.get('seller_name', dailymio_data.seller_name)
        dailymio_data.business_name = request.data.get('business_name', dailymio_data.business_name)
        dailymio_data.pan_number = request.data.get('pan_number', dailymio_data.pan_number)
        dailymio_data.gst = request.data.get('gst', dailymio_data.gst)
        dailymio_data.contact = request.data.get('contact', dailymio_data.contact)
        dailymio_data.alternate_contact = request.data.get('alternate_contact', dailymio_data.alternate_contact)
        dailymio_data.door_number = request.data.get('door_number', dailymio_data.door_number)
        dailymio_data.street_name = request.data.get('street_name', dailymio_data.street_name)
        dailymio_data.area = request.data.get('area', dailymio_data.area)
        dailymio_data.fssa = request.data.get('fssa', dailymio_data.fssa)
        dailymio_data.region = request.data.get('region', dailymio_data.region)
        dailymio_data.pincode = request.data.get('pincode', dailymio_data.pincode)
        dailymio_data.aadhar_number = request.data.get('aadhar_number', dailymio_data.aadhar_number)
        # dailymio_data.pin_your_location = request.data.get('pin_your_location', dailymio_data.pin_your_location)
        dailymio_data.name = request.data.get('name', dailymio_data.name)
        dailymio_data.account_number = request.data.get('account_number', dailymio_data.account_number)
        dailymio_data.ifsc_code = request.data.get('ifsc_code', dailymio_data.ifsc_code)
        dailymio_data.upi_id = request.data.get('upi_id', dailymio_data.upi_id)
        dailymio_data.gpay_number = request.data.get('gpay_number', dailymio_data.gpay_number)
        dailymio_data.latitude = request.data.get('latitude', dailymio_data.latitude)
        dailymio_data.longitude = request.data.get('longitude', dailymio_data.longitude)
        # Update other fields similarly

        # Save changes
        dailymio_data.aadhar = aadhar_paths
        dailymio_data.pan_file = pan_file_paths
        dailymio_data.profile = profile_paths
        dailymio_data.bank_passbook = bank_passbook_paths
        dailymio_data.gst_file = gst_file_paths
        dailymio_data.save()

        return Response(id, status=status.HTTP_200_OK)
    except:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    
# dailymio products

# dmio products  
@api_view(['POST'])
def dmio_products(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/dmio_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/dmio_products/{id}/other_images/"+str(sav).replace(" ", "_"), sav) 
        other_image.append(str(ot).replace(" ","_"))
            
    print(other_image)
    for iname in other_image:
        other_images_path = iname
        other_imagelist.append(all_image_url+fs.url(other_images_path))

    
    admin_data = business_commision.objects.get(id=1)  
    commission = float(admin_data.commission)  
    gst =   int(request.POST["gst"])
 
    
    actualprice = int(request.POST["actual_price"])
    discountprice = int(request.POST["discount_price"])

    # sellingprice = actualprice - discountprice
    sellingprice = discountprice
    commission_amount = sellingprice + ((commission / 100) * sellingprice)

    selling_price = commission_amount + ((gst / 100) * commission_amount)
   
    dmio_products = dict(request.POST)
    dmio_products['dmio_id'] = id
    dmio_products['product_id'] = product_id
    dmio_products['primary_image'] = primary_image_paths
    # dmio_products['other_images'] = other_imagelist
    dmio_products['selling_price'] = int(selling_price)
    print(dmio_products)
    cleaned_data_dict ={key:value[0] if isinstance(value,list) and len(value)==1 else value for key,value in dmio_products.items()}
    cleaned_data_dict ['other_images'] = other_imagelist

    global data
    data= {
        'dmio_id' : id,
        'product_id' : product_id,
        'status':False,
        'category':request.POST['category'],
        'subcategory':request.POST['subcategory'],
        'product':cleaned_data_dict
        
    }
    # shopping_product = models.shop_productsmodel(**shop_product_data)
    try:
        # shopping_product.save()
        print("Data saved successfully")
        return Response({'discount': cleaned_data_dict['discount_price'], 'selling_price': int(selling_price)},
                        status=status.HTTP_200_OK)
    except Exception as e:
        print("Error while saving data:", e)
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def dmio_product_save(request, id):
    print(type(data["dmio_id"]))
    print(type(id))
    print(data["dmio_id"])
    if data["dmio_id"] == id:
        print("is working")
        new_shop_product = models.dmio_productsmodel(**data)
        new_shop_product.save()
        return Response({"Data saved successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"Data saved unsuccessfully"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def dmio_get_subcategoryproducts(request, id, subcategory):
    if request.method == "GET":
        # Filter products based on dmio_id and category
        data = models.dmio_productsmodel.objects.filter(dmio_id=id, subcategory=subcategory)
        alldataserializer = business_serializers.dmio_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def dmio_get_products(request,id):
    if request.method == "GET":
        data= models.dmio_productsmodel.objects.filter(dmio_id=id)
        alldataserializer= business_serializers.dmio_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def dmio_get_my_product(request,id,product_id):

    if request.method == "GET":
        # Filter products based on dmio_id and category
        data = models.dmio_productsmodel.objects.filter(dmio_id=id, product_id=product_id)
        alldataserializer = business_serializers.dmio_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

 

@api_view(['POST'])
def dmio_delete_product(request,id,product_id):
   
    dmio_product = get_object_or_404(models.dmio_productsmodel, dmio_id=id, product_id=product_id)

    dmio_product.delete()
    return Response(id,status=status.HTTP_200_OK)

@api_view(['POST'])
def dmio_update_product(request,id,product_id):

    dmio_products = dict(request.POST)

    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/dmio_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        dmio_products['primary_image'] = primary_image_paths
    except:
        # dmio_pro=collection.find_one({"dmio_id": id,"product_id":product_id})
        # primary_image_paths=dmio_pro.get("primary_image")
        # dmio_products['primary_image'] = primary_image_paths
        pass
        
    
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/dmio_products/{id}/other_images/"+str(sav).replace(" ", "_"), sav)
            other_image.append(str(ot).replace(" ","_"))
                
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
        dmio_products['other_images'] = other_imagelist

    except:
        pass

    try:
        dmio_product_instance = models.dmio_productsmodel.objects.get(dmio_id=id, product_id=product_id)
        
        existing_product_data = dmio_product_instance.product
        
        # Updating product field with new data
        dmio_products["other_images"] = dmio_product_instance.product['other_images']
        cleaned_data_dict = {key: value[0] if isinstance(value, list) and len(value) == 1 else value for key, value in
                            dmio_products.items()}

        # existing_product_data.update(cleaned_data_dict)
        
        # Saving changes to the SQLite table
        with transaction.atomic():
            # Updating only the product field
            dmio_product_instance.product = cleaned_data_dict
            dmio_product_instance.category = request.data['category']
            dmio_product_instance.subcategory = request.data['subcategory']
            dmio_product_instance.save()
        
        return Response(id, status=status.HTTP_200_OK)
    except models.dmio_productsmodel.DoesNotExist:
        return Response({"error": "dmio product not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def dmio_imgupdate_product(request, id, product_id,index_value):
    try:
        if request.method == "POST":
            fs = FileSystemStorage()
            data = models.dmio_productsmodel.objects.get(dmio_id=id, product_id=product_id)
            dmio_pro=data.product.get("other_images")
            product_img=data.product
            print(dmio_pro)
            index_value = int(index_value)
            if index_value < 0 or index_value >= len(dmio_pro):
                return Response({"error": "Invalid index value"}, status=status.HTTP_400_BAD_REQUEST)
            if index_value == int(index_value):
                other_images = str(request.FILES['other_images']).replace(" ", "_")
                other_images_path = fs.save(f"api/dmio_products/{id}/other_images/" + other_images,
                                            request.FILES['other_images'])
                other_images_paths = all_image_url + fs.url(other_images_path)
                print(other_images_paths)
                dmio_pro[index_value] = other_images_paths
                product_img["other_images"] =dmio_pro
                data.product=product_img  #replacejson
                data.save()

            return Response({"message": "Image Updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Index value mismatch"}, status=status.HTTP_400_BAD_REQUEST)
            
    except models.dmio_productsmodel.DoesNotExist:
        return Response({"error": "Shop product not found"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST","GET"])
def dmio_productorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.Product_Ordermodel.objects.filter(Q(dmio_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data)
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
        
        if pro_data:
            
            alldata = []
            for product_id in pro_data:
                proget = models.dmio_productsmodel.objects.filter(product_id=product_id)
                alldata.extend(proget)
            
            serializer = business_serializers.delivered_productlistserializer(alldata, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
          

        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)


# pharmacy _dashboard
   
@api_view(['GET'])
def pharmacy_total_revenue(request, id):
    if request.method == 'GET':
        if models.Product_Ordermodel.objects.filter(pharm_id_id__pharm_id=id).exists():
            total_revenue = models.Product_Ordermodel.objects.filter(pharm_id_id__pharm_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
            print(total_revenue)
            pharm = models.pharmacy_model.objects.get(pharm_id=id)
            pharm.total_revenue = total_revenue
            pharm.save()
            return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)
        else:
            return Response(data={'total_revenue': 0}, status=status.HTTP_200_OK)


@api_view(['GET'])
def pharm_mon_revenue(request, id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        if models.Product_Ordermodel.objects.filter(pharm_id_id__pharm_id=id).exists():
            monthly_revenue = models.Product_Ordermodel.objects.filter(pharm_id_id__pharm_id=id, order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
            pharm = models.pharmacy_model.objects.get(pharm_id=id)
            pharm.monthly_revenue = monthly_revenue
            pharm.save()
            return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)
        else:
            return Response(data={'monthly_revenue': 0}, status=status.HTTP_200_OK)


@api_view(['GET'])
def pharm_orderstatus(request,id):
    if request.method == 'GET':

        pharm = models.Product_Ordermodel.objects.filter(pharm_id_id__pharm_id=id).first()
        # if not pharm:
        #     return Response(data={'error': 'pharm not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.Product_Ordermodel.objects.filter(pharm_id_id__pharm_id=id, status='delivered').count()
        cancelled_count = models.Product_Ordermodel.objects.filter(pharm_id_id__pharm_id=id, status='cancelled').count()
        on_process_count = models.Product_Ordermodel.objects.filter(pharm_id_id__pharm_id=id, status='on_process').count()

        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

    else:
        return Response("shop_ordernot found",status=status.HTTP_400_BAD_REQUEST)

# pharmacy_model
@api_view(['POST'])
def pharmacy(request,id):
    if request.method == "POST":
        print(request.POST)
        pincode = request.POST['pincode']

        data1 = zone.objects.all()
        print(data1)
        get_zone = None  # Initialize get_zone variable

        for x in data1:
            print(x)
            if x.pincode is not None and pincode in x.pincode:
                get_zone = x.zone
                print(get_zone)
                break  # Once the zone is found, exit the loop

        print(get_zone)  # Check if zone is retrieved correctly
        # print(request.data)
        # print(request.FILES)
        fs = FileSystemStorage()
        aadhar = str(request.FILES['aadhar']).replace(" ", "_")
        aadhar_path = fs.save(f"api/pharmacy/{id}/aahar/"+aadhar, request.FILES['aadhar'])
        pan_file = str(request.FILES['pan_file']).replace(" ", "_")
        pan_file_path = fs.save(f"api/pharmacy/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
        profile = str(request.FILES['profile']).replace(" ", "_")
        profile_path = fs.save(f"api/pharmacy/{id}/profile/"+profile, request.FILES['profile'])
        bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
        bank_passbook_path = fs.save(f"api/pharmacy/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
        gst_file = str(request.FILES['gst_file']).replace(" ", "_")
        gst_file_path = fs.save(f"api/pharmacy/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

        aadhar_paths = all_image_url+fs.url(aadhar_path)
        pan_file_paths = all_image_url+fs.url(pan_file_path)
        profile_paths = all_image_url+fs.url(profile_path)
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
        gst_file_paths = all_image_url+fs.url(gst_file_path)
        x = datetime.datetime.now()
        pharms_id=business_extension.pharm_id_generate()
        while True:
            if id == pharms_id:
                pharms_id=business_extension.pharm_id_generate()
            else:
                break
        data = {
            'Business_id': id,
            'pharm_id': pharms_id,
            'seller_name': request.POST['seller_name'],
            'business_name': request.POST['business_name'],
            'pan_number': request.POST['pan_number'],
            'gst': request.POST['gst'],
            'contact': request.POST['contact'],
            'alternate_contact': request.POST['alternate_contact'],
            'pincode': request.POST['pincode'],
            'aadhar_number' : request.POST['aadhar_number'],
            'door_number' : request.POST['door_number'],
            'street_name' : request.POST['street_name'],
            'area' : request.POST['area'],        
            'fssa':request.POST['fssa'],
            'region':get_zone,
            # 'pin_your_location': request.POST['pin_your_location'],           
            'name': request.POST['name'],           
            'account_number':request.POST['account_number'],
            'ifsc_code':request.POST['ifsc_code'],
            'upi_id':request.POST['upi_id'],
            'gpay_number':request.POST['gpay_number'],
            'aadhar':aadhar_paths,
            'pan_file': pan_file_paths,
            'profile': profile_paths,
            'bank_passbook': bank_passbook_paths,
            'gst_file': gst_file_paths,
            'category':"pharmacy",
            'latitude':request.POST['latitude'],
            'longitude':request.POST['longitude'],
            }

        print(data)
        basicdetailsserializer = business_serializers.pharmacy_serializer(data=data)
        
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            print("serializer prblm")
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def pharmacy_alldata(request):
    if request.method == "GET":
        data = pharmacy_model.objects.all()
        serializer = business_serializers.pharmacy_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def my_pharmacy_data(request,id):
    if request.method == "GET":
        data = pharmacy_model.objects.get(pharm_id=id)
        print(data)
        serializer = business_serializers.pharmacy_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def business_pharmacy_data(request,id):
    if request.method == "GET":
        data = pharmacy_model.objects.filter(Business_id=id)
        serializer = business_serializers.pharmacy_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


@api_view(["POST"])
def pharmacy_update(request,id,pharm_id):
    try:

        # Instantiate FileSystemStorage
        fs = FileSystemStorage()
        
        # Retrieve existing pharmacy data
        pharmacy_data = pharmacy_model.objects.get(Business_id=id, pharm_id=pharm_id)
        pharmacy_datas = pharmacy_model.objects.filter(Business_id=id, pharm_id=pharm_id).values()[0]

        # Handle file uploads
        if "aadhar" in request.FILES:
            aadhar = request.FILES['aadhar']
            aadhar_path = fs.save(f"api/pharmacy/{id}/aadhar/{aadhar.name}", aadhar)
            aadhar_paths = all_image_url+fs.url(aadhar_path)
        else:
            aadhar_paths = pharmacy_datas["aadhar"]

        if "pan_file" in request.FILES:
            pan_file = request.FILES["pan_file"]
            pan_file_path = fs.save(f"api/pharmacy/{id}/pan_file/{pan_file.name}", pan_file)
            pan_file_paths = all_image_url+fs.url(pan_file_path)
        else:
            pan_file_paths = pharmacy_datas["pan_file"]

        if "profile" in request.FILES:
            profile = request.FILES["profile"]
            profile_path = fs.save(f"api/pharmacy/{id}/profile/{profile.name}", profile)
            profile_paths = all_image_url+fs.url(profile_path)
        else:
            profile_paths = pharmacy_datas["profile"]

        if "bank_passbook" in request.FILES:
            bank_passbook = request.FILES["bank_passbook"]
            bank_passbook_path = fs.save(f"api/pharmacy/{id}/bank_passbook/{bank_passbook.name}", bank_passbook)
            bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
        else:
            bank_passbook_paths = pharmacy_datas["bank_passbook"]

        if "gst_file" in request.FILES:
            gst_file = request.FILES["gst_file"]
            gst_file_path = fs.save(f"api/pharmacy/{id}/gst_file/{gst_file.name}", gst_file)
            gst_file_paths = all_image_url+fs.url(gst_file_path)
        else:
            gst_file_paths = pharmacy_datas["gst_file"]
        
        # Update other fields
     
        pharmacy_data = pharmacy_model.objects.get(Business_id=id, pharm_id=pharm_id)
        pharmacy_data.seller_name = request.data.get('seller_name', pharmacy_data.seller_name)
        pharmacy_data.business_name = request.data.get('business_name', pharmacy_data.business_name)
        pharmacy_data.pan_number = request.data.get('pan_number', pharmacy_data.pan_number)
        pharmacy_data.gst = request.data.get('gst', pharmacy_data.gst)
        pharmacy_data.contact = request.data.get('contact', pharmacy_data.contact)
        pharmacy_data.alternate_contact = request.data.get('alternate_contact', pharmacy_data.alternate_contact)
        pharmacy_data.door_number = request.data.get('door_number', pharmacy_data.door_number)
        pharmacy_data.street_name = request.data.get('street_name', pharmacy_data.street_name)
        pharmacy_data.area = request.data.get('area', pharmacy_data.area)
        pharmacy_data.fssa = request.data.get('fssa', pharmacy_data.fssa)
        pharmacy_data.region = request.data.get('region', pharmacy_data.region)
        pharmacy_data.pincode = request.data.get('pincode', pharmacy_data.pincode)
        pharmacy_data.aadhar_number = request.data.get('aadhar_number', pharmacy_data.aadhar_number)
        # pharmacy_data.pin_your_location = request.data.get('pin_your_location', pharmacy_data.pin_your_location)
        pharmacy_data.name = request.data.get('name', pharmacy_data.name)
        pharmacy_data.account_number = request.data.get('account_number', pharmacy_data.account_number)
        pharmacy_data.ifsc_code = request.data.get('ifsc_code', pharmacy_data.ifsc_code)
        pharmacy_data.upi_id = request.data.get('upi_id', pharmacy_data.upi_id)
        pharmacy_data.gpay_number = request.data.get('gpay_number', pharmacy_data.gpay_number)
        pharmacy_data.latitude = request.data.get('latitude', pharmacy_data.latitude)
        pharmacy_data.longitude = request.data.get('longitude', pharmacy_data.longitude)
        # Update other fields similarly

        # Save changes
        pharmacy_data.aadhar = aadhar_paths
        pharmacy_data.pan_file = pan_file_paths
        pharmacy_data.profile = profile_paths
        pharmacy_data.bank_passbook = bank_passbook_paths
        pharmacy_data.gst_file = gst_file_paths
        pharmacy_data.save()

        return Response(id, status=status.HTTP_200_OK)
    except:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


# pharmacy products
 
@api_view(['POST'])
def pharmacy_products(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
  
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/pharmacy_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/pharmacy_products/{id}/other_images/"+str(sav).replace(" ", "_"), sav) 
        other_image.append(str(ot).replace(" ","_"))
            
    print(other_image)
    for iname in other_image:
        other_images_path = iname
        other_imagelist.append(all_image_url+fs.url(other_images_path))

    
    admin_data = business_commision.objects.get(id=1)  
    commission = float(admin_data.commission)  
    gst =   int(request.POST["gst"])
    
    actualprice = int(request.POST["actual_price"])
    discountprice = int(request.POST["discount_price"])

    # sellingprice = actualprice - discountprice
    sellingprice = discountprice
    commission_amount = sellingprice + ((commission / 100) * sellingprice)

    selling_price = commission_amount + ((gst / 100) * commission_amount)
   
    pharmacy_products = dict(request.POST)
    pharmacy_products['pharm_id'] = id
    pharmacy_products['product_id'] = product_id
    pharmacy_products['primary_image'] = primary_image_paths
    # pharmacy_products['other_images'] = other_imagelist
    pharmacy_products['selling_price'] = int(selling_price)
    print(pharmacy_products)
    cleaned_data_dict ={key:value[0] if isinstance(value,list) and len(value)==1 else value for key,value in pharmacy_products.items()}
    cleaned_data_dict ['other_images'] = other_imagelist
   
    global data
    data= {
        'pharm_id' : id,
        'product_id' : product_id,
        'status':False,
        'category':request.POST['category'],
        'subcategory':request.POST['subcategory'],
        'product':cleaned_data_dict
        
    }
    try:
  
        print("Data saved successfully")
        return Response({'discount': cleaned_data_dict['discount_price'], 'selling_price': int(selling_price)},
                        status=status.HTTP_200_OK)
    except Exception as e:
        print("Error while saving data:", e)
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def pharmacy_product_save(request, id):
    print(type(data["pharm_id"]))
    print(type(id))
    print(data["pharm_id"])
    if data["pharm_id"] == id:
        print("is working")
        new_shop_product = models.pharmacy_productsmodel(**data)
        new_shop_product.save()
        return Response({"Data saved successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"Data saved unsuccessfully"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def pharmacy_get_subcategoryproducts(request, id, subcategory):
    if request.method == "GET":
        # Filter products based on pharm_id and category
        data = models.pharmacy_productsmodel.objects.filter(pharm_id=id, subcategory=subcategory)
        alldataserializer = business_serializers.pharmacy_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def pharmacy_get_products(request,id):
    if request.method == "GET":
        data= models.pharmacy_productsmodel.objects.filter(pharm_id=id)
        alldataserializer= business_serializers.pharmacy_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def pharmacy_get_my_product(request,id,product_id):

    if request.method == "GET":
        # Filter products based on pharm_id and category
        data = models.pharmacy_productsmodel.objects.filter(pharm_id=id, product_id=product_id)
        alldataserializer = business_serializers.pharmacy_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

 
@api_view(['POST'])
def pharmacy_delete_product(request,id,product_id):
  
    pharmacy_product = get_object_or_404(models.pharmacy_productsmodel, pharm_id=id, product_id=product_id)
    pharmacy_product.delete()
    return Response(id,status=status.HTTP_200_OK)

@api_view(['POST'])
def pharmacy_update_product(request,id,product_id):

    pharmacy_products = dict(request.POST)

    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/pharmacy_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        pharmacy_products['primary_image'] = primary_image_paths
    except:
        # pharmacy_pro=collection.find_one({"pharm_id": id,"product_id":product_id})
        # primary_image_paths=pharmacy_pro.get("primary_image")
        # pharmacy_products['primary_image'] = primary_image_paths
        pass
        
    
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/pharmacy_products/{id}/other_images/"+str(sav).replace(" ", "_"), sav)
            other_image.append(str(ot).replace(" ","_"))
                
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
        pharmacy_products['other_images'] = other_imagelist

    except:
        pass

    try:
        pharmacy_product_instance = models.pharmacy_productsmodel.objects.get(pharm_id=id, product_id=product_id)
        
        existing_product_data = pharmacy_product_instance.product
        
        # Updating product field with new data
        pharmacy_products["other_images"] = pharmacy_product_instance.product['other_images']
        cleaned_data_dict = {key: value[0] if isinstance(value, list) and len(value) == 1 else value for key, value in
                            pharmacy_products.items()}

        # existing_product_data.update(cleaned_data_dict)
        
        # Saving changes to the SQLite table
        with transaction.atomic():
            # Updating only the product field
            pharmacy_product_instance.product = cleaned_data_dict
            pharmacy_product_instance.category = request.data['category']
            pharmacy_product_instance.subcategory = request.data['subcategory']
            pharmacy_product_instance.save()
        
        return Response(id, status=status.HTTP_200_OK)
    except models.pharmacy_productsmodel.DoesNotExist:
        return Response({"error": "pharmacy product not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def pharm_imgupdate_product(request, id, product_id,index_value):
    try:
        if request.method == "POST":
            fs = FileSystemStorage()
            data = models.pharmacy_productsmodel.objects.get(pharm_id=id, product_id=product_id)
            pharm_pro=data.product.get("other_images")
            product_img=data.product
            print(pharm_pro)
            index_value = int(index_value)
            if index_value < 0 or index_value >= len(pharm_pro):
                return Response({"error": "Invalid index value"}, status=status.HTTP_400_BAD_REQUEST)
            if index_value == int(index_value):
                other_images = str(request.FILES['other_images']).replace(" ", "_")
                other_images_path = fs.save(f"api/pharm_products/{id}/other_images/" + other_images,
                                            request.FILES['other_images'])
                other_images_paths = all_image_url + fs.url(other_images_path)
                print(other_images_paths)
                pharm_pro[index_value] = other_images_paths
                product_img["other_images"] =pharm_pro
                data.product=product_img  #replacejson
                data.save()

            return Response({"message": "Image Updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Index value mismatch"}, status=status.HTTP_400_BAD_REQUEST)
            
    except models.pharmacy_productsmodel.DoesNotExist:
        return Response({"error": "Shop product not found"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST","GET"])
def pharmacy_productorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.Product_Ordermodel.objects.filter(Q(pharm_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data)
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
        
        if pro_data:
            
            alldata = []
            for product_id in pro_data:
                proget = models.pharmacy_productsmodel.objects.filter(product_id=product_id)
                alldata.extend(proget)
            
            serializer = business_serializers.delivered_productlistserializer(alldata, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
          

        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)



#  d_original_dashboard
    
@api_view(['GET'])
def d_origin_total_revenue(request, id):
    if request.method == 'GET':
        if models.Product_Ordermodel.objects.filter(d_id_id__d_id=id).exists():
            total_revenue = models.Product_Ordermodel.objects.filter(d_id_id__d_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
            print(total_revenue)
            shop = models.d_originalmodel.objects.get(d_id=id)
            shop.total_revenue = total_revenue
            shop.save()
            return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)
        else:
            return Response(data={'total_revenue': 0}, status=status.HTTP_200_OK)


@api_view(['GET'])
def d_origin_mon_revenue(request, id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        if models.Product_Ordermodel.objects.filter(d_id_id__d_id=id).exists():
            monthly_revenue = models.Product_Ordermodel.objects.filter(d_id_id__d_id=id, order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
            d_origin = models.d_originalmodel.objects.get(d_id=id)
            d_origin.monthly_revenue = monthly_revenue
            d_origin.save()
            return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)
        else:
            return Response(data={'monthly_revenue': 0}, status=status.HTTP_200_OK)

@api_view(['GET'])
def d_origin_orderstatus(request,id):
    if request.method == 'GET':

        d_origin = models.Product_Ordermodel.objects.filter(d_id_id__d_id=id).first()
        # if not d_origin:
        #     return Response(data={'error': 'd_origin not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.Product_Ordermodel.objects.filter(d_id_id__d_id=id, status='delivered').count()
        cancelled_count = models.Product_Ordermodel.objects.filter(d_id_id__d_id=id, status='cancelled').count()
        on_process_count = models.Product_Ordermodel.objects.filter(d_id_id__d_id=id, status='on_process').count()

        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

# d_original
@api_view(['POST'])
def d_original(request,id):
    if request.method == "POST":
        print(request.POST)
        pincode = request.POST['pincode']

        data1 = zone.objects.all()
        print(data1)
        get_zone = None  # Initialize get_zone variable

        for x in data1:
            print(x)
            if x.pincode is not None and pincode in x.pincode:
                get_zone = x.zone
                print(get_zone)
                break  # Once the zone is found, exit the loop

        print(get_zone)  # Check if zone is retrieved correctly

        # print(request.data)
        # print(request.FILES)
        fs = FileSystemStorage()
        aadhar = str(request.FILES['aadhar']).replace(" ", "_")
        aadhar_path = fs.save(f"api/d_original/{id}/aahar/"+aadhar, request.FILES['aadhar'])
        pan_file = str(request.FILES['pan_file']).replace(" ", "_")
        pan_file_path = fs.save(f"api/d_original/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
        profile = str(request.FILES['profile']).replace(" ", "_")
        profile_path = fs.save(f"api/d_original/{id}/profile/"+profile, request.FILES['profile'])
        bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
        bank_passbook_path = fs.save(f"api/d_original/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
        gst_file = str(request.FILES['gst_file']).replace(" ", "_")
        gst_file_path = fs.save(f"api/d_original/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

        aadhar_paths = all_image_url+fs.url(aadhar_path)
        pan_file_paths = all_image_url+fs.url(pan_file_path)
        profile_paths = all_image_url+fs.url(profile_path)
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
        gst_file_paths = all_image_url+fs.url(gst_file_path)
        x = datetime.datetime.now()
        ds_id=business_extension.d_id_generate()
        while True:
            if id == ds_id:
                ds_id=business_extension.d_id_generate()
            else:
                break

        data = {
            'Business_id': id,
            'd_id':ds_id,
            'seller_name': request.POST['seller_name'],
            'business_name': request.POST['business_name'],
            'pan_number': request.POST['pan_number'],
            'gst': request.POST['gst'],
            'contact': request.POST['contact'],
            'alternate_contact': request.POST['alternate_contact'],
            'pincode': request.POST['pincode'],
            'aadhar_number' : request.POST['aadhar_number'],
            'door_number' : request.POST['door_number'],
            'street_name' : request.POST['street_name'],
            'area' : request.POST['area'],        
            'fssa':request.POST['fssa'],
            'region':get_zone,
            # 'pin_your_location': request.POST['pin_your_location'],           
            'name': request.POST['name'],           
            'account_number':request.POST['account_number'],
            'ifsc_code':request.POST['ifsc_code'],
            'upi_id':request.POST['upi_id'],
            'gpay_number':request.POST['gpay_number'],
            'aadhar':aadhar_paths,
            'pan_file': pan_file_paths,
            'profile': profile_paths,
            'bank_passbook': bank_passbook_paths,
            'gst_file': gst_file_paths,
            'category':"d_original",
            'latitude':request.POST['latitude'],
            'longitude':request.POST['longitude'],
            }

        print(data)
        basicdetailsserializer = business_serializers.d_original_serializer(data=data)
        
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            print("serializer prblm")
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def d_original_alldata(request):
    if request.method == "GET":
        data = d_originalmodel.objects.all()
        serializer = business_serializers.d_original_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def my_d_original_data(request,id):
    if request.method == "GET":
        data = d_originalmodel.objects.get(d_id=id)
        print(data)
        serializer = business_serializers.d_original_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def business_d_original_data(request,id):
    if request.method == "GET":
        data = d_originalmodel.objects.filter(Business_id=id)
        serializer = business_serializers.d_original_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
def d_original_update(request,id,d_id):
    try:

        # Instantiate FileSystemStorage
        fs = FileSystemStorage()
        
        # Retrieve existing d_original data
        d_original_data = d_originalmodel.objects.get(Business_id=id, d_id=d_id)
        d_original_datas = d_originalmodel.objects.filter(Business_id=id, d_id=d_id).values()[0]

        # Handle file uploads
        if "aadhar" in request.FILES:
            aadhar = request.FILES['aadhar']
            aadhar_path = fs.save(f"api/d_original/{id}/aadhar/{aadhar.name}", aadhar)
            aadhar_paths = all_image_url+fs.url(aadhar_path)
        else:
            aadhar_paths = d_original_datas["aadhar"]

        if "pan_file" in request.FILES:
            pan_file = request.FILES["pan_file"]
            pan_file_path = fs.save(f"api/d_original/{id}/pan_file/{pan_file.name}", pan_file)
            pan_file_paths = all_image_url+fs.url(pan_file_path)
        else:
            pan_file_paths = d_original_datas["pan_file"]

        if "profile" in request.FILES:
            profile = request.FILES["profile"]
            profile_path = fs.save(f"api/d_original/{id}/profile/{profile.name}", profile)
            profile_paths = all_image_url+fs.url(profile_path)
        else:
            profile_paths = d_original_datas["profile"]

        if "bank_passbook" in request.FILES:
            bank_passbook = request.FILES["bank_passbook"]
            bank_passbook_path = fs.save(f"api/d_original/{id}/bank_passbook/{bank_passbook.name}", bank_passbook)
            bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
        else:
            bank_passbook_paths = d_original_datas["bank_passbook"]

        if "gst_file" in request.FILES:
            gst_file = request.FILES["gst_file"]
            gst_file_path = fs.save(f"api/d_original/{id}/gst_file/{gst_file.name}", gst_file)
            gst_file_paths = all_image_url+fs.url(gst_file_path)
        else:
            gst_file_paths = d_original_datas["gst_file"]
        
        # Update other fields
     
        d_original_data = d_originalmodel.objects.get(Business_id=id, d_id=d_id)
        d_original_data.seller_name = request.data.get('seller_name', d_original_data.seller_name)
        d_original_data.business_name = request.data.get('business_name', d_original_data.business_name)
        d_original_data.pan_number = request.data.get('pan_number', d_original_data.pan_number)
        d_original_data.gst = request.data.get('gst', d_original_data.gst)
        d_original_data.contact = request.data.get('contact', d_original_data.contact)
        d_original_data.alternate_contact = request.data.get('alternate_contact', d_original_data.alternate_contact)
        d_original_data.door_number = request.data.get('door_number', d_original_data.door_number)
        d_original_data.street_name = request.data.get('street_name', d_original_data.street_name)
        d_original_data.area = request.data.get('area', d_original_data.area)
        d_original_data.region = request.data.get('region', d_original_data.region)
        d_original_data.pincode = request.data.get('pincode', d_original_data.pincode)
        d_original_data.aadhar_number = request.data.get('aadhar_number', d_original_data.aadhar_number)
        # d_original_data.pin_your_location = request.data.get('pin_your_location', d_original_data.pin_your_location)
        d_original_data.name = request.data.get('name', d_original_data.name)
        d_original_data.account_number = request.data.get('account_number', d_original_data.account_number)
        d_original_data.ifsc_code = request.data.get('ifsc_code', d_original_data.ifsc_code)
        d_original_data.upi_id = request.data.get('upi_id', d_original_data.upi_id)
        d_original_data.gpay_number = request.data.get('gpay_number', d_original_data.gpay_number)
        d_original_data.latitude = request.data.get('latitude', d_original_data.latitude)
        d_original_data.longitude = request.data.get('longitude', d_original_data.longitude)
        # Update other fields similarly

        # Save changes
        d_original_data.aadhar = aadhar_paths
        d_original_data.pan_file = pan_file_paths
        d_original_data.profile = profile_paths
        d_original_data.bank_passbook = bank_passbook_paths
        d_original_data.gst_file = gst_file_paths
        d_original_data.save()

        return Response(id, status=status.HTTP_200_OK)
    except:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)



# d_original products  
@api_view(['POST'])
def d_original_products(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/d_original_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/d_original_products/{id}/other_images/"+str(sav).replace(" ", "_"), sav) 
        other_image.append(str(ot).replace(" ","_"))
            
    print(other_image)
    for iname in other_image:
        other_images_path = iname
        other_imagelist.append(all_image_url+fs.url(other_images_path))

    
    admin_data = business_commision.objects.get(id=1)  
    commission = float(admin_data.commission)  
    gst =   int(request.POST["gst"])
    
    actualprice = int(request.POST["actual_price"])
    discountprice = int(request.POST["discount_price"])

    # sellingprice = actualprice - discountprice
    sellingprice = discountprice
    commission_amount = sellingprice + ((commission / 100) * sellingprice)

    selling_price = commission_amount + ((gst / 100) * commission_amount)
   
    d_original_products = dict(request.POST)
    d_original_products['d_id'] = id
    d_original_products['product_id'] = product_id
    d_original_products['primary_image'] = primary_image_paths
    # d_original_products['other_images'] = other_imagelist
    d_original_products['selling_price'] = int(selling_price)
    print(d_original_products)
    cleaned_data_dict ={key:value[0] if isinstance(value,list) and len(value)==1 else value for key,value in d_original_products.items()}
    cleaned_data_dict ['other_images'] = other_imagelist
   
    global data
    data= {
        'd_id' : id,
        'product_id' : product_id,
        'status':False,
        'category':request.POST['category'],
        'subcategory':request.POST['subcategory'],
        'product':cleaned_data_dict,
        'district':request.POST['district'],
        
    }
    try:
        # shopping_product.save()
        print("Data saved successfully")
        return Response({'discount': cleaned_data_dict['discount_price'], 'selling_price': int(selling_price)},
                        status=status.HTTP_200_OK)
    except Exception as e:
        print("Error while saving data:", e)
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def d_original_product_save(request, id):
    print(type(data["d_id"]))
    print(type(id))
    print(data["d_id"])
    if data["d_id"] == id:
        print("is working")
        new_shop_product = models.d_original_productsmodel(**data)
        new_shop_product.save()
        return Response({"Data saved successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"Data saved unsuccessfully"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def d_original_get_subcategoryproducts(request, id,subcategory):
    if request.method == "GET":
        # Filter products based on d_id and category
        data = models.d_original_productsmodel.objects.filter(d_id=id, subcategory=subcategory)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def d_original_get_products(request,id):
    if request.method == "GET":
        data= models.d_original_productsmodel.objects.filter(d_id=id)
        alldataserializer= business_serializers.d_original_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
 

@api_view(['GET'])
def d_original_get_district_products(request, id, district):
    if request.method == "GET":
        data = models.d_original_productsmodel.objects.filter(d_id=id, district=district)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def d_original_get_my_product(request,id,product_id):

    if request.method == "GET":
        # Filter products based on d_id and category
        data = models.d_original_productsmodel.objects.filter(d_id=id, product_id=product_id)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def d_original_delete_product(request,id,product_id):
    d_original_product = get_object_or_404(models.d_original_productsmodel, d_id=id, product_id=product_id)
    d_original_product.delete()
    return Response(id,status=status.HTTP_200_OK)

@api_view(['POST'])
def d_original_update_product(request,id,product_id):

    d_original_products = dict(request.POST)

    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/d_original_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        d_original_products['primary_image'] = primary_image_paths
    except:
        # d_original_pro=collection.find_one({"d_id": id,"product_id":product_id})
        # primary_image_paths=d_original_pro.get("primary_image")
        # d_original_products['primary_image'] = primary_image_paths
        pass
        
    
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/d_original_products/{id}/other_images/"+str(sav).replace(" ", "_"), sav)
            other_image.append(str(ot).replace(" ","_"))
                
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
        d_original_products['other_images'] = other_imagelist

    except:
        pass
    try:
        d_original_product_instance = models.d_original_productsmodel.objects.get(d_id=id, product_id=product_id)
        
        existing_product_data = d_original_product_instance.product
        
        # Updating product field with new data
   
        d_original_products["other_images"] = d_original_product_instance.product['other_images']
        cleaned_data_dict = {key: value[0] if isinstance(value, list) and len(value) == 1 else value for key, value in
                            d_original_products.items()}

        # existing_product_data.update(cleaned_data_dict)
        # Saving changes to the SQLite table
        with transaction.atomic():
            # Updating only the product field
            d_original_product_instance.product = cleaned_data_dict
            d_original_product_instance.category = request.data['category']
            d_original_product_instance.subcategory = request.data['subcategory']
            d_original_product_instance.save()
        
        return Response(id, status=status.HTTP_200_OK)
    except models.d_original_productsmodel.DoesNotExist:
        return Response({"error": "d_original product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def d_original_imgupdate_product(request, id, product_id,index_value):
    try:
        if request.method == "POST":
            fs = FileSystemStorage()
            data = models.d_original_productsmodel.objects.get(d_id=id, product_id=product_id)
            d_original_pro=data.product.get("other_images")
            product_img=data.product
            print(d_original_pro)
            index_value = int(index_value)
            if index_value < 0 or index_value >= len(d_original_pro):
                return Response({"error": "Invalid index value"}, status=status.HTTP_400_BAD_REQUEST)
            if index_value == int(index_value):
                other_images = str(request.FILES['other_images']).replace(" ", "_")
                other_images_path = fs.save(f"api/d_original_products/{id}/other_images/" + other_images,
                                            request.FILES['other_images'])
                other_images_paths = all_image_url + fs.url(other_images_path)
                print(other_images_paths)
                d_original_pro[index_value] = other_images_paths
                product_img["other_images"] =d_original_pro
                data.product=product_img  #replacejson
                data.save()

            return Response({"message": "Image Updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Index value mismatch"}, status=status.HTTP_400_BAD_REQUEST)
            
    except models.d_original_productsmodel.DoesNotExist:
        return Response({"error": "Shop product not found"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST","GET"])
def d_original_productorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.Product_Ordermodel.objects.filter(Q(d_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data)
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
        
        if pro_data:
            
            alldata = []
            for product_id in pro_data:
                proget = models.d_original_productsmodel.objects.filter(product_id=product_id)
                alldata.extend(proget)
            
            serializer = business_serializers.delivered_productlistserializer(alldata, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
          

        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dorigin_district_products_only(request,district):
    if request.method == "GET":
        data = models.d_original_productsmodel.objects.filter(district=district)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_normalproduct_order(request, id):
    if models.shoppingmodel.objects.filter(shop_id=id).exists():
        shopp = models.shoppingmodel.objects.get(shop_id=id)
        orders = models.Product_Ordermodel.objects.filter(shop_id__shop_id=shopp.shop_id, delivery_type='Normal')
    elif models.jewellerymodel.objects.filter(jewel_id=id).exists():
        jewel = models.jewellerymodel.objects.get(jewel_id=id)
        orders = models.Product_Ordermodel.objects.filter(jewel_id__jewel_id=jewel.jewel_id, delivery_type='Normal')
    elif models.d_originalmodel.objects.filter(d_id=id).exists():
        dorigin = models.d_originalmodel.objects.get(d_id=id)
        orders = models.Product_Ordermodel.objects.filter(d_id__d_id=dorigin.d_id, delivery_type='Normal')
    
    order_data = []  # Define order_data list outside of the if-else blocks
    if orders:
        for order in orders:
            if order.shop_product: 
                order_data.append(order)
            elif order.jewel_product: 
                order_data.append(order)
            elif order.d_original_product: 
                order_data.append(order)
            else:
                return Response("Unknown product type for order", status=status.HTTP_204_NO_CONTENT)

        # Serialize the order data
        serializer = end_user_serializers.product_orderlistSerializer(order_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("No orders found", status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def get_quickproduct_order(request, id):
    orders = None  
    if models.pharmacy_model.objects.filter(pharm_id=id).exists():
        pharm = models.pharmacy_model.objects.get(phram_id=id)
        orders = models.Product_Ordermodel.objects.filter(pharm_id__pharm_id=pharm.pharm_id, delivery_type='Quick')
    elif models.dailymio_model.objects.filter(dmio_id=id).exists():
        dmio = models.dailymio_model.objects.get(dmio_id=id)
        orders = models.Product_Ordermodel.objects.filter(dmio_id__dmio_id=dmio.dmio_id, delivery_type='Quick')
    elif models.foodmodel.objects.filter(food_id=id).exists():
        food = models.foodmodel.objects.get(food_id=id)
        orders = models.Product_Ordermodel.objects.filter(food_id__food_id=food.food_id, delivery_type='Quick')
    elif models.freshcutsmodel.objects.filter(fresh_id=id).exists():
        fresh = models.freshcutsmodel.objects.get(fresh_id=id)
        orders = models.Product_Ordermodel.objects.filter(fresh_id__fresh_id=fresh.fresh_id, delivery_type='Quick')
    
    order_data = []  # Define order_data list outside of the if-else blocks
    if orders:
        for order in orders:
            if order.food_product: 
                order_data.append(order)
            elif order.freshcut_product: 
                order_data.append(order)
            elif order.pharmacy_product: 
                order_data.append(order)
            elif order.dmio_product: 
                order_data.append(order)
            else:
                return Response("Unknown product type for order", status=status.HTTP_204_NO_CONTENT)
        serializer = end_user_serializers.product_orderlistSerializer(order_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("No orders found", status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def businessnotify_status_true(request,id):
    try:
        user=get_object_or_404(models.Businessmodel,uid=id)
        user.notification_status=True
        user.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def business_notify_status_false(request,id):
    try:
        user=get_object_or_404(models.Businessmodel,uid=id)
        user.notification_status=False
        user.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)
    



@api_view(["GET"])
def dashboardproduct_count(request,id):
    try:
        if models.shoppingmodel.objects.filter(shop_id=id).exists():
            id=models.shoppingmodel.objects.get(shop_id=id)
            data=models.shop_productsmodel.objects.all()
        elif models.jewellerymodel.objects.filter(jewel_id=id).exists():
            id=models.jewellerymodel.objects.get(jewel_id=id)
            data=models.jewel_productsmodel.objects.all()
        elif models.foodmodel.objects.filter(food_id=id).exists():
            id=models.foodmodel.objects.get(food_id=id)
            data=models.food_productsmodel.objects.all()
        elif models.freshcutsmodel.objects.filter(fresh_id=id).exists():
            id=models.freshcutsmodel.objects.get(fresh_id=id)
            data=models.fresh_productsmodel.objects.all()
        elif models.dailymio_model.objects.filter(dmio_id=id).exists():
            id=models.dailymio_model.objects.get(dmio_id=id)
            data=models.dmio_productsmodel.objects.all()
        elif models.pharmacy_model.objects.filter(pharm_id=id).exists():
            id=models.pharmacy_model.objects.get(pharm_id=id)
            data=models.pharmacy_productsmodel.objects.all()
        elif models.d_originalmodel.objects.filter(d_id=id).exists():
            id=models.d_originalmodel.objects.get(d_id=id)
            data=models.d_original_productsmodel.objects.all()
        print(data.count())
        return Response({"product":data.count()},status=status.HTTP_200_OK)
    except:
        return Response({"product":0},status=status.HTTP_200_OK)



# Getting Notification List for all users 
   
@api_view(['GET'])
def get_notification_data(request,id):
    if request.method == 'GET':
       allDataa = models.Notification.objects.filter(sender_id=id).order_by('-notify_date')
       alldataserializer = business_serializers.notificationlistSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def single_notify_delete(request,id):
    try:
        delete_data = models.Notification.objects.filter(notify_id =id)
        print(delete_data)
        if delete_data:
            delete_data.delete()
            return Response("Deleted", status=status.HTTP_200_OK)
        else:
            return Response({"Data not found"}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])  
def business_delete_all_notification(request,id):
    try:
        delete_all=models.Notification.objects.filter(sender_id = id)
        print(delete_all)
        if delete_all:
            delete_all.delete()
            return Response({'All Deleted'},status=status.HTTP_200_OK)
        else:
            return Response({'no data'},status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'server prblm'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(["GET"])
def accepted_ordered_list(request, food_id):

    data = models.Product_Ordermodel.objects.filter(food_id_id__food_id=food_id, status="accepted")
    enduser = []

    for order_data in data:
        order_dict = serializers.serialize('python', [order_data])[0]['fields']
        enduser.append(order_dict)
     
    print(enduser)
    return JsonResponse(enduser, safe=False, status=status.HTTP_200_OK)




@api_view(["GET"])
def business_food_order(request,seller_id,category):
    try:
        if "food" == category:
            order_data = models.Product_Ordermodel.objects.filter(food_id__food_id = seller_id,category_data = "food",status = "accepted")
            print(order_data)
            my_user=[]
            for get_end_user in order_data:
                if get_end_user.end_user.uid not in my_user:
                    my_user.append(get_end_user.end_user.uid)
            print(my_user)
            separate_list_all_data = []
            for separate_list in my_user:
                enduser = models.End_Usermodel.objects.filter(uid = separate_list).values()[0]
                add_order_data = models.Product_Ordermodel.objects.filter(food_id__food_id = seller_id,category_data = "food",status = "accepted",end_user__uid = separate_list)
                enduser['food_status'] = []
                for y in add_order_data.values():
                    print(y['food_product_id'])
                    food_product = models.food_productsmodel.objects.filter(id = y['food_product_id']).values()
                    y['product'] = food_product[0]
                    print(y)
                    enduser['food_status'].append(y)
                separate_list_all_data.append(enduser)
        elif "daily_mio" == category:
            order_data = models.Product_Ordermodel.objects.filter(dmio_id__dmio_id = seller_id,category_data = "daily_mio",status = "accepted")
            print(order_data)
            my_user=[]
            for get_end_user in order_data:
                if get_end_user.end_user.uid not in my_user:
                    my_user.append(get_end_user.end_user.uid)
            print(my_user)
            separate_list_all_data = []
            for separate_list in my_user:
                enduser = models.End_Usermodel.objects.filter(uid = separate_list).values()[0]
                add_order_data = models.Product_Ordermodel.objects.filter(dmio_id__dmio_id = seller_id,category_data = "daily_mio",status = "accepted",end_user__uid = separate_list)
                enduser['food_status'] = []
                for y in add_order_data.values():
                    print(y['food_product_id'])
                    food_product = models.food_productsmodel.objects.filter(id = y['food_product_id']).values()
                    y['product'] = food_product[0]
                    print(y)
                    enduser['food_status'].append(y)
                separate_list_all_data.append(enduser)
        elif "pharmacy" == category:
            order_data = models.Product_Ordermodel.objects.filter(pharm_id__pharm_id = seller_id,category_data = "pharmacy",status = "accepted")
            print(order_data)
            my_user=[]
            for get_end_user in order_data:
                if get_end_user.end_user.uid not in my_user:
                    my_user.append(get_end_user.end_user.uid)
            print(my_user)
            separate_list_all_data = []
            for separate_list in my_user:
                enduser = models.End_Usermodel.objects.filter(uid = separate_list).values()[0]
                add_order_data = models.Product_Ordermodel.objects.filter(pharm_id__pharm_id = seller_id,category_data = "pharmacy",status = "accepted",end_user__uid = separate_list)
                enduser['food_status'] = []
                for y in add_order_data.values():
                    print(y['food_product_id'])
                    food_product = models.food_productsmodel.objects.filter(id = y['food_product_id']).values()
                    y['product'] = food_product[0]
                    print(y)
                    enduser['food_status'].append(y)
                separate_list_all_data.append(enduser)
        elif "fresh_cuts" == category:
            order_data = models.Product_Ordermodel.objects.filter(fresh_id__fresh_id = seller_id,category_data = "fresh_cuts",status = "accepted")
            print(order_data)
            my_user=[]
            for get_end_user in order_data:
                if get_end_user.end_user.uid not in my_user:
                    my_user.append(get_end_user.end_user.uid)
            print(my_user)
            separate_list_all_data = []
            for separate_list in my_user:
                enduser = models.End_Usermodel.objects.filter(uid = separate_list).values()[0]
                add_order_data = models.Product_Ordermodel.objects.filter(fresh_id__fresh_id = seller_id,category_data = "fresh_cuts",status = "accepted",end_user__uid = separate_list)
                enduser['food_status'] = []
                for y in add_order_data.values():
                    print(y['food_product_id'])
                    food_product = models.food_productsmodel.objects.filter(id = y['food_product_id']).values()
                    y['product'] = food_product[0]
                    print(y)
                    enduser['food_status'].append(y)
                separate_list_all_data.append(enduser)
        return Response(separate_list_all_data,status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def business_order_history(request,seller_id,category):
    try:
        if "food" == category:
            order_data = models.Product_Ordermodel.objects.filter(food_id__food_id = seller_id,category_data = "food",status = "delivered",payment_status = "payment_settled")
            print(order_data)
            my_user=[]
            for get_end_user in order_data:
                if get_end_user.end_user.uid not in my_user:
                    my_user.append(get_end_user.end_user.uid)
            print(my_user)
            separate_list_all_data = []
            for separate_list in my_user:
                enduser = models.End_Usermodel.objects.filter(uid = separate_list).values()[0]
                add_order_data = models.Product_Ordermodel.objects.filter(food_id__food_id = seller_id,category_data = "food",status = "delivered",payment_status = "payment_settled",end_user__uid = separate_list)
                enduser['food_status'] = []
                for y in add_order_data.values():
                    print(y['food_product_id'])
                    food_product = models.food_productsmodel.objects.filter(id = y['food_product_id']).values()
                    y['product'] = food_product[0]
                    print(y)
                    enduser['food_status'].append(y)
                separate_list_all_data.append(enduser)
        elif "daily_mio" == category:
            order_data = models.Product_Ordermodel.objects.filter(dmio_id__dmio_id = seller_id,category_data = "daily_mio",status = "delivered",payment_status = "payment_settled")
            print(order_data)
            my_user=[]
            for get_end_user in order_data:
                if get_end_user.end_user.uid not in my_user:
                    my_user.append(get_end_user.end_user.uid)
            print(my_user)
            separate_list_all_data = []
            for separate_list in my_user:
                enduser = models.End_Usermodel.objects.filter(uid = separate_list).values()[0]
                add_order_data = models.Product_Ordermodel.objects.filter(dmio_id__dmio_id = seller_id,category_data = "daily_mio",status = "delivered",payment_status = "payment_settled",end_user__uid = separate_list)
                enduser['food_status'] = []
                for y in add_order_data.values():
                    print(y['food_product_id'])
                    food_product = models.food_productsmodel.objects.filter(id = y['food_product_id']).values()
                    y['product'] = food_product[0]
                    print(y)
                    enduser['food_status'].append(y)
                separate_list_all_data.append(enduser)
        elif "pharmacy" == category:
            order_data = models.Product_Ordermodel.objects.filter(pharm_id__pharm_id = seller_id,category_data = "pharmacy",status = "delivered",payment_status = "payment_settled")
            print(order_data)
            my_user=[]
            for get_end_user in order_data:
                if get_end_user.end_user.uid not in my_user:
                    my_user.append(get_end_user.end_user.uid)
            print(my_user)
            separate_list_all_data = []
            for separate_list in my_user:
                enduser = models.End_Usermodel.objects.filter(uid = separate_list).values()[0]
                add_order_data = models.Product_Ordermodel.objects.filter(pharm_id__pharm_id = seller_id,category_data = "pharmacy",status = "delivered",payment_status = "payment_settled",end_user__uid = separate_list)
                enduser['food_status'] = []
                for y in add_order_data.values():
                    print(y['food_product_id'])
                    food_product = models.food_productsmodel.objects.filter(id = y['food_product_id']).values()
                    y['product'] = food_product[0]
                    print(y)
                    enduser['food_status'].append(y)
                separate_list_all_data.append(enduser)
        elif "fresh_cuts" == category:
            order_data = models.Product_Ordermodel.objects.filter(fresh_id__fresh_id = seller_id,category_data = "fresh_cuts",status = "delivered",payment_status = "payment_settled")
            print(order_data)
            my_user=[]
            for get_end_user in order_data:
                if get_end_user.end_user.uid not in my_user:
                    my_user.append(get_end_user.end_user.uid)
            print(my_user)
            separate_list_all_data = []
            for separate_list in my_user:
                enduser = models.End_Usermodel.objects.filter(uid = separate_list).values()[0]
                add_order_data = models.Product_Ordermodel.objects.filter(fresh_id__fresh_id = seller_id,category_data = "fresh_cuts",status = "delivered",payment_status = "payment_settled",end_user__uid = separate_list)
                enduser['food_status'] = []
                for y in add_order_data.values():
                    print(y['food_product_id'])
                    food_product = models.food_productsmodel.objects.filter(id = y['food_product_id']).values()
                    y['product'] = food_product[0]
                    print(y)
                    enduser['food_status'].append(y)
                separate_list_all_data.append(enduser)
        return Response(separate_list_all_data,status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)