import json
from django.http import HttpResponse,HttpResponseForbidden
from django.shortcuts import render, redirect
from .models import Shopping_basket, Client, Ship, Reservation, Port
from accounts.models import CustomUser
from django.utils import timezone
from .forms import ReservationTimeForm,ReservationTimeUnloggedForm, EditProfileForm
from catalog.forms import ReservationDataForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ValidationError
from catalog.forms import dates_form
from catalog.filters import ship_filter



def home(request):

    ships = Ship.objects.all()[:8]
    ports = Port.objects.all()
    f = ship_filter(request.GET, queryset=(Ship.objects.all()))
    form = dates_form()
    context = {"ships": ships, "ports": ports, "filter": f, "form": form}
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
            try:
                user = CustomUser.objects.get(Email=email)
                user = True
            except:
                user = False

            if user:
                ''' Ese email está en uso, nanai '''
                return HttpResponse("Ese email ya existe, si tienes cuenta inicia sesión por favor",status=401)
            
            user = CustomUser()
            user.username = hash(" ".join([name,email]))
            try:
                CustomUser.objects.get(username=user.username)
                exists=True
            except:
                exists=False
            if not exists:
                user.email = email
                user.name = name
                user.surname = surname
                client = Client()
                client.license_number=""
                client.license_validated=False
                shopping_basket = Shopping_basket()
                shopping_basket.rental_start_date = timezone.now()
                shopping_basket.rental_end_date = timezone.now()
                shopping_basket.captain_amount = 0 # TODO arreglar esto
                shopping_basket.save()
                shopping_basket.ships.add(ship)
                shopping_basket.save()
                client.shopping_basket = shopping_basket
                client.save()
                user.shopping_basket = shopping_basket
                user.client = client
                user.save()
            

            form = ReservationTimeUnloggedForm()
            form.initial['user'] = user.username
            # TODO crear lista con los intervalos en los que el barco no está disponible
            taken_days = []

            return render(request,'./business/reservation.html', {'form':form,'taken_days':taken_days,'ship':ship})

        else:

            if request.user.is_authenticated:
                # TODO crear lista con los intervalos en los que el barco no está disponible
                taken_days = []
                form = ReservationTimeForm()
                return render(request,'./business/reservation.html', {'form':form,'taken_days':taken_days,'ship':ship})


            ''' ¿Que? '''
            return HttpResponse("Rellene el formulario correctamente por favor",status=405)


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
                user = CustomUser.objects.get(Email=email)
                user = True
            except:
                user = False

            if user:
                ''' Ese email está en uso, nanai '''
                return HttpResponse("Ese email ya existe, si tienes cuenta inicia sesión por favor",status=401)
            
            user = CustomUser()
            user.username = hash(" ".join([name,email]))
            try:
                CustomUser.objects.get(username=user.username)
                exists=True
            except:
                exists=False
            if not exists:
                user.email = email
                user.name = name
                user.surname = surname
                client = Client()
                client.license_number=""
                client.license_validated=False
                shopping_basket = Shopping_basket()
                shopping_basket.rental_start_date = timezone.now()
                shopping_basket.rental_end_date = timezone.now()
                shopping_basket.captain_amount = 0 # TODO arreglar esto
                shopping_basket.save()
                client.shopping_basket = shopping_basket
                client.save()
                user.shopping_basket = shopping_basket
                user.client = client
                user.save()
            

            form = ReservationTimeUnloggedForm()
            form.initial['user'] = user.username
            # TODO crear lista con los intervalos en los que el barco no está disponible
            taken_days = []

            return render(request,'./business/reservation_cart.html', {'form':form,'taken_days':taken_days})

        else:
            return HttpResponse("Algo ha ido mal",status=500)

    else:
        form = False
        form2 = False
        if request.user.is_authenticated:
            form = ReservationTimeUnloggedForm()
            form.initial['user'] = request.user.username
        else:
            form2 = ReservationDataForm()
        
        # TODO crear lista con los intervalos en los que el barco no está disponible
        taken_days = []
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
        else:
            return HttpResponse("Algo ha ido mal",status=400)

        user = CustomUser.objects.get(username=request.user.username)
        reservation = Reservation()
        reservation.rental_start_date = start_date
        reservation.rental_end_date = end_date
        reservation.reservation_state = 'R'
        reservation.captain_amount = 0 # TODO fix this
        reservation.total_cost = 0 # TODO calcular coste
        reservation.client = user.client
        reservation.port = user.shopping_basket.ships.all()[0].port
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
        else:
            return HttpResponse("Algo ha salido mal",status=500)

        user = CustomUser.objects.get(username=username)
        reservation = Reservation()
        reservation.rental_start_date = start_date
        reservation.rental_end_date = end_date
        reservation.reservation_state = 'R'
        reservation.captain_amount = 0 # TODO fix this
        reservation.total_cost = 0 # TODO calcular coste
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





