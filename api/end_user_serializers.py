from rest_framework import serializers

from api import models
from api.business_serializers import BusinessSerializer, jewel_productlistserializer,shop_productlistserializer,dmio_productlistserializer,d_original_productlistserializer,pharmacy_productlistserializer,dailymio_list_serializer,food_productlistserializer,fresh_productlistserializer
from api.business_serializers import jewellery_list_serializer,shopping_list_serializer,freshcuts_list_serializer,food_list_serializer,dailymio_list_serializer,d_original_list_serializer,pharmacy_list_serializer
from api.delivery_serializers import DeliverypersonSerializer

class EnduserSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.IntegerField()
    user_otp = serializers.IntegerField()
    profile_picture = serializers.CharField()
    full_name = serializers.CharField()
    created_date = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    address_data = serializers.JSONField()


class SignupSerializer(serializers.Serializer):
    uid = serializers.CharField()
    full_name=serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    otp = serializers.IntegerField()
    password = serializers.CharField()
    created_date=serializers.CharField()

    def create(self, data):
        return models.End_Usermodel.objects.create(
            uid = data['uid'],
            full_name = data['full_name'],
            email = data['email'],
            phone_number = data['phone_number'],
            otp = data['otp'],
            password = data['password'],
            created_date = data['created_date'],

        )
    
class OTPSerializer(serializers.Serializer):
    user_otp = serializers.IntegerField()
    
    def update(self, instance, data):
        instance.user_otp = data['user_otp']
        instance.save()
        return instance
    
class forget_password_serializer(serializers.Serializer):
    password = serializers.CharField()
    
    def update (self,instance,data):
        instance.password=data["password"]
        instance.save()
        return instance


class profile_picture_Serializer(serializers.Serializer):
    profile_picture = serializers.CharField()
    
    def update(self, instance, data):
        instance.profile_picture = data['profile_picture']
        instance.save()
        return instance
    

class forget_password_serializer(serializers.Serializer):
    password = serializers.CharField()
    
    def update (self,instance,data):
        instance.password=data["password"]
        instance.save()
        return instance
    


class AddressSerializer(serializers.Serializer):
    doorno = serializers.CharField()
    area = serializers.CharField()
    landmark = serializers.CharField()
    place = serializers.CharField()
    district = serializers.CharField()
    state = serializers.CharField()
    pincode = serializers.CharField()

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        new_address = {
            'doorno': validated_data.get('doorno'),
            'area': validated_data.get('area'),
            'landmark': validated_data.get('landmark'),
            'place': validated_data.get('place'),
            'district': validated_data.get('district'),
            'state': validated_data.get('state'),
            'pincode': validated_data.get('pincode')
        }
        address_data = instance.address_data or []
        address_data.append(new_address)
        instance.address_data = address_data
        instance.save()
        return instance




class locationSerializer(serializers.Serializer):
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    def update(self,instance,data):
        instance.latitude = data["latitude"]
        instance.longitude = data['longitude']
        instance.save()
        return instance
    

    

class product_orderSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    track_id = serializers.CharField()
    quantity = serializers.CharField()
    total_amount = serializers.CharField()
    # business_id = serializers.CharField()
    end_user_id = serializers.CharField()
    # delivery = serializers.CharField()
    # shop_id= serializers.CharField()
    shop_product_id = serializers.CharField()
    food_product_id = serializers.CharField()
    jewel_product_id = serializers.CharField()
    dmio_product_id =serializers.CharField()
    pharmacy_product_id = serializers.CharField()
    d_original_product_id = serializers.CharField()
    freshcut_product_id = serializers.CharField()
    status = serializers.CharField()    
    # delivery_date = serializers.CharField()
    # payment_status = serializers.CharField()
    delivery_type= serializers.CharField()
    category_data = serializers.CharField()
    # distance = serializers.CharField()
    # earn_perkm_amount = serializers.CharField()
    def create(self, data):
        return models.Product_Ordermodel.objects.create(
            order_id = data[' order_id'],
            track_id = data['track_id'],
            quantity = data['quantity'],
            total_amount = data['total_amount'],
            # business_id = data['business_id'],
            end_user_id = data['end_user_id'],
            shop_product_id = data['shop_product_id'],
            food_product_id =data['food_product_id'],
            jewel_product_id = data['jewel_product_id'],
            dmio_product_id = data['dmio_product_id'],
            pharmacy_product_id = data['pharmacy_product_id'],
            d_original_product_id = data['d_original_product_id'],
            freshcut_product_id = data['freshcut_product_id'],
            status = data['status'],
            delivery_type = data['delivery_type'],
            category_data = data['category_data'],

        )
    





