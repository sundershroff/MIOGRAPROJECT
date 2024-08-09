from rest_framework import serializers
from api import models

class DeliverypersonSerializer(serializers.Serializer):
    otp=serializers.IntegerField()
    uid = serializers.CharField()
    name = serializers.CharField()
    phone_number = serializers.CharField()
    wp_number = serializers.CharField()
    email = serializers.EmailField()
    aadhar_number = serializers.CharField()
    pan_number = serializers.CharField()
    driving_licensenum = serializers.CharField()
    profile_picture = serializers.CharField()
    bank_name = serializers.CharField()
    acc_number = serializers.CharField()
    name_asper_passbook = serializers.CharField()
    ifsc_code = serializers.CharField()
    bank_passbok_pic = serializers.CharField()
    aadhar_pic = serializers.CharField()
    pan_pic = serializers.CharField()
    drlicence_pic = serializers.CharField()
    delivery_type = serializers.CharField()
    approve_status = serializers.CharField()
    today_earnings = serializers.CharField()
    region =serializers.CharField()
    submit_issues = serializers.CharField()
    upload_issues = serializers.CharField()
    device_id = serializers.CharField()
    total_order_amount=serializers.CharField()
    has_withdrawn =serializers.BooleanField()
    notification_status=serializers.CharField()


class SignupSerializer(serializers.Serializer):
    # Your fields here

    name = serializers.CharField()
    # phone_number = serializers.CharField()
    wp_number = serializers.CharField()
    email = serializers.EmailField()
    aadhar_number = serializers.CharField()
    pan_number = serializers.CharField()
    driving_licensenum = serializers.CharField()
    profile_picture = serializers.CharField()
    bank_name = serializers.CharField()
    acc_number = serializers.CharField()
    name_asper_passbook = serializers.CharField()
    ifsc_code = serializers.CharField()
    bank_passbok_pic = serializers.CharField()
    aadhar_pic = serializers.CharField()
    pan_pic = serializers.CharField()
    drlicence_pic = serializers.CharField()
    delivery_type = serializers.CharField()
    region =serializers.CharField()
    approve_status =serializers.CharField()
    device_id = serializers.CharField()
    def update(self, instance, data):
        instance.name = data['name']
        # instance.phone_number = data['phone_number']
        instance.wp_number = data['wp_number']
        instance.email = data['email']
        instance.aadhar_number = data['aadhar_number']
        instance.pan_number = data['pan_number']
        instance.driving_licensenum = data['driving_licensenum']
        instance.profile_picture = data['profile_picture']
        instance.bank_name = data['bank_name']
        instance.acc_number = data['acc_number']
        instance.name_asper_passbook = data['name_asper_passbook']
        instance.ifsc_code = data['ifsc_code']
        instance.bank_passbok_pic = data['bank_passbok_pic']
        instance.aadhar_pic = data['aadhar_pic']
        instance.pan_pic = data['pan_pic']
        instance.drlicence_pic = data['drlicence_pic']
        instance.delivery_type = data['delivery_type']
        instance.drlicence_pic = data['drlicence_pic']
        instance.region = data['region']
        instance.approve_status = data['approve_status']
        instance.device_id = data['device_id']
        instance.save()
        return instance

    


class deliveryperson_edit_serializer(serializers.Serializer):

    name = serializers.CharField()
    # phone_number = serializers.CharField()
    wp_number = serializers.CharField()
    email = serializers.EmailField()
    aadhar_number = serializers.CharField()
    driving_licensenum = serializers.CharField()
    pan_number = serializers.CharField()
    profile_picture = serializers.CharField()
    bank_name = serializers.CharField()
    acc_number = serializers.CharField()
    name_asper_passbook = serializers.CharField()
    ifsc_code = serializers.CharField()
    bank_passbok_pic = serializers.CharField()
    aadhar_pic = serializers.CharField()
    pan_pic = serializers.CharField()
    drlicence_pic = serializers.CharField()
    delivery_type = serializers.CharField()
    region = serializers.CharField()
    # today_earnings = serializers.CharField()
    def update(self,instance,data):
        instance.name = data["name"]
        # instance.phone_number = data["phone_number"]
        instance.wp_number = data["wp_number"]
        instance.email = data["email"]
        instance.aadhar_number = data["aadhar_number"]
        instance.driving_licensenum = data["driving_licensenum"]
        instance.pan_number = data["pan_number"]
        instance.profile_picture = data["profile_picture"]
        instance.bank_name = data["bank_name"]
        instance.acc_number = data["acc_number"]
        instance.name_asper_passbook = data["name_asper_passbook"]
        instance.ifsc_code = data["ifsc_code"]
        instance.bank_passbok_pic = data["bank_passbok_pic"]
        instance.aadhar_pic = data["aadhar_pic"]
        instance.pan_pic = data["pan_pic"]
        instance.drlicence_pic = data["drlicence_pic"]
        instance.delivery_type = data["delivery_type"]
        instance.region =data['region']
        
        # instance.today_earnings = data['today_earnings']
        instance.save()
        return instance


class delivery_yourissue_serializer(serializers.Serializer):
    submit_issues = serializers.CharField()
    upload_issues = serializers.CharField()
    def update(self,instance,data):
        instance.submit_issues = data["submit_issues"]
        instance.upload_issues = data['upload_issues']
        instance.save()
        return instance


class deliverytimetablelistSerializer(serializers.Serializer):
    today_date= serializers.DateField()
    login_time = serializers.TimeField()
    logout_time= serializers.TimeField()
    deliveryperson= serializers.PrimaryKeyRelatedField(queryset=models.Delivery_model.objects.all())
    status=serializers.BooleanField()
    # Your fields here

class OTPSerializer(serializers.Serializer):
    user_otp = serializers.IntegerField()
    
    def update(self, instance, data):
        instance.user_otp = data['user_otp']
        instance.save()
        return instance
    




class notificationlistSerializer(serializers.Serializer):
    recipient = serializers.CharField()
    message_title = serializers.CharField()
    message_desc = serializers.CharField()
    notify_date = serializers.DateField()
    earnings = serializers.CharField()
    amount = serializers.CharField()
    is_read=serializers.BooleanField()