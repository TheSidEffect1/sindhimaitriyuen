from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Registration
import random, requests
from django.conf import settings
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.http import require_POST
import json


# -------------------------
# Render Pages
# -------------------------
def index(request):
    return render(request, 'index.html')

def page1(request):
    return render(request, 'registration/page1.html')

def page2(request):
    return render(request, 'registration/page2.html')

def page3(request):
    return render(request, 'registration/page3.html')

def services(request):
    return render(request, 'services.html')

def sindhisoc(request):
    return render(request, 'sindhisoc.html')

def team(request):
    return render(request, 'team.html')

def contact(request):
    return render(request, 'contact.html')

def login_page(request):
    return render(request, 'login/login.html')

def afterlogin(request):
    return render(request, 'login/logged.html')

def profile(request):
    return render(request, 'login/profile.html')


# -------------------------
# OTP Sending
# -------------------------


FAST2SMS_API_KEY    = settings.FAST2SMS_API_KEY
DLT_TEMPLATE_ID     = settings.FAST2SMS_DLT_TEMPLATE_ID  # e.g. "1207........"
SENDER_ID           = settings.FAST2SMS_SENDER_ID        # "SMBSMJ"
OTP_TTL_SECONDS     = getattr(settings, "OTP_TTL_SECONDS", 300)
OTP_RESEND_COOLDOWN = getattr(settings, "OTP_RESEND_COOLDOWN", 45)

def _digits_only(s): return "".join(ch for ch in (s or "") if ch.isdigit())

@require_POST
def send_otp(request):
    data = json.loads(request.body.decode("utf-8"))
    mobile = _digits_only(data.get("mobile"))

    if len(mobile) != 10:
        return JsonResponse({"success": False, "error": "Invalid mobile number"})

    if cache.get(f"otp_cooldown_{mobile}"):
        return JsonResponse({"success": False, "error": "Please wait before requesting a new OTP."})

    otp = f"{random.randint(100000, 999999)}"
    cache.set(f"otp_{mobile}", otp, OTP_TTL_SECONDS)
    cache.set(f"otp_cooldown_{mobile}", True, OTP_RESEND_COOLDOWN)

    payload = {
        "route": "dlt",
        "sender_id": SENDER_ID,
        "message": (
            "Dear User,\n"
            "Your OTP to register on SindhiMaitriyen.com is {#var#}. "
            "Valid for 5 minutes. Please do not share this OTP.\n\n"
            "Regards,\n"
            "Israni International"
        ),
        "variables_values": otp,
        "flash": "0",
        "numbers": mobile,
        "dlt_template_id": DLT_TEMPLATE_ID,
    }
    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        r = requests.post("https://www.fast2sms.com/dev/bulkV2", json=payload, headers=headers, timeout=10)
        resp = r.json() if r.headers.get("content-type","").startswith("application/json") else {}
        if r.status_code != 200 or not resp.get("return", False):
            # optional: log r.text for debugging
            return JsonResponse({"success": False, "error": "SMS send failed. Try again."})
    except Exception:
        return JsonResponse({"success": False, "error": "SMS provider error. Try again."})

    return JsonResponse({"success": True})


# -------------------------
# OTP Verification
# -------------------------

@require_POST
def verify_otp(request):
    data = json.loads(request.body.decode("utf-8"))
    mobile = _digits_only(data.get("mobile"))
    otp = _digits_only(data.get("otp"))

    if len(mobile) != 10 or len(otp) != 6:
        return JsonResponse({"success": False, "error": "Invalid input"})

    saved = cache.get(f"otp_{mobile}")
    if not saved:
        return JsonResponse({"success": False, "error": "OTP expired"})

    if otp != saved:
        return JsonResponse({"success": False, "error": "Incorrect OTP"})

    cache.delete(f"otp_{mobile}")  # one-time use
    return JsonResponse({"success": True})


# -------------------------
# Step 1: Save Registration
# -------------------------
def save_registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            registration = Registration(
                your_name=data.get("yourName", ""),
                your_mob=data.get("yourMob", ""),
                father_name=data.get("fatherName", ""),
                father_mob=data.get("fatherMob", ""),
                mother_name=data.get("motherName", ""),
                mother_mob=data.get("motherMob", ""),
                city=data.get("city", ""),
                state=data.get("state", ""),
                email=data.get("email", ""),
                password=data.get("password", ""),
                aadhar=data.get("aadhar", ""),
                blood_group=data.get("bloodGroup", ""),
                partner_choice=data.get("partnerChoice", ""),
                gender=data.get("gender", ""),
                passport_photo=data.get("passportPhoto", ""),
                full_photo=data.get("fullPhoto", "")
            )
            registration.save()
            return JsonResponse({"success": True, "registration_id": registration.id})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})


