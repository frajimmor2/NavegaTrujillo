import json
from random import randint
from django.http import HttpResponse,HttpResponseForbidden
from django.shortcuts import render
from .models import Shopping_basket, Client, Ship, Reservation, Port
from accounts.models import CustomUser
from django.utils import timezone
from .forms import ReservationTimeForm,ReservationTimeUnloggedForm
from catalog.forms import ReservationDataForm,ReservationForm,ReservationFormNotLogged
from datetime import datetime,timedelta
from django.contrib.auth.decorators import login_required



def home(request):

    ships = Ship.objects.all()[:8]
    ports = Port.objects.all()
    context = {"ships": ships, "ports": ports}
    return render(request,"./business/home_view.html", context)


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        ships = Ship.objects.all()
        for ship in ships:
            if str(ship.id) not in cart.keys():
                cart[str(ship.id)] = {"quantity": 0}
        
        
    except:
        cart = {}
    
    
    '''ships_dict = {}
    for ship in Ship.objects.all():
        print(ship.id)
        ships_dict[ship.id] = {"quantity": 1}
    
        
    cart = ships_dict'''
        
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False, 'captain_amount': 0, 'captain_cost': 0, 'total_with_captain': 0}
    cartItems = order['get_cart_items']

    rental_start_date = request.GET.get('rental_start_date', None)
    rental_end_date = request.GET.get('rental_end_date', None)
    rental_days = 0

    # Este if calcula los dias alquilados y si no esta especificado el rango de fechas, se pone por default 1 dia
    if rental_start_date and rental_end_date:
            rental_days = (datetime.strptime(rental_end_date, "%Y-%m-%d") - datetime.strptime(rental_start_date, "%Y-%m-%d")).days
            rental_days = max(1, rental_days)  # Hace que el mínimo de días sea 1
    else:
        rental_days = 1
    
    for i in cart:
        
        try:
            cartItems += cart[i]["quantity"]
            ship = Ship.objects.get(id=i)
            total = (ship.rent_per_day * cart[i]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]
            
            items.append({'ship': ship, 'quantity':cart[i]["quantity"],'get_total':total})

        except:
            pass

    captain_amount = cart.get('captain_amount', 0)
    if captain_amount > cartItems:  # Este if es el que limita la cantidad de capitanes a la cantidad de barcos
        captain_amount = cartItems  

    order['captain_amount'] = captain_amount
    order['captain_cost'] = captain_amount * 120 * rental_days # Aqui guarda el precio de los capitanes para invocarlo usando order['coste_capitan']
    order['total_with_captain'] = order['get_cart_total'] + order['captain_cost']

    return {"items": items, "order": order, "cartItems": cartItems, "ships": Ship.objects.all()}

def reservation(request,ship_id):
    ''' Punto de toma de los datos de la reserva (plazo en el que se va a reservar, y método de pago (contrareembolso por ahora)
        Se llega desde la toma de datos inicial si el usuario no está logueado, o directamente si sí '''
    try:
        ship = Ship.objects.get(id=ship_id)
    except:
        ship = False

    if request.method=="POST":
        if not ship:
            ''' No debería pasar sin herramientas externas, este endpoint solo recibe Posts '''
            return HttpResponse("Ese barco no existe; ¿como has llegado aquí?", status=404)
        
        form = ReservationDataForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            captain = form.cleaned_data['captain']
            try:
                user1 = CustomUser.objects.get(Email=email)
                user1 = True
            except:
                user1 = False

            
            user = CustomUser()
            user.username = hash(" ".join([name,email,str(randint(1,100000))]))
            user.email = ""
            user.name = email if user1 else name
            user.surname = str(name+surname) if user1 else surname
            client = Client()
            client.license_number=""
            client.license_validated=False
            shopping_basket = Shopping_basket()
            shopping_basket.rental_start_date = timezone.now()+timedelta(days=1)
            shopping_basket.rental_end_date = timezone.now()+timedelta(days=1)
            shopping_basket.captain_amount = 1 if captain else 0
            shopping_basket.save()
            shopping_basket.ships.add(ship)
            shopping_basket.save()
            client.shopping_basket = shopping_basket
            client.save()
            user.shopping_basket = shopping_basket
            user.client = client
            user.save()
            

            form = ReservationTimeUnloggedForm() # TODO
            form.initial['user'] = user.username
            form.initial['captain'] = captain
            return render(request,'./business/reservation_payment.html', {'form':form,'ship':ship})

        form = ReservationForm(request.POST)
        if form.is_valid():
            captain = form.cleaned_data['captain']
        else:
            form = ReservationFormNotLogged(request.POST)
            if form.is_valid():
                captain = form.cleaned_data['captain']
        name = request.user.name
        surname = request.user.surname
        email = request.user.email
        user = CustomUser()
        user.username = hash(" ".join([name,email,str(randint(1,100000))]))
        user.email = ""
        user.name = email 
        user.surname = str(name+surname) 
        client = Client()
        client.license_number=""
        client.license_validated=False
        shopping_basket = Shopping_basket()
        shopping_basket.rental_start_date = timezone.now()+timedelta(days=1)
        shopping_basket.rental_end_date = timezone.now()+timedelta(days=1)
        shopping_basket.captain_amount = 1 if captain else 0
        shopping_basket.save()
        shopping_basket.ships.add(ship)
        shopping_basket.save()
        client.shopping_basket = shopping_basket
        client.save()
        user.shopping_basket = shopping_basket
        user.client = client
        user.save()

        form = ReservationTimeUnloggedForm() # TODO
        form.initial['user'] = user.username
        form.initial['captain'] = captain
        return render(request,'./business/reservation_payment.html',{'form':form,'ship':ship})

    else:
        if not request.user.is_authenticated:
            return HttpResponse("Acceda desde el escaparate o la página del barco por favor",status=405)
        if not ship:
            return HttpResponse("Ese barco no existe",status=404)




