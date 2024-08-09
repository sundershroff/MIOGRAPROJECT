from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
import requests
import json
from django.contrib.auth.models import User,auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from rest_framework.response import Response
from django.contrib import messages
from collections import Counter

jsondec = json.decoder.JSONDecoder()
#shopping Without user
@csrf_exempt
def shop(request):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['shopping'] == False:
        return redirect("/soon/")
    else:
    # print(shopping)
        shopdata = requests.get("https://miogra.clovion.org/all_shopproducts").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/shopping").json()[0]
        context={
            
        'shop':shopdata,
        'banner':banner,
        
            }
            
        return render(request,"index.html",context)
    

@csrf_exempt
def shop_products(request,category):
    product_data=requests.get(f"https://miogra.clovion.org/category_based_shop/{category}/").json()
    # print(product_data.content)
    print(type(product_data))
    products=[]
    for x in product_data:
        shop_id= x.get('shop_id')
        shop=requests.get(f"https://miogra.clovion.org/my_shopping_data/{shop_id}").json()
        products.append({'items' : x, 'shop':shop})   
    context={
            'products' : products,
             }

    return render(request,"shop-left-sidebar.html",context)

@csrf_exempt
def shop_based_product(request):
    # product_data=requests.get(f"https://miogra.clovion.org/shop_get_products/{id}").json()
    shop_data = requests.get("https://miogra.clovion.org/all_shopproducts").json()
    
    print(shop_data)
    context ={
        'shop':shop_data,
        
    }
    
    return render(request,"shops_product_only.html",context)

@csrf_exempt
def single_shopproducts(request,id,product_id):
    single_product=requests.get(f"https://miogra.clovion.org/get_single_shopproduct/{id}/{product_id}").json()[0]
    product_review = requests.get(f"https://miogra.clovion.org/get_all_reviews/").json()
    review=[]
    for x in product_review:
        if product_id == x.get('product_id'):
            review.append(x)
        

    context={
        'single' : single_product,
        'reviews' : review,
    }

    return render(request,"single-product.html",context)

@csrf_exempt
def food(request):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['food'] == False:
        return redirect("/soon/")
    else:
        food_data= requests.get("https://miogra.clovion.org/all_foodproducts/").json()
        shop_data =requests.get("https://miogra.clovion.org/food_alldata").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/food").json()[0]
        print(shop_data)

        context={
            'food':food_data,
            'shops' : shop_data,
            'banner': banner
        }

        return render(request,"food_index.html",context)

@csrf_exempt
def food_products(request,category):
    food_product=[]
    food_data=requests.get(f"https://miogra.clovion.org/category_based_food/{category}/").json()
    # print(product_data.content)
    print((food_data))
    for x in food_data:
        food_id=x.get('food_id')
        hotel=requests.get(f"https://miogra.clovion.org/my_food_data/{food_id}").json()
        food_product.append({'food_item': x, 'hotel': hotel})
    
    context={
            'foods' : food_product,
            
             }

    return render(request,"food_shop-left-sidebar.html",context)

@csrf_exempt
def restaurant_based_products(request,id):
    restaurant=requests.get(f"https://miogra.clovion.org/my_food_data/{id}").json()
    products= requests.get(f"https://miogra.clovion.org/enduser_resturant_get_products/{id}").json()
    
    context ={
        'shop':restaurant,
        'foods':products
    }
    
    return render(request,"restaurant_based_product.html",context)
    

@csrf_exempt
def single_food_products(request,id,product_id):
    food_data=requests.get(f"https://miogra.clovion.org/single_foodproduct/{id}/{product_id}").json()[0]
    reviews=requests.get(f"https://miogra.clovion.org/get_product_all_reviews/{product_id}").json()
    # print(product_data.content)
    print((food_data))
   

       
    context={
            'foods': food_data,
            'reviews' :reviews,
             }

    return render(request,"food_single-product.html",context)

@csrf_exempt
def fresh_cuts(request):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['fresh_cuts'] == False:
        return redirect("/soon/")
    else:
        fresh_data= requests.get("https://miogra.clovion.org/all_freshcutproducts/").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/fresh_cuts").json()[0]
        print(fresh_data)

        context={
            'fresh':fresh_data,
            'banner' :banner
        }

        return render(request,"fresh_cuts_index.html",context)

@csrf_exempt
def fresh_cut_products(request,category):
    fresh_data=requests.get(f"https://miogra.clovion.org/category_based_fresh/{category}/").json()
    # print(product_data.content)
    print(type(fresh_data))
    products=[]
    for x in fresh_data:
        shop_id= x.get('fresh_id')
        shop=requests.get(f"https://miogra.clovion.org/my_freshcuts_data/{shop_id}").json()
        products.append({'item' : x, 'shop':shop})   
    context={
            'fresh_cuts' : products,
             }   
   

    return render(request,"fresh_cuts-left-sidebar.html",context)

@csrf_exempt
def freshShop_based_products(request,id):
    shop=requests.get(f"https://miogra.clovion.org/my_freshcuts_data/{id}").json()
    products=requests.get(f"https://miogra.clovion.org/fresh_get_products/{id}").json()
    context={
        'shop':shop,
        'fresh_cuts': products
    }
    return render(request,"freshshop_based_product.html",context)

@csrf_exempt
def fresh_cut_singel_products(request,id,product_id):
    fresh_data=requests.get(f"https://miogra.clovion.org/single_freshproduct/{id}/{product_id}").json()[0]
    reviews = requests.get(f"https://miogra.clovion.org/get_product_all_reviews/{product_id}").json()
    # print(product_data.content)
    print((fresh_data))
       
    context={
            'fresh_cuts': fresh_data,
            'reviews' :reviews,
             }

    return render(request,"fresh_cuts_single-product.html",context)


@csrf_exempt
def doriginal(request):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['d_original'] == False:
        return redirect("/soon/")
    else:
        dorigin_data= requests.get("https://miogra.clovion.org/all_d_originalproducts/").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/d_original").json()[0]
        # print(dorigin_data)
        products=[]
        for x in dorigin_data:
            shop_id= x.get('d_id')
            shop=requests.get(f"https://miogra.clovion.org/my_d_original_data/{shop_id}").json()
            products.append({'item' : x, 'shop':shop})

        
        if "district" in request.POST:
            if request.POST['district'] == '':
                return redirect("/doriginalproducts/doriginal")
            else:
                district = request.POST['district']
                return redirect(f"/doriginalproducts/district_based/{district}/")

        

        context={
            'dorigin':products,
            'banner' :banner
        }
        return render(request,"doriginal_index.html",context)

@csrf_exempt
def dorigin_district_based_products(request,district):
    dorigin_district=requests.get(f"https://miogra.clovion.org/d_original_district_based_product/{district}").json()
    print(dorigin_district)

    if "district" in request.POST:
        if request.POST['district'] == '':
            return redirect("/doriginalproducts/doriginal")
        else:
            district = request.POST['district']
            return redirect(f"/doriginalproducts/district_based/{district}/")
        
    context = {
        'd_origins':  dorigin_district,
    }
    return render(request,"d_origin_district_based.html",context)

@csrf_exempt
def d_original_single_products(request,d_id,product_id):
    dorigin_data=requests.get(f"https://miogra.clovion.org/single_d_originalproduct/{d_id}/{product_id}").json()[0]
    reviews = requests.get(f"https://miogra.clovion.org/get_product_all_reviews/{product_id}").json()
    
    context={
        'd_origin' : dorigin_data,
        'reviews' : reviews,
    }
    return render(request,"doriginal_single_product.html",context)

@csrf_exempt
def daily_mio(request):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['daily_mio'] == False:
        return redirect("/soon/")
    else:
        dmio_data= requests.get("https://miogra.clovion.org/all_dmioproducts/").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/daily_mio").json()[0]
        print(dmio_data)

        context={
            'dmio':dmio_data,
            'banner'  :banner
        }
        return render(request,"daily_mio_index.html",context)

@csrf_exempt
def daily_mio_products(request,category):
    dmio_data= requests.get(f"https://miogra.clovion.org/category_based_dmio/{category}/").json()
    print(dmio_data)
    products=[]
    for x in dmio_data:
        shop_id= x.get('dmio_id')
        shop=requests.get(f"https://miogra.clovion.org/my_dailymio_data/{shop_id}").json()
        products.append({'item' : x, 'shop':shop})
    context={
        'dmios':products,
    }
    return render(request,"daily_mio_shop-left-sidebar.html",context)

@csrf_exempt
def dmioshop_based_products(request,id):
    shop=requests.get(f"https://miogra.clovion.org/my_dailymio_data/{id}").json()
    products=requests.get(f"https://miogra.clovion.org/dmio_get_products/{id}").json()
    context = {
        'shop' : shop,
        'dmios': products
    }
    
    
    return render(request,"dmioshop_based_product.html",context)

@csrf_exempt
def daily_mio_single_products(request,id,product_id):
    dmio_data= requests.get(f"https://miogra.clovion.org/get_single_dmio_product/{id}/{product_id}").json()[0]
    reviews = requests.get(f"https://miogra.clovion.org/get_product_all_reviews/{product_id}").json()
    print(dmio_data)

    context={
        'dmios':dmio_data,
        'reviews' : reviews
    }
    return render(request,"daily_mio_single_product.html",context)

@csrf_exempt
def jewellery(request):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['jewellery'] == False:
        return redirect("/soon/")
    else:
        jewel_data= requests.get("https://miogra.clovion.org/all_jewelproducts/").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/jewellery").json()[0]
        print(jewel_data)

        context={
            'jewels': jewel_data,
            'banner' :banner
        }
        return render(request,"jwellery_index.html",context)

@csrf_exempt
def jewellery_products(request,category):
    jewel_data= requests.get(f"https://miogra.clovion.org/category_based_jewel/{category}/").json()
    
    print(jewel_data)
    products=[]
    for x in jewel_data:
        shop_id= x.get('jewel_id')
        shop=requests.get(f"https://miogra.clovion.org/my_jewellery_data/{shop_id}").json()
        products.append({'item' : x, 'shop':shop})
    context={
        'jewels': products,
        
    }
    return render(request,"jwellery_shop-left-sidebar.html",context)

