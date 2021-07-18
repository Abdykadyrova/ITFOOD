from django.contrib import admin
from .models import FoodCategory, Food, Order, OrderDescription

admin.site.register(FoodCategory)
admin.site.register(Food)

class OrderAdmin(admin.ModelAdmin):
    model = 'Order'
    list_display = [
        'order_nomer',
        'client_name',
        'client_phone',
        'client_address',
        'order_sum',
    ]

    def order_nomer(self, obj):
        return obj.id

admin.site.register(Order, OrderAdmin)


class OrderDescAdmin(admin.ModelAdmin):
    model = 'OrderDescription'
    list_display = [
        'order_title', 
        'food_name', 
        'food_count_total',
        'summa'
    ]

    def order_title(self, obj):
        return '№'+str(obj.order.id) + '-'+obj.order.client_name

    def food_name(self, obj):
        return obj.food.name

    def food_count_total(self, obj):
        return obj.food_count
    
    def summa(self, obj):
        return str(obj.sum) + ' сом'

    order_title.short_description  = 'Номер заказа'
    food_name.short_description  = 'Блюдо'
    food_count_total.short_description  = 'Кол-во'
    summa.short_description  = 'Сумма'

admin.site.register(OrderDescription, OrderDescAdmin)