@login_required
def manage_license(request, username):
    # Solo usuarios con permisos de staff pueden acceder a la pagina
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")

    # Obtén el usuario a partir del username
    user = get_object_or_404(CustomUser, username=username)

    # Intenta obtener el cliente asociado al usuario
    try:
        client = Client.objects.get(id=user.client_id)  # Relación entre CustomUser y Client usando `client_id`
    except Client.DoesNotExist:
        return HttpResponse("El usuario no tiene un cliente asociado.", status=404)

    if request.method == "POST":
        # Toma los datos enviados desde el formulario para actualizar la licencia del cliente
        license_number = request.POST.get("license_number")
        license_validated = request.POST.get("license_validated") == "on"

        # Actualiza los atributos del cliente que corresponda al campo username que ponemos en la ruta
        client.license_number = license_number
        client.license_validated = license_validated
        client.save()

        # Redirige al usuario al home después de guardar para que sea mas comodo
        return redirect("home")

    
    return render(request, './business/manage_license.html', {"client": client, "username": username})

@login_required
def add_ship(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")

    if request.method == "POST":
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        rent_per_day = request.POST.get("rent_per_day")
        available = request.POST.get("available") == "on"
        need_license = request.POST.get("need_license") == "on"
        description = request.POST.get("description")
        port_id = request.POST.get("port")
        image = request.FILES.get("image")

        if name and capacity and rent_per_day and description and port_id:
            try:
                port = Port.objects.get(id=port_id)

                Ship.objects.create(
                    name=name,
                    capacity=int(capacity),
                    rent_per_day=float(rent_per_day),
                    available=available,
                    need_license=need_license,
                    description=description,
                    image=image,
                    port=port  
                )
                return redirect("home")

            except Port.DoesNotExist:
                return render(request, "./business/add_ship.html", {
                    "ports": Port.objects.all(),
                    "error": "El puerto seleccionado no existe."
                })

            except ValidationError as e:
                return render(request, "./business/add_ship.html", {
                    "ports": Port.objects.all(),
                    "error": f"Error de validación: {e.messages}"
                })

    return render(request, "./business/add_ship.html", {
        "ports": Port.objects.all()  
    })

def profile(request):
    user = request.user
    client = user.client
    return render(request, "./business/profile.html", {"user": user, "client": client})

def edit_profile(request):
    user = request.user

    # Prellenar el formulario con los datos del usuario y del cliente
    initial_data = {
        'name': user.name,
        'surname': user.surname,
        'username': user.username,
        'email': user.email,
    }
    if user.client:
        initial_data['license_number'] = user.client.license_number

    if request.method == 'POST':
        user = request.user

    # Prellenar el formulario con los datos del usuario y del cliente
    initial_data = {
        'name': user.name,
        'surname': user.surname,
        'username': user.username,
        'email': user.email,
    }
    if user.client:
        initial_data['license_number'] = user.client.license_number

    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            # Actualizar los datos del usuario
            user.name = form.cleaned_data['name']
            user.surname = form.cleaned_data['surname']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()

            # Actualizar los datos del cliente (si existe)
            if user.client:
                user.client.license_number = form.cleaned_data['license_number']
                user.client.save()

            return redirect('profile')  # Redirigir al perfil después de guardar
    else:
        form = EditProfileForm(initial=initial_data)

    return render(request, 'business/edit_profile.html', {'form': form})