@csrf_exempt
def jewelshop_based_products(request,id):
    shop=requests.get(f"https://miogra.clovion.org/my_jewellery_data/{id}").json()
    products=requests.get(f"https://miogra.clovion.org/jewel_get_products/{id}").json() 
    
    context = {
        'shop' :shop, 
        'jewels' :products
    }
    
    return render(request,"jewelshop_based_products.html",context)

@csrf_exempt
def jewellery_single_products(request,id,product_id):
    jewel_data= requests.get(f"https://miogra.clovion.org/single_jewelproduct/{id}/{product_id}").json()[0]
    product_review = requests.get(f"https://miogra.clovion.org/get_all_reviews/").json()
    reviews=[]
    for x in product_review:
        if product_id == x.get('product_id'):
            reviews.append(x)
   
        
    context={
        'jewels': jewel_data,
        'reviews':reviews
    }
    return render(request,"jwellery_single_product.html",context)

@csrf_exempt
def pharmacy(request):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['pharmacy'] == False:
        return redirect("/soon/")
    else:
        pharm_data= requests.get("https://miogra.clovion.org/all_pharmproducts/").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/pharmacy").json()[0]
        print(pharm_data)
        

        context={
            'pharms':pharm_data,
            'banner' :banner
        }
        return render(request,"pharmacy_index.html",context)

@csrf_exempt
def pharmac_products(request,category):
    pharm_data= requests.get(f"https://miogra.clovion.org/category_based_pharm/{category}/").json()
    print(pharm_data)
    products=[]
    for x in pharm_data:
        shop_id= x.get('pharm_id')
        shop=requests.get(f"https://miogra.clovion.org/my_pharmacy_data/{shop_id}").json()
        products.append({'item' : x, 'shop':shop})

    context={
        'pharms':products,
    }
    return render(request,"pharmacy_shop-left-sidebar.html",context)

@csrf_exempt
def medicalshop_products(request,id):
    shop=requests.get(f"https://miogra.clovion.org/my_pharmacy_data/{id}").json()
    products=requests.get(f"https://miogra.clovion.org/pharmacy_get_products/{id}").json()
    
    context = {
        'shop' : shop,
        'pharms' : products
    }
    
    return render(request,"medical_shop_based.html",context)

@csrf_exempt
def pharmac_single_products(request,id,product_id):
    pharm_data= requests.get(f"https://miogra.clovion.org/single_pharmproduct/{id}/{product_id}").json()[0]
    reviews = requests.get(f"https://miogra.clovion.org/get_product_all_reviews/{product_id}").json()

    print(pharm_data)
    
    context={
        'pharms':pharm_data,
        'reviews' : reviews
    }
    return render(request,"pharmacy_single-product.html",context)

@csrf_exempt
def used_product(request):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['used_products'] == False:
        return redirect("/soon/")
    else:
        used_product=requests.get("https://miogra.clovion.org/get_allused_products/").json()
        # print(used_product)
        print(type(used_product))
    
        context={
            'products' : used_product,
            'produc' : used_product[::-1]
        }
        return render(request,"used_product_index.html",context)

@csrf_exempt
def used_product_category(request,subcategory):
    used_product=requests.get(f"https://miogra.clovion.org/get_used_products_category/{subcategory}/").json()
    # print(used_product)
    print(type(used_product))
    # products=[]
    # for x in pharm_data:
    #     shop_id= x.get('pharm_id')
    #     shop=requests.get(f"https://miogra.clovion.org/my_pharmacy_data/{shop_id}").json()
    #     products.append({'item' : x, 'shop':shop})

    context={
        'products':used_product,
    }
    return render(request,"used_product_left-sidebar.html",context)


@csrf_exempt
def usedproduct_single_data(request,product_id):
    used_data= requests.get(f"https://miogra.clovion.org/get_single_used_products/{product_id}").json()

    product_details = used_data[0]['product']
    products=dict(product_details)
    
    keys_to_remove = ["other_images", "primary_image", "description", "productId", 
                      "product_id", "category", "Category", "subcategory", 
                      "contact", "location"]
    
    for key in keys_to_remove:
        if key in products:
            products.pop(key)
            
    # print("typet",type(products))
    # print(products)
    formatted_data =[(key, value) for key, value in products.items()]
    print("formatted_data",formatted_data)
    context={
        'used':used_data,
        'product':product_details,
        'formated':formatted_data,
    }
    return render(request,"usedproduct_single_data.html",context)
# <------------------End of Before login------------------------------------------------>

#<---------------------------End-User Afer Login----------------------------------------------------------->

@csrf_exempt
def signout_view(request,id):
    # mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    logout(request)
    return redirect("/")

@csrf_exempt
def usersignup(request):
    error = ""
    if request.method == "POST":
        print(request.POST)
        if request.POST['password'] == request.POST['confirm_password']:
                response = requests.post("https://miogra.clovion.org/end_user_signup/",data=request.POST)
                print(response.status_code)
                print(response.text)
                uidd = (response.text[1:-1]) 
                print(uidd)
                if response.status_code == 200:
                   return redirect(f"/enduser/end_user_otp/{uidd}")
                elif response.status_code == 302:
                    error = "User Already Exist"
        else:
            print("password doesn't match")
    context = {'error':error}
    return render(request,"enduser_signup.html",context)

@csrf_exempt
def usersignin(request):

    error = ""
    if request.method == "POST":
        print(request.POST)
        response = requests.post("https://miogra.clovion.org/end_user_signin/",data=request.POST)
        uid = jsondec.decode(response.text)
        if response.status_code == 200:
            mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{uid}").json()[0]
            print(mydata.get("otp"))
            if mydata.get("otp") == None:
                return redirect(f"/enduser/end_user_otp/{uid}")
            else:
                return redirect(f"/products/foodproducts/food/{uid}")
        else:
          error = "YOUR EMAIL OR PASSWORD IS INCORRECT"
    context = {'error':error}
    return render(request,"enduser_signin.html",context)

