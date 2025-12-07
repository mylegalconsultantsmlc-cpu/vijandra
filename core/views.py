from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .utils import generate_unique_username
from .models import Booking, LegalQuery
from .models import HomeGallery

from .models import (
    User, ClientProfile, AdvocateProfile,
    ServiceCategory, Service,
    Booking, ContactFormSubmission,
    FAQ, Blog, LegalQuery
)
from django.utils import timezone

def get_post_value(request, *names, default=None):
    """
    Return first non-empty POST value for any of the provided names.
    Helpful when form field name had case differences (e.g. "Expertise" vs "expertise").
    """
    for n in names:
        v = request.POST.get(n)
        if v is not None:
            return v
    return default

def get_file(request, *names, default=None):
    for n in names:
        f = request.FILES.get(n)
        if f is not None:
            return f
    return default


def home(request):
    featured_services = Service.objects.filter(featured=True)
    categories = ServiceCategory.objects.all()
    services = Service.objects.exclude(title="Urgent Consultation")
    blogs = Blog.objects.all().order_by('-created_at')[:3]

    # IMPORTANT: Remove limit or loop will never run
    gallery_images = HomeGallery.objects.all()

    context = {
        'featured_services': featured_services,
        'categories': categories,
        'services': services,
        'blogs': blogs,
        'gallery_images': gallery_images,
    }
    return render(request, 'core/home.html', context)



def all_services(request):
    query = request.GET.get('q')
    services = Service.objects.exclude(title="Urgent Consultation")
    if query:
        services = services.filter(title__icontains=query)
    categories = ServiceCategory.objects.all()
    context = {
        'services': services,
        'categories': categories,
        'search_query': query
    }
    return render(request, 'core/service_list.html', context)


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'core/blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'core/blog_detail.html', {'blog': blog})

from django.core.mail import send_mail
from django.conf import settings


def contact_us(request):
    faqs = FAQ.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message')
        terms = request.POST.get('terms')

        if not terms:
            messages.error(request, "Please accept Terms & Privacy Policy")
            return redirect('contact_us')


        ContactFormSubmission.objects.create(
            name=name, email=email, mobile=mobile, message=message
        )


        subject = f"New Contact Form Submission - {name}"
        
        message_body = f"""
A new contact enquiry has been received:

Name: {name}
Email: {email}
Mobile: {mobile}

Message:
{message}

Contact form submitted from My Legal Consultants website.
        """

        send_mail(
            subject,
            message_body,
            settings.EMAIL_HOST_USER,
            ["mylegalconsultants.mlc@gmail.com"],
            fail_silently=False,
        )

        messages.success(request, "Your message has been submitted successfully")
        return redirect('contact_us')

    return render(request, 'core/contact_us.html', {'faqs': faqs})


@login_required
def ask_query(request):

    if request.user.user_type != 'client':
        messages.error(request, "Only clients can submit queries.")
        resp = redirect('home')
        resp['X-Robots-Tag'] = 'noindex, nofollow'
        return resp

    if request.method == 'POST':
        question = request.POST.get('question', '').strip()

        if question:
            LegalQuery.objects.create(
                client=request.user,
                question=question
            )
            messages.success(request, "Your query has been submitted.")
        else:
            messages.error(request, "Please enter a question.")

        resp = redirect('client_dashboard')
        resp['X-Robots-Tag'] = 'noindex, nofollow'
        return resp

    resp = redirect('client_dashboard')
    resp['X-Robots-Tag'] = 'noindex, nofollow'
    return resp



