from api.models import Businessmodel,shoppingmodel,jewellerymodel,foodmodel,freshcutsmodel,pharmacy_model,d_originalmodel,dailymio_model
from rest_framework import serializers
from api import models


class BusinessSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.IntegerField() 
    full_name=serializers.CharField()
    created_date=serializers.CharField()
    user_otp = serializers.IntegerField()
    profile_picture = serializers.CharField()
    device_id = serializers.JSONField()
    notification_status=serializers.CharField()


class SignupSerializer(serializers.Serializer):
    uid = serializers.CharField()
    otp = serializers.IntegerField()
    full_name=serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    created_date=serializers.CharField()
    device_id = serializers.JSONField()

    def create(self, data):
        return Businessmodel.objects.create(
            uid = data['uid'],
            otp = data['otp'],
            full_name = data['full_name'],
            email = data['email'],
            phone_number = data['phone_number'],
            password = data['password'],
            created_date = data['created_date'],
            device_id = data['device_id'],
        )
class update_acc_serializer(serializers.Serializer):
    phone_number = serializers.CharField()
    profile_picture=serializers.CharField()
    def update(self,instance,data):
        instance.phone_number=data["phone_number"]
        instance.profile_picture=data["profile_picture"]
        instance.save()
        return instance

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

# shop_order

class shop_order_serializer(serializers.Serializer):
    order_id =serializers.CharField()
    track_id = serializers.CharField()
    quantity = serializers.CharField()
    order_date =serializers.DateField()
    total_amount = serializers.CharField()
    business_id = serializers.CharField()
    shop_id= serializers.CharField()
    product_id = serializers.CharField()
    e_user_id = serializers.CharField()
    status = serializers.CharField()
    delivery_id = serializers.CharField(read_only=True)
    payment_status = serializers.CharField()
    distance = serializers.CharField()

   

# shopping

class shopping_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    shop_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    region = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    # date = serializers.CharField()
    category= serializers.CharField()   
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    def create(self,data):
        return shoppingmodel.objects.create(
            Business_id = data['Business_id'],
            shop_id = data['shop_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            region = data['region'],
            pincode = data['pincode'],
            aadhar_number = data['aadhar_number'],
            # pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            # date = data['date'],
            category =data['category'],
            latitude = data['latitude'],
            longitude = data['longitude'],
        )

class shopping_list_serializer(serializers.Serializer):
    shop_id = serializers.CharField()
    Business_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    region = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()
    category = serializers.CharField()
    total_revenue = serializers.CharField()
    monthly_revenue = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
class shopping_edit_serializer(serializers.Serializer):

    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    # region = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    # date = serializers.CharField()

    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        # instance.region = data['region']
        instance.pincode = data['pincode']
        instance.aadhar_number = data['aadhar_number']
        # instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        # instance.date = data['date']
        instance.latitude=data['latitude']
        instance.longitude=data['longitude']
        instance.save()
        return instance

# shopping products
class shop_productserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    category = serializers.CharField()
    subcategory=serializers.CharField()
    product = serializers.CharField()
    def create(self,data):
        return models.shop_productsmodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id'],
            category = data['category'],
            subcategory=data['subcategory'],
            product = data['product'],
            
        )
class shop_productlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.CharField()
    category = serializers.CharField()
    subcategory=serializers.CharField()
    product = serializers.JSONField()
    business_status=serializers.CharField()
    rating=serializers.CharField()

class delivered_productlistserializer(serializers.Serializer):
    product = serializers.JSONField()

# jewellery