def cart_reservation(request):
    ''' Punto de toma de los datos de la reserva (plazo en el que se va a reservar, y método de pago (contrareembolso por ahora)
        Se llega desde la toma de datos inicial si el usuario no está logueado, o directamente si sí '''

    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']
            
    if request.method=="POST":
        
        form = ReservationDataForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            try:
                user1 = CustomUser.objects.get(Email=email)
                user1 = True
            except:
                user1 = False

            user = CustomUser()
            user.username = hash(" ".join([name,email,str(randint(1,1000000))]))
            user.email = ""
            user.name = email if user1 else name
            user.surname = str(name+surname) if user1 else surname
            client = Client()
            client.license_number=""
            client.license_validated=False
            shopping_basket = Shopping_basket()
            shopping_basket.rental_start_date = timezone.now()
            shopping_basket.rental_end_date = timezone.now()
            shopping_basket.captain_amount = order['captain_amount']
            shopping_basket.save()
            client.shopping_basket = shopping_basket
            client.save()
            user.shopping_basket = shopping_basket
            user.client = client
            user.save()
            

            form = ReservationTimeUnloggedForm()
            form.initial['user'] = user.username
            form.initial['captain'] = False
            taken_days = []
            ships = []
            for i in items:
                ship = i['ship']
                ship = Ship.objects.get(id = ship.id)
                for o in range(i['quantity']):
                    ships.append(ship)
            if not ships:
                return HttpResponse("Algo ha ido mal",status = 500)

            taken_days = set()
            for ship in ships:
                for reservation in ship.reservation_set.all():
                    start_date = reservation.rental_start_date
                    end_date = reservation.rental_end_date
                    if start_date in taken_days and end_date in taken_days:
                        break
                    delta = end_date-start_date
                    delta = delta.days
                    for i in range(delta+1):
                        taken_days.add(start_date+timedelta(days=i))            

            return render(request,'./business/reservation_cart.html', {'form':form,'taken_days':taken_days})

        else:
            return HttpResponse("Algo ha ido mal",status=500)

    else:
        form = False
        form2 = False
        if request.user.is_authenticated:
            form = ReservationTimeUnloggedForm()
            form.initial['captain'] = False
            form.initial['user'] = hash(request.user.email+request.user.username+str(randint(1,10000)))
            user = CustomUser()
            user.username = form.initial['user']
            user.email = ""
            user.name = request.user.email
            user.surname = str(request.user.name+request.user.surname)
            client = Client()
            client.license_number=""
            client.license_validated=False
            shopping_basket = Shopping_basket()
            shopping_basket.rental_start_date = timezone.now()
            shopping_basket.rental_end_date = timezone.now()
            shopping_basket.captain_amount = order['captain_amount']
            shopping_basket.save()
            client.shopping_basket = shopping_basket
            client.save()
            user.shopping_basket = shopping_basket
            user.client = client
            user.save()
        else:
            form2 = ReservationDataForm()
        
        ships = []
        for i in items:
            ship = i['ship']
            ship = Ship.objects.get(id = ship.id)
            for o in range(i['quantity']):
                ships.append(ship)
        if not ships:
            return HttpResponse("Algo ha ido mal",status = 500)

        taken_days = set()
        for ship in ships:
            for reservation in ship.reservation_set.all():
                start_date = reservation.rental_start_date
                end_date = reservation.rental_end_date
                if start_date in taken_days and end_date in taken_days:
                    break
                delta = end_date-start_date
                delta = delta.days+1
                for i in range(delta):
                    taken_days.add(start_date+timedelta(days=i))

        return render(request,'./business/reservation_cart.html', {'form':form,'form2':form2,'taken_days':taken_days})


