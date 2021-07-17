from django.shortcuts import redirect, render
from django.contrib import messages
from .models import FoodCategory,Food

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
    for card_food in card_foods:
        card_food.count = foods_ids.count(card_food.id)
        card_food.sum = card_food.count * card_food.sale_price

    return render(request, 
        'card_view.html',
        {
            'foods_ids': foods_ids,
            'card_foods':card_foods,
            'foodCategories':foodCategories
        }
    )

def order_add(request):
    if request.method == "POST" :
        foods_ids = request.session.get('food_cards',[])
        if len(foods_ids) ==0:
            messages.error(request,'Ваша карзина пустая',
            extra_tags='danger')
            prev = request.POST.get('prev_url')
            return redirect(prev)
        else:    
            client_name = request.POST.get('client_name')
            client_phone = request.POST.get('client_pphone')  
            client_address = request.POST.get('client_address')
      