# -------------------------
# Step 2: Save Personal Profile
# -------------------------
def save_step2(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reg_id = data.get("registration_id")
            if not reg_id:
                return JsonResponse({"success": False, "error": "Registration ID missing."})

            registration = get_object_or_404(Registration, id=reg_id)

            # Step 2 fields
            registration.house = data.get("house", "")
            registration.sqft = int(data.get("sqft") or 0)
            registration.floors = int(data.get("floors") or 0)
            registration.vehicles2 = int(data.get("vehicles2") or 0)
            registration.vehicles4 = int(data.get("vehicles4") or 0)
            registration.education = data.get("education", "")
            registration.subject = data.get("subject", "")
            registration.jobType = data.get("jobType", "")
            registration.age = int(data.get("age") or 0)
            registration.birthDate = data.get("birthDate")
            registration.birthTime = data.get("birthTime")
            registration.birthPlace = data.get("birthPlace", "")
            registration.skinColour = data.get("skinColour", "")
            registration.height = float(data.get("height") or 0)
            registration.weight = float(data.get("weight") or 0)
            registration.diseases = data.get("diseases", "")
            registration.personalIncome = float(data.get("personalIncome") or 0)
            registration.jointIncome = float(data.get("jointIncome") or 0)
            registration.company = data.get("company", "")
            registration.position = data.get("position", "")
            registration.profession = data.get("profession", "")
            registration.profAddress = data.get("profAddress", "")

            registration.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})


# -------------------------
# Step 3: Save Family Profile & Preferences
# -------------------------
def save_step3(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reg_id = data.get("registration_id")
            if not reg_id:
                return JsonResponse({"success": False, "error": "Registration ID missing."})

            registration = get_object_or_404(Registration, id=reg_id)

            # Step 3 fields
            registration.address = data.get("address")
            registration.members = int(data.get("members") or 0)
            registration.grandfather = bool(data.get("grandfather"))
            registration.grandmother = bool(data.get("grandmother"))
            registration.father = bool(data.get("father"))
            registration.mother = bool(data.get("mother"))
            registration.brother = int(data.get("brother") or 0)
            registration.marriedb = int(data.get("marriedb") or 0)
            registration.sister = int(data.get("sister") or 0)
            registration.marrieds = int(data.get("marrieds") or 0)
            registration.sindh = data.get("sindh", "")
            registration.nukha = data.get("nukha", "")
            registration.aakay = data.get("aakay", "")
            registration.FatherBusiness = data.get("FatherBusiness", "")
            registration.FatherPos = data.get("FatherPos", "")
            registration.FatherBusinessAd = data.get("FatherBusinessAd", "")
            registration.BrotherBusiness = data.get("BrotherBusiness", "")
            registration.BrotherPos = data.get("BrotherPos", "")
            registration.BrotherBusinessAd = data.get("BrotherBusinessAd", "")
            registration.interests = data.get("interests", "")
            registration.otherInfo = data.get("otherInfo", "")
            registration.widow = data.get("widow", "")
            registration.widowAccept = data.get("widowAccept", "")
            registration.nonVegAccept = data.get("nonVegAccept", "")
            registration.nonVeg = data.get("nonVeg", "")
            registration.drinksAccept = data.get("drinksAccept", "")
            registration.drinks = data.get("drinks", "")
            registration.smokesAccept = data.get("smokesAccept", "")
            registration.smokes = data.get("smokes", "")

            registration.save()
            return JsonResponse({"success": True})

        except Registration.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registration not found."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})


# -------------------------
# Login and Session Management
# -------------------------
@csrf_exempt
def login_check(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mob = data.get("mob")
        password = data.get("password")

        try:
            user = Registration.objects.get(your_mob=mob, password=password)
            # Save login session
            request.session['user_id'] = user.id
            request.session['user_name'] = user.your_name
            return JsonResponse({"success": True})
        except Registration.DoesNotExist:
            return JsonResponse({"success": False, "error": "Invalid number or password"})
    return JsonResponse({"success": False, "error": "Invalid request method"})


def afterlogin(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    # Start with all profiles except the logged-in user
    profiles_list = Registration.objects.exclude(id=user_id)

    # --- Filter parameters ---
    gender = request.GET.get('gender')
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    education = request.GET.get('education')

    # Apply filters
    if gender:
        profiles_list = profiles_list.filter(gender__iexact=gender)
    if min_age:
        profiles_list = profiles_list.filter(age__gte=min_age)
    if max_age:
        profiles_list = profiles_list.filter(age__lte=max_age)
    if education:
        profiles_list = profiles_list.filter(education__iexact=education)

    # --- Pagination ---
    paginator = Paginator(profiles_list.order_by('-created_at'), 4)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Pass filters back to template to retain selection
    context = {
        'page_obj': page_obj,
        'gender': gender,
        'min_age': min_age,
        'max_age': max_age,
        'education': education,
    }

    return render(request, 'login/logged.html', context)


def profile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return render(request, 'login/login.html', {"error": "Please login first."})

    user = Registration.objects.filter(id=user_id).first()

    if not user:
        return render(request, 'login/login.html', {"error": "User not found. Please login again."})

    return render(request, 'login/profile.html', {"profile": user})


@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({"success": False, "error": "Not logged in."})

            registration = Registration.objects.filter(id=user_id).first()
            if not registration:
                return JsonResponse({"success": False, "error": "Profile not found."})

            data = json.loads(request.body)

            registration.your_name = data.get("your_name", registration.your_name)
            registration.age = data.get("age", registration.age)
            registration.city = data.get("city", registration.city)
            registration.state = data.get("state", registration.state)
            registration.email = data.get("email", registration.email)
            registration.profession = data.get("profession", registration.profession)
            registration.company = data.get("company", registration.company)
            registration.partner_choice = data.get("partner_choice", registration.partner_choice)

            registration.save()
            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method."})


# -------------------------
# Logout
# -------------------------
def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')

