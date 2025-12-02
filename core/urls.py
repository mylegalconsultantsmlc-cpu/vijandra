from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, ServiceSitemap, BlogSitemap
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'blog': BlogSitemap,
}


urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Services
    path('services/', views.all_services, name='all_services'),

    # Blog / Legal Awareness
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),

    # Contact Us
    path('contact-us/', views.contact_us, name='contact_us'),

    # Ask Anything / Legal Queries
    path('ask-query/', views.ask_query, name='ask_query'),

    # Registration
    path('register/client/', views.register_client, name='register_client'),
    path('register/advocate/', views.register_advocate, name='register_advocate'),

    # Login / Logout
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Dashboards
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    path('dashboard/advocate/', views.advocate_dashboard, name='advocate_dashboard'),

    # Book Consultation
    path('book-consultation/<int:service_id>/', views.book_consultation, name='book_consultation'),

    # Password reset (using Django auth views)
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'),
         name='password_reset_complete'),
    # edit profile
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    
    path('book-urgent-consultation/', views.book_urgent_consultation, name='book_urgent_consultation'),
    
    path("about-us/", views.about_us, name="about_us"),
    path("terms-and-conditions/", views.terms_and_conditions, name="terms_and_conditions"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

]
