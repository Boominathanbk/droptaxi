from django.shortcuts import render,redirect,get_object_or_404
# 
#import googlemaps
from django.conf import settings
import requests
from geopy.distance import geodesic
from shapely import get_coordinates

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import JsonResponse

from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd
from shapely.geometry import Point
from twilio.rest import Client
from django.core.mail import send_mail
from datetime import datetime


def homepage(request):
   
    return render(request,'home.html')
 

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
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import requests
import os


def booking(request):
    if request.method == 'POST':
        pickup = request.POST.get('pickup')
        drop = request.POST.get('drop')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        fare = request.POST.get('fare')
        driverCharge = request.POST.get('driverCharge')
        total = request.POST.get('totalFare')
        distance = request.POST.get('distance')
        carType = request.POST.get('carType')

        # ✅ Validation
        if not all([pickup, drop, name, phone, date, time]):
            messages.error(request, "All fields are required.")
            return redirect('homepage')

        # ✅ Format date & time
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
            formatted_time = datetime.strptime(time, "%H:%M").strftime("%I:%M %p")
        except Exception as e:
            messages.error(request, "Invalid date or time format.")
            print("DATE/TIME ERROR:", e)
            return redirect('homepage')

        # ✅ EMAIL (Brevo SMTP)
        subject = "Booking Confirmed ✅"
        message = f"""
Your booking is confirmed!

🚗 TRIP DETAILS:
Pickup: {pickup}
Drop: {drop}
Name: {name}
Phone: {phone}
Email: {email}
Distance: {distance} km (approx)
Date: {formatted_date}
Time: {formatted_time}
Fare: ₹{fare}
Driver Bata: ₹{driverCharge}
Total Amount: ₹{total}
Car Type: {carType}
"""
        try:
            send_mail(
                subject,
                message,
                os.getenv("DEFAULT_FROM_EMAIL"),
                [email],
                fail_silently=False,
            )
            print(f"Email sent to {email}")
        except Exception as e:
            print("EMAIL FAILED:", e)

        # ✅ TELEGRAM (Only)
        telegram_message = f"""
📩 New Booking - ONE WAY TRIP

📍 Pickup: {pickup}
📍 Drop: {drop}

👤 Name: {name}
📱 Phone: +91 {phone}
✉️ Email: {email}

🗓️ Date: {formatted_date}
⏰ Time: {formatted_time}

💰 Fare: ₹{fare}
🚗 Car Type: {carType}
🧾 Driver Bata: ₹{driverCharge}
🔖 Total Fare: ₹{total}
"""
        try:
            telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN") or "8410338451:AAExpqr7sO18NkW9tjvwEw4p_AEkd2XNqzM"
            telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID") or "1313402845"

            telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
            response = requests.post(telegram_url, data={
                "chat_id": telegram_chat_id,
                "text": telegram_message
            })
            print("Telegram status:", response.status_code, response.text)
        except Exception as e:
            print("TELEGRAM FAILED:", e)

        messages.success(request, "Booking successful! Email & notification sent.")
        return redirect('homepage')

    return render(request, 'home.html')
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # 🔥 IMPORTANT
def enquries(request):
    if request.method == "POST":
        try:
            # ✅ Decode body properly
            data = json.loads(request.body.decode("utf-8"))

            # ✅ Required fields
            pickup = data.get("pickup")
            drop = data.get("drop")
            name = data.get("name")
            phone = data.get("phone")
            email = data.get("email")
            date = data.get("date")
            time = data.get("time")

            if not all([pickup, drop, name, phone, date, time]):
                return JsonResponse({
                    "status": "error",
                    "message": "All required fields are required"
                })

            # ✅ Optional fields with defaults
            fare = data.get("fare", "0")
            driverCharge = data.get("driverCharge", "0")
            total = data.get("totalFare", "0")
            distance = data.get("distance", "0")
            carType = data.get("carType", "Not specified")

            # ✅ Prepare Telegram message
            admin_message = f"""
📩 NEW ENQUIRY

👤 Name: {name}
📱 Phone: {phone}
✉️ Email: {email}

📍 Pickup: {pickup}
📍 Drop: {drop}

🗓 Date: {date}
⏰ Time: {time}

💰 Fare: {fare}
🧾 Drivercharge: {driverCharge}
🔖 Total: {total}
📏 Distance: {distance}
🚗 Car Type: {carType}
"""

            # ✅ Send Telegram
            telegram_bot_token = "8410338451:AAExpqr7sO18NkW9tjvwEw4p_AEkd2XNqzM"
            telegram_chat_id = "1313402845"
            telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"

            response = requests.post(telegram_url, data={
                "chat_id": telegram_chat_id,
                "text": admin_message
            })

            if response.status_code != 200:
                return JsonResponse({
                    "status": "error",
                    "message": f"Telegram failed: {response.text}"
                })

            return JsonResponse({
                "status": "success",
                "message": "Enquiry sent to admin"
            })

        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON format"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })

    return JsonResponse({"status": "invalid request"})


