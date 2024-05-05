from django.shortcuts import render,get_object_or_404
from api import business_serializers,end_user_serializers,delivery_serializers
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework import status,generics
from django.core.files.storage import FileSystemStorage
from api import delivery_extension
from rest_framework.decorators import api_view
from api import models
from mio_admin.models import comission_Editing,zone,admin_to_business_payment
import json
import datetime
from django.http import HttpRequest
from django.http import JsonResponse
from datetime import date
from bson.json_util import dumps,loads
from pymongo import MongoClient
from geopy.distance import geodesic
import requests
import random
from django.utils.timezone import now
from django.db.models import Q
from django.db.models import Sum
from django.db.models import Sum, F
client = MongoClient('localhost', 27017)
all_image_url = "http://127.0.0.1:3000/"

def send_notification(message_title , message_desc):
    fcm_api = "AAAAbIibZeo:APA91bEHlJFNQjqRjMjX2N-YfgDAjOU_fXdt8HkQiQYhOYbGcv9B6MqGykeaG7zQVdrMOEQrOGckrUwKbl4XWdEOboEY9uDUSALHdzbpdW-DJbUxlVzCG_ayQJIPJfAnEPcCeKX86sqg"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api
    }    
    ex_registration_ids=[]
    delivery = models.deliverylogintable_model.objects.filter(status=True,delivery_type= "Quick")
    for i in delivery:
        ex_registration_ids.append((i.deliveryperson.device_id))

    print(ex_registration_ids)
    for x in ex_registration_ids:

        payload = {
            "registration_ids" :x,
            "priority" : "high",
            "notification" : {
                "body" : message_desc,
                "title" : message_title,
                "image" : "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
                "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",
                
            }
        }

        result = requests.post(url,  data=json.dumps(payload), headers=headers )
        print(result.status_code)
        print(result.json())


# send_notification('hi' , 'hello world')

