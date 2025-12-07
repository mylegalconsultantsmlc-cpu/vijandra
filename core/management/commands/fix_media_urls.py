from django.core.management.base import BaseCommand
from core.models import (
    Service,
    ClientProfile,
    AdvocateProfile,
    Blog,
    HomeGallery,
    User
)

class Command(BaseCommand):
    help = "Fix media URLs by converting local filenames to Cloudinary URLs"

    def handle(self, *args, **kwargs):

        cloud_prefix = "https://res.cloudinary.com/dc0ucrbt8/image/upload/mlc/"

        def fix_field(instance, field_name):
            file_field = getattr(instance, field_name, None)
            if not file_field:
                return
            
            url = str(file_field)

            # skip if already full URL
            if url.startswith("http"):
                return

            # get filename
            filename = url.split("/")[-1]
            if not filename:
                return

            new_url = cloud_prefix + filename

            setattr(instance, field_name, new_url)
            instance.save(update_fields=[field_name])
            self.stdout.write(self.style.SUCCESS(f"UPDATED {instance} → {new_url}"))

        # SERVICES
        for s in Service.objects.all():
            fix_field(s, "image")

        # CLIENT PROFILES
        for c in ClientProfile.objects.all():
            fix_field(c.user, "profile_pic")

        # ADVOCATE PROFILES
        for a in AdvocateProfile.objects.all():
            fix_field(a.user, "profile_pic")
            fix_field(a.user, "bar_council_id")
            fix_field(a.user, "document")

        # BLOG MAIN IMAGE
        for b in Blog.objects.all():
            fix_field(b, "image")
            fix_field(b, "og_image")

        # HOME GALLERY
        for g in HomeGallery.objects.all():
            fix_field(g, "image")

        self.stdout.write(self.style.SUCCESS("=== ALL MEDIA URLS FIXED SUCCESSFULLY ==="))