class jewellery_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    jewel_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    region = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    # date = serializers.CharField()
    category = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()

    def create(self,data):
        return jewellerymodel.objects.create(
            Business_id = data['Business_id'],
            jewel_id = data['jewel_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            region = data['region'],
            pincode = data['pincode'],
            aadhar_number = data['aadhar_number'],
            # pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            # date = data['date'],
            category = data['category'],
            latitude=data['latitude'],
            longitude=data['longitude'],
        )

class jewellery_list_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    jewel_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    region = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()
    category = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
class jewellery_edit_serializer(serializers.Serializer):

    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    # region = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    # date = serializers.CharField()
    
    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        # instance.region = data['region']
        instance.pincode = data['pincode']
        instance.aadhar_number = data['aadhar_number']
        # instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        # instance.date = data['date']
        instance.latitude=data['latitude']
        instance.longitude=data['longitude']
        instance.save()
        return instance   

# jewellery products
class jewel_productlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    jewel_id = serializers.CharField()
    status=serializers.CharField()
    category = serializers.CharField()
    subcategory=serializers.CharField()
    product = serializers.JSONField()
    business_status=serializers.CharField()
    rating=serializers.CharField()
class jewel_productserializer(serializers.Serializer):
    product_id = serializers.CharField()
    jewel_id = serializers.CharField()
    category = serializers.CharField()
    subcategory=serializers.CharField()
    product = serializers.CharField()

    def create(self,data):
        return models.jewel_productsmodel.objects.create(

            product_id = data['product_id'],
            jewel_id = data['jewel_id'],
            category = data['category'],
            subcategory=data['subcategory'],

        )



# food

class food_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    food_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    # date = serializers.CharField()
    category = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()

    def create(self,data):
        return foodmodel.objects.create(
            Business_id = data['Business_id'],
            food_id = data['food_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            pincode = data['pincode'],
            aadhar_number = data['aadhar_number'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            fssa = data['fssa'],
            region = data['region'],
            # pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            # date = data['date'],
            category = data['category'],
            latitude=data['latitude'],
            longitude=data['longitude'],
        )

class food_list_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    food_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number=serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()
    category = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
class food_edit_serializer(serializers.Serializer):

    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    # region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    # date = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.pincode = data['pincode']
        instance.aadhar_number = data['aadhar_number']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        instance.fssa = data['fssa']
        # instance.region = data['region']
        # instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        # instance.date = data['date']
        instance.latitude=data['latitude']
        instance.longitude=data['longitude']
        instance.save()
        return instance

# foodproducts
    

class food_productlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.CharField()
    category = serializers.CharField()
    subcategory=serializers.CharField()
    product = serializers.JSONField()
    business_status=serializers.CharField()
    rating=serializers.CharField()



# freshcuts
class freshcuts_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    fresh_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    # date = serializers.CharField()
    category = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    def create(self,data):
        return freshcutsmodel.objects.create(
            Business_id = data['Business_id'],
            fresh_id = data['fresh_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            pincode = data['pincode'],
            aadhar_number = data['aadhar_number'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            fssa = data['fssa'],
            region = data['region'],
            # pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            # date = data['date'],
            category=data['category'],
            latitude=data['latitude'],
            longitude=data['longitude'],
        )

class freshcuts_list_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    fresh_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()
    category = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()

class freshcuts_edit_serializer(serializers.Serializer):

    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    # region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    # date = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.pincode = data['pincode']
        instance.aadhar_number = data['aadhar_number']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        instance.fssa = data['fssa']
        # instance.region = data['region']
        # instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        # instance.date = data['date']
        instance.latitude=data['latitude']
        instance.longitude=data['longitude']

        instance.save()
        return instance



class fresh_productlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    status=serializers.CharField()
    category = serializers.CharField()
    subcategory=serializers.CharField()
    product = serializers.JSONField()
    business_status=serializers.CharField()
    rating=serializers.CharField()
# dailymio

class dailymio_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    dmio_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    # date = serializers.CharField()
    category = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    def create(self,data):
        return dailymio_model.objects.create(
            Business_id = data['Business_id'],
            dmio_id = data['dmio_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            pincode = data['pincode'],
            aadhar_number = data['aadhar_number'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            fssa = data['fssa'],
            region = data['region'],
            # pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            # date = data['date'],
            category = data['category'],
            latitude=data['latitude'],
            longitude=data['longitude'],
        )

class dailymio_list_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    dmio_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()
    category = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()


class dailymio_edit_serializer(serializers.Serializer):

    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    # region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    # date = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()

    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.pincode = data['pincode']
        instance.aadhar_number = data['aadhar_number']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        instance.fssa = data['fssa']
        # instance.region = data['region']
        # instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        # instance.date = data['date']
        instance.latitude=data['latitude']
        instance.longitude=data['longitude']
        instance.save()
        return instance

class dmio_productlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    status=serializers.CharField()
    category = serializers.CharField()
    subcategory=serializers.CharField()
    product = serializers.JSONField()
    business_status=serializers.CharField()
    rating=serializers.CharField()

# pharmacy
class pharmacy_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    pharm_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    # date = serializers.CharField()
    category = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()   
    def create(self,data):
        return pharmacy_model.objects.create(
            Business_id = data['Business_id'],
            pharm_id = data['pharm_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            pincode = data['pincode'],
            aadhar_number = data['aadhar_number'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            fssa = data['fssa'],
            region = data['region'],
            # pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            # date = data['date'],
            category=data['category'],
            latitude=data['latitude'],
            longitude=data['longitude'],
        )

class pharmacy_list_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    pharm_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()
    category=serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
class pharmacy_edit_serializer(serializers.Serializer):
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    # region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    # date = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.pincode = data['pincode']
        instance.aadhar_number = data['aadhar_number']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        instance.fssa = data['fssa']
        # instance.region = data['region']
        # instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        # instance.date = data['date']
        instance.latitude=data['latitude']
        instance.longitude=data['longitude']
        instance.save()
        return instance



class pharmacy_productlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    pharm_id = serializers.CharField()
    status=serializers.CharField()
    category = serializers.CharField()
    subcategory=serializers.CharField()
    product = serializers.JSONField()
    business_status=serializers.CharField()
    rating=serializers.CharField()

# d_originalmodel
class d_original_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    d_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    # date = serializers.CharField()
    category =serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()   
    def create(self,data):
        return d_originalmodel.objects.create(
            Business_id = data['Business_id'],
            d_id = data['d_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            pincode = data['pincode'],
            aadhar_number = data['aadhar_number'],
            fssa = data['fssa'],
            region = data['region'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            # pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            # date = data['date'],
            category = data['category'],
            latitude=data['latitude'],
            longitude=data['longitude'],
        )

class d_original_list_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    d_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()
    category = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
class d_original_edit_serializer(serializers.Serializer):
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pincode = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    # region = serializers.CharField()
    # pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    # date = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.pincode = data['pincode']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        instance.fssa = data['fssa']
        # instance.region = data['region']
        # instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        # instance.date = data['date']
        instance.latitude=data['latitude']
        instance.longitude=data['longitude']
        instance.save()
        return instance


class d_original_productlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    d_id = serializers.CharField()
    status=serializers.CharField()
    category = serializers.CharField()
    subcategory=serializers.CharField()
    product = serializers.JSONField()
    district = serializers.CharField()
    business_status=serializers.CharField()
    rating=serializers.CharField()



class notificationlistSerializer(serializers.Serializer):
    notify_id=serializers.CharField()
    recipient = serializers.CharField()
    sender_id = serializers.CharField()
    message_title = serializers.CharField()
    message_desc = serializers.CharField()
    notify_date = serializers.DateField()
    is_read=serializers.BooleanField()