def round(request):
    return render(request,'round.html')



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
        try:
            # Get data
            pickup = request.POST.get('pickup')
            drop = request.POST.get('drop')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            date = request.POST.get('date')
            time = request.POST.get('time')
            fare = request.POST.get('fare')
            driverCharge = request.POST.get('driverCharge')
            total = request.POST.get('totalFare')
            distance = request.POST.get('distance')
            carType = request.POST.get('carType')
            number_of_days = request.POST.get('number_of_days')

            # ✅ Validation
            if not all([pickup, drop, name, phone, date, number_of_days]):
                messages.error(request, "All fields are required.")
                return redirect('round')

            # ✅ EMAIL
            subject = "Booking Completed ✅"
            message = f"""
Your booking is confirmed.

TRIP TYPE: ROUND TRIP
Pickup: {pickup} → {drop} → {pickup}

Name: {name}
Phone: +91 {phone}
Email: {email}

Date: {date}
Time: {time}
Number of Days: {number_of_days}

Fare (Minimum 250 km)
Driver Bata (Per Day): ₹{driverCharge}
Total Amount: ₹{total}

Car Type: {carType}

Thank you for booking with us!
"""

            try:
                send_mail(
                    subject,
                    message,
                    "boominathanpoongavanam@gmail.com",
                    [email],
                    fail_silently=False,
                )
                messages.success(request, "Round trip booking successful! Email sent.")
            except Exception as e:
                print("EMAIL ERROR:", e)
                messages.warning(request, "Booking done, but email failed.")

            # ✅ TELEGRAM
            telegram_message = f"""
📩 NEW ROUND TRIP BOOKING

📍 {pickup} → {drop} → {pickup}

👤 Name: {name}
📱 Phone: {phone}
✉️ Email: {email}

🗓 Date: {date}
⏰ Time: {time}
📆 Days: {number_of_days}

🚗 Car Type: {carType}
🧾 Driver Bata: ₹{driverCharge}
💰 Total Fare: ₹{total}
"""

            try:
                telegram_bot_token = "8410338451:AAExpqr7sO18NkW9tjvwEw4p_AEkd2XNqzM"
                telegram_chat_id = "1313402845"
                telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"

                response = requests.post(telegram_url, data={
                    "chat_id": telegram_chat_id,
                    "text": telegram_message
                })

                if response.status_code != 200:
                    print("Telegram Error:", response.text)

            except Exception as te:
                print("TELEGRAM ERROR:", te)

            return redirect('homepage')

        except Exception as e:
            print("ROUND BOOKING ERROR:", e)
            messages.error(request, "Something went wrong.")
            return redirect('round')

    return redirect('homepage')
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def enquries(request):

    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Invalid request method"
        })

    # ------------------ GET DATA ------------------
    name = request.POST.get("name", "").strip()
    phone = request.POST.get("phone", "").strip()
    pickup = request.POST.get("pickup", "").strip()
    drop = request.POST.get("drop", "").strip()
    date = request.POST.get("date", "").strip()
    time = request.POST.get("time", "").strip()

    number_of_days = request.POST.get('number_of_days',"").strip()
    car_type = request.POST.get("car_type", "").strip()
    distance = request.POST.get("distance", "").strip()
    total_fare = request.POST.get("total_fare", "").strip()

    # ------------------ REQUIRED VALIDATION ------------------
    if not all([name, phone, pickup, drop, date, time, number_of_days]):
        return JsonResponse({
            "status": "error",
            "message": "All required fields must be filled."
        })

    if not phone.isdigit() or len(phone) != 10:
        return JsonResponse({
            "status": "error",
            "message": "Enter valid 10 digit phone number."
        })

    try:
        days = int(number_of_days)
        if days <= 0:
            raise ValueError
    except ValueError:
        return JsonResponse({
            "status": "error",
            "message": "Invalid number of days."
        })

    # ------------------ TELEGRAM MESSAGE ------------------
    message = f"""
🚗 NEW BOOKING ENQUIRY

👤 Name: {name}
📞 Phone: {phone}

📍 Pickup: {pickup}
📍 Drop: {drop}

📅 Date: {date}
⏰ Time: {time}
🗓 Days: {number_of_days}

🚘 Car Type: {car_type}
📏 Distance: {distance} KM
💰 Total Fare: ₹{total_fare}
"""

    telegram_bot_token = "8410338451:AAExpqr7sO18NkW9tjvwEw4p_AEkd2XNqzM"
    telegram_chat_id = "1313402845"
    telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"

    try:
        response = requests.post(
            telegram_url,
            data={
                "chat_id": telegram_chat_id,   # ✅ FIXED HERE
                "text": message
            },
            timeout=10
        )

        print(response.text)  # 🔥 DEBUG

        if response.status_code != 200:
            return JsonResponse({
                "status": "error",
                "message": "Telegram sending failed"
            })

    except requests.exceptions.RequestException as e:
        print("Telegram Error:", e)
        return JsonResponse({
            "status": "error",
            "message": "Server error while sending enquiry"
        })

    return JsonResponse({
        "status": "success",
        "message": "Enquiry sent successfully"
    })



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
