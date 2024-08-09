from api import models
from api import business_serializers
import random
import string
import yagmail


def id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id

def otp_generate():
    return int(random.randrange(1000,9999))

def validate_email(id):
    valid_data = models.Businessmodel.objects.all()
    valid_email = business_serializers.BusinessSerializer(valid_data,many=True)
    data = False
    for i in valid_email.data:
        if id==i['email']:
            data = True
            break
    print("hii")
    return data
    
def validate_otp(id, otp):
    UserData = models.Businessmodel.objects.get(uid = id)
    data = business_serializers.BusinessSerializer(UserData)
    valid = False
    if data.data['otp'] == otp:
        valid = True
    return valid

def verify_user(email, password):
    Data = models.Businessmodel.objects.get(email = email)
    data = business_serializers.BusinessSerializer(Data)
    authentication = False
    if data.data['email'] == email and data.data['password'] == password:
        authentication = True
    print("hii")
    return authentication


def verify_user_otp(email):
    Data = models.Businessmodel.objects.get(email = email)
    data = business_serializers.BusinessSerializer(Data)
    authentication = False
    if data.data['otp'] == data.data['user_otp']:
        authentication = True
    return authentication

def send_mail(receiver_email, otp):
    sender = 'miofeatures2002@gmail.com'
    password = 'xhej oirn pbds ofzs'
    subject = "Miogra Sign Up OTP"
    content = f"""
    OTP : {otp}
    """
    yagmail.SMTP(sender, password).send(
    # yagmail(user = sender,password = password,host='smtp.gmail.com').send(
        to=receiver_email,
        subject=subject,
        contents=content
    )

def get_user_id(email):
    Data = models.Businessmodel.objects.get(email = email)
    data = business_serializers.BusinessSerializer(Data)
    print(data.data["uid"])
    return data.data['uid']


def shop_id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id
def jewel_id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id
def food_id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id
def fresh_id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id
def dmio_id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id
def pharm_id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id
def d_id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id



def product_id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id