from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import User, Service, Blog, HomeGallery
import os

class Command(BaseCommand):
    help = "Fix all media file paths so Django can find actual files"

    def handle(self, *args, **kwargs):
        MEDIA_ROOT = settings.MEDIA_ROOT

        self.stdout.write(self.style.WARNING("=== FIXING ALL MEDIA PATHS ==="))

        # Create mapping of all real media files
        all_files = {}

        for root, dirs, files in os.walk(MEDIA_ROOT):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, MEDIA_ROOT).replace("\\", "/")
                all_files[f.lower()] = rel_path

        # Helper to fix single file field
        def fix_field(instance, field_name):
            file_field = getattr(instance, field_name)
            if not file_field:
                return

            old_name = file_field.name.split("/")[-1].lower()

            if old_name in all_files:
                correct = all_files[old_name]
                file_field.name = correct
                instance.save()
                self.stdout.write(self.style.SUCCESS(f"FIXED: {instance} → {correct}"))
            else:
                self.stdout.write(self.style.ERROR(f"NOT FOUND → {old_name} (DB)"))

        # Fix Users
        for u in User.objects.all():
            fix_field(u, "profile_pic")
            fix_field(u, "bar_council_id")
            fix_field(u, "document")

        # Fix Services
        for s in Service.objects.all():
            fix_field(s, "image")

        # Fix Blogs
        for b in Blog.objects.all():
            fix_field(b, "image")
            fix_field(b, "og_image")

        # Fix Gallery
        for g in HomeGallery.objects.all():
            fix_field(g, "image")

        self.stdout.write(self.style.SUCCESS("=== ALL PATHS FIXED SUCCESSFULLY ==="))
