from django.shortcuts import render,redirect,get_object_or_404
# 
#import googlemaps
from django.conf import settings
import requests
from geopy.distance import geodesic
from shapely import get_coordinates
from .models import Booking, RoundTrip
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.http import JsonResponse
from .models import sedancar
from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd
from shapely.geometry import Point
from twilio.rest import Client
from django.core.mail import send_mail


def homepage(request):
    car = sedancar.objects.all()
    return render(request,'home.html',{'car':car})
 

# # Booking view
# def booking(request):
#     if request.method == 'POST':
#         # Get data from the form
#         pickup = request.POST['pickup']
#         drop = request.POST['drop']
#         name = request.POST['name']
#         phone = request.POST['phone']
#         email = request.POST['email']
#         date = request.POST['date']
#         time = request.POST['time']
#         fare = request.POST['fare']
#         driverCharge = request.POST['driverCharge']
#         total = request.POST['totalFare']
#         distance = request.POST['distance']
#         carType = request.POST['carType']

#         # Validate the data (you can add more validations here)
#         if not pickup or not drop or not name or not phone or not email or not date or not time:
#             messages.error(request, "All fields are required.")
#             return redirect('login')  # Stay on the same page if fields are missing

#         try:
#             # Create a booking instance
#             booking = Booking.objects.create(
#                 pickup=pickup,
#                 drop=drop,
#                 name=name,
#                 phone=phone,
#                 email=email,
#                 date=date,
#                 time=time,
#                 fare=fare,
#                 total=total,
#                 driverCharge=driverCharge,
#                 distance=distance,
#                 carType=carType
#             )
#             booking.save()

#             # Success message and redirect to the homepage or success page
#             subject = "Booking Completed"
#             message = f"""\nYour Booking confirmed.\nTRIP TYPE\n ONE WAY TRIP

#             Pickup: {pickup},
#             Drop: {drop},
#             Dear: {name}
#             Phone: {phone}
#             Email: {email}
#             Distance: {distance} km (Approximate)
#             Date: {date}
#             Time: {time}
#             Fare (minimum fare 130 km): ₹ {fare}
#             Driver Bata: ₹{driverCharge}
#             Total Amount: ₹{total}
#             Car Type: {carType}

#             Thank you for booking with us!"""
#             recipient = email
#             send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)

#             messages.success(request, "Booking successful! A confirmation message has been sent to your Email.")
#             return redirect('homepage')  # Adjust the redirection as per your URL configuration

#         except Exception as e:
#             messages.error(request, f"An error occurred: {e}")
#             return redirect('homepage')  # Stay on the same page and show the error

#     # Render the booking form if it's a GET request
#     return render(request, 'home.html')

import requests

# Booking view
def booking(request):
    if request.method == 'POST':
        # Get data from the form
        pickup = request.POST['pickup']
        drop = request.POST['drop']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        date = request.POST['date']
        time = request.POST['time']
        fare = request.POST['fare']
        driverCharge = request.POST['driverCharge']
        total = request.POST['totalFare']
        distance = request.POST['distance']
        carType = request.POST['carType']

        # Validate the data (you can add more validations here)
        if not pickup or not drop or not name or not phone or not email or not date or not time:
            messages.error(request, "All fields are required.")
            return redirect('login')  # Stay on the same page if fields are missing

        try:
            # Create a booking instance
            booking = Booking.objects.create(
                pickup=pickup,
                drop=drop,
                name=name,
                phone=phone,
                email=email,
                date=date,
                time=time,
                fare=fare,
                total=total,
                driverCharge=driverCharge,
                distance=distance,
                carType=carType
            )
            booking.save()

            # Send confirmation email to the user
            subject = "Booking Completed"
            message = f"""Your Booking confirmed.\nTRIP TYPE: ONE WAY TRIP

Pickup: {pickup},

Drop: {drop},

Dear: {name}

Phone: {phone}

Email: {email}

Distance: {distance} km (Approximate)

Date: {date}

Time: {time}

Fare : ₹ {fare}

Driver Bata: ₹{driverCharge}

Total Amount: ₹{total}

Car Type: {carType}

Note : Toll & Permit, Hills, package =Rs 300, cleaning = Rs 300, carrer charge =Rs 300, Extre Luggage=Rs 300

Charges Applicable

Thank you for booking with us!"""
            recipient = email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)

            # Send Telegram message to Admin
            telegram_message = f"""New Booking\nTRIP TYPE: ONE WAY TRIP:

Pickup: {pickup}
Drop: {drop}
Name: {name}
Phone: {phone}
Email: {email}
Date: {date}
Time: {time}
Fare: ₹{fare}
Driver Bata: ₹{driverCharge}
Total Fare: ₹{total}
Car Type: {carType}
"""
            telegram_bot_token = ''  # Replace with your bot's token
            telegram_chat_id = ''
            telegram_url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'

            payload = {
                'chat_id': telegram_chat_id,
                'text': telegram_message
            }

            # Send the Telegram message
            response = requests.post(telegram_url, data=payload)
            if response.status_code != 200:
                raise Exception(f"Telegram error: {response.text}")

            # Success message and redirect to the homepage or success page
            messages.success(request, "Booking successful! A confirmation message has been sent to your Email.")
            return redirect('homepage')  # Adjust the redirection as per your URL configuration

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('homepage')  # Stay on the same page and show the error

    # Render the booking form if it's a GET request
    return render(request, 'home.html')


def round(request):
    return render(request,'round.html')

