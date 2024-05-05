from django.shortcuts import render,get_object_or_404
from api import business_serializers,end_user_serializers
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework import status,generics
from django.core.files.storage import FileSystemStorage
from api import end_user_extension
from rest_framework.decorators import api_view
from api import models
import json
import datetime
from bson.json_util import dumps,loads
from pymongo import MongoClient
import math
from mio_admin.models import business_commision,zone
from django.db import transaction
from django.db.models import Avg
from hub import models

from django.http import JsonResponse
from .models import Reviews

client = MongoClient('localhost', 27017)
all_image_url = "http://127.0.0.1:3000/"
x = datetime.datetime.now()

@api_view(['POST'])
def end_user_signup(request):
    try:
        try:
            if end_user_extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                x = datetime.datetime.now()
                datas = {
                    'uid': end_user_extension.id_generate(),
                    'otp': end_user_extension.otp_generate(),
                    'full_name':request.data["full_name"],
                    'email': request.data["email"],
                    'phone_number': request.data['phone_number'],
                    'password': request.data["password"],
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year),
             
                }
                print(datas)
                dataserializer = end_user_serializers.SignupSerializer(data=datas)
                print(dataserializer)
                
                if dataserializer.is_valid():            
                    dataserializer.save()
                    print("Valid Data")
                    end_user_extension.send_mail(datas['email'], datas['otp'])
                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