def confirm_reservation_cart(request):
    
    if request.method=="GET":
        ''' No debería pasar, aquí solo se entra desde la vista anterior '''
        return HttpResponse("Para realizar reservas, accede desde el escaparate", status=405)
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

    form = ReservationTimeUnloggedForm(request.POST)
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        username = form.cleaned_data['user']

        user = CustomUser.objects.get(username=username)
        reservation = Reservation()
        reservation.rental_start_date = start_date
        reservation.rental_end_date = end_date
        reservation.reservation_state = 'R'
        reservation.captain_amount = order['captain_amount']
        reservation.total_cost = order['total_with_captain']
        ships = []
        for i in items:
            ship = i['ship']
            ship = Ship.objects.get(id = ship.id)
            for o in range(i['quantity']):
                ships.append(ship)
        if not ships:
            return HttpResponse("Algo ha ido mal",status = 500)
        reservation.port = ships[0].port
        reservation.save()
        reservation.ships.set(ships)
        reservation.save()
        user.client.reservation = reservation
        user.save()
        return render(request, './business/reservation_cart_confirmed.html', {'lookup_id':user.username})



def confirm_reservation(request,ship_id):
    ''' Último paso, creamos la reserva y hemos terminado (falta devolver la id de seguimiento únicamente '''

    if request.method=="GET":
        ''' No debería pasar, aquí solo se entra desde la vista anterior '''
        return HttpResponse("Para realizar reservas, accede desde el escaparate",status=405)
    
    try:
        ship = Ship.objects.get(id=ship_id)
    except:
        ship = False

    if not ship:
        ''' Para que esto pase hacen falta herramientas externas y ser tontito '''
        # Castigamos al usuario por hacer cosas raras
        # os.sleep(100000)
        return HttpResponse("¿Cómo has llegado aquí?",status=400)

    if request.user.is_authenticated:
        form = ReservationTimeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            captain = form.cleaned_data['captain']
        else:
            return HttpResponse("Algo ha ido mal",status=400)

        user = CustomUser.objects.get(username=request.user.username)
        reservation = Reservation()
        reservation.rental_start_date = start_date
        reservation.rental_end_date = end_date
        reservation.reservation_state = 'R'
        reservation.captain_amount = 1 if captain else 0
        reservation.total_cost = ship.rent_per_day+reservation.captain_amount*120
        reservation.client = user.client
        reservation.port = ship.port
        reservation.save()
        reservation.ships.set(user.shopping_basket.ships.all())
        reservation.save()
        user.save()         
        return render(request, './business/reservation_confirmed.html')

    else:
        form = ReservationTimeUnloggedForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            username = form.cleaned_data['user']
            captain = form.cleaned_data['captain']
        else:
            return HttpResponse("Algo ha salido mal",status=500)

        user = CustomUser.objects.get(username=username)
        reservation = Reservation()
        reservation.rental_start_date = start_date
        reservation.rental_end_date = end_date
        reservation.reservation_state = 'R'
        reservation.captain_amount = 1 if captain else 0
        reservation.total_cost = ship.rent_per_day+reservation.captain_amount*120
        reservation.client = user.client
        reservation.port = user.shopping_basket.ships.all()[0].port
        reservation.save()
        reservation.ships.set(user.shopping_basket.ships.all())
        reservation.save()
        user.save()

        return render(request, './business/reservation_confirmed.html', {'lookup_id':user.username})

def cart(request):
    '''
    if request.user.is_authenticated:      
        shopping_basket, created = Shopping_basket.objects.get_or_create(customuser=request.user)
        has_ships = shopping_basket.ships.exists()

        return render(request, './business/cart.html', {
        'shopping_basket': shopping_basket,
        'has_ships': has_ships
    })
    
    else:
    '''
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']
    return render(request, './business/cart.html', {
    'cartItems':cartItems ,'order':order, 'items':items  #, 'shopping_basket': shopping_basket, 'has_ships': has_ships
    })





@login_required
def add_port(request):
    # Verifica si el usuario tiene permiso de staff
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")

    if request.method == "POST":
        ubication = request.POST.get("ubication")
        if ubication:
            Port.objects.create(ubication=ubication)
            return redirect("home")  # Redirige al usuario al inicio después de añadir el puerto

    return render(request, "./business/add_port.html")
