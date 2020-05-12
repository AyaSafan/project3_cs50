from pizza_app.models import User
from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.contrib import messages


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError

from .models import Type, Topping, Extra, Meal, Order , PlacedOrder
import datetime
import os 

from django.core.mail import send_mail

admin = os.getenv('EMAIL')


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("main")) 
    else:
        return render(request, "pizza_templates/index.html", {"alert": None} )

def signup(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse("index"));
    
    username =      request.POST.get("sign_username")
    first_name =    request.POST["sign_fname"]
    last_name =     request.POST["sign_lname"]
    username =      request.POST["sign_username"]
    mobile_num =    request.POST["sign_num"]
    address =       request.POST["address"]
    email=          request.POST["sign_email"]
    password=       request.POST["sign_pswd"]
    repassword=     request.POST["sign_rpswd"]
    if (password != repassword):
        messages.info(request, 'The Password and Repeat Paassword didn\'t match. Sign Up failed.')
        return HttpResponseRedirect(reverse("index")) 
    try:
        user = User.objects.create_user(email = email, username= username, password =password)
        user.first_name = first_name
        user.last_name=last_name
        user.phone=mobile_num 
        user.address=address
        user.save()
        messages.info(request, 'Successful Sign Up.')
        return HttpResponseRedirect(reverse("index"))      
    except IntegrityError:
        messages.info(request, 'This Username or Email already exists.')
        return HttpResponseRedirect(reverse("index")) 

def edit(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse("index"));
    
    
    first_name =    request.POST["sign_fname"]
    last_name =     request.POST["sign_lname"]
    mobile_num =    request.POST["sign_num"]
    address =       request.POST["address"]
    
    user = request.user
    user.first_name = first_name
    user.last_name=last_name
    user.phone=mobile_num 
    user.address=address
    user.save()
    return HttpResponseRedirect(reverse("index"))      
    

def login(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse("index"));
    username =      request.POST["log_username"]
    password=       request.POST["log_pswd"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        dj_login(request, user)
        return HttpResponseRedirect(reverse("main"))
    else:
        messages.info(request, 'Invalid credentials.')
        return HttpResponseRedirect(reverse("index"))

def main(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    context = {
        "user": request.user
    }
    return render(request, "pizza_templates/main.html", context)

def menu(request):
    context = {
        "user":request.user,
        "types": Type.objects.all(),
        "meals": Meal.objects.all(),
        "alltoppings": Topping.objects.all(),
        "extras": Extra.objects.all()
    }
    return render(request, "pizza_templates/menu.html", context)


def order_item(request):
    if request.method == 'POST':
        meal_id =        int(request.POST["id"])
        user=            request.user
        meal =           Meal.objects.get(pk=meal_id)
        size =           request.POST["size"]
        if size == "Small":
            price = meal.small_price
        else:
            price = meal.large_price
        
        order= Order(user=user,meal=meal, size=size)
        order.save()
        
        toppings_num=    Topping.objects.all().count()+1

        for i in range(1, toppings_num):
            try: 
                topping_id= int(request.POST["topping{}".format(i)])
                topping = Topping.objects.get(pk=topping_id)
                order.toppings.add(topping)
            except:
                pass

        extras_num=      Extra.objects.all().count()+1

        for i in range(1, extras_num):
            try: 
                extra_id= int(request.POST["extra{}".format(i)])
                extra = Extra.objects.get(pk=extra_id)
                price += extra.price
                order.extras.add(extra)
            except:
                pass

        order.price=price
        order.save()
        return HttpResponseRedirect(reverse("menu"))
    
    else:
        return HttpResponseRedirect(reverse("menu"))


@login_required(login_url='/') 
def cart(request):
    user=       request.user
    orders = Order.objects.filter(user=user)
    total = 0
    for order in orders:
        total += order.price
    
    total=round(total, 2)

    context = {
       "orders": orders,
       "total": total
    }
    return render(request, "pizza_templates/cart.html", context)

@login_required(login_url='/') 
def place_order(request):
    
    user=       request.user
    orders=     Order.objects.filter(user=user)
    order_count = Order.objects.filter(user=user).count()
    if order_count == 0:
        return HttpResponseRedirect(reverse("cart"))
    
    date=       datetime.datetime.now() 
    order_items= ''
    price=0  

    for order in orders:
        order_items += '{} \n Size: {}'.format(order.meal,order.size)
        order_items += '\n Toppings: '
        for topping in order.toppings.all():
            order_items += '{}, '.format(topping)
        order_items += '\n Extras: '
        for extra in order.extras.all():
            order_items += '{}, '.format(extra)
        
        order_items += '\n \n'
        
        price += order.price        
        
    placedorder= PlacedOrder(user=user,date=date)
    placedorder.save()
    placedorder.price=price
    placedorder.order=order_items
    placedorder.save()

    for order in orders:
        order.delete()
    
    
    body='\n Welcome to Pinnochio\' Pizza & Subs! \n \n Order Number: {} \n You ordered:\n {}  Total Price: $ {} \n \n Thanks for using our online service! \n  Made with Love from Pinnochio\'s pizza & subs!♡ '.format(order.id, price, order_items)
    send_mail(
    'Pinnochio Pizza & Subs Order',
    body,
    admin,
    [user.email],
    fail_silently=False,
    )    
    
    return HttpResponseRedirect(reverse("cart"))

@login_required(login_url='/') 
def delete(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return HttpResponseRedirect(reverse("cart"))

@login_required(login_url='/') 
def myorders(request):
    user=       request.user
    orders = PlacedOrder.objects.filter(user=user)
    context = {
       "orders": orders
    }
    return render(request, "pizza_templates/orders.html", context)

@login_required(login_url='/') 
def allorders(request):
    user=       request.user
    if user.is_superuser:
        orders = PlacedOrder.objects.all()
        context = {
        "orders": orders
        }
        return render(request, "pizza_templates/allorders.html", context)
    else:
        return HttpResponseRedirect(reverse("myorders")) 

@login_required(login_url='/') 
def done(request, order_id):
    
    order = PlacedOrder.objects.get(pk=order_id)
    user=order.user
    order.done= True
    order.save()
    body='\n Welcome to Pinnochio\' Pizza & Subs! \n \n Order Number: {} is now Done! \n \n Thanks for using our online service! \n  Made with Love from Pinnochio\'s pizza & subs!♡ '.format(order.id)
    send_mail(
    'Pinnochio Pizza & Subs Order',
    body,
    admin,
    [user.email],
    fail_silently=False,
    ) 
    return HttpResponseRedirect(reverse("allorders"))

def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse("index"))  
