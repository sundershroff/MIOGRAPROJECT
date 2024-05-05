from django.shortcuts import render,redirect
from api.models import *
from hub.models import *
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.decorators import api_view
import requests
import json
from api.end_user_serializers import *
# Create your views here.

def send_notification(registration_ids , message_title , message_desc):
    fcm_api = "AAAAbIibZeo:APA91bEHlJFNQjqRjMjX2N-YfgDAjOU_fXdt8HkQiQYhOYbGcv9B6MqGykeaG7zQVdrMOEQrOGckrUwKbl4XWdEOboEY9uDUSALHdzbpdW-DJbUxlVzCG_ayQJIPJfAnEPcCeKX86sqg"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api
    }    

    payload = {
        "registration_ids" :registration_ids,
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

def hub_dashboard(request,hub):
    
    hub = hub
    order_products = Product_Ordermodel.objects.filter(delivery_type = "Normal",jewel_id__region = hub,status="accepted",ready_to_pick_up=0) | Product_Ordermodel.objects.filter(delivery_type = "Normal",shop_id__region = hub,status="accepted",ready_to_pick_up=0) | Product_Ordermodel.objects.filter(delivery_type = "Normal",d_id__region = hub,status="accepted",ready_to_pick_up=0)
    delivery_boy = Delivery_model.objects.filter(region = hub)
    print(order_products)
    context = {
        'hub':hub,
        'order_products':order_products,
        'delivery_boy':delivery_boy,
    }
    if request.method == "POST":
        print(request.POST)
        order_data = Product_Ordermodel.objects.get(order_id = request.POST['order_id'])
        order_data.ready_to_pick_up = 1
        order_data.save()
        create_data = product_arrive.objects.create(
            order = order_data
        )
        create_data.save()
        send_noti = Delivery_model.objects.filter(uid = request.POST['assign_to_delivery_person'])
        # accepted
        # send_notification("resgistration" , 'hi' , 'hello world')
        return redirect(f"/hub/hub_product_arrive/{hub}")
    return render(request,"hub_dashboard.html",context)



def hub_product_arrive(request,hub):
    product_pick = (product_arrive.objects.filter(order_id__jewel_id__region = hub,product_arrived=0,order_id__ship_to_other_region = None)
    | 
    product_arrive.objects.filter(order_id__shop_id__region = hub,product_arrived=0,order_id__ship_to_other_region = None) 
    |
    product_arrive.objects.filter(order_id__d_id__region = hub,product_arrived=0,order_id__ship_to_other_region = None)
    |
    product_arrive.objects.filter(order_id__jewel_id__region = hub,product_arrived=0,order_id__ship_to_other_region = "0")
    | 
    product_arrive.objects.filter(order_id__shop_id__region = hub,product_arrived=0,order_id__ship_to_other_region = "0") 
    |
    product_arrive.objects.filter(order_id__d_id__region = hub,product_arrived=0,order_id__ship_to_other_region = "0")
    )
    delivery_boy = Delivery_model.objects.filter(region = hub)
    

    context = {
        'hub':hub,
        'product_pick':product_pick,
        'delivery_boy':delivery_boy,
    }
    if request.method == "POST":
        # for hub
        if "arrived" in request.POST:
            print(request.POST)
            order_data = Product_Ordermodel.objects.get(order_id = request.POST['seller_region'])
            if order_data.shop_id != None:
                order_table = order_data.shop_id.region
            elif order_data.jewel_id != None:
                order_table = order_data.jewel_id.region
            elif order_data.d_id != None:
                order_table = order_data.d_id.region
            
            if order_table != order_data.region:
                print("ship")
                order_data.ship_to_other_region = "0"
                order_data.save()
                return redirect(f"/hub/hub_product_arrive/{hub}")
            else:
                data = product_arrive.objects.get(id = request.POST['id'])
                data.product_arrived = request.POST['arrived']
                data.save()
                return redirect(f"/hub/delivery/{hub}")
        
        elif "ship" in request.POST:
            order_data = Product_Ordermodel.objects.get(order_id = request.POST['seller_region'])
            order_data.ship_to_other_region = "1"
            order_data.save()
        # again assign to deliver person
        elif "assign_to_delivery_person" in request.POST:
            order_data = Product_Ordermodel.objects.get(order_id = request.POST['order_id'])
            order_data.status = "accepted"
            order_data.save()
            send_noti = Delivery_model.objects.filter(uid = request.POST['assign_to_delivery_person'])
            # accepted
            # send_notification("resgistration" , 'hi' , 'hello world')
            return redirect(f"/hub/hub_product_arrive/{hub}")
        # for order status
        
    return render(request,"hub_product_arrrive.html",context)

def delivery(request,hub):
    ready_to_delivery = (product_arrive.objects.filter(order__region = hub,product_arrived = 1)
    |
    product_arrive.objects.filter(order__region = hub,product_arrived_to_me = 1))
    delivery_boy = Delivery_model.objects.filter(region = hub)
    context = {
        'hub':hub,
        'ready_to_delivery':ready_to_delivery,
        'delivery_boy':delivery_boy,
    }
    if request.method == "POST":
        print(request.POST)
        if "assign_work" in request.POST:
            order_data = Product_Ordermodel.objects.get(order_id = request.POST['order_id'])
            assign_delivery_boy = Delivery_model.objects.get(uid = request.POST['assign_work'])
            order_data.deliveryperson_id = assign_delivery_boy
            order_data.status = "shipped"
            order_data.save()
            return redirect(f"/hub/delivery/{hub}")
    return render(request,"delivery.html",context)

def delivery_boy(request,hub):
    hub = hub
    delivery_boy = Delivery_model.objects.filter(region = hub)
    context = {
        'hub':hub,
        'delivery_boy':delivery_boy,
    }
    return render(request,"delivery_boy.html",context)

def hub_other_region(request,hub):
    other_region = []
    print(hub)
    order_my_region = Product_Ordermodel.objects.filter(region = hub,delivery_type = "Normal")
    print(order_my_region)
    order_products = (Product_Ordermodel.objects.filter(delivery_type = "Normal",jewel_id__region = hub) 
    |
    Product_Ordermodel.objects.filter(delivery_type = "Normal",shop_id__region = hub) 
    |
    Product_Ordermodel.objects.filter(delivery_type = "Normal",d_id__region = hub)
    )
    print(order_products)
    if order_products:
        for i in order_my_region:
            for j in order_products:
                print(i.order_id,j.order_id)
                if i.order_id == j.order_id:
                    print("equal")
                    break
                else:
                    if i not in other_region:
                        print("no equal")
                        other_region.append(i)
        
    else:
        for i in order_my_region:
            other_region.append(i)
    print(other_region)
    delivery_boy = Delivery_model.objects.filter(region = hub)

    context = {
        'hub':hub,
        'delivery_boy':delivery_boy,
        'other_region':other_region[::-1]
    }
    if request.method == "POST":
        # for hub
        if "arrived_to_me" in request.POST:
            order_data = Product_Ordermodel.objects.get(order_id = request.POST['id'])
            order_data.ship_to_other_region = "2"
            order_data.save()
            data = product_arrive.objects.get(order__order_id = request.POST['id'])
            data.product_arrived_to_me = request.POST['arrived_to_me']
            data.save()
            
            return redirect(f"/hub/delivery/{hub}")
        # again assign to deliver person
        elif "assign_to_delivery_person" in request.POST:
            order_data = Product_Ordermodel.objects.get(order_id = request.POST['order_id'])
            order_data.status = "accepted"
            order_data.save()
            send_noti = Delivery_model.objects.filter(uid = request.POST['assign_to_delivery_person'])
            # accepted
            # send_notification("resgistration" , 'hi' , 'hello world')
            return redirect(f"/hub/hub_product_arrive/{hub}")
        # for order status
        
    return render(request,"other_region.html",context)

def invoice(request,id):
    data = product_arrive.objects.get(id = id)
    context = {
        'i':data
    }
    return render(request,"invoice_hub.html",context)


@api_view(['POST'])
def hub_picked(request,order_id,delivery_person):
    try:
        if request.method == "POST":
            order_data = Product_Ordermodel.objects.get(order_id = order_id)
            data = product_arrive.objects.get(order__order_id = order_id)
            delivery_boy = Delivery_model.objects.get(uid = delivery_person)
            print(data)
            data.product_picked = request.data['product_picked']
            data.delivery_person = delivery_boy
            data.save()
            # if "order-confirmed" in request.POST:
            #     order_data.status = "order-confirmed"
            # elif "rejected" in request.POST:
            #     order_data.status = "rejected"
            #     order_data.reason = request.POST['reason']
            # order_data.save()
            return Response("Product picked from store successfully",status=status.HTTP_200_OK)
    except:
        return Response("invalid data",status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def normal_delivery_get_product_order(request,id,region):
    if request.method =="GET":
        if models.deliverylogintable_model.objects.filter(deliveryperson__uid=id,delivery_type="Normal",region=region,status="1").exists():
            delivery=models.deliverylogintable_model.objects.filter(deliveryperson__uid=id,delivery_type="Normal",region=region,status="1")
            print(delivery)
            qs=models.Product_Ordermodel.objects.filter(status="accepted",delivery_type="Normal",region=region,ready_to_pick_up=1)
            print(qs)
            serializers= product_orderlistSerializer(qs,many=True)
            return Response(data=serializers.data,status=status.HTTP_200_OK)
        else:
            return Response({"deliverypersons not available"},status=status.HTTP_400_BAD_REQUEST)
        
@api_view(["GET"])
def shipped_delivery_product(request,id):
    try:
        if request.method =="GET":
                qs=models.Product_Ordermodel.objects.filter(status="shipped",deliveryperson_id__uid = id)
                print(qs)
                serializers= product_orderlistSerializer(qs,many=True)
                return Response(data=serializers.data,status=status.HTTP_200_OK)
    except:
        return Response("You Have No shipped Products",status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def out_of_delivery(request,order_id):
    try:
        if request.method == "POST":
            order_data = Product_Ordermodel.objects.get(order_id = order_id)
            order_data.status = "picked"
            order_data.save()
            return Response("Out of Delivered",status=status.HTTP_200_OK)
    except:
        return Response("Invalid Data",status=status.HTTP_400_BAD_REQUEST)
