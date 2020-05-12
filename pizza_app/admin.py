from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin
from .models import Type, Topping, Extra, Meal, Order, PlacedOrder

User = get_user_model()
@admin.register(User)
class UserAdmin(OrigUserAdmin):
  list_display = (
    'username', 'first_name', 'last_name', 'phone', 'email', 'address'
  )

class TypeAdmin(admin.ModelAdmin):
      list_display = ('name',)
admin.site.register(Type, TypeAdmin)

class ToppingAdmin(admin.ModelAdmin):
      list_display = ('name',)
admin.site.register(Topping, ToppingAdmin)

class ExtraAdmin(admin.ModelAdmin):
      list_display = ('name', 'price')
admin.site.register(Extra, ExtraAdmin)

class MealAdmin(admin.ModelAdmin):
  list_display = ('name', 'type', 'small_price','large_price')
admin.site.register(Meal, MealAdmin)

'''
class ToppingInline(admin.StackedInline):
    model = Order.toppings.through
    extra = 1
class ExtraInline(admin.StackedInline):
    model = Order.extras.through
    extra = 1

class OrderAdmin(admin.ModelAdmin):
      inlines = [ToppingInline,ExtraInline]
      list_display = ('user', 'meal')
admin.site.register(Order, OrderAdmin)

'''
class PlacedOrderAdmin(admin.ModelAdmin):
      list_display = ('user', 'date', 'done')
admin.site.register(PlacedOrder, PlacedOrderAdmin)




