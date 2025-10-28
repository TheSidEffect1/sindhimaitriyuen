from django.urls import path
from . import views

urlpatterns = [
    # ------------------------
    # Main Pages
    # ------------------------
    path('', views.index, name='index'),                     # Home page
    path('services/', views.services, name='services'),
    path('sindhisoc/', views.sindhisoc, name='sindhisoc'),
    path('contact/', views.contact, name='contact'),
    path('team/', views.team, name='team'),

    # ------------------------
    # Registration Pages (Multi-Step)
    # ------------------------
    path('page1/', views.page1, name='page1'),               # Step 1 page
    path('page2/', views.page2, name='page2'),               # Step 2 page
    path('page3/', views.page3, name='page3'),               # Step 3 page

    # ------------------------
    # Authentication
    # ------------------------
    path('login/', views.login_page, name='login'),
    path('login_check/', views.login_check, name='login_check'),
    path('logout/', views.logout_view, name='logout'),       # ✅ new logout route

    # ------------------------
    # Logged-in Pages
    # ------------------------
    path('logged/', views.afterlogin, name='logged'),
    path('profile/', views.profile, name='profile'),

    # ------------------------
    # AJAX Save Endpoints
    # ------------------------
    path('save_registration/', views.save_registration, name='save_registration'),
    path('save_step2/', views.save_step2, name='save_step2'),
    path('save_step3/', views.save_step3, name='save_step3'),
    path('update_profile/', views.update_profile, name='update_profile'),
]
