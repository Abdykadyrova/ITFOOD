from django.shortcuts import redirect, render
from django.contrib import messages
from .models import FoodCategory,Food,Order,OrderDescription

def home(request):
    foodCategories = FoodCategory.objects.all()
    foods = Food.objects.all()
    return render(request,'home.html',{
        'foodCategories':foodCategories,
        'foods':foods
    })

#показывает блюд по категории
def get_foods_by_category(request,category_id):
    foods = Food.objects.filter(food_category_id = category_id)
    category = FoodCategory.objects.get(id= category_id)
    foodcategories = FoodCategory.objects.all()
    return render(request,
        'foods_by_category.html',
        {
            'foods':foods,
            'category':category,
            'foodCategories':foodcategories
        }
        )


def food_detail_views(request,food_id):

    #получаем еду по d
    food = Food.objects.get(id = food_id)
#
    foodCategories = FoodCategory.objects.all()

    return render(request,
    'food_detail.html',
    {
        'food':food,
        'foodCategories':foodCategories
    }
    )

def add_to_card(request,food_id):
    cards = request.session.get('food_cards',[])
    print(cards)
    cards.append(food_id)
        #сохраняем временно 
    request.session['food_cards'] = cards
    prev = request.GET.get('prev')
    return redirect(prev)
    

def del_to_card(request,food_id):
    cards = request.session.get('food_cards',[])
    cards.remove(food_id)
    #сохраняем временно 
    request.session['food_cards'] = cards
    prev = request.GET.get('prev')
    return redirect(prev)



def remove_to_card(request,food_id):
    cards = request.session.get('food_cards',[])
    new_cards = []
    for card in cards:
        if card != food_id:
            new_cards.append(card)
         
    #сохраняем временно 
    request.session['food_cards'] = new_cards
    prev = request.GET.get('prev')
    return redirect(prev)    
# обработчик показа блюд в корзине
def card_view(request):

    foodCategories = FoodCategory.objects.all()
    # id блюд кторые находится в корзине
    foods_ids = request.session.get('food_cards', [])
  
    foods_count =  {}
    card_foods = Food.objects.filter(id__in = foods_ids)
    order_sum = 0
    for card_food in card_foods:
        card_food.count = foods_ids.count(card_food.id)
        card_food.sum = card_food.count * card_food.sale_price
        order_sum = order_sum + card_food.sum

    return render(request, 
        'card_view.html',
        {
            'foods_ids': foods_ids,
            'card_foods':card_foods,
            'foodCategories':foodCategories,
            'order_sum':order_sum
        }
    )



def order_add(request):
    if request.method == 'POST':
        # id блюд которые находятся в корзине
        foods_ids = request.session.get('food_cards', [])
        # проверяем не пустая ли наша корзина
        if len(foods_ids) == 0:
            # Если наша корзина пустая отправляем сообщение клиенту об ошибке: Ваша корзина пустая
            messages.error(request, 'Ваша корзина пустая', extra_tags='danger')
            prev = request.POST.get('prev_url')
            return redirect(prev)
        # если корзина непустая
        else:
            # принимаем данные клиента для добавление в базу
            client_name = request.POST.get('client_name')
            client_phone = request.POST.get('client_phone')
            client_address = request.POST.get('client_address')
            
            # проверяем поля имя клиента или телефон клиента
            if len(client_phone) == 0:
                messages.warning(request, 'Вы не ввели телефонный номер', extra_tags='warning')
                prev = request.POST.get('prev_url')
                return redirect(prev)
            elif len(client_address) == 0:
                messages.warning(request, 'Вы не заполнили поле адрес', extra_tags='warning')
                prev = request.POST.get('prev_url')
                return redirect(prev)
            
            # получаем все блюда из базы по ids блюд из корзины
            card_foods = Food.objects.filter(id__in = foods_ids)
            # переменная для хранения для общей суммы заказа
            order_summ = 0
            # делаем перебор всех блюд для вычисления общий суммы заказа
            for card_food in card_foods:
                # вычисление количество одного блюда
                card_food.count = foods_ids.count(card_food.id)
                # сумма одного блюда с учетом кол-во
                card_food.sum = card_food.count * card_food.sale_price
                # общая сумма заказа
                order_summ = order_summ + card_food.sum
            
            # когда все поля заполнены мы сохраняем заказ в базу
            new_order = Order(
                client_name = client_name,
                client_address = client_address,
                client_phone = client_phone,
                client_location = '',
                order_status = 'новый',
                order_sum = order_summ
            )
            # сохраняем заказ в базу
            new_order.save()
            for card_food in card_foods:
                new_order_desc = OrderDescription()
                new_order_desc.order_id = new_order.id
                new_order_desc.food_id = card_food.id
                new_order_desc.food_count = card_food.count
                new_order_desc.sum = card_food.sum
                new_order_desc.save()

            
            messages.success(request, 'Ваш заказ принят. Спасибо за заказ)). Мы свяжемся с вами в течении суток.', extra_tags='success')

            request.session['food_cards'] = []
            prev = request.POST.get('prev_url')
            return redirect(prev)    