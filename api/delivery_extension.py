from api import models
from api import delivery_serializers
import random
import string
import yagmail


def id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id

    
def validate_email(email):
    email_exists = models.Delivery_model.objects.filter(email=email).exists()
    return email_exists

    
def verify_user(phone_number):
    Data = models.Delivery_model.objects.get(phone_number = phone_number)
    data = delivery_serializers.DeliverypersonSerializer(Data)
    authentication = False
    if data.data['phone_number'] == phone_number:
        authentication = True
    print("hii")
    return authentication



def get_user_id(phone_number):
    Data = models.Delivery_model.objects.get(phone_number = phone_number)
    data = delivery_serializers.DeliverypersonSerializer(Data)
    print(data.data["uid"])
    return data.data['uid']



def validate_otp(id, otp):
    UserData = models.Delivery_model.objects.get(uid = id)
    data = delivery_serializers.DeliverypersonSerializer(UserData)
    valid = False
    if data.data['otp'] == otp:
        valid = True
    return valid

def verify_user_otp(phone_number):
    Data = models.Delivery_model.objects.get(phone_number = phone_number)
    data = delivery_serializers.DeliverypersonSerializer(Data)
    authentication = False
    if data.data['otp'] == data.data['user_otp']:
        authentication = True
    return authentication