def end_user_otp(request, id):
    try:
        try:
            if end_user_extension.validate_otp(id, int(request.data['user_otp'])):
                try:
                    userData = models.End_Usermodel.objects.get(uid=id)
                    print(userData)
                    serializer_validate = end_user_serializers.OTPSerializer(
                        instance=userData, data=request.POST, partial=True)
                    if serializer_validate.is_valid():
                        serializer_validate.save()
                        print("Valid OTP")
                        return Response(id, status=status.HTTP_200_OK)
                    else:
                        return Response({"Cannot Verify OTP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except:
                    return Response({"serializer Issue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"Wrong OTP"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def end_user_signin(request):
    try:
       
        try:
            if end_user_extension.validate_email(request.data['email']):
                if end_user_extension.verify_user(request.data['email'], request.data['password']):
                    if end_user_extension.verify_user_otp(request.data['email']):
                        if end_user_extension.get_user_id(request.data['email']):
                            return Response(end_user_extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
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


@api_view(["GET"])
def all_users_data(request):
    if request.method == "GET":
        data=models.End_Usermodel.objects.all()
        serializers=end_user_serializers.EnduserSerializer(data,many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    


@api_view(['POST'])
def endresend_otp(request,id):

    try:
        try:
            new_otp = end_user_extension.otp_generate()
            user = models.End_Usermodel.objects.get(uid=id)
            email = user.email 
            print(f"Email: {email}")
            end_user_extension.send_mail(email, new_otp)
            user.otp = new_otp
            user.save()
            return Response({"New OTP": new_otp, "Email": email}, status=status.HTTP_200_OK)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def endforget_password(request):

    try:
        try:
            print(request.POST)
            if end_user_extension.validate_email(request.data['email']):
                Data = models.End_Usermodel.objects.get(email=request.data['email'])

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
def end_profile_picture(request,id):
    try:
        print(request.FILES['profile_picture'])
        fs = FileSystemStorage()
        userdata = models.End_Usermodel.objects.get(uid=id)
        
        profile_picture = str(request.FILES['profile_picture']).replace(" ", "_")
     
        path = fs.save(f"api/end_user/{id}/profile_picture/"+profile_picture, request.FILES['profile_picture'])
        full_path = all_image_url+fs.url(path)
        print(full_path)

        data = {          
            'profile_picture': full_path           
        }

        print(data)
        basicdetailsserializer = end_user_serializers.profile_picture_Serializer(
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
def end_user_address(request,id):
    try:
        if request.method == "POST":
            print(request.POST)
            userdata = models.End_Usermodel.objects.get(uid=id)
            data={
                'doorno' : request.data["doorno"],
                'area' : request.data["area"],
                'landmark': request.data["landmark"],
                'place' : request.data["place"],
                'district' : request.data["district"],
                'state' : request.data["state"],
                'pincode' : request.data["pincode"],
            
               }

            addressSerializer = end_user_serializers.AddressSerializer(instance=userdata, data=data, partial=True)
            if addressSerializer.is_valid():
                addressSerializer.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
            else:
                return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_end_user_address(request, id):
    try:
        end_user = models.End_Usermodel.objects.get(uid=id)
        existing_address_data = end_user.address_data
        
        address_index_str = request.POST.get('address_index')
        if address_index_str is None:
            return Response({"error": "Address index is missing"}, status=status.HTTP_400_BAD_REQUEST)

        address_index = int(address_index_str)

        if address_index < 0 or address_index >= len(existing_address_data):
            return Response({"error": "Invalid address index"}, status=status.HTTP_400_BAD_REQUEST)
        new_address_data = {
            "doorno": request.POST.get("doorno"),
            "area": request.POST.get("area"),
            "landmark": request.POST.get("landmark"),
            "place": request.POST.get("place"),
            "district": request.POST.get("district"),
            "state": request.POST.get("state"),
            "pincode": request.POST.get("pincode"),

        }
        print(new_address_data)
        existing_address = existing_address_data[address_index]
        for key, value in new_address_data.items():
            if value is not None:
                existing_address[key] = value  
        # Save the changes to the database
        end_user.address_data = existing_address_data
        end_user.save()
        
        return Response({"message": "Address updated successfully"}, status=status.HTTP_200_OK)

    except models.End_Usermodel.DoesNotExist:
        return Response({"error": "End user not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({"error": "Invalid address index format"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    
@api_view(['POST'])
def enduser_profile_update(request,id):
    
    print(request.FILES)
    fs = FileSystemStorage()
    userdata = models.End_Usermodel.objects.get(uid=id)
    print(userdata)
    datas = models.End_Usermodel.objects.filter(uid=id).values()[0]
    print(datas)
    
    if "profile_picture" in request.FILES:
        profile_picture= str(request.FILES['profile_picture']).replace(" ", "_")
        path = fs.save(f"api/business/{id}/profile_picture/"+profile_picture, request.FILES['profile_picture'])
        full_path = all_image_url+fs.url(path)
        print(full_path)
    else:
        full_path = datas['profile_picture']
    print("valid")

    data = {
        'profile_picture': full_path
        
    }

    # print(data)
    basicdetailsserializer = end_user_serializers.update_acc_serializer(
        instance=userdata, data=data, partial=True)
    if basicdetailsserializer.is_valid():
        basicdetailsserializer.save()
        print("Valid Data")
        return Response(id, status=status.HTTP_200_OK)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def locationupdate(request,id):
    try:
       
        userdata = models.End_Usermodel.objects.get(uid=id)

        print(request.POST)
   
        data={
            'latitude' : request.data["latitude"],
            'longitude' : request.data["longitude"],
            }
        
       
        Serializer = end_user_serializers.locationSerializer(instance=userdata, data=data, partial=True)
        if Serializer.is_valid():
            Serializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def single_users_data(request,id):
    if request.method == "GET":
        data=models.End_Usermodel.objects.filter(uid=id)
        print(data)
        serializers=end_user_serializers.EnduserSerializer(data,many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

# ....................shop products............
#   ......before login--------
@api_view(['GET'])
def all_shopproducts(request): 
    if request.method == "GET":
        data= models.shop_productsmodel.objects.filter(status=True)
        print(data)
        alldataserializer= business_serializers.shop_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def category_based_shop(request,subcategory):
    if request.method == "GET":
        data = models.shop_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.shop_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_single_shopproduct(request,id,product_id):
    if request.method == "GET":
        # user_id= models.End_Usermodel.objects.get(uid=user_id)
        # print(user_id)
        data = models.shop_productsmodel.objects.filter(shop_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.shop_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
# .................after login...............
@api_view(['GET'])
def user_get_all_shopproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.shop_productsmodel.objects.filter(shop_id=id,status=True)
        alldataserializer= business_serializers.shop_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_get_category_shop(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.shop_productsmodel.objects.filter(shop_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.shop_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_shopproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.shop_productsmodel.objects.filter(shop_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.shop_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)



# ................jewellery products.............

@api_view(['GET'])
def all_jewelproducts(request):
    if request.method == "GET":
        data= models.jewel_productsmodel.objects.filter(status=True)
        alldataserializer= business_serializers.jewel_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def category_based_jewel(request,subcategory):
    if request.method == "GET":
        data = models.jewel_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.jewel_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_single_jewelproduct(request,id,product_id):
    if request.method == "GET":
        data = models.jewel_productsmodel.objects.filter(jewel_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.jewel_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
# .................after login...............

@api_view(['GET'])
def user_get_all_jewelproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.jewel_productsmodel.objects.filter(jewel_id=id,status=True)
        alldataserializer= business_serializers.jewel_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_get_category_jewel(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.jewel_productsmodel.objects.filter(jewel_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.jewel_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_jewelproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.jewel_productsmodel.objects.filter(jewel_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.jewel_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)



# ....................food products............
@api_view(['GET'])
def all_foodproducts(request):
    if request.method == "GET":
        data= models.food_productsmodel.objects.filter(status=True)
        alldataserializer= business_serializers.food_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def category_based_food(request,subcategory):
    if request.method == "GET":
        data = models.food_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.food_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_foodproduct(request,id,product_id):
    if request.method == "GET":
        data = models.food_productsmodel.objects.filter(food_id=id,product_id=product_id,status=True)
        alldataserializer = business_serializers.food_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# .................after login...............

def user_get_all_foodproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.food_productsmodel.objects.filter(food_id=id,status=True)
        alldataserializer= business_serializers.food_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_get_category_food(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.food_productsmodel.objects.filter(food_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.food_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_foodproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.food_productsmodel.objects.filter(food_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.food_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


# ....................freshcuts products..........

@api_view(['GET'])
def all_freshcutproducts(request):
    if request.method == "GET":
        data= models.fresh_productsmodel.objects.filter(status=True)
        alldataserializer= business_serializers.fresh_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_based_fresh(request,subcategory):
    if request.method == "GET":
        data = models.fresh_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.fresh_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_single_freshproduct(request,id,product_id):
    if request.method == "GET":
        data = models.fresh_productsmodel.objects.filter(fresh_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.fresh_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
# .................after login...............

@api_view(['GET'])
def user_get_all_freshproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.fresh_productsmodel.objects.filter(fresh_id=id,status=True)
        alldataserializer= business_serializers.fresh_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_get_category_fresh(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.fresh_productsmodel.objects.filter(fresh_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.fresh_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_freshproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.fresh_productsmodel.objects.filter(fresh_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.fresh_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# ....................dailymio products............


@api_view(['GET'])
def all_dmioproducts(request):
    if request.method == "GET":
        data= models.dmio_productsmodel.objects.filter(status=True)
        alldataserializer= business_serializers.dmio_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def category_based_dmio(request,subcategory):
    if request.method == "GET":
 
        data = models.dmio_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.dmio_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_dmioproduct(request,id,product_id):
    if request.method == "GET":
        data = models.dmio_productsmodel.objects.filter(dmio_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.dmio_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
# .................after login..............


@api_view(['GET'])
def user_get_all_dmioproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.dmio_productsmodel.objects.filter(dmio_id=id,status=True)
        alldataserializer= business_serializers.dmio_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_category_dmio(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.dmio_productsmodel.objects.filter(dmio_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.dmio_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_dmioproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.dmio_productsmodel.objects.filter(dmio_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.dmio_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# ....................pharmacy products............
@api_view(['GET'])
def all_pharmproducts(request):
    if request.method == "GET":
        data= models.pharmacy_productsmodel.objects.filter(status=True)
        alldataserializer= business_serializers.pharmacy_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def category_based_pharm(request,subcategory):
    if request.method == "GET":

        data = models.pharmacy_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.pharmacy_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_pharmproduct(request,id,product_id):
    if request.method == "GET":
        data = models.pharmacy_productsmodel.objects.filter(pharm_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.pharmacy_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK) 
# .................after login...............


@api_view(['GET'])
def user_get_all_pharmproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.pharmacy_productsmodel.objects.filter(pharm_id=id,status=True)
        alldataserializer= business_serializers.pharmacy_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_get_category_pharm(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.pharmacy_productsmodel.objects.filter(pharm_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.pharmacy_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_pharmproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.pharmacy_productsmodel.objects.filter(pharm_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.pharmacy_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# ....................dorigin products............


@api_view(['GET'])
def all_d_originalproducts(request):
    if request.method == "GET":

        data= models.d_original_productsmodel.objects.filter(status=True)
        alldataserializer= business_serializers.d_original_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def category_based_d_original(request,subcategory):
    if request.method == "GET":
 
        data = models.d_original_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_d_originalproduct(request,id,product_id):
    if request.method == "GET":
        data = models.d_original_productsmodel.objects.filter(d_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def d_original_district_products(request, id, district):
    if request.method == "GET":
        data = models.d_original_productsmodel.objects.filter(d_id=id, district=district,status=True)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)



    
# .................after login...............


@api_view(['GET'])
def user_get_all_d_originalproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.d_original_productsmodel.objects.filter(d_id=id,status=True)
        alldataserializer= business_serializers.d_original_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_get_category_d_original(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id) 
        print(user_id)
        data = models.d_original_productsmodel.objects.filter(d_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_d_originalproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.d_original_productsmodel.objects.filter(d_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def user_d_original_district_products(request, id,user_id, district):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.d_original_productsmodel.objects.filter(d_id=id, district=district,status=True)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

#  Oreder Creation (Quick And Normal)
@api_view(["POST"])
def enduser_order_create(request,id,product_id,category):
    if request.method == "POST":
        user_data= models.End_Usermodel.objects.get(uid=id)
        
        order_id = end_user_extension.order_id_generate()
        while True:
            if id == order_id:
                order_id = end_user_extension.order_id_generate()
            else:
                break
        # shopping

        if category.lower() == "shopping":
            
            products= models.shop_productsmodel.objects.get(product_id = product_id)
            print(products,"products")
            shopping = models.shoppingmodel.objects.get(shop_id=products.shop_id)
            print(shopping.Business_id)
            business = models.Businessmodel.objects.get(uid=shopping.Business_id) 
            print(business)
            pincode = request.POST['pincode']
            print(pincode)

            data1 = zone.objects.all()
            print(data1)
            get_zone = None  # Initialize get_zone variable
            Zonepincode=None
            for x in data1:
                print(x)
                if x.pincode is not None and pincode in x.pincode:
                    Zonepincode=x.pincode
                    get_zone = x.zone
                    print(get_zone)

                    break  # Once the zone is found, exit the loop

            print(get_zone)
            print(Zonepincode)
            if products:

                # selling_price = product_data.get("selling_price", 0)
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.ceil(total_amount)
                print(total_amount)
            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending",
                'shop_product':products,
                'shop_id' : shopping,
                'product_id':products.product_id,
                'business':business,
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' : "Normal",
                'delivery_address':request.POST["delivery_address"],
                'payment_type':request.POST["payment_type"],
                'pincode':request.POST["pincode"],
                'region':get_zone,
                'float_cash':selling_price,
            }
            print(data)
            if Zonepincode is None:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)
            for i in Zonepincode:
                print(i)
                if i == request.POST["pincode"]:
                    pincode_found = True
                    break  

            if pincode_found:
                productorder = models.Product_Ordermodel(**data)
                productorder.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
            else:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)

            # else:
            #     print("serializer prblm")
            #     return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
        # Food
        elif category.lower() == "food":
            products= models.food_productsmodel.objects.get(product_id = product_id)
            food = models.foodmodel.objects.get(food_id=products.food_id)
            print(food.Business_id)
            business = models.Businessmodel.objects.get(uid=food.Business_id) 
            print(business)
            pincode = request.POST['pincode']
            print(pincode)

            data1 = zone.objects.all()
            print(data1)
            get_zone = None  # Initialize get_zone variable
            Zonepincode=None
            for x in data1:
                print(x)
                if x.pincode is not None and pincode in x.pincode:
                    Zonepincode=x.pincode
                    get_zone = x.zone
                    print(get_zone)

                    break  # Once the zone is found, exit the loop

            print(get_zone)
            print(Zonepincode)
            if products:
                # selling_price = product_data.get("selling_price", 0) 
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.ceil(total_amount)

            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending",
                'food_product':products,
                'food_id' : food,
                'product_id':products.product_id,
                'business':business,
                
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' : "Quick",
                'delivery_address':request.POST["delivery_address"],
                'payment_type':request.POST["payment_type"],
                'pincode':request.POST["pincode"],
                'region':get_zone,
                'float_cash':selling_price,
            }
            if Zonepincode is None:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)
            for i in Zonepincode:
                print(i)
                if i == request.POST["pincode"]:
                    pincode_found = True
                    break  

            if pincode_found:
                productorder = models.Product_Ordermodel(**data)
                productorder.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
            else:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)
            
        # FreshCut
        elif category.lower() == "fresh_cuts":
            products= models.fresh_productsmodel.objects.get(product_id = product_id)
            freshcut = models.freshcutsmodel.objects.get(fresh_id=products.fresh_id)
            print(freshcut.Business_id)
            business = models.Businessmodel.objects.get(uid=freshcut.Business_id) 
            print(business)
            pincode = request.POST['pincode']
            print(pincode)

            data1 = zone.objects.all()
            print(data1)
            get_zone = None  # Initialize get_zone variable

            Zonepincode=None
            for x in data1:
                print(x)
                if x.pincode is not None and pincode in x.pincode:
                    Zonepincode=x.pincode
                    get_zone = x.zone
                    print(get_zone)

                    break  # Once the zone is found, exit the loop

            print(get_zone)
            print(Zonepincode)
            if products:
                # selling_price = product_data.get("selling_price", 0) 
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.ceil(total_amount)

            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending",
                'freshcut_product':products,
                'fresh_id' : freshcut,
                'product_id':products.product_id,
                'business':business,
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' : "Quick",
                'delivery_address':request.POST["delivery_address"],
                'payment_type':request.POST["payment_type"],
                'pincode':request.POST["pincode"],
                'region':get_zone,
                'float_cash':selling_price,

            }
            if Zonepincode is None:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)
            for i in Zonepincode:
                print(i)
                if i == request.POST["pincode"]:
                    pincode_found = True
                    break  

            if pincode_found:
                productorder = models.Product_Ordermodel(**data)
                productorder.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
            else:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)


        # Pharmacy
        elif category.lower() == "pharmacy":
            products= models.pharmacy_productsmodel.objects.get(product_id = product_id)
            pharmacy = models.pharmacy_model.objects.get(pharm_id=products.pharm_id)
            print(pharmacy.Business_id)
            business = models.Businessmodel.objects.get(uid=pharmacy.Business_id) 
            print(business)
            pincode = request.POST['pincode']
            print(pincode)

            data1 = zone.objects.all()
            print(data1)
            get_zone = None  # Initialize get_zone variable
            Zonepincode=None
            for x in data1:
                print(x)
                if x.pincode is not None and pincode in x.pincode:
                    Zonepincode=x.pincode
                    get_zone = x.zone
                    print(get_zone)

                    break  # Once the zone is found, exit the loop

            print(get_zone)
            print(Zonepincode)
            if products:
                # selling_price = product_data.get("selling_price", 0) 
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.ceil(total_amount)

            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending",
                'pharmacy_product':products,
                'phram_id' : pharmacy,
                'product_id':products.product_id,
                'business':business,
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' :"Quick",
                'delivery_address':request.POST["delivery_address"],
                'payment_type':request.POST["payment_type"],
                'pincode':request.POST["pincode"],
                'region':get_zone,
                'float_cash':selling_price,

            }
            if Zonepincode is None:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)
            for i in Zonepincode:
                print(i)
                if i == request.POST["pincode"]:
                    pincode_found = True
                    break  

            if pincode_found:
                productorder = models.Product_Ordermodel(**data)
                productorder.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
            else:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)

           
        # D-Original
        elif category.lower() == "d_original": 
            products= models.d_original_productsmodel.objects.get(product_id = product_id)
            d_origin = models.d_originalmodel.objects.get(d_id=products.d_id)
            print(d_origin.Business_id)
            business = models.Businessmodel.objects.get(uid=d_origin.Business_id) 
            print(business)
            pincode = request.POST['pincode']
            print(pincode)

            data1 = zone.objects.all()
            print(data1)
            get_zone = None  # Initialize get_zone variable
            Zonepincode=None
            for x in data1:
                print(x)
                if x.pincode is not None and pincode in x.pincode:
                    Zonepincode=x.pincode
                    get_zone = x.zone
                    print(get_zone)

                    break  # Once the zone is found, exit the loop

            print(get_zone)
            print(Zonepincode)
            if products:
                # selling_price = product_data.get("selling_price", 0) 
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.ceil(total_amount)

            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending",
                'd_original_product':products,
                'd_id' : d_origin,
                'product_id':products.product_id,
                'business':business,
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' : "Normal",
                'delivery_address':request.POST["delivery_address"],
                'payment_type':request.POST["payment_type"],
                'pincode':request.POST["pincode"],
                'region':get_zone, 
                'float_cash':selling_price,
           
                }
            if Zonepincode is None:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)
            for i in Zonepincode:
                print(i)
                if i == request.POST["pincode"]:
                    pincode_found = True
                    break  

            if pincode_found:
                productorder = models.Product_Ordermodel(**data)
                productorder.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
            else:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)
        # Daily_MIO
        elif category.lower() == "daily_mio":
            products= models.dmio_productsmodel.objects.get(product_id = product_id)
            daily_mio = models.dailymio_model.objects.get(dmio_id=products.dmio_id)
            print(daily_mio.Business_id)
            business = models.Businessmodel.objects.get(uid=daily_mio.Business_id) 
            print(business)
            pincode = request.POST['pincode']
            print(pincode)

            data1 = zone.objects.all()
            print(data1)
            get_zone = None  # Initialize get_zone variable
            Zonepincode=None
            for x in data1:
                print(x)
                if x.pincode is not None and pincode in x.pincode:
                    Zonepincode=x.pincode
                    get_zone = x.zone
                    print(get_zone)

                    break  # Once the zone is found, exit the loop

            print(get_zone)
            print(Zonepincode) 
            if products:
                # selling_price = product_data.get("selling_price", 0) 
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.ceil(total_amount)

            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending",
                'dmio_product':products,
                'dmio_id' : daily_mio,
                'product_id':products.product_id,
                'business':business,
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' : "Quick",
                'delivery_address':request.POST["delivery_address"],
                'payment_type':request.POST["payment_type"],
                'pincode':request.POST["pincode"],
                'region':get_zone,
                'float_cash':selling_price,

            }
            if Zonepincode is None:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)
            for i in Zonepincode:
                print(i)
                if i == request.POST["pincode"]:
                    pincode_found = True
                    break  

            if pincode_found:
                productorder = models.Product_Ordermodel(**data)
                productorder.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
            else:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Jewellery
        elif category.lower() == "jewellery": 
            products= models.jewel_productsmodel.objects.get(product_id = product_id)
            jewellery = models.jewellerymodel.objects.get(jewel_id=products.jewel_id)
            print(jewellery.Business_id)
            business = models.Businessmodel.objects.get(uid=jewellery.Business_id) 
            print(business)
            pincode = request.POST['pincode']
            print(pincode)

            data1 = zone.objects.all()
            print(data1)
            get_zone = None  # Initialize get_zone variable
            Zonepincode=None
            for x in data1:
                print(x)
                if x.pincode is not None and pincode in x.pincode:
                    Zonepincode=x.pincode
                    get_zone = x.zone
                    print(get_zone)

                    break  # Once the zone is found, exit the loop

            print(get_zone)
            print(Zonepincode)         
            if products:
                # selling_price = product_data.get("selling_price", 0) 
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.ceil(total_amount)

            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending", 
                'jewel_product':products,
                'jewel_id' : jewellery,
                'product_id':products.product_id,
                'business':business,
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' : "Normal",
                'delivery_address':request.POST["delivery_address"],
                'payment_type':request.POST["payment_type"],
                'pincode':request.POST["pincode"],
                'region':get_zone,
                'float_cash':selling_price,

            }
            if Zonepincode is None:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)
            for i in Zonepincode:
                print(i)
                if i == request.POST["pincode"]:
                    pincode_found = True
                    break  

            if pincode_found:
                productorder = models.Product_Ordermodel(**data)
                productorder.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
            else:
                return Response({"You are out of region"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(["GET"])
def enduser_order_list(request, id):
    
    user = models.End_Usermodel.objects.get(uid=id)
    orderdata = models.Product_Ordermodel.objects.filter(end_user=user)
    serializer = end_user_serializers.product_orderlistSerializer(orderdata, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def enduser_single_order_list(request, id,order_id):
    
    user = models.End_Usermodel.objects.get(uid=id)
    orderdata = models.Product_Ordermodel.objects.filter(end_user=user,order_id=order_id)
    serializer = end_user_serializers.product_orderlistSerializer(orderdata, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def enduser_order_cancel(request,id,order_id):
    user=models.End_Usermodel.objects.get(uid = id)
    user_id=user.id
    print(user_id)
    order_data=get_object_or_404(models.Product_Ordermodel,order_id = order_id)
    product_user_id = order_data.end_user.id
    print(product_user_id)
    if order_data:
        if user_id == product_user_id:
            print(order_data.status)
            order_data.status="cancel"
            order_data.save()
            print(order_data.status)
            return Response("success",status=status.HTTP_200_OK)
        else:
            return Response({"user not found"},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"no data"},status=status.HTTP_400_BAD_REQUEST)



# Carts add the product
@api_view(["POST"])
def cart_product(request, id, product_id, category):
    if request.method == "POST":
    
        user = models.End_Usermodel.objects.get(uid=id)
        if category.lower() == "shopping": 
            products = models.shop_productsmodel.objects.get(product_id=product_id)

            if products:
                quantity = int(request.data.get("quantity", 0))
                if quantity <= 0:
                    return Response("Quantity should be a positive integer", status=status.HTTP_400_BAD_REQUEST)
                total = products.product.get("selling_price")* quantity
                total = math.ceil(total)

            else:
                pass            
            data ={
                "cart_id": end_user_extension.cart_id_generate(),
                "user": user,
                "quantity": quantity,
                "category": category,
                "total": total,
                "shop_product":products,
                "status":"in-cart"

            }
            carts = models.Carts(**data)
            carts.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        if category.lower() == "jewellery": 
            products = models.jewel_productsmodel.objects.get(product_id=product_id)

            if products:
                quantity = int(request.data.get("quantity", 0))
                if quantity <= 0:
                    return Response("Quantity should be a positive integer", status=status.HTTP_400_BAD_REQUEST)
                total = products.product.get("selling_price")* quantity
                total = math.ceil(total)

            else:
                pass            
            data ={
                "cart_id": end_user_extension.cart_id_generate(),
                "user": user,
                "quantity": quantity,
                "category": category,
                "total": total,
                "jewel_product":products,
                "status":"in-cart"

            }
            carts = models.Carts(**data)
            carts.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        if category.lower() == "food": 
            products = models.food_productsmodel.objects.get(product_id=product_id)

            if products:
                quantity = int(request.data.get("quantity", 0))
                if quantity <= 0:
                    return Response("Quantity should be a positive integer", status=status.HTTP_400_BAD_REQUEST)
                total = products.product.get("selling_price")* quantity
                total = math.ceil(total)

            else:
                pass            
            data ={
                
                "cart_id": end_user_extension.cart_id_generate(),
                "user": user,
                "quantity": quantity,
                "category": category,
                "total": total,
                "food_product":products,
                "status":"in-cart"

            }
            carts = models.Carts(**data)
            carts.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        if category.lower() == "d_original": 
            products = models.d_original_productsmodel.objects.get(product_id=product_id)

            if products:
                quantity = int(request.data.get("quantity", 0))
                if quantity <= 0:
                    return Response("Quantity should be a positive integer", status=status.HTTP_400_BAD_REQUEST)
                total = products.product.get("selling_price")* quantity
                total = math.ceil(total)

            else:
                pass            
            data ={
                "cart_id": end_user_extension.cart_id_generate(),
                "user": user,
                "quantity": quantity,
                "category": category,
                "total": total,
                "d_origin_product":products,
                "status":"in-cart"

            }
            carts = models.Carts(**data)
            carts.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        if category.lower() == "fresh_cuts": 
            products = models.fresh_productsmodel.objects.get(product_id=product_id)

            if products:
                quantity = int(request.data.get("quantity", 0))
                if quantity <= 0:
                    return Response("Quantity should be a positive integer", status=status.HTTP_400_BAD_REQUEST)
                total = products.product.get("selling_price")* quantity
                total = math.ceil(total)

            else:
                pass            
            data ={
                
                "cart_id": end_user_extension.cart_id_generate(),
                "user": user,
                "quantity": quantity,
                "category": category,
                "total": total,
                "freshcut_product":products,
                "status":"in-cart"

               
            }
            carts = models.Carts(**data)
            carts.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        if category.lower() == "daily_mio": 
            products = models.dmio_productsmodel.objects.get(product_id=product_id)

            if products:
                quantity = int(request.data.get("quantity", 0))
                if quantity <= 0:
                    return Response("Quantity should be a positive integer", status=status.HTTP_400_BAD_REQUEST)
                total = products.product.get("selling_price")* quantity
                total = math.ceil(total)

            else:
                pass            
            data ={

                "cart_id": end_user_extension.cart_id_generate(),
                "user": user,
                "quantity": quantity,
                "category": category,
                "total": total,
                "dailymio_product":products,
                "status":"in-cart"
   
            }
            carts = models.Carts(**data)
            carts.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        if category.lower() == "pharmacy": 
            products = models.pharmacy_productsmodel.objects.get(product_id=product_id)

            if products:
                quantity = int(request.data.get("quantity", 0))
                if quantity <= 0:
                    return Response("Quantity should be a positive integer", status=status.HTTP_400_BAD_REQUEST)
                total = products.product.get("selling_price")* quantity
                total = math.ceil(total)

            else:
                pass            
            data ={

                "cart_id": end_user_extension.cart_id_generate(),
                "user": user,
                "quantity": quantity,
                "category": category,
                "total": total,
                "pharmacy_product":products,
                "status":"in-cart"
               
            }
            carts = models.Carts(**data)
            carts.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)




@api_view(["POST"])
def cartupdate(request, id):
    if request.method == "POST":
        try:
            userdata = models.Carts.objects.get(cart_id=id)
        except models.Carts.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)


        print(userdata.total)
        print(userdata.quantity)
        totalvalue=(int(userdata.total)/int(userdata.quantity))
        print(totalvalue)
        total=totalvalue*int(request.POST.get("quantity"))
        data = {
            'quantity': request.POST.get("quantity"),
            'total':total
        }
        print(data)
        
        basicdetailsserializer = end_user_serializers.Cartupdateserializer(instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("valid data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Serializer issue", "details": basicdetailsserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
   
    else:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

        


@api_view(["GET"])
def cartlist(request,id):
    if request.method == "GET":
        user=models.End_Usermodel.objects.get(uid=id)
        qs=models.Carts.objects.filter(user=user,status="in-cart")
        serializer = end_user_serializers.Cartserializer(qs,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def cartremove(request,id,cart_id):
    if request.method =="POST":
        user = models.End_Usermodel.objects.get(uid=id)
        cart_entry = models.Carts.objects.get(cart_id=cart_id)
        cart_entry.delete()
        return Response(id, status=status.HTTP_200_OK)


# whishlist create

@api_view(["POST"])
def whishlist_product(request, id, product_id, category):
    if request.method == "POST":
        user = models.End_Usermodel.objects.get(uid=id)
        if category.lower() == "shopping": 
            products = models.shop_productsmodel.objects.get(product_id=product_id)           
            data ={
                "user": user,
                "category": category,
                "shop_product":products,
              
            }
            wishlist = models.whishlistmodel(**data)
            wishlist.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        if category.lower() == "jewellery": 
            products = models.jewel_productsmodel.objects.get(product_id=product_id)

            data ={
                "user": user,
                "category": category,
                "jewel_product":products,
              
            }
            wishlist = models.whishlistmodel(**data)
            wishlist.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        if category.lower() == "food": 
            products = models.food_productsmodel.objects.get(product_id=product_id)                

            data ={
                "user": user,
                "category": category,
                "food_product":products,
              
            }
            wishlist = models.whishlistmodel(**data)
            wishlist.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        if category.lower() == "d_original": 
            products = models.d_original_productsmodel.objects.get(product_id=product_id)                


            data ={
                "user": user,
                "category": category,
                "d_origin_product":products,
              
            }
            wishlist = models.whishlistmodel(**data)
            wishlist.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        if category.lower() == "fresh_cuts": 
            products = models.fresh_productsmodel.objects.get(product_id=product_id)                

            data ={
                "user": user,
                "category": category,
                "freshcut_product":products,
              
            }
            wishlist = models.whishlistmodel(**data)
            wishlist.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        if category.lower() == "daily_mio": 
            products = models.dmio_productsmodel.objects.get(product_id=product_id)                
            data ={
                "user": user,
                "category": category,
                "dailymio_product":products,
              
            }
            wishlist = models.whishlistmodel(**data)
            wishlist.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        if category.lower() == "pharmacy": 
            products = models.pharmacy_productsmodel.objects.get(product_id=product_id)               

            data ={
                "user": user,
                "category": category,
                "pharmacy_product":products,
              
            }
            wishlist = models.whishlistmodel(**data)
            wishlist.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        

@api_view(["GET"])
def all_wishlist(request, id):
    if request.method == "GET":
        wishlist = models.whishlistmodel.objects.filter(user__uid=id)
        serializer = end_user_serializers.wishlistSerializer(wishlist,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
  


@api_view(["POST"])
def remove_wish(request,id,product_id):
    user = models.End_Usermodel.objects.get(uid=id)
    print(user)
    shopcart_item=models.whishlistmodel.objects.filter(user=user,shop_product__product_id=product_id)
    jewelcart_item =models.whishlistmodel.objects.filter(user=user,jewel_product__product_id=product_id)
    foodcart_item =models.whishlistmodel.objects.filter(user=user,food_product__product_id=product_id)
    freshcart_item=models.whishlistmodel.objects.filter(user=user,freshcut_product__product_id=product_id)
    dailymiocart_item=models.whishlistmodel.objects.filter(user=user,dailymio_product__product_id=product_id)
    doriginalcart_item=models.whishlistmodel.objects.filter(user=user,d_origin_product__product_id=product_id)
    pharmacycart_item=models.whishlistmodel.objects.filter(user=user,pharmacy_product__product_id=product_id)
    cart_items = shopcart_item | jewelcart_item | foodcart_item | freshcart_item | dailymiocart_item | doriginalcart_item | pharmacycart_item
    cart_items.delete()
    return Response(id, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_reviews_for_delivered_products(request, id, product_id):
    if request.method == "POST":
        try:
            user = models.End_Usermodel.objects.get(uid=id)
            product = None
            for model in [models.shop_productsmodel, models.jewel_productsmodel, models.food_productsmodel,
                          models.fresh_productsmodel, models.dmio_productsmodel, models.d_original_productsmodel,
                          models.pharmacy_productsmodel]:
                if model.objects.filter(product_id=product_id).exists():
                    delivered_orders = model.objects.filter(product_id=product_id)
                    product = delivered_orders.first()  # Assuming the product is the same across all orders
                    break
            else:
                return JsonResponse({'error': 'Product does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Creating a review for the product
            review = Reviews.objects.create(
                user=user,
                shop_product=product.shop_product if hasattr(product, 'shop_product') else None,
                jewel_product=product.jewel_product if hasattr(product, 'jewel_product') else None,
                d_origin_product=product.d_original_product if hasattr(product, 'd_original_product') else None,
                dailymio_product=product.dmio_product if hasattr(product, 'dmio_product') else None,
                pharmacy_product=product.pharmacy_product if hasattr(product, 'pharmacy_product') else None,
                food_product=product.food_product if hasattr(product, 'food_product') else None,
                freshcut_product=product.freshcut_product if hasattr(product, 'freshcut_product') else None,
                comment=request.data.get('comment'),
                rating=request.data.get('rating'),
                product_id=product_id,
            )
            
            # You might want to do something else here like sending notifications, etc.
            
            return JsonResponse({'message': 'Review created successfully'}, status=status.HTTP_201_CREATED)
        except models.End_Usermodel.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def get_all_reviews(request):
    if request.method == "GET":
        data = models.Reviews.objects.all()
        serializers = end_user_serializers.review_serializer(data,many=True)
        return Response(data=serializers.data,status=status.HTTP_200_OK)

@api_view(["GET"])
def get_product_all_reviews(request,product_id):
    if request.method == "GET":
        data = models.Reviews.objects.filter(product_id=product_id)
        serializers = end_user_serializers.review_serializer(data,many=True)
        return Response(data=serializers.data,status=status.HTTP_200_OK)
# used products
@api_view(['POST'])
def used_products(request,id):
    product_id = end_user_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = end_user_extension.product_id_generate()
        else:
            break
   
    #add
    fs = FileSystemStorage()
    print(request.POST)
    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/used_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/used_products/{id}/other_images/"+sav.name, sav) 
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))


    used_products = dict(request.POST)
  
    used_products['product_id'] = product_id
    used_products['primary_image'] = primary_image_paths
    used_products['other_images'] = other_imagelist
    
    print(used_products)
    cleaned_data_dict ={key:value[0] if isinstance(value,list) and len(value)==1 else value for key,value in used_products.items()}

    data= {
        'user':id,
        'product_id' : product_id,
        'status':False,
        'category':request.POST['category'],
        'subcategory':request.POST['subcategory'],
        'product':cleaned_data_dict,  
    }
    print(data)

    new_uesd_product = models.used_productsmodel(**data)
    try:
        # new_shop_product.full_clean()  # Validate model fields if needed
        new_uesd_product.save()
        print("Data saved successfully")
        return Response(id, status=status.HTTP_200_OK)
    except Exception as e:
        print("Error while saving data:", e)
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_allused_products(request):

    if request.method == "GET":
        data = models.used_productsmodel.objects.all()
        print(data)
        serializers = end_user_serializers.used_productlistserializer(data,many =True) 
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_used_products_category(request,subcategory):
    if request.method == "GET":

        data = models.used_productsmodel.objects.filter(subcategory=subcategory)
        alldataserializer = end_user_serializers.used_productlistserializer(data,many =True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)   
    
    
@api_view(['GET'])
def get_single_used_products(request,product_id):

    if request.method == "GET":
        data = models.used_productsmodel.objects.filter(product_id =product_id)
        print(data)
        serializers = end_user_serializers.used_productlistserializer(data,many =True) 
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def get_used_products(request,id):

    if request.method == "GET":
        data = models.used_productsmodel.objects.filter(user=id)
        print(data)
        serializers = end_user_serializers.used_productlistserializer(data,many =True) 
        return Response(data=serializers.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_single_used_products(request,id,product_id):
    if request.method == "GET":
        data = models.used_productsmodel.objects.filter(user=id,product_id =product_id)
        print(data)
        serializers = end_user_serializers.used_productlistserializer(data,many =True) 
        return Response(data=serializers.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def used_update_product(request,id,product_id):

    used_products = dict(request.POST)
    print(used_products)

    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/used_products/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        used_products['primary_image'] = primary_image_paths
    except:
        # used_pro=collection.find_one({"used_id": id,"product_id":product_id})
        # primary_image_paths=used_pro.get("primary_image")
        # used_products['primary_image'] = primary_image_paths
        pass
        


    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/used_products/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        used_products['other_images'] = other_imagelist

    except:
        pass
        
    try:
        used_product_instance = models.used_productsmodel.objects.get(user=id, product_id=product_id)
        print(used_product_instance)
        
        existing_product_data = used_product_instance.product
        
        # Updating product field with new data
        new_product_data = dict(request.POST)
        existing_product_data.update(new_product_data)
        
        # Saving changes to the SQLite table
        with transaction.atomic():
            # Updating only the product field
            used_product_instance.product = existing_product_data
            used_product_instance.save()
        
        return Response(id, status=status.HTTP_200_OK)
    except models.used_productsmodel.DoesNotExist:
        return Response({"error": "used product not found"}, status=status.HTTP_404_NOT_FOUND)





@api_view(["POST"])
def calculate_average_ratings(request,category):
    if category == "food":
        products=models.food_productsmodel.objects.filter(category="food")
        for product in products:
            reviews = models.Reviews.objects.filter(food_product=product) 
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            product.rating = average_rating
            product.save()

    elif category == "jewellery":
        products=models.jewel_productsmodel.objects.filter(category="jewellery")
        for product in products:
            reviews = models.Reviews.objects.filter(jewel_product=product)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            product.rating = average_rating
            product.save()

    elif category == "shopping":
        products=models.shop_productsmodel.objects.filter(category="shopping")
        for product in products:
            reviews = models.Reviews.objects.filter(shop_product=product)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            product.rating = average_rating
            product.save()

    
    elif category == "d_original":
        products=models.d_original_productsmodel.objects.filter(category="d_original")
        for product in products:
            reviews = models.Reviews.objects.filter(d_origin_product=product)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            product.rating = average_rating
            product.save()

    elif category == "dailymio":
        products=models.dmio_productsmodel.objects.filter(category="dailymio")
        for product in products:
            reviews = models.Reviews.objects.filter(dailymio_product=product)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            product.rating = average_rating
            product.save()

    elif category == "freshcuts":
        products=models.fresh_productsmodel.objects.filter(category="freshcuts")
        for product in products:
            reviews = models.Reviews.objects.filter(freshcut_product=product)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            product.rating = average_rating
            product.save()

    elif category == "pharmacy":
        products=models.pharmacy_productsmodel.objects.filter(category="pharmacy")
        for product in products:
            reviews = models.Reviews.objects.filter(pharmacy_product=product)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            product.rating = average_rating
            product.save()
    else:
        print("no data")
    return Response({'success'}, status=status.HTTP_200_OK)



@api_view(['GET'])
def user_product_timeline(request,id):
    if request.method == "GET":
        data = models.Product_Ordermodel.objects.get(order_id=id)
        print(data)
        serializers = end_user_serializers.product_orderlistSerializer(data,many =False) 
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    


@api_view(["POST"])
def user_product_order_status_return(request,id,order_id):
    try:
        user = models.End_Usermodel.objects.get(uid=id)
        print(user)
        product_orders = models.Product_Ordermodel.objects.filter(order_id=order_id)
        print(product_orders)
        if product_orders.exists():
            for product_order in product_orders:
                # Update the status field with the new value
                product_order.status = "end_user_return"
                product_order.save()
                #returned product for hub
                data = models.product_return.objects.create(
                order = product_orders
                )
                data.save()
            return Response(id,status=status.HTTP_200_OK)
        else:
            return Response("Product order not found", status=status.HTTP_404_NOT_FOUND)
    except:
        return Response("Product order not found", status=status.HTTP_404_NOT_FOUND)




