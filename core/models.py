from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('advocate', 'Advocate'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, blank=True, default='client')
    mobile_number = models.CharField(max_length=15, blank=True, default='')

    address = models.TextField(blank=True, default='')
    state = models.CharField(max_length=50, blank=True, default='')
    city = models.CharField(max_length=50, blank=True, default='')

    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    enrollment_number = models.CharField(max_length=50, blank=True, null=True)
    bar_council_id = models.FileField(upload_to='bar_council_ids/', blank=True, null=True)
    experience = models.IntegerField(default=0, blank=True)
    expertise = models.CharField(max_length=200, blank=True, default='')
    document = models.FileField(upload_to='advocate_docs/', blank=True, null=True)

    # ✅ Manual verification field (NEW)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.get_username()



class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class AdvocateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Assigned', 'Assigned'),
    ('Completed', 'Completed'),
)

class Booking(models.Model):
    client = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    assigned_advocate = models.ForeignKey(
        'core.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bookings'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    booking_time = models.DateTimeField(auto_now_add=True)
    replacement_count = models.IntegerField(default=3)
    case_details = models.TextField(blank=True, default='')
    is_urgent = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking: {self.client.username} - {self.service.title}"

class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, default='')
    mobile = models.CharField(max_length=15, blank=True, default='')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ContactForm: {self.name}"



class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)

    canonical_url = models.URLField(blank=True, null=True)


    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    og_image = models.ImageField(upload_to='blogs/og/', blank=True, null=True)

    def __str__(self):
        return self.title


class LegalQuery(models.Model):
    client = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='legal_queries')
    question = models.TextField()
    answer = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query: {self.client.username}"

class HomeGallery(models.Model):
    image = models.ImageField(upload_to='home_gallery/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Gallery Image {self.id}"


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default="My Legal Consultants")

    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    whatsapp = models.CharField(max_length=50, blank=True, null=True)


    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return "Site Settings (Footer)"

    class Meta:
        verbose_name = "Footer Settings"
        verbose_name_plural = "Footer Settings"
