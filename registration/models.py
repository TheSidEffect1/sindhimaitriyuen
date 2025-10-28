from django.db import models
from django.contrib.auth.models import User

class Registration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="registration", null=True, blank=True)
    # Step 1: Basic Info
    your_name = models.CharField(max_length=255)
    your_mob = models.CharField(max_length=15)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    father_mob = models.CharField(max_length=15, blank=True, null=True)
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    mother_mob = models.CharField(max_length=15, blank=True, null=True)
    aadhar = models.CharField(max_length=14)
    blood_group = models.CharField(max_length=5)
    gender = models.CharField(max_length=1)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    partner_choice = models.TextField(blank=True, null=True)
    passport_photo = models.TextField(blank=True, null=True)
    full_photo = models.TextField(blank=True, null=True)

    # Step 2: Personal / Professional Info
    house = models.CharField(max_length=50, blank=True, null=True)
    sqft = models.IntegerField(blank=True, null=True)
    floors = models.IntegerField(blank=True, null=True)
    vehicles2 = models.IntegerField(blank=True, null=True)
    vehicles4 = models.IntegerField(blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    jobType = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    birthDate = models.DateField(blank=True, null=True)
    birthTime = models.TimeField(blank=True, null=True)
    birthPlace = models.CharField(max_length=255, blank=True, null=True)
    skinColour = models.CharField(max_length=50, blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    diseases = models.TextField(blank=True, null=True)
    personalIncome = models.FloatField(blank=True, null=True)
    jointIncome = models.FloatField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    profession = models.CharField(max_length=255, blank=True, null=True)
    profAddress = models.TextField(blank=True, null=True)

    # Step 3: Family Info
    address = models.TextField(blank=True, null=True)
    members = models.PositiveIntegerField(default=0)
    grandfather = models.BooleanField(default=False)
    grandmother = models.BooleanField(default=False)
    father = models.BooleanField(default=False)
    mother = models.BooleanField(default=False)
    brother = models.PositiveIntegerField(default=0)
    sister = models.PositiveIntegerField(default=0)
    marriedb = models.BooleanField(null=True, blank=True)  # brother married
    marrieds = models.BooleanField(null=True, blank=True)  # sister married
    sindh = models.CharField(max_length=50, blank=True, null=True)
    nukha = models.CharField(max_length=100, blank=True, null=True)
    aakay = models.CharField(max_length=100, blank=True, null=True)
    FatherBusiness = models.CharField(max_length=200, blank=True, null=True)
    FatherPos = models.CharField(max_length=200, blank=True, null=True)
    FatherBusinessAd = models.CharField(max_length=200, blank=True, null=True)
    BrotherBusiness = models.CharField(max_length=200, blank=True, null=True)
    BrotherPos = models.CharField(max_length=200, blank=True, null=True)
    BrotherBusinessAd = models.CharField(max_length=200, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    otherInfo = models.TextField(blank=True, null=True)

    # Preferences
    widow = models.CharField(max_length=10, blank=True, null=True)
    widowAccept = models.CharField(max_length=10, blank=True, null=True)
    nonVeg = models.CharField(max_length=10, blank=True, null=True)
    nonVegAccept = models.CharField(max_length=10, blank=True, null=True)
    drinks = models.CharField(max_length=10, blank=True, null=True)
    drinksAccept = models.CharField(max_length=10, blank=True, null=True)
    smokes = models.CharField(max_length=10, blank=True, null=True)
    smokesAccept = models.CharField(max_length=10, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.your_name or f"Registration #{self.id}"
