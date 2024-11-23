from django.http import HttpResponse
from django.shortcuts import render
from .models import Shopping_basket, Client, Ship, Reservation
from accounts.models import CustomUser
from django.utils import timezone
from .forms import ReservationTimeForm,ReservationTimeUnloggedForm
from catalog.forms import ReservationDataForm



def home(request):
    return render(request,"./business/home_view.html")

def cart(request):
    print(request.user)
    print(dir(request))
    if request.user.is_authenticated:
        print(Shopping_basket.client)
        print("user ahora")
        print(request.user.client)
        
        shopping_basket, created = Shopping_basket.objects.get_or_create(client=request.user.client)
        print(shopping_basket)
        if shopping_basket.ships.exists():
            has_ships = shopping_basket.ships.exists() 
            print(has_ships)
        else:
            has_ships = False
    else:
        return HttpResponse("Usuario no autentificado", status=401)
    
    return render(request, './business/cart.html', {'shopping_basket': shopping_basket, 'has_ships': has_ships})

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
            user.username = hash(" ".join([name,email,str(ship.id)]))
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
        reservation.port = ship.port 
        reservation.save()
        reservation.ships.add(ship)
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
        reservation.port = user.client.shopping_basket.ships.all()[0].port
        reservation.save()
        reservation.ships.set(user.client.shopping_basket.ships.all())
        reservation.save()
        user.save()

        return render(request, './business/reservation_confirmed.html', {'lookup_id':user.username})


