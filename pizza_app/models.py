from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone =     models.CharField(max_length=11, blank=True)
    address =   models.CharField(max_length=200, blank=True)
    def __str__(self):
        return f"{self.username} ({self.phone}) \n ({self.address})"
    

# Create your models here.
'''
Type model
    --> type_id
    --> type_name
        -- Regular Pizza
        -- Sicilian Pizza
        -- Subs    *
        -- Pasta
        -- Salads
        -- Dinner Platters
    --> offers extras 
        --boolen value
'''
class Type(models.Model):
    name =          models.CharField(max_length=64)
    extras =        models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name}"


class Topping(models.Model):
    name =          models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"


class Extra(models.Model):
    name =          models.CharField(max_length=64)
    price =         models.FloatField(default=0.5)
    def __str__(self):
        return f"{self.name}"

'''
meals model
    --> meal_id
    --> meal name
    --> meal type (meal_type model)
    --> small price 
    --> large price
    --> num of toppings offered 
'''
class Meal(models.Model):
    name =              models.CharField(max_length=64)
    type =              models.ForeignKey(Type, on_delete=models.CASCADE, related_name="meals")
    small_price =       models.FloatField(default=0)
    large_price =       models.FloatField(default=0)
    toppings =          models.IntegerField(default=0)
    def __str__(self):
        return f"{self.name} ({self.type})"

    

'''
orders model
    --> order_id
    --> user obj(User table)
    --> meal obj (meals model)
    --> size choosen
    --> toppings chosen
    --> Extras chosen
    --> time stamp
    --> done
'''
class Order(models.Model):
    user =           models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    meal =           models.ForeignKey(Meal, on_delete=models.CASCADE)
    size =           models.CharField(max_length=5)
    toppings =       models.ManyToManyField(Topping, blank=True)
    extras =         models.ManyToManyField(Extra, blank=True)
    price =          models.FloatField(default=0)

    def __str__(self):
        return f"{self.user} ({self.meal})"
    

class PlacedOrder(models.Model):
    user =          models.ForeignKey(User, on_delete=models.CASCADE) 
    order =         models.TextField(blank = True)
    comment =       models.TextField(blank = True)
    date=           models.DateTimeField() 
    done =          models.BooleanField(default=False) 
    price =         models.FloatField(default=0)  

    def __str__(self):
        return f"{self.order}"
    