def register_client(request):
    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        terms = request.POST.get('terms')


        if terms != 'on':
            messages.error(request, "Please accept Terms & Conditions.")
            resp = redirect('register_client')
            resp['X-Robots-Tag'] = 'noindex, nofollow'
            return resp


        if not (email or mobile):
            messages.error(request, "Email or Mobile number is required.")
            resp = redirect('register_client')
            resp['X-Robots-Tag'] = 'noindex, nofollow'
            return resp

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            resp = redirect('register_client')
            resp['X-Robots-Tag'] = 'noindex, nofollow'
            return resp


        if email and User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email already registered.")
            resp = redirect('register_client')
            resp['X-Robots-Tag'] = 'noindex, nofollow'
            return resp

        if mobile and User.objects.filter(mobile_number=mobile).exists():
            messages.error(request, "Mobile number already registered.")
            resp = redirect('register_client')
            resp['X-Robots-Tag'] = 'noindex, nofollow'
            return resp

        username = email.lower() if email else mobile

        if User.objects.filter(username=username).exists():
            messages.error(request, "An account with this identifier already exists.")
            resp = redirect('register_client')
            resp['X-Robots-Tag'] = 'noindex, nofollow'
            return resp


        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name,
            mobile_number=mobile,
            address=address,
            state=state,
            city=city,
            user_type='client',
        )

        ClientProfile.objects.create(user=user)

        messages.success(request, "Client registration successful.")
        resp = redirect('login')
        resp['X-Robots-Tag'] = 'noindex, nofollow'
        return resp


    response = render(request, 'core/register_client.html')
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response



def register_advocate(request):
    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        state = request.POST.get("state")
        city = request.POST.get("city")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        enrollment_number = request.POST.get("enrollment_number")
        expertise = request.POST.get("expertise")
        experience = request.POST.get("experience")
        bar_id = request.FILES.get("bar_council_id")

        terms = request.POST.get("terms")


        if terms != "on":
            messages.error(request, "Please accept Terms & Conditions.")
            resp = redirect("register_advocate")
            resp['X-Robots-Tag'] = 'noindex, nofollow'
            return resp


        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            resp = redirect("register_advocate")
            resp['X-Robots-Tag'] = 'noindex, nofollow'
            return resp


        if not email:
            messages.error(request, "Email is required for advocate registration.")
            resp = redirect("register_advocate")
            resp['X-Robots-Tag'] = 'noindex, nofollow'
            return resp

        username = email.lower().strip()


        if User.objects.filter(username=username).exists():
            messages.error(request, "Email already registered.")
            resp = redirect("register_advocate")
            resp['X-Robots-Tag'] = 'noindex, nofollow'
            return resp


        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name,
            mobile_number=mobile,
            address=address,
            state=state,
            city=city,
            user_type="advocate",
        )


        user.enrollment_number = enrollment_number
        user.expertise = expertise
        user.experience = experience

        if bar_id:
            user.bar_council_id = bar_id

        user.save()

        AdvocateProfile.objects.create(user=user)

        messages.success(request, "Advocate registration successful.")
        resp = redirect("login")
        resp['X-Robots-Tag'] = 'noindex, nofollow'
        return resp


    response = render(request, "core/register_advocate.html")
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response



