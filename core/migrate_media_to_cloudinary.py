import os
from django.conf import settings
from django.core.files import File
from cloudinary.uploader import upload
from core.models import (
    User, Service, Blog, HomeGallery
)

# Helper: Upload and return Cloudinary URL
def upload_to_cloudinary(local_path):
    if not os.path.exists(local_path):
        print(f"File not found: {local_path}")
        return None

    try:
        result = upload(local_path)
        return result.get("secure_url")
    except Exception as e:
        print(f"Error uploading {local_path}: {e}")
        return None


# MAIN MIGRATION FUNCTION
def migrate_all():
    print("========== STARTING MEDIA MIGRATION ==========")

    media_root = settings.MEDIA_ROOT

    # -----------------------------
    # 1. USER PROFILE PICS & DOCS
    # -----------------------------
    for user in User.objects.all():
        if user.profile_pic:
            old = os.path.join(media_root, user.profile_pic.name)
            url = upload_to_cloudinary(old)
            if url:
                user.profile_pic = url
                user.save()
                print("Uploaded profile:", url)

        if user.bar_council_id:
            old = os.path.join(media_root, user.bar_council_id.name)
            url = upload_to_cloudinary(old)
            if url:
                user.bar_council_id = url
                user.save()
                print("Uploaded bar council:", url)

        if user.document:
            old = os.path.join(media_root, user.document.name)
            url = upload_to_cloudinary(old)
            if url:
                user.document = url
                user.save()
                print("Uploaded advocate document:", url)

    # -----------------------------
    # 2. SERVICES IMAGES
    # -----------------------------
    for s in Service.objects.all():
        if s.image:
            old = os.path.join(media_root, s.image.name)
            url = upload_to_cloudinary(old)
            if url:
                s.image = url
                s.save()
                print("Uploaded Service:", s.title)

    # -----------------------------
    # 3. BLOG IMAGES
    # -----------------------------
    for b in Blog.objects.all():
        if b.image:
            old = os.path.join(media_root, b.image.name)
            url = upload_to_cloudinary(old)
            if url:
                b.image = url
                b.save()
                print("Uploaded Blog:", b.title)

        if b.og_image:
            old = os.path.join(media_root, b.og_image.name)
            url = upload_to_cloudinary(old)
            if url:
                b.og_image = url
                b.save()
                print("Uploaded OG image:", b.title)

    # -----------------------------
    # 4. HOME GALLERY
    # -----------------------------
    for g in HomeGallery.objects.all():
        if g.image:
            old = os.path.join(media_root, g.image.name)
            url = upload_to_cloudinary(old)
            if url:
                g.image = url
                g.save()
                print("Uploaded Gallery Image:", g.id)

    print("========== MIGRATION COMPLETED ==========")
