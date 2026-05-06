import json
import requests
import os

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime



def homepage(request):
    return render(request,'home.html')
             
def round(request):
   return render(request, 'round.html')



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

Note: Excluding - Hills, Tollgate & Permit Charges Applicable if use only.

Thank you for booking with us! DROP TAXI BOOKING..!
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
            telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN") or "8749101532:AAGyz-1mLJNA5vObrtdw9Ytm2H8ZR8cP7OA"
            telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID") or "1941956017"
            
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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # 🔥 IMPORTANT
def enqurie(request):
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
            try:
               formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
               formatted_time = datetime.strptime(time, "%H:%M").strftime("%I:%M %p")
            except Exception as e:
               messages.error(request, "Invalid date or time format.")
               print("DATE/TIME ERROR:", e)
               return redirect('homepage')
                
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

🗓️ Date: {formatted_date}
⏰ Time: {formatted_time}

💰 Fare: ₹ ₹{fare}
🧾 Drivercharge: ₹ {driverCharge}
🔖 Total:₹ {total}
📏 Distance: {distance} Km
🚗 Car Type: {carType}


Thank you for booking with us!
"""

            # ✅ Send Telegram
            telegram_bot_token = "8749101532:AAGyz-1mLJNA5vObrtdw9Ytm2H8ZR8cP7OA"
            telegram_chat_id = "1941956017"
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
            try:
               formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
               formatted_time = datetime.strptime(time, "%H:%M").strftime("%I:%M %p")
            except Exception as e:
               messages.error(request, "Invalid date or time format.")
               print("DATE/TIME ERROR:", e)
               return redirect('homepage')    
            
            # ✅ EMAIL
            subject = "Booking Completed ✅"
            message = f"""
Your round booking is confirmed.

TRIP TYPE: ROUND TRIP
Pickup: {pickup} → {drop} → {pickup}

Name: {name}
Phone: +91 {phone}
Email: {email}

🗓️ Date: {formatted_date}
⏰ Time: {formatted_time}
📆 Days: {number_of_days}


Driver Bata (Per Day): ₹{driverCharge}
Total Amount: ₹{total}
Car Type: {carType}


Note: Excluding - Hills, Tollgate & Permit Charges Applicable if use only.

Thank you for booking with us! DROP TAXI BOOKING..!
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
                messages.success(request, "Round trip booking successful! Email sent.")
            except Exception as e:
                print("EMAIL FAILED:", e)

            # ✅ TELEGRAM
            telegram_message = f"""
📩 NEW ROUND TRIP BOOKING

📍 {pickup} → {drop} → {pickup}

👤 Name: {name}
📱 Phone: {phone}
✉️ Email: {email}

🗓️ Date: {formatted_date}
⏰ Time: {formatted_time}
📆 Days: {number_of_days}

🚗 Car Type: {carType}
🧾 Driver Bata: ₹{driverCharge}
📏 Distance: {distance} KM
💰 Total Fare: ₹{total}
"""

            try:
                # ✅ Send Telegram
                telegram_bot_token = "8749101532:AAGyz-1mLJNA5vObrtdw9Ytm2H8ZR8cP7OA"
                telegram_chat_id = "1941956017"
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
    car_type = request.POST.get("carType", "").strip()
    distance = request.POST.get("distance", "").strip()
    total_fare = request.POST.get("totalFare", "").strip()

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
    # ✅ Format date & time
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
        formatted_time = datetime.strptime(time, "%H:%M").strftime("%I:%M %p")
    except Exception as e:
        messages.error(request, "Invalid date or time format.")
        print("DATE/TIME ERROR:", e)
        return redirect('round')    

    # ------------------ TELEGRAM MESSAGE ------------------
    message = f"""
🚗 NEW BOOKING Round Trip ENQUIRY

👤 Name: {name}
📞 Phone: {phone}

📍 Pickup: {pickup}
📍 Drop: {drop}

🗓️ Date: {formatted_date}
⏰ Time: {formatted_time}
🗓 Days: {number_of_days}

🚘 Car Type: {car_type}
📏 Distance: {distance} KM
💰 Total Fare: ₹{total_fare}
"""

    # ✅ Send Telegram
    telegram_bot_token = "8749101532:AAGyz-1mLJNA5vObrtdw9Ytm2H8ZR8cP7OA"
    telegram_chat_id = "1941956017"
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

def terms(request):
    return render(request, 'terms.html')



def chennai_madurai(request):
    return render(request, 'chennai_madurai.html')

def route_page(request, route_name):

    route_titles = {
        "chennai-to-trichy-one-way-taxi": "Chennai to Trichy One Way Taxi",
        "chennai-to-coimbatore-drop-taxi": "Chennai to Coimbatore Drop Taxi",
        "chennai-to-tirunelveli-drop-taxi": "Chennai to Tirunelveli Drop Taxi",
        "madurai-to-chennai-drop-taxi": "Madurai to Chennai Drop Taxi",
        "chennai-to-kanyakumari-drop-taxi": "Chennai to Kanyakumari Drop Taxi",
        "chennai-to-thanjavur-drop-taxi": "Chennai to Thanjavur Drop Taxi",
        "chennai-to-erode-drop-taxi": "Chennai to Erode Drop Taxi",
    }

    title = route_titles.get(route_name)

    if not title:
        return render(request, "404.html")

    return render(request, "route_template.html", {
        "title": title
    })