def user_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        password = request.POST.get('password')
        user = None


        user = authenticate(request, username=identifier, password=password)

        if not user:

            if "@" in identifier:
                u = User.objects.filter(email__iexact=identifier).first()
                if u:
                    user = authenticate(request, username=u.username, password=password)
            else:

                u = User.objects.filter(mobile_number=identifier).first()
                if u:
                    user = authenticate(request, username=u.username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful")

            if user.user_type == 'client':
                return redirect('client_dashboard')
            return redirect('advocate_dashboard')
        
        else:
            messages.error(request, "Invalid credentials")


    response = render(request, 'core/login.html')
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response




@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':

        user.first_name = request.POST.get('first_name', user.first_name)
        user.email = request.POST.get('email', user.email)
        user.mobile_number = request.POST.get('mobile_number', user.mobile_number)


        if user.user_type == 'client':
            user.address = request.POST.get('address', user.address)
            user.city = request.POST.get('city', user.city)
            user.state = request.POST.get('state', user.state)

        if user.user_type == 'advocate':
            user.experience = request.POST.get('experience', user.experience)
            user.expertise = request.POST.get('expertise', user.expertise)
            user.enrollment_number = request.POST.get('enrollment_number', user.enrollment_number)

        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']

        user.save()
        messages.success(request, "Profile updated successfully!")

        return redirect('edit_profile')


    if user.user_type == 'client':
        response = render(request, 'core/edit_client_profile.html', {'user': user})
    else:
        response = render(request, 'core/edit_advocate_profile.html', {'user': user})

    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response

def user_logout(request):
    logout(request)
    response = redirect('home')
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response


@login_required
def book_consultation(request, service_id):

    if request.user.user_type != 'client':
        messages.error(request, "Only clients can book consultations.")
        resp = redirect('home')
        resp['X-Robots-Tag'] = 'noindex, nofollow'
        return resp

    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        case_details = request.POST.get('case_details', '').strip()


        Booking.objects.create(
            client=request.user,
            service=service,
            status='Pending',
            replacement_count=3, 
            case_details=case_details
        )

        messages.success(request, "Booking confirmed! You will get a call within 24 hours.")
        resp = redirect('client_dashboard')
        resp['X-Robots-Tag'] = 'noindex, nofollow'
        return resp

    response = render(request, 'core/book_consultation.html', {'service': service})
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response




@login_required
def client_dashboard(request):
    user = request.user

    if user.user_type != 'client':
        return redirect('home')


    bookings = (
        Booking.objects
        .filter(client=user)
        .select_related('service', 'assigned_advocate')
        .order_by('-booking_time')
    )

    assigned_bookings_meta = []
    for b in bookings:
        assigned_bookings_meta.append({
            "booking": b,
            "service_title": b.service.title,
            "advocate_name": b.assigned_advocate.first_name if b.assigned_advocate else None,
            "status": b.status,
            "booking_time": b.booking_time,
            "replacement_count": b.replacement_count,
            "urgent": b.is_urgent,
            "case_details": b.case_details,
        })

    client_queries = LegalQuery.objects.filter(client=user).order_by('-created_at')


    support = {
        "phone": "+91-8826669309",
        "email": "mylegalconsultants.mlc@gmail.com"
    }

    context = {
        "user": user,
        "assigned_bookings_meta": assigned_bookings_meta,
        "client_queries": client_queries,
        "support": support,
    }


    response = render(request, "core/dashboard_client.html", context)
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response



@login_required
def advocate_dashboard(request):
    user = request.user

    if user.user_type != 'advocate':
        return redirect('home')

    assigned_bookings = Booking.objects.filter(
        assigned_advocate=user
    ).select_related("client", "service").order_by('-booking_time')

    context = {
        "user": user,
        "assigned_bookings": assigned_bookings,
        "support_email": "mylegalconsultants.mlc@gmail.com",
        "support_contact": "+91-8826669309",
    }

    response = render(request, 'core/dashboard_advocate.html', context)
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response


@login_required
def book_urgent_consultation(request):


    if request.user.user_type != 'client':
        messages.error(request, "Only clients can book consultations.")
        resp = redirect('home')
        resp['X-Robots-Tag'] = 'noindex, nofollow'
        return resp

    if request.method == 'POST':
        case_details = request.POST.get('case_details', '').strip()


        urgent_category, _ = ServiceCategory.objects.get_or_create(
            name="Urgent Services",
            defaults={'description': 'Category for urgent consultation services'}
        )


        urgent_service, _ = Service.objects.get_or_create(
            title="Urgent Consultation",
            defaults={
                'category': urgent_category,
                'description': 'Urgent legal consultation',
                'featured': False
            }
        )


        Booking.objects.create(
            client=request.user,
            service=urgent_service,
            status='Pending',
            replacement_count=0,
            case_details=case_details,
            is_urgent=True
        )

        messages.success(request, "Your urgent request is submitted! Advocate will contact you shortly.")
        resp = redirect('client_dashboard')
        resp['X-Robots-Tag'] = 'noindex, nofollow'
        return resp


    response = render(request, 'core/book_urgent_consultation.html')
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response

def about_us(request):
    return render(request, "core/about_us.html")

def terms_and_conditions(request):
    return render(request, "core/terms_and_conditions.html")

def privacy_policy(request):
    return render(request, "core/privacy_policy.html")