def admin_page(request):
    if request.user.is_superuser:
        round = RoundTrip.objects.all()
        new_bookings = Booking.objects.filter(is_active=True) 
        pending_count = new_bookings.count()
        
        round_bookings = RoundTrip.objects.filter(is_active=True)  # Assuming is_active=False indicates new or pending bookings          
        pending_round = round_bookings.count()
        
        return render(request, 'admin.html', {'new_bookings': new_bookings, 'pending_count': pending_count,'round':round, 'pending_round':pending_round})
    else:
        return redirect('homepage')


def approve_booking(request, pk):
    try:
        booking = Booking.objects.get(id=pk)
        booking.is_active = False  

        booking.save()
        messages.success(request, f'Booking has been confirm.')

    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
    return redirect('admin_page')


def approve_round(request, pk):
    try:
        round = RoundTrip.objects.get(id=pk)
        round.is_active = False  

        round.save()
        messages.success(request, f'Booking has been confirm.')

    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
    return redirect('admin_page')
    
    


def booking_details(request):
    # Get all bookings, you can filter this if needed
    bookings = Booking.objects.all()
    new_bookings = Booking.objects.filter(is_active=True)  # Assuming is_active=False indicates new or pending bookings
        
        # Count the number of new/pending bookings
    pending_count = new_bookings.count()
    round_bookings = RoundTrip.objects.filter(is_active=True)  # Assuming is_active=False indicates new or pending bookings          
    pending_round = round_bookings.count()
    # Pass the bookings to the template
    return render(request, 'booking_details.html', {'bookings': bookings,'pending_count':pending_count,'pending_round':pending_round})

def Delete(request,pk):
    delete=Booking.objects.get(id=pk)
    delete.delete()
    messages.success(request,"deleted successfully")
    return redirect("booking_details")

def Delete_round(request,pk):
    delete=RoundTrip.objects.get(id=pk)
    delete.delete()
    messages.success(request,"deleted successfully")
    return redirect("roundtrip")

def login(request):
    return render(request,'login.html')

def login_data(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            if(user.is_superuser):
                return redirect("admin_page")
            else:
                request.session['uid']=user.id
                return redirect("user_page")
        else:
            messages.info(request,"Invalid username and password")
            return redirect("login")
    else:
        return redirect("login")  
    


def round_booking(request):
    if request.method == 'POST':
        # Get data from the form
        pickup = request.POST['pickup']
        drop = request.POST['drop']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        date = request.POST['date']
        time = request.POST['time']
        fare = request.POST['fare']
        driverCharge = request.POST['driverCharge']
        total = request.POST['totalFare']
        distance = request.POST['distance']
        carType = request.POST['carType']
        number_of_days = request.POST['number_of_days']

        # Validate the data (you can add more validations here)
        if not pickup or not drop or not name or not phone or not email or not date or not number_of_days :
            messages.error(request, "All fields are required.")
            return redirect('login')  # Stay on the same page if fields are missing

        try:
            # Create a booking instance
            round = RoundTrip.objects.create(
                pickup=pickup,
                drop=drop,
                name=name,
                phone=phone,
                email=email,
                date=date,
                time=time,
                fare=fare,
                total=total,
                driverCharge=driverCharge,
                distance=distance,
                carType=carType,
                number_of_days=number_of_days,
            )
            round.save()

            # Success message and redirect to the homepage or success page
            subject = "Booking Completed"
            message = f"""\nYour Booking confirmed.\nTRIP TYPE\n ROUND TRIP

Pickup: {pickup}-->{drop}-->{pickup},
Dear: {name}
Phone: {phone}
Email: {email}

Date: {date}
Time: {time}
Number_of_days: {number_of_days}
Fare (minimum fare 250 km):
Driver Bata (per day): ₹{driverCharge}
Total Amount: ₹{total}
Car Type: {carType}

Thank you for booking with us!"""
            recipient = email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            
            telegram_message = f"""New Booking\nTRIP TYPE: ROUND TRIP:

Pickup: {pickup}
Drop: {drop}
Name: {name}
Phone: {phone}
Email: {email}
Date: {date}
Time: {time}
Number_of_days: {number_of_days}
Driver Bata: ₹{driverCharge}
Total Fare: ₹{total}
Car Type: {carType}
"""
            telegram_bot_token = ''  # Replace with your bot's token
            telegram_chat_id = ''  # Replace with your admin's chat ID
            telegram_url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'

            payload = {
                'chat_id': telegram_chat_id,
                'text': telegram_message
            }

            # Send the Telegram message
            response = requests.post(telegram_url, data=payload)
            if response.status_code != 200:
                raise Exception(f"Telegram error: {response.text}")

            messages.success(request, "Booking successful! A confirmation message has been sent to your Email.")
            return redirect('homepage')  # Adjust the redirection as per your URL configuration

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('homepage')  # Stay on the same page and show the error

    # Render the booking form if it's a GET request
    return render(request, 'home.html')

def roundtrip(request):
    bookings = Booking.objects.all()
    round = RoundTrip.objects.all()
     
    round_bookings = RoundTrip.objects.filter(is_active=True)  # Assuming is_active=False indicates new or pending bookings          
    pending_round = round_bookings.count()
    new_bookings = Booking.objects.filter(is_active=True) 
    pending_count = new_bookings.count()
    return render(request,'round_admin.html',{'bookings': bookings,'pending_count':pending_count,'round':round, 'pending_round':pending_round})

def about(request):
    return render(request,'about.html')