@csrf_exempt
def otp(request,id):
    context = {'invalid':"invalid",'id':id}
    new=[]
    if request.method == "POST":
        new.append(request.POST["otp1"])
        new.append(request.POST["otp2"])
        new.append(request.POST["otp3"])
        new.append(request.POST["otp4"])
        data = {
            'user_otp':int(''.join(new).strip())
           
        }
        print(data)
        response = requests.post(f"https://miogra.clovion.org/end_user_otp/{id}", data=data)
        print(response)
        print(response.status_code)
        print(data['user_otp'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:

            return redirect(f"/products/foodproducts/food/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid,'id':id}
    return render(request,"enduser_otpcheck.html",context)
    
@csrf_exempt
def resend_otp(request,id):
    response=requests.post(f"https://miogra.clovion.org/endresend_otp/{id}")
    if response.status_code == 200:
        return redirect(f"/enduser/end_user_otp/{id}")
    else:
        context={'invalid':"Server Error",'id':id}
        return render(request,"enduser_otpcheck.html",context)
        
@csrf_exempt
def profile_picture(request,id):
    if request.method == "POST":
        print(request.FILES)
        response = requests.post(f"https://miogra.clovion.org/end_profile_picture/{id}",  files=request.FILES)
        print(response)
        print(response.status_code)
        print(response.text)
        uidd = (response.text[1:-1])
        if response.status_code == 200:
            return redirect(f"/products/foodproducts/food/{uidd}")
            
        else:
            return HttpResponse("INVALId")
    return render(request,"enduser_profilepic.html")

@csrf_exempt
def dashboard(request,id):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['shopping'] == False:
        return redirect(f"/comming/{id}")
    else:
        mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
        shopdata = requests.get("https://miogra.clovion.org/all_shopproducts").json()
        wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/shopping").json()[0]
        cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
        cartcount= len(cartlist)
        wishcount= len(wishlist)
        tot=0
        for i in cartlist:
            tot += float(i.get('total'))
        print(type(shopdata))
        context={
            
            'key':mydata,
            'shopdata':shopdata,
            'category' :"shopping",
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'banner': banner,
            'tot':tot
        
            }
        return render(request,"user_dashboard.html",context)

@csrf_exempt
def shopproduct_category(request,id,category):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    product_data=requests.get(f"https://miogra.clovion.org/category_based_shop/{category}/").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    products=[]
    for x in product_data:
        shop_id= x.get('shop_id')
        shop=requests.get(f"https://miogra.clovion.org/my_shopping_data/{shop_id}").json()
        products.append({'items' : x, 'shop':shop})
    # print(product_data.content)   
    context={

            'key': mydata,
            'products' : products,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot

             }

    return render(request,"user_shopproduct_category.html",context)

@csrf_exempt
def user_shopbased_products(request,id,shop_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    product_data=requests.get(f"https://miogra.clovion.org/shop_get_products/{shop_id}").json()
    shop_data =requests.get(f"https://miogra.clovion.org/my_shopping_data/{shop_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    
    print(shop_data)
    context ={
        'key' : mydata,
        'shop':shop_data,
        'products':product_data,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot
    }
    
    return render(request,"user_shopbased_product.html",context)

@csrf_exempt
def user_single_products(request,id,shop_id,product_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    single_product=requests.get(f"https://miogra.clovion.org/get_single_shopproduct/{shop_id}/{product_id}").json()[0]
    reviews=requests.get(f"https://miogra.clovion.org/get_product_all_reviews/{product_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    print(single_product)
    if request.method=="POST":
        if "add_cart" in request.POST:
            quantity=request.POST['quantity']
            data={
                'quantity' :quantity,
                'shop_id': shop_id,
                'product_id':product_id,
            'category' :"shopping",
            

            }
            response = requests.post(f"https://miogra.clovion.org/cart_product/{id}/{product_id}/shopping/",data=data)
            if response.status_code == 200:
                return redirect(f"/user/shopping_cart_products/{id}/")
            else:
                pass
    
        if "reviewsubmit"  in request.POST:
            product_id=request.POST['productId']

            data={
                "id":id,
                'product_id' : product_id,
                'rating' : request.POST['rating'],
                'comment' :request.POST['comment'],
            }
            print(data)
            response=requests.post(f"https://miogra.clovion.org/create_reviews_for_delivered_products/{id}/{product_id}/",data=data)
            if response.status_code == 201:
                category="shopping"
                rating_up=requests.post(f"https://miogra.clovion.org/calculate_average_ratings/{category}")
                print(rating_up.status_code)
                return redirect(f"/products/singleproduct/enduser/{id}/{shop_id}/{product_id}")
    context={
        
        'key':mydata,
        'single':single_product,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'reviews' : reviews,
        'tot':tot
    
        }

    return render(request,"single_shop_product.html",context)

@csrf_exempt
def user_foodpage(request,id):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['food'] == False:
        return redirect(f"/comming/{id}")
    else:
        mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
        food_data= requests.get("https://miogra.clovion.org/all_foodproducts/").json()
        shop_data =requests.get("https://miogra.clovion.org/food_alldata").json()
        wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/food").json()[0]
        cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
        cartcount= len(cartlist)
        wishcount= len(wishlist)
        tot=0
        for i in cartlist:
            tot += float(i.get('total'))
        print(wishcount)
        for x in food_data:
            fid=x.get('food_id')
            rating_up=requests.post(f"https://miogra.clovion.org/restautant/review/{fid}")
            if rating_up.status_code == 200:
                print("")
            else:
                print("error")

        food_product=[]
        for x in food_data:
            food_id=x.get('food_id')
            hotel=requests.get(f"https://miogra.clovion.org/my_food_data/{food_id}").json()
            food_product.append({'item': x, 'shop': hotel})
          
        print(shop_data)
        context={
            'key' : mydata,
            'foods':food_product,
            'shops':shop_data,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'banner': banner,
            'tot':tot,  
            }

        return render(request,"user_food_index.html",context)

@csrf_exempt
def food_products_category(request,id,category):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    food_data=requests.get(f"https://miogra.clovion.org/category_based_food/{category}/").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    # print(product_data.content)
    food_product=[]
    print((food_data))
    for x in food_data:
        food_id=x.get('food_id')
        hotel=requests.get(f"https://miogra.clovion.org/my_food_data/{food_id}").json()
        food_product.append({'item': x, 'shop': hotel})   
    context={
            'key' : mydata,
            'foods' : food_product,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot,
             }

    return render(request,"user_food_category.html",context)

@csrf_exempt
def user_restaurant_products(request,id,food_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    restaurant=requests.get(f"https://miogra.clovion.org/my_food_data/{food_id}").json()
    products= requests.get(f"https://miogra.clovion.org/enduser_resturant_get_products/{food_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    
    context ={
        'key' : mydata,
        'shop':restaurant,
        'foods':products,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot,
    }
    if request.method == "POST":
        print(request.POST)
    return render(request,"user_restaurants.html",context)

@csrf_exempt
def user_singlefood_products(request,id,shop_id,product_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    food_data=requests.get(f"https://miogra.clovion.org/single_foodproduct/{shop_id}/{product_id}").json()[0]
    reviews=requests.get(f"https://miogra.clovion.org/get_product_all_reviews/{product_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
   # print(product_data.content)
    
    print((food_data))
    if request.method=="POST":
        if "add_cart" in request.POST:
            quantity=request.POST['quantity']
            data={
                'quantity' :quantity,
                'shop_id': shop_id,
                'product_id':product_id,
            'category' :"food",
            'cartcount':cartcount,
                'wishcount' : wishcount,
                'cart_data':cartlist,
                'reviews' : reviews

            }
            response = requests.post(f"https://miogra.clovion.org/cart_product/{id}/{product_id}/food/",data=data)
            if response.status_code == 200:
                return redirect(f"/user/food_cart/{id}/")
            else:
                pass
        elif "reviewsubmit" in request.POST:
            product_id=request.POST['productId']

            print(request.POST)
            data={
                "id":id,
                'product_id' : product_id,
                'rating' : request.POST['rating'],
                'comment' :request.POST['comment'],
            }
            print('data',data)
            response=requests.post(f"https://miogra.clovion.org/create_reviews_for_delivered_products/{id}/{product_id}/",data=data)
            print(response.status_code)
            if response.status_code == 201:
                category="food"
                rating_up=requests.post(f"https://miogra.clovion.org/calculate_average_ratings/{category}")
                print(rating_up.status_code)
                return redirect(f"/products/food_products/single_food/{id}/{shop_id}/{product_id}")     

    context={
             'key' : mydata,
             'foods': food_data,
             'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot,
             'reviews' : reviews,
             }

    return render(request,"user_singlefood.html",context)

@csrf_exempt
def user_fresh_cuts(request,id):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['fresh_cuts'] == False:
        return redirect(f"/comming/{id}")
    else:
        mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
        fresh_data= requests.get("https://miogra.clovion.org/all_freshcutproducts/").json()
        wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
        cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/fresh_cuts").json()[0]
        cartcount= len(cartlist)
        wishcount= len(wishlist)
        tot=0
        for i in cartlist:
            tot += float(i.get('total'))
        print(fresh_data)

        context={
            'key' : mydata,
            'fresh':fresh_data,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'banner':banner,
            'tot':tot
        }

        return render(request,"user_freshcuts_index.html",context)

@csrf_exempt
def user_freshcut_products(request,id,category):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    fresh_data=requests.get(f"https://miogra.clovion.org/category_based_fresh/{category}/").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    # print(product_data.content)
    print(type(fresh_data))
    products=[]
    for x in fresh_data:
        fresh_id=x.get('fresh_id')
        shop=requests.get(f"https://miogra.clovion.org/my_freshcuts_data/{fresh_id}").json()
        products.append({'item': x, 'shop': shop})
    
       
    context={
            'key' : mydata,
            'fresh_cuts' : products,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot
             }

    return render(request,"user_freshcut_sidebar.html",context)

@csrf_exempt
def user_freshcut_shop_products(request,id,fresh_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    shop=requests.get(f"https://miogra.clovion.org/my_freshcuts_data/{fresh_id}").json()
    products=requests.get(f"https://miogra.clovion.org/fresh_get_products/{fresh_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    context={
        'key' : mydata,
        'shop':shop,
        'fresh_cuts': products,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot
    }
    return render(request,"user_freshcut_shops.html",context)

@csrf_exempt
def user_freshcut_single_products(request,id,shop_id,product_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    fresh_data=requests.get(f"https://miogra.clovion.org/single_freshproduct/{shop_id}/{product_id}").json()[0]
    reviews=requests.get(f"https://miogra.clovion.org/get_product_all_reviews/{product_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    # print(product_data.content)
    print((fresh_data))
    if request.method=="POST":
        if "add_cart" in request.POST:
            quantity=request.POST['quantity']
            data={
                'quantity' :quantity,
                'shop_id': shop_id,
                'product_id':product_id,
            'category' :"fresh_cuts",
            'cartcount':cartcount,
                'wishcount' : wishcount,
                'cart_data':cartlist

            }
            response = requests.post(f"https://miogra.clovion.org/cart_product/{id}/{product_id}/fresh_cuts/",data=data)
            if response.status_code == 200:
                return redirect(f"/user/shopping_cart_products/{id}/")
            else:
                pass
        elif "reviewsubmit"  in request.POST:
            product_id=request.POST['productId']

            data={
                "id":id,
                'product_id' : product_id,
                'rating' : request.POST['rating'],
                'comment' :request.POST['comment'],
            }
            print(data)
            response=requests.post(f"https://miogra.clovion.org/create_reviews_for_delivered_products/{id}/{product_id}/",data=data)
            if response.status_code == 201:
                category="freshcuts"
                rating_up=requests.post(f"https://miogra.clovion.org/calculate_average_ratings/{category}")
                print(rating_up.status_code)
                return redirect(f"/products/freshproducts/single_product/{id}/{shop_id}/{product_id}") 
          
    context={
            'key': mydata,
            'fresh_cuts': fresh_data,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'reviews': reviews,
            'tot':tot
             }

    return render(request,"user_freshcut_single.html",context)


@csrf_exempt
def user_doriginal(request,id):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['d_original'] == False:
        return redirect(f"/comming/{id}")
    else:
        mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
        dorigin_data= requests.get("https://miogra.clovion.org/all_d_originalproducts/").json()
        wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
        cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/d_original").json()[0]
        cartcount= len(cartlist)
        wishcount= len(wishlist)
        tot=0
        for i in cartlist:
            tot += float(i.get('total'))
        print(dorigin_data)
        products=[]
        for x in dorigin_data:
            shop_id= x.get('d_id')
            shop=requests.get(f"https://miogra.clovion.org/my_d_original_data/{shop_id}").json()
            products.append({'item' : x, 'shop':shop})

        
        if "district" in request.POST:
            if request.POST['district'] == '':
                return redirect(f"/products/doriginalproducts/doriginal/{id}")
            else:
                district = request.POST['district']
                return redirect(f"/products/doriginal/district/{id}/{district}/")


        context={
        'key': mydata,
            'dorigin':dorigin_data,
            'cartcount':cartcount,
                'wishcount' : wishcount,
                'cart_data':cartlist,
                'banner':banner,
                'tot':tot
        }
        return render(request,"user_dorigin_index.html",context)

@csrf_exempt
def user_dorigin_district(request,id,district):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    dorigin_district=requests.get(f"https://miogra.clovion.org/d_original_district_based_product/{district}").json()
    print(dorigin_district)
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))

    if "district" in request.POST:
        if request.POST['district'] == '':
            pass

        else:
            district = request.POST['district']
            return redirect(f"/products/doriginal/district/{id}/{district}/")


    context = {
        'key': mydata,
        'd_origins': dorigin_district,
        'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot

    }
    return render(request,"user_dorigin_district.html",context)

@csrf_exempt
def user_doriginal_single_products(request,id,shop_id,product_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    dorigin_data=requests.get(f"https://miogra.clovion.org/single_d_originalproduct/{shop_id}/{product_id}").json()[0]
    reviews=requests.get(f"https://miogra.clovion.org/get_product_all_reviews/{product_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    if request.method=="POST":
        if "add_cart" in request.POST:
            quantity=request.POST['quantity']
            data={
                'quantity' :quantity,
                'shop_id': shop_id,
                'product_id':product_id,
            'category' :"d_original",
            'cartcount':cartcount,
                'wishcount' : wishcount,
                'cart_data':cartlist

            }
            response = requests.post(f"https://miogra.clovion.org/cart_product/{id}/{product_id}/d_original/",data=data)
            if response.status_code == 200:
                return redirect(f"/products/doriginalproducts/doriginal/{id}")
            else:
                pass

        elif "reviewsubmit" in request.POST:
            product_id=request.POST['productId']

            data={
                "id":id,
                'product_id' : product_id,
                'rating' : request.POST['rating'],
                'comment' :request.POST['comment'],
            }
            print(data)
            response=requests.post(f"https://miogra.clovion.org/create_reviews_for_delivered_products/{id}/{product_id}/",data=data)
            if response.status_code == 201:
                category="d_original"
                rating_up=requests.post(f"https://miogra.clovion.org/calculate_average_ratings/{category}")
                print(rating_up.status_code)
                return redirect(f"/products/doriginalproducts/doriginal/{id}/{shop_id}/{product_id}")
    context={
      'key':mydata,
        'd_origin' : dorigin_data,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'reviews' : reviews,
        'tot':tot
    }
    return render(request,"user_dorigin_single.html",context)

@csrf_exempt
def user_daily_mio(request,id):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['daily_mio'] == False:
        return redirect(f"/comming/{id}")
    else:
        mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
        dmio_data= requests.get("https://miogra.clovion.org/all_dmioproducts/").json()
        wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
        cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/daily_mio").json()[0]
        cartcount= len(cartlist)
        wishcount= len(wishlist)
        tot=0
        for i in cartlist:
            tot += float(i.get('total'))
        print(dmio_data)

        context={
        'key': mydata,
            'dmio':dmio_data,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'banner': banner,
            'tot':tot
        }
        return render(request,"user_dmio.html",context)

@csrf_exempt
def user_dmio_products(request,id,category):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    dmio_data= requests.get(f"https://miogra.clovion.org/category_based_dmio/{category}/").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    print(dmio_data)
    # products=[]
    # for x in dmio_data:
    #     shop_id= x.get('dmio_id')
    #     shop=requests.get(f"https://miogra.clovion.org/my_dailymio_data/{shop_id}").json()
    #     print(shop.text)
    #     products.append({'item' : x, 'shop':shop})
   

    context={
         'key':mydata,
        'dmios':dmio_data,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot
    }
    return render(request,"user_dmio_category.html",context)

@csrf_exempt
def user_dmioshops_products(request,id,dmio_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    shop=requests.get(f"https://miogra.clovion.org/my_dailymio_data/{dmio_id}").json()
    products=requests.get(f"https://miogra.clovion.org/dmio_get_products/{dmio_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    context = {
        'key' : mydata,
        'shop' : shop,
        'dmios': products,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot
    }
    
    
    return render(request,"user_dmio_shops.html",context)

@csrf_exempt
def user_dailymio_single_products(request,id,shop_id,product_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    dmio_data= requests.get(f"https://miogra.clovion.org/get_single_dmio_product/{shop_id}/{product_id}").json()[0]
    reviews=requests.get(f"https://miogra.clovion.org/get_product_all_reviews/{product_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    print(dmio_data)
    if request.method=="POST":
        if "add_cart" in request.POST:
            quantity=request.POST['quantity']
            data={
                'quantity' :quantity,
                'shop_id': shop_id,
                'product_id':product_id,
            'category' :"daily_mio",
            

            }
            response = requests.post(f"https://miogra.clovion.org/cart_product/{id}/{product_id}/daily_mio/",data=data)
            if response.status_code == 200:
                return redirect(f"/user/shopping_cart_products/{id}/")
            else:
                pass
        elif "reviewsubmit"  in request.POST:
            product_id=request.POST['productId']

            data={
                "id":id,
                'product_id' : product_id,
                'rating' : request.POST['rating'],
                'comment' :request.POST['comment'],
            }
            print(data)
            response=requests.post(f"https://miogra.clovion.org/create_reviews_for_delivered_products/{id}/{product_id}/",data=data)
            if response.status_code == 201:
                category="dailymio"
                rating_up=requests.post(f"https://miogra.clovion.org/calculate_average_ratings/{category}")
                print(rating_up.status_code)
                return redirect(f"/products/dailymioproducts/dmio_singleproduct/{id}/{shop_id}/{product_id}")

    context={
          'key':mydata,
        'dmios':dmio_data,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'reviews' :reviews,
        'tot':tot
    }
    return render(request,"user_dmio_singlepage.html",context)

@csrf_exempt
def user_jewellery(request,id):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['jewellery'] == False:
        return redirect(f"/comming/{id}")
    else:
        mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
        jewel_data= requests.get("https://miogra.clovion.org/all_jewelproducts/").json()
        wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
        cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/jewellery").json()[0]
        cartcount= len(cartlist)
        wishcount= len(wishlist)
        tot=0
        for i in cartlist:
            tot += float(i.get('total'))
        print(jewel_data)

        context={
            'key':mydata,
            'jewels': jewel_data,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'banner':banner,
            'tot':tot
        }
        return render(request,"user_jewels_index.html",context)

@csrf_exempt
def user_jewellery_products(request,id,category):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    jewel_data= requests.get(f"https://miogra.clovion.org/category_based_jewel/{category}/").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    print(jewel_data)
    products=[]
    for x in jewel_data:
        shop_id= x.get('jewel_id')
        shop=requests.get(f"https://miogra.clovion.org/my_jewellery_data/{shop_id}").json()
        products.append({'item' : x, 'shop':shop})

    context={
      'key': mydata,
        'jewels': jewel_data,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot
    }
    return render(request,"user_jewels_category.html",context)

@csrf_exempt
def user_jewellery_based_products(request,id,jewel_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    shop=requests.get(f"https://miogra.clovion.org/my_jewellery_data/{jewel_id}").json()
    products=requests.get(f"https://miogra.clovion.org/jewel_get_products/{jewel_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist) 
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    context = {
        'key' : mydata,
        'shop' :shop, 
        'jewels' :products,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot
    }
    
    return render(request,"user_jewellery_shops.html",context)

@csrf_exempt
def user_jewel_single_product(request,id,shop_id,product_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    jewel_data= requests.get(f"https://miogra.clovion.org/single_jewelproduct/{shop_id}/{product_id}").json()[0]
    reviews=requests.get(f"https://miogra.clovion.org/get_product_all_reviews/{product_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    print(jewel_data)
    if request.method=="POST":
        if "add_cart" in request.POST:
            quantity=request.POST['quantity']
            data={
                'quantity' :quantity,
                'shop_id': shop_id,
                'product_id':product_id,
            'category' :"jewellery"

            }
            response = requests.post(f"https://miogra.clovion.org/cart_product/{id}/{product_id}/jewellery/",data=data)
            if response.status_code == 200:
                return redirect(f"/user/shopping_cart_products/{id}/")
            else:
                pass
        
        elif "reviewsubmit"  in request.POST:
            product_id=request.POST['productId']

            data={
                "id":id,
                'product_id' : product_id,
                'rating' : request.POST['rating'],
                'comment' :request.POST['comment'],
            }
            print(data)
            response=requests.post(f"https://miogra.clovion.org/create_reviews_for_delivered_products/{id}/{product_id}/",data=data)
            if response.status_code == 201:
                category="jewellery"
                rating_up=requests.post(f"https://miogra.clovion.org/calculate_average_ratings/{category}")
                print(rating_up.status_code)
                return redirect(f"/products/jewelleryproducts/jewellery/{id}/{shop_id}/{product_id}")

    context={
         'key':mydata,
        'jewels': jewel_data,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'reviews' : reviews,
        'tot':tot
    }
    return render(request,"user_jewels_singlepage.html",context)

@csrf_exempt
def user_pharmacy(request,id):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['pharmacy'] == False:
        return redirect(f"/comming/{id}")
    else:
        mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
        pharm_data= requests.get("https://miogra.clovion.org/all_pharmproducts/").json()
        wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
        cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
        banner = requests.get("https://miogra.clovion.org/admin/banner_display/pharmacy").json()[0]
        cartcount= len(cartlist)
        wishcount= len(wishlist)
        tot=0
        for i in cartlist:
            tot += float(i.get('total'))
    
        products=[]
        for x in pharm_data:
            shop_id= x.get('pharm_id')
            shop=requests.get(f"https://miogra.clovion.org/pharmacy_get_products/{shop_id}").json()
            products.append({'item' : x, 'shop':shop})
        

        context={
        'key': mydata,
            'pharms':products,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'banner':banner,
            'tot':tot
        }
        return render(request,"user_pharmacy_index.html",context)

@csrf_exempt
def user_pharm_products(request,id,category):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    pharm_data= requests.get(f"https://miogra.clovion.org/category_based_pharm/{category}/").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    print(pharm_data)
    products=[]
    for x in pharm_data:
        shop_id= x.get('pharm_id')
        shop=requests.get(f"https://miogra.clovion.org/pharmacy_get_products/{shop_id}").json()
        products.append({'item' : x, 'shop':shop})

    context={
       'key': mydata,
        'pharms':products,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot
    }
    return render(request,"user_pharmacy_products.html",context)

@csrf_exempt
def user_medical_pharmacy_product(request,id,pharm_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    shop=requests.get(f"https://miogra.clovion.org/my_pharmacy_data/{pharm_id}").json()
    products=requests.get(f"https://miogra.clovion.org/pharmacy_get_products/{pharm_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    
    context = {
        'key' : mydata,
        'shop' : shop,
        'pharms' : products,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot,
    }
    
    return render(request,"user_medical_shops.html",context)

@csrf_exempt
def user_pharmac_singleproduct(request,id,shop_id,product_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    pharm_data= requests.get(f"https://miogra.clovion.org/single_pharmproduct/{shop_id}/{product_id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    reviews=requests.get(f"https://miogra.clovion.org/get_product_all_reviews/{product_id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    print(pharm_data)
    if request.method=="POST":
        if "add_cart" in request.POST:
            quantity=request.POST['quantity']
            data={
                'quantity' :quantity,
                'shop_id': shop_id,
                'product_id':product_id,
            'category' :"pharmacy"

            }
            response = requests.post(f"https://miogra.clovion.org/cart_product/{id}/{product_id}/pharmacy/",data=data)
            if response.status_code == 200:
                return redirect(f"/user/shopping_cart_products/{id}/")
            else:
                pass

        elif "reviewsubmit"  in request.POST:
            product_id=request.POST['productId']

            data={
                "id":id,
                'product_id' : product_id,
                'rating' : request.POST['rating'],
                'comment' :request.POST['comment'],
            }
            print(data)
            response=requests.post(f"https://miogra.clovion.org/create_reviews_for_delivered_products/{id}/{product_id}/",data=data)
            if response.status_code == 201:
                category="pharmacy"
                rating_up=requests.post(f"https://miogra.clovion.org/calculate_average_ratings/{category}")
                print(rating_up.status_code)
                return redirect(f"/products/pharmacyproducts/pharmacy_single/{id}/{shop_id}/{product_id}")
    
    context={
       'key': mydata,
        'pharms':pharm_data,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'reviews' : reviews,
        'tot':tot,
    }
    return render(request,"user_pharm_single.html",context)

@csrf_exempt
def used_product_index(request,id):
    print(id)
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    if admin[0]['used_products'] == False:
        return redirect(f"/comming/{id}")
    else:
        mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
        used_data=requests.get("https://miogra.clovion.org/get_allused_products/").json()
        wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
        cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
        cartcount= len(cartlist)
        wishcount= len(wishlist)
        tot=0
        for i in cartlist:
            tot += float(i.get('total'))
        print(used_data)
    
        context={
           'key': mydata,
            'products':used_data,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot,
        }
        return render(request,"usedproduct_all_list.html",context)

@csrf_exempt
def used_category_based(request,id,subcategory):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    used_product=requests.get(f"https://miogra.clovion.org/get_used_products_category/{subcategory}/").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    # print(used_product)
    print(used_product)
   
    context={
        'key' : mydata,
        'products':used_product,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot,
    }
    return render(request,"usedproduct_select_category.html",context)


@csrf_exempt
def used_single_product(request,id,product_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    used_data= requests.get(f"https://miogra.clovion.org/get_single_used_products/{product_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    
    product_details = used_data[0]['product']
    user_id=used_data[0]['user']
    products=dict(product_details)
    
    keys_to_remove = ["other_images", "primary_image", "description", "productId", 
                      "product_id", "category", "Category", "subcategory", 
                      "contact", "location"]
    
    for key in keys_to_remove:
        if key in products:
            products.pop(key)

    formatted_data =[(key, value) for key, value in products.items()]
       
    context={
        'key' : mydata,
        'user':user_id,
        'product_id':product_id,
        'product': product_details,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot,
        'formated':formatted_data,
    }
    
    return render(request,"used_products_single_products.html",context)

@csrf_exempt
def user_usedproduct_reg(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]

    if request.method == "POST":
        print(request.POST)
        primary_image=request.FILES['primary_image']
        other_images = request.FILES.getlist('other_images')
        # print(request.POST.getlist('heading'))
        # print(request.POST.getlist('data'))
        for_product = dict(request.POST)
        
        for_product.pop("csrfmiddlewaretoken")
        try:
            for_product.pop("heading")
        except:
            pass
        try:
            for_product.pop("data")
        except:
            pass
        
        #add custom discription
        new_data={}
        for x,y in zip(request.POST.getlist('heading'),request.POST.getlist('data')):
            new_data[x.lower()] = y.lower().split()
        # print(new_data)
        for_product.update(new_data)
        
        cleaned_data_dict ={key:value[0] if isinstance(value,list) and len(value)==1 else value for key,value in for_product.items()}
        # cleaned_data_dict['other_images'] = other_images
        print("clean",cleaned_data_dict)
        response=requests.post(f"https://miogra.clovion.org/used_products/{id}",data=cleaned_data_dict,files=request.FILES)
        if response.status_code == 200:
            return redirect(f"/enduser/used_products/products/{id}")
        else:
            return redirect(f"/enduser/usedproduct/registration/{id}/")
            
    context={
        'key' : mydata,
        
            }
    return render(request,"usedproduct_registration_form.html",context)

def user_product_edit(request,id,product_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    used_data= requests.get(f"https://miogra.clovion.org/get_single_used_products/{product_id}").json()
    product_details = used_data[0]['product']
    user_id=used_data[0]['user']
    context={
        'key' : mydata,
        'user':user_id,
        'product': product_details,
        
    }
    if request.method == "POST":
        if "productId" in request.POST:
            print(request.POST)
            # primary_image=request.FILES['primary_image']
            # other_images = request.FILES.getlist('other_images')
            # print(request.POST.getlist('heading'))
            # print(request.POST.getlist('data'))
            for_product = dict(request.POST)
            
            for_product.pop("csrfmiddlewaretoken")
            try:
                for_product.pop("heading")
            except:
                pass
            try:
                for_product.pop("data")
            except:
                pass
            
            #add custome discription
            new_data={}
            for x,y in zip(request.POST.getlist('heading'),request.POST.getlist('data')):
                new_data[x.lower()] = y.lower().split()
            # print(new_data)
            for_product.update(new_data)
            
            cleaned_data_dict ={key:value[0] if isinstance(value,list) and len(value)==1 else value for key,value in for_product.items()}
            # cleaned_data_dict['primary_image'] = primary_image
            # cleaned_data_dict['other_images'] = other_images
            print("clean",cleaned_data_dict)
            response=requests.post(f"https://miogra.clovion.org/used_update_product/{id}/{product_id}",data=cleaned_data_dict,files=request.FILES)
            if response.status_code == 200:
                return redirect(f"/enduser/used_products/products/{id}")
            else:
                return redirect(f"/enduser/usedproduct/edit/{id}/{product_id}")
            
        elif "img_index" in request.POST:
            index_value=request.POST['img_index']
            response= requests.post(f"https://miogra.clovion.org/used_imgupdate_product/{id}/{product_id}/{index_value}/",files=request.FILES)
            if response.status_code == 200:
                return redirect(f"/enduser/used_products/single_data/{id}/{product_id}")
            else:
                return redirect(f"/enduser/usedproduct/edit/{id}/{product_id}")
        else:
            pass

    return render(request,"user_product_editing.html",context)
 
# --------------------------- Address ------------------------------
@csrf_exempt
def user_add_address_cart(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    if request.method == "POST":
        print("request",request.POST)
        response=requests.post(f"https://miogra.clovion.org/end_user_address/{id}",request.POST)
        if response.status_code == 200:
            return redirect(f"/user_cart_to_checkout/{id}")
        else:

            return redirect(f"/user/update_address/{id}")

    context = {
        'key' : mydata,
        'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data' :cartlist,
            'tot':tot,
    }
    return render(request,"address-form.html",context)



@csrf_exempt
def user_address_cartchange(request,id,change):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    index=int(change)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    address=mydata.get('address_data',[index])
    if address:
    # Access the first address in the list
        first_address = address[index]
    print(first_address)
    if request.method == "POST":
        if "altnumber" in request.POST:
            altnumber=request.POST['altnumber']
        else:
            altnumber=None
        data={
            'address_index':change,
            "doorno": request.POST["doorno"],
            "altnumber":altnumber,
            "area": request.POST["area"],
            "landmark": request.POST["landmark"],
            "place": request.POST["place"],
            "district": request.POST["district"],
            "state": request.POST["state"],
            "pincode": request.POST["pincode"],
        }
        response=requests.post(f"https://miogra.clovion.org/update_end_user_address/{id}/",data=data)
        if response.status_code == 200:
            print("changed")
            return redirect(f"/user_cart_to_checkout/{id}")
        else:
            pass

    context = {
        'key' : mydata,
        'address':first_address,
        'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data' :cartlist,
            'tot':tot,
    }
    return render(request,"user_address_edit.html",context)



@csrf_exempt
def user_add_address_foodcart(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    if request.method == "POST":
        print("request",request.POST)
        response=requests.post(f"https://miogra.clovion.org/end_user_address/{id}",request.POST)
        if response.status_code == 200:
            return redirect(f"/user/food_cart/checkout/{id}")
        else:

            return redirect(f"/user_update_address/{id}")

    context = {
        'key' : mydata,
        'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data' :cartlist,
            'tot':tot,
    }
    return render(request,"address-form.html",context)




@csrf_exempt
def user_address_foodchange(request,id,change):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    index=int(change)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    address=mydata.get('address_data',[index])
    if address:
    # Access the first address in the list
        first_address = address[index]
    print(first_address)
    if request.method == "POST":
        if "altnumber" in request.POST:
            altnumber=request.POST['altnumber']
        else:
            altnumber=None
        data={
            'address_index':change,
            "doorno": request.POST["doorno"],
            "altnumber":altnumber,
            "area": request.POST["area"],
            "landmark": request.POST["landmark"],
            "place": request.POST["place"],
            "district": request.POST["district"],
            "state": request.POST["state"],
            "pincode": request.POST["pincode"],
        }
        response=requests.post(f"https://miogra.clovion.org/update_end_user_address/{id}/",data=data)
        if response.status_code == 200:
            print("changed")
            return redirect(f"/user/food_cart/checkout/{id}")
        else:
            pass

    context = {
        'key' : mydata,
        'address':first_address,
        'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data' :cartlist,
            'tot': tot,
    }
    
    return render(request,"user_address_edit.html",context)


# ---------------------------  Oreder placing------------------------------
@csrf_exempt
def user_checkout_page(request,id,category,shop_id,product_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    user_address =[]
    if category == "shopping":
        products=requests.get(f"https://miogra.clovion.org/get_single_shopproduct/{shop_id}/{product_id}").json()[0]
    elif category == "food":
        products=requests.get(f"https://miogra.clovion.org/single_foodproduct/{shop_id}/{product_id}").json()[0]
    elif category == "freshcuts":   
        products=requests.get(f"https://miogra.clovion.org/single_freshproduct/{shop_id}/{product_id}").json()[0]
    elif category == "doriginal":
        products=requests.get(f"https://miogra.clovion.org/single_d_originalproduct/{shop_id}/{product_id}").json()[0]
    elif category == "dmio":
        products= requests.get(f"https://miogra.clovion.org/get_single_dmio_product/{shop_id}/{product_id}").json()[0]
    elif category == "jewellery":
        products= requests.get(f"https://miogra.clovion.org/single_jewelproduct/{shop_id}/{product_id}").json()[0]
    elif category == "pharmacy":
        products= requests.get(f"https://miogra.clovion.org/single_pharmproduct/{shop_id}/{product_id}").json()[0]
    else:
        print("no data")
    prices=products.get('product', {})
    selling_price = prices['selling_price']
    delivery_fees=50
    discount =0
    total_price=float(selling_price) + float(delivery_fees) - float(discount)
    for i in mydata['address_data'] :
        user_address.append(i)

    if "pay_option" in request.POST:
        qty = request.POST['quantity']
        d_a = request.POST['address']
        return redirect(f"/user_payment/{id}/option/{category}/{shop_id}/product/{product_id}/with/{qty}/{d_a}",{'quantity':qty})      

    context={  
        'key':mydata,
        'items' : products,
        'selling_price':selling_price,
        'delivery_fee' :delivery_fees,
        'discount' :discount,
        'total_price':total_price,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot,

        }     
    return render(request,"user_order.html",context)

@csrf_exempt
def user_payment_option(request,id,category,shop_id,product_id,qty,d_a):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    index=int(d_a)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    if category == "shopping":
        products=requests.get(f"https://miogra.clovion.org/get_single_shopproduct/{shop_id}/{product_id}").json()[0]
    elif category == "food":
        products=requests.get(f"https://miogra.clovion.org/single_foodproduct/{shop_id}/{product_id}").json()[0]
    elif category == "freshcuts":   
        products=requests.get(f"https://miogra.clovion.org/single_freshproduct/{shop_id}/{product_id}").json()[0]
    elif category == "doriginal":
        products=requests.get(f"https://miogra.clovion.org/single_d_originalproduct/{shop_id}/{product_id}").json()[0]
    elif category == "dmio":
        products= requests.get(f"https://miogra.clovion.org/get_single_dmio_product/{shop_id}/{product_id}").json()[0]
    elif category == "jewellery":
        products= requests.get(f"https://miogra.clovion.org/single_jewelproduct/{shop_id}/{product_id}").json()[0]
    elif category == "pharmacy":
        products= requests.get(f"https://miogra.clovion.org/single_pharmproduct/{shop_id}/{product_id}").json()[0]
    else:
        print("no data")
    quantity =int(qty)
    prices=products.get('product', {})
    selling = prices['selling_price']
    selling_price = float(selling) * quantity
    delivery_fees=50
    discount =products['product']['discount'][0]
    total_price=float(selling_price) + float(delivery_fees) - float(discount)
    delivery_address=mydata.get('address_data', [index])
    print(delivery_address) 
    if delivery_address:
    # Access the first address in the list
        first_address = delivery_address[index]
        pincode = first_address.get('pincode')
        print(pincode)
    else:
        print("No delivery address available")
    if "order_place" in request.POST:
        print(request.POST['paymentMethod'])
        
        data={
            'quantity' : qty,
            'payment_type' : request.POST['paymentMethod'],
            'delivery_address' : first_address,
            'pincode' : pincode,
        }
        response = requests.post(f"https://miogra.clovion.org/enduser_order_create/{id}/{product_id}/{category}/",data = data)
        if response.status_code == 200:
            print("Order placed")
            return redirect(f"/success_page/{id}/")

        else:
            return redirect(f"/user_payment/{id}/option/{category}/{shop_id}/product/{product_id}/with/{qty}/")

    context={ 
             
            'key' : mydata,
            'items' :products,
            'quantity':qty,
            'selling_price':selling_price,
            'delivery_fee' :delivery_fees,
            'discount' :discount,
            'total_price':total_price,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot' : tot,

             }
    
    return render(request,"payment.html",context)
# -------------------add_cart---------------------
@csrf_exempt
def add_to_cart(request,id,category,shop_id,product_id):
    shop_id = shop_id

    # if "quantity" in request.POST:
    #     quantity = request.POST['quantity']
        
    #     data={
    #     'quantity' : quantity
    #         }
    #     response = requests.post(f"https://miogra.clovion.org/cart_product/{id}/{product_id}/{category}/",data=data)
    
    #     if response.status_code == 200:
    #         if category != "food":
    #             return redirect(f"/user/shopping_cart_products/{id}/")
    #         else:
    #             return redirect(f"/user/food_cart/{id}/")
    #     else:
    #         print("no data")
       
    # else:
    quantity="1"
    
    data={
        'quantity' : quantity
    }
    response = requests.post(f"https://miogra.clovion.org/cart_product/{id}/{product_id}/{category}/",data=data)
    if response.status_code == 200:
        if category != "food":
            return redirect(f"/user/shopping_cart_products/{id}/")
        else:
            return redirect(f"/user/food_cart/{id}/")
    else:
        print("no data")
    
    
@csrf_exempt
def user_shopping_cart(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    
    carts = requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    cart_data=[]
    tot=0
    for i in carts:
        tot += float(i.get('total'))
        if i.get('status') == "in-cart" and i.get('category') != "food":
            cart_data.append(i)

    sub_total=0
    for x in cart_data:
    #    print(x.get('total'))
       sub_total+= float(x.get('total'))
    print(sub_total)
    
    if request.method == "POST":
        if "cart_del" in request.POST:
            cart_id=request.POST['cart_del']
            dele_data = requests.post(f"https://miogra.clovion.org/cartremove/{id}/{cart_id}/")
            if dele_data.status_code == 200:
                return redirect(f"/user/shopping_cart_products/{id}/")
            else:
                pass
        elif "update_cart" in request.POST:
            quantity = int(request.POST['qty_add'])
            if quantity > 0:
                cart_id=request.POST['update_cart']
                data={
                    'user_id' : id,
                    'quantity' : quantity,
                    'cart_id' : cart_id
                }
                print(data)
                response=requests.post(f"https://miogra.clovion.org/cartupdate/{cart_id}",data=data)
                if response.status_code == 200:
                    return redirect(f"/user/shopping_cart_products/{id}/")
                else:
                    pass
            else:
                cart_id=request.POST['update_cart']
                dele_data = requests.post(f"https://miogra.clovion.org/cartremove/{id}/{cart_id}/")
                if dele_data.status_code == 200:
                    return redirect(f"/user/shopping_cart_products/{id}/")
                else:
                    pass
                


    context={  
        'key':mydata,
        'cart_data' :cart_data,
        'sub_total' : sub_total,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'tot':tot,
    
        }     

    return render(request,"user_shopping-cart.html",context)


@csrf_exempt
def cart_to_checkout(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    user_address=[]
    carts = requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    # delivery_charge=requests.get(f"https://miogra.clovion.org/admin/normal_delivery_commision").json()
    delivery_charge=50

    
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    cart_data=[]
   
    for i in carts:
        if i.get('status') == "in-cart" and i.get('category') != "food":
            cart_data.append(i)

    sub_total=0
    discount_total=0
    for x in cart_data:   
    #    discount= x['shop_product']['product']['discount_price'][0]
       sub_total+= float(x.get('total'))
    #    discount_total+= float(discount)
    selling_price = int(sub_total)
    
    discount =0
    total_price=float(selling_price) + float(delivery_charge) 
    if mydata['address_data'] != None:
        for i in mydata['address_data']:
            print(i)
            user_address.append(i)
    else:
        user_address = None

    if request.method == "POST":

        if "pay_option" in request.POST:
            if "address" not in request.POST:
                error="Add Your Address for Proceed"
                return redirect(f"/user/food_cart/checkout/{id}") 

            else:   
                add = request.POST['address']
                        
                return redirect(f"/user_cart_payment/{id}/{add}")
                
        elif "ad_change" in request.POST:
            change=request.POST['ad_change']
            return redirect(f"/user/addess_edit/{id}/{change}")

        
    context={  
        'key':mydata,
        'cart_data' :cart_data,
        'sub_total' : sub_total,
        'selling_price':selling_price,
        'delivery_fee' :delivery_charge,
        'discount' :discount,
        'total_price':total_price,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'tot':tot
    
        }    

    return render(request,"user_cart_to_order.html",context)

@csrf_exempt
def user_cart_payment(request,id,add):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    cod_shutdown = str(admin[0]['cod'])
    razorpay = ""
    razor_id = ""
    razor_amount = ""
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    carts = requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    # delivery_fees=requests.get(f"https://miogra.clovion.org/admin/normal_delivery_commision").json()
    delivery_fees = 50
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    cart_data=[]
    print(carts)
    for i in carts:
        if i.get('status') == "in-cart" and i.get('category') != "food":
            cart_data.append(i)
    address=int(add)
    sub_total=0
    discount_total=0
    for x in cart_data:   
    #    discount= x['shop_product']['product']['discount_price'][0]
       sub_total+= float(x.get('total'))
    #    discount_total+= float(discount)
    selling_price = int(sub_total)
    total_price=float(selling_price) + float(delivery_fees)
       
    delivery_address=mydata.get('address_data', [address])
    print(delivery_address) 
    if delivery_address:
    # Access the address in the list
        first_address = delivery_address[address]
        pincode = first_address.get('pincode')
        print(pincode)
    else:
        print("No delivery address available")

    if "order_place" in request.POST:
        print("wsxggggggggggggggggggg")
        print(request.POST['paymentMethod'])
        orders_created = False
        if request.POST['paymentMethod'] == "netBanking":
            print(request.POST['order_place'])
            response = requests.post(f"https://miogra.clovion.org/razor_pay_order", data={"amount":request.POST['order_place']})
            if response.status_code == 200:
                print(response.text)
                razorpay = jsondec.decode(response.text)
                print(type(razorpay))
                razor_amount = razorpay['amount']
                razor_id = razorpay['id']
                
        else:
            print("aaaaaaaaaaaaaaaa")
            for x in cart_data:
                category = x.get('category')
                if category.lower() in ["shopping", "daily_mio", "d_original", "jewellery", "pharmacy", "fresh_cuts"]:
                    if category.lower() == "shopping":
                        product_id = x['shop_product']['product_id']
                    elif category.lower() == "daily_mio":
                        product_id = x['dailymio_product']['product_id']
                    elif category.lower() == "d_original":
                        product_id = x['d_origin_product']['product_id']
                    elif category.lower() == "jewellery":
                        product_id = x['jewel_product']['product_id']
                    elif category.lower() == "pharmacy":
                        product_id = x['pharmacy_product']['product_id']
                    elif category.lower() == "fresh_cuts":
                        product_id = x['freshcut_product']['product_id']
                    
                    quantity = x['quantity']
                    cart_id = x['cart_id']
                    data = {
                        'quantity': quantity,
                        'payment_type': request.POST['paymentMethod'],
                        'delivery_address': delivery_address,
                        'pincode': pincode,
                        'address_index': address
                    }
                    
                    response = requests.post(f"https://miogra.clovion.org/enduser_order_create/{id}/{product_id}/{category}/", data=data)
                    if response.status_code == 200:
                        cart_del = requests.post(f"https://miogra.clovion.org/cartremove/{id}/{cart_id}/")
                        orders_created = True
                    else:
                        print("Failed to create order")
    
    # After processing all items in the cart, check if any orders were created
            if orders_created:
                return redirect(f"/success_page/{id}/")
            else:
                # return redirect("/error_page/no_orders_created/")
                pass
    elif "razorpay_payment_id" in request.POST:
        orders_created = False
        for x in cart_data:
                category = x.get('category')
                if category.lower() in ["shopping", "daily_mio", "d_original", "jewellery", "pharmacy", "fresh_cuts"]:
                    if category.lower() == "shopping":
                        product_id = x['shop_product']['product_id']
                    elif category.lower() == "daily_mio":
                        product_id = x['dailymio_product']['product_id']
                    elif category.lower() == "d_original":
                        product_id = x['d_origin_product']['product_id']
                    elif category.lower() == "jewellery":
                        product_id = x['jewel_product']['product_id']
                    elif category.lower() == "pharmacy":
                        product_id = x['pharmacy_product']['product_id']
                    elif category.lower() == "fresh_cuts":
                        product_id = x['freshcut_product']['product_id']
                    
                    quantity = x['quantity']
                    cart_id = x['cart_id']
                    data = {
                        'quantity': quantity,
                        'payment_type': request.POST['paymentMethod'],
                        'delivery_address': delivery_address,
                        'pincode': pincode,
                        'address_index': address,
                        'razorpay_payment_id':request.POST['razorpay_payment_id'],
                        'razorpay_order_id':request.POST['razorpay_order_id'],
                        'razorpay_signature':request.POST['razorpay_signature'],
                    }
                    
                    response = requests.post(f"https://miogra.clovion.org/enduser_order_create/{id}/{product_id}/{category}/", data=data)
                    if response.status_code == 200:
                        cart_del = requests.post(f"https://miogra.clovion.org/cartremove/{id}/{cart_id}/")
                        orders_created = True
                    else:
                        print("Failed to create order")
    
    # After processing all items in the cart, check if any orders were created
        if orders_created:
            return redirect(f"/success_page/{id}/")
        else:
            # return redirect("/error_page/no_orders_created/")
            pass
        
    context={
        'key':mydata,
        'cod_shutdown':cod_shutdown,
        'cart_data' :cart_data,
        'sub_total' : sub_total,
        'selling_price':selling_price,
        'delivery_fee' :delivery_fees,
        'discount' :0,
        'total_price':total_price,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'tot':tot,
        "razorpay":razorpay,
        "razor_amount":razor_amount,
        "razor_id":razor_id,
            }

    return render(request,"payment.html",context)

# ---------------------------- Food Cart view function-------------------------------------
@csrf_exempt
def user_food_cart(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    carts = requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    cart_data=[]

    for i in carts:
        if i.get('status') == "in-cart":
            if i.get('category') == "food":
                cart_data.append(i)
                
            else:
                pass
                
    sub_total=0
    for x in cart_data:
    #    print(x.get('total'))
       sub_total+= float(x.get('total'))
    print(sub_total)

    if request.method == "POST":
        if "cart_del" in request.POST:
            cart_id=request.POST['cart_del']
            dele_data = requests.post(f"https://miogra.clovion.org/cartremove/{id}/{cart_id}/")
            if dele_data.status_code == 200:
                return redirect(f"/user/food_cart/{id}/")
            else:
                pass
        elif "update_cart" in request.POST:
            quantity = int(request.POST['qty_add'])
            if quantity > 0:
                cart_id=request.POST['update_cart']
                data={
                    'user_id' : id,
                    'quantity' : quantity,
                    'cart_id' : cart_id
                    }
                print(data)
                response=requests.post(f"https://miogra.clovion.org/cartupdate/{cart_id}",data=data)
                if response.status_code == 200:
                    return redirect(f"/user/food_cart/{id}/")
                else:
                    pass
            else:
                cart_id=request.POST['update_cart']
                dele_data = requests.post(f"https://miogra.clovion.org/cartremove/{id}/{cart_id}/")
                if dele_data.status_code == 200:
                    return redirect(f"/user/food_cart/{id}/")
                else:
                    pass


    context={  
        'key':mydata,
        'cart_data' :cart_data,
        'sub_total' : sub_total,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'tot':tot
    
        }     

    return render(request,"user_foods_cart.html",context)

@csrf_exempt
def foods_cart_checkout(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    carts = requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    error=""
    # delivery_charge=requests.get(f"https://miogra.clovion.org/admin/normal_delivery_commision").json()
    # print(delivery_charge,"from admin\n")
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    cart_data=[]
    # print(carts)
    for i in carts:
        if i.get('status') == "in-cart":
            if i.get('category') == "food":
                cart_data.append(i)
            else:
                pass
    sub_total=0
    discount_total=0
    for x in cart_data:
    #    print(x['food_product']['product']['discount_price'])
       discount= x['food_product']['product']['discount_price'][0]
       sub_total+= float(x.get('total'))
       discount_total+= float(discount)
    print(sub_total)
    print(discount_total)
    selling_price = int(sub_total)
    # delivery_fees=requests.get("https://miogra.clovion.org/admin/normal_delivery_commision").json()
    delivery_fees = 50
    total_price=float(selling_price) + float(delivery_fees) 
    if request.method == "POST":

        if "pay_option" in request.POST:
            if "address" not in request.POST:
                error="Add Your Address for Proceed"
                return redirect(f"/user/food_cart/checkout/{id}") 

            else:   
                # shop_id ="22"
                # category="shopping"
                # qty = request.POST['quantity']
                add1 = int(request.POST['address'])
                delivery_address=mydata.get('address_data', [add1])

            
                data={
                    'id':id,
                    'delivery_address' : delivery_address,
                    'cart_data':cart_data,
                }

                return redirect(f"/user/foodcart/payment/{id}/{add1}",data)
                
        elif "ad_change" in request.POST:
            change=request.POST['ad_change']
            return redirect(f"/user_addess_edit/{id}/{change}")
        
    context={  
        'key':mydata,
        'cart_data' :cart_data,
        'sub_total' : sub_total,
        'selling_price':selling_price,
        'delivery_fee' :delivery_fees,
        'discount' :discount_total,
        'total_price':total_price,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'tot':tot,
        'error':error
    
        }    

    return render(request,"user_foodcart_to_order.html",context)

@csrf_exempt
def user_foods_cart_payment(request,id,add1):
    admin=requests.get("https://miogra.clovion.org/admin/get_shutdown").json()
    cod_shutdown = str(admin[0]['cod'])
    razorpay = ""
    razor_id = ""
    razor_amount = ""
    error=""
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    carts = requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    cart_data=[]
    add=int(add1)
    print(carts)
    for i in carts:
        if i.get('status') == "in-cart":
            if i.get('category') == "food":
                cart_data.append(i)
            else:
                pass
    sub_total=0
    discount_total=0
    for x in cart_data:   
       discount= x['food_product']['product']['discount_price'][0]
       sub_total+= float(x.get('total'))
       discount_total+= float(discount)
    selling_price = int(sub_total)
    # delivery_fees=requests.get("https://miogra.clovion.org/quick_delivery_km_for_order/FGZRC78XEIE/Z3NZCVEANTB").json()
    delivery_fees = 50
    total_price=float(selling_price) + float(delivery_fees)
    delivery_address=mydata.get('address_data', [add])
    print(delivery_address) 
    if delivery_address:
    # Access the first address in the list
        first_address = delivery_address[add]
        pincode = first_address.get('pincode')
        print(pincode)
    else:
        print("No delivery address available")   
    
       
    if "order_place" in request.POST:
        print(request.POST['paymentMethod'])
        if request.POST['paymentMethod'] == "netBanking":
            print(request.POST['order_place'])
            response = requests.post(f"https://miogra.clovion.org/razor_pay_order", data={"amount":request.POST['order_place']})
            if response.status_code == 200:
                print(response.text)
                razorpay = jsondec.decode(response.text)
                print(type(razorpay))
                razor_amount = razorpay['amount']
                razor_id = razorpay['id']
        
        else:
            for x in cart_data:
                category=x.get('category')
                
                cart_id=x['cart_id']
                product_id=x['food_product']['product_id']
                quantity = x['quantity']
                data={
                    'quantity' : quantity,
                    'payment_type' : request.POST['paymentMethod'],
                    'delivery_address' : first_address,
                    'pincode' : pincode
                    
                }
                print(data)
                response = requests.post(f"https://miogra.clovion.org/enduser_order_create/{id}/{product_id}/{category}/",data = data)
                if response.status_code == 200:
                    cart_del=requests.post(f"https://miogra.clovion.org/cartremove/{id}/{cart_id}/")
                    orders_created = True
                   
                else:
                    print("Failed to create order")
    
    # After processing all items in the cart, check if any orders were created
            if orders_created:
                return redirect(f"/success_page/{id}/")
            else:
                error="You are out of region"
                # pass
        
        
    elif "razorpay_payment_id" in request.POST:
        orders_created = False
        for x in cart_data:
                category=x.get('category')
                
                cart_id=x['cart_id']
                product_id=x['food_product']['product_id']
                quantity = x['quantity']
                data={
                    'quantity' : quantity,
                    'payment_type' : request.POST['paymentMethod'],
                    'delivery_address' : first_address,
                    'pincode' : pincode,
                     'razorpay_payment_id':request.POST['razorpay_payment_id'],
                        'razorpay_order_id':request.POST['razorpay_order_id'],
                        'razorpay_signature':request.POST['razorpay_signature'],
                    
                }
                print(data)
                response = requests.post(f"https://miogra.clovion.org/enduser_order_create/{id}/{product_id}/{category}/",data = data)
                if response.status_code == 200:
                    cart_del=requests.post(f"https://miogra.clovion.org/cartremove/{id}/{cart_id}/")
                    orders_created = True
                   
                else:
                    print("Failed to create order")
    
    # After processing all items in the cart, check if any orders were created
        if orders_created:
            return redirect(f"/success_page/{id}/")
        else:
            error="You are out of region"
            pass
        
    
            

    context={
        'key':mydata,
        'cod_shutdown':cod_shutdown,
        'cart_data' :cart_data,
        'sub_total' : sub_total,
        'selling_price':selling_price,
        'delivery_fee' :delivery_fees,
        'discount' :discount_total,
        'total_price':total_price,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'tot':tot,
        "razorpay":razorpay,
        "razor_amount":razor_amount,
        "razor_id":razor_id,
        'error':error
    
    }

    return render(request,"user_foods_payment.html",context)


# -----------------------------------Wishlist------------------------
@csrf_exempt
def add_to_wishlist(request,id,category,product_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    quantity="1"
    data={
        'quantity' : quantity
    }
    response = requests.post(f"https://miogra.clovion.org/whishlist_product/{id}/{product_id}/{category}/",data=data)
    print(response)
    if response.status_code == 200:
        return redirect(f"/user/shopping_wishlist_products/{id}/")
    else:
        pass
 
       
@csrf_exempt
def user_wish_list_data(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wish_list = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    print(wish_list)
    if request.method=="POST":
        if "wish_del" in request.POST:
            print(request.POST['wish_del'])
            product_id=request.POST['wish_del']
            print(id)
            delete_data = requests.post(f"https://miogra.clovion.org/remove_wish/{id}/{product_id}/")
            if delete_data.status_code == 200:
                return redirect(f"/user/shopping_wishlist_products/{id}/")
            else:
                pass
        if "cartup" in request.POST:
            product_id =request.POST['cartup']
            quantity=request.POST['quantity']
            category=request.POST['category']
            
            
            data={
                'quantity':quantity,
            }
            print(data)
            print(product_id, quantity, category)
            response = requests.post(f"https://miogra.clovion.org/cart_product/{id}/{product_id}/{category}/",data=data)
            if response.status_code ==200:
                remove_wish = requests.post(f"https://miogra.clovion.org/remove_wish/{id}/{product_id}/")
                if remove_wish.status_code == 200:
                    return redirect(f"/user/shopping_cart_products/{id}/")
                else:
                    return redirect(f"/user/shopping_wishlist_products/{id}/")
            else:
                pass
                
    
    context = {
        'key' : mydata,
        'wish_list' : wish_list,
        'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot

    }
    
    return render(request,"wishlist.html",context)

# --------------------- order page--------------
@csrf_exempt
def user_order_data(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    order_data = requests.get(f"https://miogra.clovion.org/enduser_order_list/{id}/").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))

    if request.method=="POST":
        if "reviewsubmit"  in request.POST:
            product_id=request.POST['productId']

            data={
                "id":id,
                'product_id' : product_id,
                'rating' : request.POST['rating'],
                'comment' :request.POST['comment'],
            }
            print(data)
            response=requests.post(f"https://miogra.clovion.org/create_reviews_for_delivered_products/{id}/{product_id}/",data=data)
            if response.status_code == 201:
                for x in order_data:
                    if product_id == x.get('product_id'):
                        category=x.get('category_data')
                        rating_up=requests.post(f"https://miogra.clovion.org/calculate_average_ratings/{category}")
                        print(rating_up.status_code)
                        return redirect(f"/user_order_product_list/{id}")
    context = {
        'key' : mydata,
        'orders' : order_data,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot
    }
    return render(request,"order_display.html",context)   

@csrf_exempt
def success(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    context = {
        'key' : mydata,
        'cartcount':cartcount,
        'wishcount' : wishcount,
        'cart_data':cartlist,
        'tot':tot

    }
    return render(request,"order_success.html",context)
# Tracking Order
@csrf_exempt
def tracking_order(request,id,order_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    order_data = requests.get(f"https://miogra.clovion.org/user_product_timeline/{order_id}").json()
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    context = {
            'key' : mydata,
            'order' : order_data,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot

        }
    return render(request,"track.html",context)

# return of product
@csrf_exempt
def user_product_return(request,id,order_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    response=requests.post(f"https://miogra.clovion.org/user_product_order_status_return/{id}/{order_id}/")
    if response.status_code == 200:
        return redirect(f"/user_order_product_list/{id}")
    else:
        print("error")
        context={'error':"Server Error"}
        return redirect(f"/user_order_product_list/{id}",context)
        
@csrf_exempt
def enduser_order_cancel(request,id,order_id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    response=requests.post(f"https://miogra.clovion.org/enduser_order_cancel/{id}/{order_id}")
    if response.status_code == 200:
        return redirect(f"/user_order_product_list/{id}")
    else:
        print("error")
        context={'error':"Server Error"}
        return redirect(f"/user_order_product_list/{id}",context)
# -------------------SEARCH---------------
@csrf_exempt
def search_view(request):
    query=request.GET.get('query')
    print(query)
    allproducts=[]
    shopdata = requests.get("https://miogra.clovion.org/all_shopproducts").json()
    for x in shopdata:
        allproducts.append(x['product'])
    food_data= requests.get("https://miogra.clovion.org/all_foodproducts/").json()
    for x in food_data:
        allproducts.append(x['product'])   
    fresh_data= requests.get("https://miogra.clovion.org/all_freshcutproducts/").json()
    for x in fresh_data:
        allproducts.append(x['product']) 
    dorigin_data= requests.get("https://miogra.clovion.org/all_d_originalproducts/").json()
    for x in dorigin_data:
        allproducts.append(x['product'])

    dmio_data= requests.get("https://miogra.clovion.org/all_dmioproducts/").json()
    for x in dmio_data:
        allproducts.append(x['product'])

    jewel_data= requests.get("https://miogra.clovion.org/all_jewelproducts/").json()
    for x in jewel_data:
        allproducts.append(x['product'])   

    pharm_data= requests.get("https://miogra.clovion.org/all_pharmproducts/").json()
    for x in pharm_data:
        allproducts.append(x['product'])
       
    for y in allproducts:
        print(y.get('subcategory'))

    matching_products = []

    for product in allproducts:
        if query.lower() in product.get('model_name', '').lower():
            matching_products.append(product)
        elif query.lower() in product.get('subcategory', '').lower():
            matching_products.append(product)
        elif query.lower() in product.get('category', '').lower():
            matching_products.append(product)
        elif query.lower() in product.get('brand', '').lower():
            matching_products.append(product)
       
    if "user" in request.GET:
        id=request.GET.get('user')
        mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
        wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
        cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
        cartcount= len(cartlist)
        wishcount= len(wishlist)
        tot=0
        for i in cartlist:
            tot += float(i.get('total'))

        context={
            'key':mydata,
            'products':matching_products,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot

            }

        return render(request,"search.html",context)
    else:
        mydata = None
   
        context={
            'products':matching_products
        }

        return render(request,"search_normal.html",context)
    
# ---------------SEARCH END------------------------------------
@csrf_exempt
def single(request):
    return render(request,"single-product.html")

@csrf_exempt
def comming_soon(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))
    
    context = {
        'key' : mydata,'cartcount':cartcount,
        'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot
        }
    return render(request,"coming_soon.html",context)

@csrf_exempt
def com_soon(request):
    return render(request,"soon.html")

# ----------------About Us----------------------
@csrf_exempt
def about_miogra(request):
    return render(request,"about-us.html")

@csrf_exempt
def aboutus_miogra(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))

    context = {
            'key' : mydata,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot
        }

    return render(request,"about-us.html",context)


@csrf_exempt
def contact(request):
    return render(request,"contact.html")

@csrf_exempt
def contact_details(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))

    context = {
            'key' : mydata,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot
        }

    return render(request,"contact.html",context)

@csrf_exempt
def terms_condition(request):
    return render(request,"terms_and_use.html")

@csrf_exempt
def mio_terms_condition(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))

    context = {
            'key' : mydata,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot
        }

    return render(request,"terms_and_use.html",context)

@csrf_exempt
def privacypolicy(request):
    return render(request,"privacy_policy.html")

@csrf_exempt
def miogra_privacypolicy(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))

    context = {
            'key' : mydata,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot
        }

    return render(request,"privacy_policy.html",context)

@csrf_exempt
def mio_services(request):
    return render(request,"services.html")

@csrf_exempt
def miogra_services(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))

    context = {
            'key' : mydata,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot
        }

    return render(request,"services.html",context)
@csrf_exempt
def cancel_refund(request):
    return render(request,"refund_cancellation.html")

@csrf_exempt
def miogra_refund_cancel(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))

    context = {
            'key' : mydata,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot
        }

    return render(request,"refund_cancellation.html",context)

@csrf_exempt
def miogra_shipping_delivery(request):
    return render(request,"shipping_and_delivery.html")

@csrf_exempt
def miogra_shipping_delivery_policy(request,id):
    mydata = requests.get(f"https://miogra.clovion.org/single_users_data/{id}").json()[0]
    wishlist = requests.get(f"https://miogra.clovion.org/all_wishlist/{id}").json()
    cartlist= requests.get(f"https://miogra.clovion.org/cartlist/{id}").json()
    cartcount= len(cartlist)
    wishcount= len(wishlist)
    tot=0
    for i in cartlist:
        tot += float(i.get('total'))

    context = {
            'key' : mydata,
            'cartcount':cartcount,
            'wishcount' : wishcount,
            'cart_data':cartlist,
            'tot':tot
        }

    return render(request,"shipping_and_delivery.html",context)

def dummy(request):
    return render(request,"dummy.html")