class update_acc_serializer(serializers.Serializer):

    profile_picture=serializers.CharField()
    def update(self,instance,data):
       
        instance.profile_picture=data["profile_picture"]
        instance.save()
        return instance

class Cartserializer(serializers.Serializer):
    cart_id =serializers.CharField()
    shop_product=shop_productlistserializer()
    jewel_product=jewel_productlistserializer()
    d_origin_product=d_original_productlistserializer()
    dailymio_product=dmio_productlistserializer()
    pharmacy_product=pharmacy_productlistserializer()
    food_product=food_productlistserializer()
    freshcut_product=fresh_productlistserializer()
    user=EnduserSerializer()
    created_date=serializers.DateTimeField()
    quantity=serializers.CharField()
    total=serializers.IntegerField()
    category = serializers.CharField()
    status = serializers.CharField()


class Cartupdateserializer(serializers.Serializer):
    quantity = serializers.CharField()
    total = serializers.FloatField()
    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.total = validated_data.get('total', instance.total)
        instance.save()
        return instance

        
        


class wishlistSerializer(serializers.Serializer):
    shop_product=shop_productlistserializer()
    jewel_product=jewel_productlistserializer()
    d_origin_product=d_original_productlistserializer()
    dailymio_product=dmio_productlistserializer()
    pharmacy_product=pharmacy_productlistserializer()
    food_product=food_productlistserializer()
    freshcut_product=fresh_productlistserializer()
    user=EnduserSerializer()
    date_added=serializers.DateTimeField()
    category = serializers.CharField()



class product_orderlistSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    track_id = serializers.CharField()
    quantity = serializers.CharField()
    total_amount = serializers.CharField()
    business=BusinessSerializer()
    end_user = EnduserSerializer()
    # delivery = DeliverypersonSerializer()
    shop_product = shop_productlistserializer()
    food_product = food_productlistserializer()
    jewel_product= jewel_productlistserializer()
    dmio_product =dmio_productlistserializer()
    pharmacy_product = pharmacy_productlistserializer()
    d_original_product = d_original_productlistserializer()
    freshcut_product = fresh_productlistserializer()
    shop_id= shopping_list_serializer()
    jewel_id=jewellery_list_serializer()
    food_id=food_list_serializer()
    fresh_id=freshcuts_list_serializer()
    d_id=d_original_list_serializer()
    dmio_id= dailymio_list_serializer()
    pharm_id= pharmacy_list_serializer()
    product_id= serializers.CharField()
    status = serializers.CharField()    
    delivery_date = serializers.CharField()
    payment_status = serializers.CharField()
    delivery_type= serializers.CharField()
    category_data = serializers.CharField()
    payment_type = serializers.CharField()
    delivery_address =serializers.JSONField()
    expected_deliverydate = serializers.DateField()
    distance=serializers.CharField()
    region=serializers.CharField()
    business_pickup=serializers.CharField()
    # business_status=serializers.CharField()
    ready_to_pick_up = serializers.CharField()
    incentive = serializers.CharField()
    ship_to_other_region = serializers.CharField()
    order_date = serializers.DateField()


class review_serializer(serializers.Serializer):
    user= EnduserSerializer()
    shop_product=shop_productlistserializer()
    jewel_product=jewel_productlistserializer()
    d_origin_product=d_original_productlistserializer()
    dailymio_product=dmio_productlistserializer()
    pharmacy_product=pharmacy_productlistserializer()
    food_product=food_productlistserializer()
    freshcut_product=fresh_productlistserializer()
    comment=serializers.CharField()
    rating=serializers.CharField()
    product_id=serializers.CharField()

class used_productserializer(serializers.Serializer):
    user = serializers.CharField()
    product_id = serializers.CharField()
    category = serializers.CharField()
    subcategory=serializers.CharField()
    product = serializers.CharField()
    def create(self,data):
        return models.used_productsmodel.objects.create(
            user=data['user'],
            product_id = data['product_id'],
            category = data['category'],
            subcategory=data['subcategory'],
            product = data['product'],
            
        )
class used_productlistserializer(serializers.Serializer):
    user = serializers.CharField()
    product_id = serializers.CharField()
    status=serializers.CharField()
    category = serializers.CharField()
    subcategory=serializers.CharField()
    product = serializers.JSONField()