@api_view(['POST'])
def delivery_person_signup(request,id):
    try:
        if delivery_extension.validate_email(request.data.get('email')):
            return Response("User Already Exists", status=status.HTTP_302_FOUND)
        else:
            if request.method == "POST":
                userdata=models.Delivery_model.objects.get(uid=id)
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
                datas = {
                        # 'uid': delivery_extension.id_generate(),
                        'name':request.data["name"],
                        # 'phone_number': request.data['phone_number'],
                        'wp_number': request.data['wp_number'],
                        'email': request.data["email"],
                        'aadhar_number':request.data['aadhar_number'],                    
                        'driving_licensenum':request.data['driving_licensenum'],
                        'pan_number':request.data['pan_number'],                    
                        'profile_picture':profile_picturepaths,
                        'bank_name':request.data['bank_name'],
                        'acc_number':request.data['acc_number'],
                        'name_asper_passbook':request.data['name_asper_passbook'],
                        'ifsc_code':request.data['ifsc_code'],
                        'bank_passbok_pic':bank_passbok_pic_paths,
                        'aadhar_pic':aadhar_pic_paths,
                        'pan_pic':pan_pic_paths,
                        'drlicence_pic':drlicence_pic_paths,
                        'delivery_type':request.data['delivery_type'],
                        'region':request.data['region'],
                        'approve_status':"False",
                        'device_id':request.POST['device_id'],
                }

                
                dataserializer = delivery_serializers.SignupSerializer(instance=userdata, data=datas, partial=True)
                if dataserializer.is_valid():
                    dataserializer.save()
                    print("valid_data")
                    return Response(id, status=status.HTTP_200_OK)
                else:
                    return Response(dataserializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)

    except KeyError as e:
        return Response({"Invalid Key": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(["POST"])
def delivery_send_otp(request):
    
    url = "https://www.fast2sms.com/dev/bulkV2"
    global logindata
    # global uidd
    # Generate a random 4-digit OTP
 
    otp = ''.join(random.choices('0123456789', k=4))
    try:
        existing_delivery = models.Delivery_model.objects.get(phone_number=request.POST['phone_number'])
        uid = existing_delivery.uid
    except models.Delivery_model.DoesNotExist:
        uid = delivery_extension.id_generate()
    # Replace the placeholder in the payload with the generated OTP and phone number
    payload = f"variables_values={otp}&route=otp&numbers={request.POST['phone_number']}&uid={uid}"

    headers = {
        'authorization': "ngpY1A5PqHfF0IE7SzsceVhBM6OmtjQxbRr9KCiwL2aGJoD8vkALKMNP8Sfp6Tk3Csouw427rDFga0Ox",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    logindata = {
            'otp': otp,
            'phone_number':request.POST["phone_number"],
            'uid':uid,
    }
    print(logindata)
    print(response.text)
        # Service Route Success Response:
    {
        "return": True,
        "request_id": "lwdtp7cjyqxvfe9",
        "message": [
            "Message sent successfully"
        ]
    }
    
    return Response({"otp": otp,"uid":uid}, status=status.HTTP_200_OK)


@api_view(["POST"])
def delivery_verify_otp(request):
    try:
        otp = request.data.get('user_otp')
        existing_delivery = models.Delivery_model.objects.filter(phone_number=logindata['phone_number']).first()

        if existing_delivery:
            return Response({"Phone number already exists"}, status=status.HTTP_409_CONFLICT)
        if int(logindata['otp']) == int(otp):
            try:
                user = models.Delivery_model.objects.create(**logindata)
                user.save()
                return Response(logindata['uid'], status=status.HTTP_200_OK)
            except Exception as e:
                print(f"Error creating Delivery_model instance: {e}")
                return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Wrong OTP"}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        print(f"Error: {e}")
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def delivery_signin_otp(request,id):
    try:
        otp=request.POST.get('user_otp')
        user = models.Delivery_model.objects.get(uid=id)
        print(otp,user)
        if int(logindata['otp']) == int(otp):
            models.Delivery_model.objects.filter(uid=id).update(otp=otp)
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"otp incorrect"}, status=status.HTTP_200_OK)
        
    except models.Delivery_model.DoesNotExist:
        return Response({"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def all_delivery_person_data(request):
    if request.method == "GET":
        data=models.Delivery_model.objects.all()
        serializers=delivery_serializers.DeliverypersonSerializer(data,many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)



# one person data    
@api_view(["GET"])
def single_delivery_person_data(request,id):
    if request.method == "GET":
        data=models.Delivery_model.objects.get(uid=id)
        print(data)
        serializers=delivery_serializers.DeliverypersonSerializer(data,many=False)
        print(serializers)
        return Response(data=serializers.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def delivery_person_update(request,id):
    if request.method=="POST":
        fs=FileSystemStorage
        # print(request.data)
        # print(request.FILES)
        d_data = models.Delivery_model.objects.get(uid=id)
        print(d_data)
        datas = models.Delivery_model.objects.filter(uid=id).values()[0]
        print(datas)

        if "profile_picture" in request.FILES:
            profile_picture = str(request.FILES['profile_picture']).replace(" ","_")
            profile_picture_path = fs.save(f"api/delivery/{id}/profile_picture/"+profile_picture, request.FILES["profile_picture"])
            profile_picturepaths = all_image_url+fs.url(profile_picture_path)
        else:
            profile_picturepaths = datas["profile_picture"]
            print(profile_picturepaths) 
        if "bank_passbok_pic" in request.FILES:
            bank_passbok_pic = str(request.FILES["pan_file"]).replace(" ","_")
            bank_passbok_pic_path = fs.save(f"api/delivery/{id}/bank_passbok_pic/"+bank_passbok_pic,request.FILES["bank_passbok_pic"])
            bank_passbok_pic_paths = all_image_url+fs.url(bank_passbok_pic_path)
        else:
            bank_passbok_pic_paths = datas["bank_passbok_pic"]
            print(bank_passbok_pic_paths)
        if "aadhar_pic" in request.FILES:
            aadhar_pic = str(request.FILES["aadhar_pic"]).replace(" ","_")
            aadhar_pic_path = fs.save(f"api/delivery/{id}/aadhar_pic/"+aadhar_pic,request.FILES["aadhar_pic"])
            aadhar_pic_paths = all_image_url+fs.url(aadhar_pic_path)
        else:
            aadhar_pic_paths = datas["aadhar_pic"]
            print(aadhar_pic_paths)
        if "pan_pic" in request.FILES:
            pan_pic = str(request.FILES["pan_pic"]).replace(" ","_")
            pan_pic_path = fs.save(f"api/delivery/{id}/pan_pic/"+pan_pic,request.FILES["pan_pic"])
            pan_pic_paths = all_image_url+fs.url(pan_pic_path)
        else:
            pan_pic_paths = datas["pan_pic"]
            print(pan_pic_paths)
        if "drlicence_pic" in request.FILES:
            drlicence_pic = str(request.FILES["drlicence_pic"]).replace(" ","_")
            drlicence_pic_path = fs.save(f"api/delivery/{id}/drlicence_pic/"+drlicence_pic,request.FILES["drlicence_pic"])
            drlicence_pic_paths = all_image_url+fs.url(drlicence_pic_path)
        else:
            drlicence_pic_paths = datas["drlicence_pic"]
            print(drlicence_pic_paths)
        print(request.data)
        data= {
            'name':request.data['name'],
            'phone_number':request.data['phone_number'],
            'wp_number': request.data['wp_number'],
            'email': request.data["email"],
            'aadhar_number':request.data['aadhar_number'],                    
            'driving_licensenum':request.data['driving_licensenum'],
            'pan_number':request.data['pan_number'],                    
            'profile_picture':profile_picturepaths,
            'bank_name':request.data['bank_name'],
            'acc_number':request.data['acc_number'],
            'name_asper_passbook':request.data['name_asper_passbook'],
            'ifsc_code':request.data['ifsc_code'],
            'bank_passbok_pic':bank_passbok_pic_paths,
            'aadhar_pic':aadhar_pic_paths,
            'pan_pic':pan_pic_paths,
            'drlicence_pic':drlicence_pic_paths,
            'delivery_type':request.data['delivery_type'],
            'region':request.data['region']
        }
        print(data,"data")
        dataserializer = delivery_serializers.deliveryperson_edit_serializer(instance=d_data, data=data, partial=True)
        print(dataserializer)
        if dataserializer.is_valid():
            dataserializer.save()
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def delivery_yourissue(request,id):
    try:
       
        userdata = models.Delivery_model.objects.get(uid=id)

        print(request.POST)
        fs = FileSystemStorage()
        upload_issues = str(request.FILES['upload_issues']).replace(" ", "_")
    
        path = fs.save(f"api/delivery/{id}/upload_issues/"+upload_issues, request.FILES['upload_issues'])
        uploadfull_path = all_image_url+fs.url(path)
        print(uploadfull_path)
        data={
            'submit_issues' : request.data["submit_issues"],
            'upload_issues' : uploadfull_path,
            }
        
       
        addressSerializer = delivery_serializers.delivery_yourissue_serializer(instance=userdata, data=data, partial=True)
        if addressSerializer.is_valid():
            addressSerializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(["POST"])
def delivery_login_table(request, id):
    try:
        delivery = models.Delivery_model.objects.get(uid=id)
        
        if request.data.get('action') == 'login':
            login_entry = models.deliverylogintable_model.objects.create(
                deliveryperson=delivery,
                status=True,
                delivery_type=delivery.delivery_type,
                region=delivery.region

            )
            login_entry.save() 
            if request.data['device_id'] not in delivery.device_id:
                print("new")
                print(type(delivery.device_id))
                print(type(request.data['device_id']))
                delivery.device_id.append(request.data['device_id'])
                delivery.save()
            return Response("Login successful", status=status.HTTP_200_OK)
        
        elif request.data.get('action') == 'logout':
           
            try:
                last_login_entry = models.deliverylogintable_model.objects.filter(deliveryperson=delivery).latest('today_date')
            except models.deliverylogintable_model.DoesNotExist:
                return Response("No login entry found for this delivery person", status=status.HTTP_404_NOT_FOUND)
            last_login_entry.logout_time = datetime.datetime.now().time()
            last_login_entry.status = False  # Assuming status False represents logout
            last_login_entry.save()
            return Response("Logout successful", status=status.HTTP_200_OK)
        
        else:
            return Response("Invalid action specified", status=status.HTTP_400_BAD_REQUEST)
    
    except models.Delivery_model.DoesNotExist:
        return Response("Delivery person not found", status=status.HTTP_404_NOT_FOUND)





@api_view(["POST"])
def delivery_product_order_status_accept(request,id,product_id,order_id):
    try:
        delivery = models.Delivery_model.objects.get(uid=id)
        print(delivery)
        product_orders = models.Product_Ordermodel.objects.filter(product_id=product_id,order_id=order_id)
        print(product_orders)
        if product_orders.exists():
            for product_order in product_orders:
                # Update the status field with the new value
                product_order.status = "order_confirmed"
                product_order.deliveryperson = delivery

                product_order.save()

            return Response({"order_id":order_id,"distance":product_order.distance,"order_total":product_order.order_total}, status=status.HTTP_200_OK)
        else:
            return Response("Product order not found", status=status.HTTP_404_NOT_FOUND)
    except:
        return Response("Product order not found", status=status.HTTP_404_NOT_FOUND)

 

@api_view(["POST"])
def product_status_delivered(request,id,order_id):
    try:
        user=models.Delivery_model.objects.get(uid=id)
        print(user)
        pro=get_object_or_404(models.Product_Ordermodel,order_id=order_id)
        print(pro)
        pro.status="delivered"
        pro.save()
        payable_amount_of_seller = models.Product_Ordermodel.objects.get(order_id=order_id)
        print(payable_amount_of_seller.shop_id.shop_id)
        if payable_amount_of_seller.shop_id is not None:
            seller_id = payable_amount_of_seller.shop_id.shop_id
        elif payable_amount_of_seller.food_id is not None:
            pass
        
        #add payment
        if admin_to_business_payment.objects.filter(seller = seller_id).exists() == True:
            #add
            print("Add")
            seller_payable_data = admin_to_business_payment.objects.get(seller = seller_id)
            balance_amount = seller_payable_data.balance_amount
            
            balance_amount += float(payable_amount_of_seller.total_amount) - (float(payable_amount_of_seller.total_amount) / int(payable_amount_of_seller.admin_commission_amount))
            print(balance_amount)
            if type(balance_amount) is float:
                # Convert the decimal number to a string
                decimal_string = str(balance_amount)

                # Find the index of the decimal point
                decimal_point_index = decimal_string.index('.')

                # Get the decimal value with the last two digits
                decimal_last_two_digits = decimal_string[:decimal_point_index + 3]
            else:
                decimal_last_two_digits = balance_amount
            print(decimal_last_two_digits)
            seller_payable_data.balance_amount = decimal_last_two_digits
            seller_payable_data.save()
        else:
            #create
            balance_amount = float(payable_amount_of_seller.total_amount) - (float(payable_amount_of_seller.total_amount) / int(payable_amount_of_seller.admin_commission_amount))
            seller_payable_data = admin_to_business_payment.objects.create(
                balance_amount = balance_amount,
                seller = seller_id,
                order = payable_amount_of_seller,
            )
            seller_payable_data.save()
                    
# send_notification('hii' , 'order_delivered')
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def product_status(request,id,order_id,orderstatus):
    try:
        user=models.Delivery_model.objects.get(uid=id)
        print(user)
        pro=get_object_or_404(models.Product_Ordermodel,order_id=order_id)
        print(pro)

        distance=pro.distance
        pro.status=orderstatus

        pro.save()
        return Response({"status updated succesfully"},status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delivery_product_order_status_reject(request,id,product_id,order_id):
    try:
        delivery = models.Delivery_model.objects.get(uid=id)
        print(delivery)
        product_orders = models.Product_Ordermodel.objects.filter(product_id=product_id, order_id=order_id)
        print(product_orders)
        if product_orders.exists():
            for product_order in product_orders:
                # Update the status field with the new value
                product_order.status = "rejected"
                product_order.deliveryperson = delivery
                product_order.reason =request.POST["reason"]
                product_order.reason_optional= request.POST["reason_optional"]
                product_order.save()
            return Response(id,status=status.HTTP_200_OK)
        else:
            return Response("Product order not found", status=status.HTTP_404_NOT_FOUND)
    except:
        return Response("Product order not found", status=status.HTTP_404_NOT_FOUND)



# emergency
 

@api_view(["POST"])
def delivery_produt_emergency(request,id,order_id):
    try:
        delivery = models.Delivery_model.objects.get(uid=id)
        print(delivery)
        product_orders = models.Product_Ordermodel.objects.filter(order_id=order_id)
        print(product_orders)
        if product_orders.exists():
            for product_order in product_orders:
                # Update the status field with the new value
               
                product_order.deliveryperson = delivery
                product_order.emergency =request.POST["emergency"]
                product_order.emergency_optional= request.POST['emergency_optional']
                product_order.save()
            return Response(id,status=status.HTTP_200_OK)
        else:
            return Response("Product order not found", status=status.HTTP_404_NOT_FOUND)
    except:
        return Response("Product order not found", status=status.HTTP_404_NOT_FOUND)






@api_view(["GET"])
def delivery_get_product_order(request,id,region):
    if request.method =="GET":
        if models.deliverylogintable_model.objects.filter(deliveryperson__uid =id,status="1",delivery_type="Quick",region=region).exists():
            data=models.deliverylogintable_model.objects.filter(deliveryperson__uid =id,status="1",delivery_type="Quick",region=region)
            print(data)
            qs=models.Product_Ordermodel.objects.filter(status="accepted",delivery_type="Quick",region=region)
            serializers=end_user_serializers.product_orderlistSerializer(qs,many=True)
            return Response(data=serializers.data,status=status.HTTP_200_OK)
        # elif models.deliverylogintable_model.objects.filter(deliveryperson__uid=id,delivery_type="Normal",region=region,status="1").exists():
        #     delivery=models.deliverylogintable_model.objects.filter(deliveryperson__uid=id,delivery_type="Normal",region=region,status="1")
        #     print(delivery)
        #     qs=models.Product_Ordermodel.objects.filter(status="accepted",delivery_type="Normal",region=region)
        #     print(qs)
        #     serializers=end_user_serializers.product_orderlistSerializer(qs,many=True)
        #     return Response(data=serializers.data,status=status.HTTP_200_OK)
        else:
            return Response({"deliverypersons not available"},status=status.HTTP_400_BAD_REQUEST)




# @api_view(["GET"])
# def delivery_get_Normalproduct_order(request,id,region):
#     if request.method =="GET":
#         delivery=models.deliverylogintable_model.objects.filter(deliveryperson__uid=id,delivery_type="Normal",region=region,status="1")
#         print(delivery)
#         qs=models.Product_Ordermodel.objects.filter(status="accepted",delivery_type="Normal",region=region)
#         print(qs)
#         serializers=end_user_serializers.product_orderlistSerializer(qs,many=True)
#         return Response(data=serializers.data,status=status.HTTP_200_OK)
#     else:
#         return Response({"deliverypersons not available"},status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def todays_order(request,id,delivery_date):
    if models.Product_Ordermodel.objects.filter(deliveryperson__uid=id,delivery_date=delivery_date,delivery_type="Quick").exists():
        data=models.Product_Ordermodel.objects.filter(deliveryperson__uid=id,delivery_date=delivery_date,delivery_type="Quick")
        print(data)
        serializer=end_user_serializers.product_orderlistSerializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    # elif models.Product_Ordermodel.objects.filter(deliveryperson__uid=id,delivery_date=delivery_date,delivery_type="Normal").exists():
    #     data=models.Product_Ordermodel.objects.filter(deliveryperson__uid=id,delivery_date=delivery_date,delivery_type="Normal")
    #     print(data)
    #     serializer=end_user_serializers.product_orderlistSerializer(data,many=True)
    #     return Response(data=serializer.data,status=status.HTTP_200_OK)
    else:
        return Response({"no orders found"},status=status.HTTP_200_OK)

        
@api_view(["POST","GET"])
def delivered_productorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        if models.Product_Ordermodel.objects.filter(Q(deliveryperson__uid=id) & Q(status="delivered")& Q(delivery_type="Normal")).exists():
            data=models.Product_Ordermodel.objects.filter(Q(deliveryperson__uid=id) & Q(status="delivered")& Q(delivery_type="Normal")& Q(delivery_date__range=[from_date, to_date])).values()
            pro_data=[]
            for item in data:
                pro_id = item.get("product_id")
                pro_data.append(pro_id) 
            print(pro_data)
            if pro_data:
                
                alldata = []
                for product_id in pro_data:
                    proget = models.Product_Ordermodel.objects.filter(deliveryperson__uid=id,product_id=product_id,status="delivered",delivery_type="Normal")
                    alldata.extend(proget)
                print(alldata)
                serializer = end_user_serializers.product_orderlistSerializer(alldata, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif models.Product_Ordermodel.objects.filter(Q(deliveryperson__uid=id) & Q(status="delivered")& Q(delivery_type="Quick")).exists():
            data=models.Product_Ordermodel.objects.filter(Q(deliveryperson__uid=id) & Q(status="delivered")& Q(delivery_type="Quick")& Q(delivery_date__range=[from_date, to_date])).values()


            pro_data=[]
            for item in data:
                pro_id = item.get("product_id")
                pro_data.append(pro_id) 
            print(pro_data)
            if pro_data:
                
                alldata = []
                for product_id in pro_data:
                    proget = models.Product_Ordermodel.objects.filter(deliveryperson__uid=id,product_id=product_id,status="delivered",delivery_type="Quick")
                    alldata.extend(proget)
                print(alldata)
                serializer = end_user_serializers.product_orderlistSerializer(alldata, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def todays_incencentiveorder(request,id,delivery_date):
    if models.Product_Ordermodel.objects.filter(deliveryperson__uid=id,delivery_date=delivery_date,delivery_type="Quick").exists():
        data=models.Product_Ordermodel.objects.filter(deliveryperson__uid=id,delivery_date=delivery_date,delivery_type="Quick")
        print(data)
        serializer=end_user_serializers.product_orderlistSerializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    else:
        return Response({"no orders found"},status=status.HTTP_400_BAD_REQUEST)




@api_view(["POST"])
def delivery_payableamount(request, id):
    try:
        delivery_person = models.Delivery_model.objects.get(uid=id)
        print(delivery_person)
        orders = models.Product_Ordermodel.objects.filter(deliveryperson_id__uid=delivery_person.uid, status="delivered")
        print(orders)
        total_amount_today = orders.aggregate(total=Sum('order_total')).get('total', 0)
        print(total_amount_today)

        if total_amount_today is not None:
            if delivery_person.has_withdrawn == 1:
                orders.update(order_total=0)

                delivery_person.total_order_amount = 0
            else:
                orders.exclude(deliveryperson_id=delivery_person.id).update(order_total=F('order_total') + total_amount_today)

                total_order_amount = models.Product_Ordermodel.objects.filter(deliveryperson_id__uid=delivery_person.uid, status="delivered").aggregate(total=Sum('order_total')).get('total', 0)
                delivery_person.total_order_amount = total_order_amount
            delivery_person.save()
        return JsonResponse({'daily_total': delivery_person.total_order_amount}, status=status.HTTP_200_OK)
    except models.Delivery_model.DoesNotExist:
        return Response({"error": "Delivery person not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
def delivery_withdraw_status(request,id):
    if request.method == "POST":
        delivery_person = models.Delivery_model.objects.get(uid=id)
        print(delivery_person)
        orders = models.Product_Ordermodel.objects.filter(deliveryperson_id__uid=delivery_person.uid, status="delivered")
        if orders:
            delivery_person.has_withdrawn = 1
            delivery_person.save()
            return Response(id,status=status.HTTP_200_OK)
        else:
            return Response("amount not found",status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("withdraw not updated",status=status.HTTP_400_BAD_REQUEST)




# notification
@api_view(['POST'])
def delivery_notification(request):
    if request.method == "POST":
        print(request.data)
        data={
            'notify_id':delivery_extension.id_generate(),
            'sender_id': request.data['sender_id'],
            'notify_message': request.data['notify_message'],
            'recever_id':request.data['recever_id'],

        }
        basicdetailsserializer = delivery_serializers.notificationSerializer(data = data)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response('success',status=status.HTTP_200_OK)
        else:
            print("not valid")
            return Response({"serializer prblm"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        


# Getting Notification List for all users    
@api_view(['GET'])
def notification_data(request,id):
    if request.method == 'GET':
       allDataa = models.Notification.objects.filter(recever_id = id).order_by('-notify_date')
       alldataserializer = delivery_serializers.notificationlistSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# delete single notification 
@api_view(["POST"])
def delivery_person_notify_delete(request,id):
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
    
# Delete All Notification
@api_view(['POST'])  
def delete_all_notification(request,id):
    try:
        delete_all=models.Notification.objects.filter(recever_id = id)
        print(delete_all)
        if delete_all:
            delete_all.delete()
            return Response({'All Deleted'},status=status.HTTP_200_OK)
        else:
            return Response({'no data'},status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'server prblm'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# notification Status change
@api_view(["POST"])
def deliverynotify_status_true(request,id):
    try:
        user=get_object_or_404(models.Delivery_model,uid=id)
        user.notification_status=True
        user.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def delivery_notify_status_false(request,id):
    try:
        user=get_object_or_404(models.Delivery_model,uid=id)
        user.notification_status=False
        user.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delivery_floating_status(request,id):
    if request.method == "POST":
        delivery_person = models.Delivery_model.objects.get(uid=id)
        print(delivery_person)
        orders = models.Product_Ordermodel.objects.filter(deliveryperson_id__uid=delivery_person.uid, status="delivered")
        if orders:
            delivery_person.floating_status = 1
            delivery_person.save()
            return Response(id,status=status.HTTP_200_OK)
        else:
            return Response("amount not found",status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("withdraw not updated",status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delivery_floating_cash(request, id):
    try:
        delivery_person = models.Delivery_model.objects.get(uid=id)
        print(delivery_person)
        orders = models.Product_Ordermodel.objects.filter(deliveryperson_id__uid=delivery_person.uid, status="delivered")
        print(orders)
        total_amount_today = orders.aggregate(total=Sum('float_cash')).get('total', 0)
        print(total_amount_today)

        if total_amount_today is not None:
            if delivery_person.floating_status == 1:
                orders.update(float_cash=0)

                delivery_person.float_amount = 0
            else:
                orders.exclude(deliveryperson_id=delivery_person.id).update(float_cash=F('float_cash') + total_amount_today)

                float_amount = models.Product_Ordermodel.objects.filter(deliveryperson_id__uid=delivery_person.uid, status="delivered").aggregate(total=Sum('float_cash')).get('total', 0)
                delivery_person.float_amount = float_amount
            delivery_person.save()
        return JsonResponse({'daily_total': delivery_person.float_amount}, status=status.HTTP_200_OK)
    except models.Delivery_model.DoesNotExist:
        return Response({"error": "Delivery person not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    