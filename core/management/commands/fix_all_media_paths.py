from django.core.management.base import BaseCommand
from core.models import Service, HomeGallery, Blog, User
from cloudinary.uploader import upload
import os

BASE_PATH = "C:/Users/LENOVO/MLC1/media/"

FOLDERS = {
    "services": BASE_PATH + "services/",
    "profile_pics": BASE_PATH + "profile_pics/",
    "bar_ids": BASE_PATH + "bar_council_ids/",
    "gallery": BASE_PATH + "home_gallery/",
    "blogs": BASE_PATH + "blogs/",
}


def upload_if_exists(local_path, cloud_folder):
    if not os.path.exists(local_path):
        print("❌ Not found:", local_path)
        return None

    print("⬆ Uploading:", local_path)
    result = upload(local_path, folder=cloud_folder)
    return result.get("secure_url")


class Command(BaseCommand):
    help = "Fix all media paths and re-upload to Cloudinary"

    def handle(self, *args, **kwargs):
        print("=== START FIX ===")

        # SERVICES
        for s in Service.objects.all():
            if not s.image:
                continue
            filename = os.path.basename(s.image.name)
            p = os.path.join(FOLDERS['services'], filename)

            new_url = upload_if_exists(p, "mlc/services")
            if new_url:
                s.image = new_url
                s.save()

        # USERS
        for u in User.objects.all():

            if u.profile_pic:
                f = os.path.basename(u.profile_pic.name)
                p = os.path.join(FOLDERS['profile_pics'], f)
                new = upload_if_exists(p, "mlc/profile_pics")
                if new:
                    u.profile_pic = new
                    u.save()

            if u.bar_council_id:
                f = os.path.basename(u.bar_council_id.name)
                p = os.path.join(FOLDERS['bar_ids'], f)
                new = upload_if_exists(p, "mlc/bar_ids")
                if new:
                    u.bar_council_id = new
                    u.save()

        # GALLERY
        for g in HomeGallery.objects.all():
            if g.image:
                f = os.path.basename(g.image.name)
                p = os.path.join(FOLDERS['gallery'], f)
                new = upload_if_exists(p, "mlc/gallery")
                if new:
                    g.image = new
                    g.save()

        # BLOGS
        for b in Blog.objects.all():
            if b.image:
                f = os.path.basename(b.image.name)
                p = os.path.join(FOLDERS['blogs'], f)
                new = upload_if_exists(p, "mlc/blogs")
                if new:
                    b.image = new
                    b.save()

            if b.og_image:
                f = os.path.basename(b.og_image.name)
                p = os.path.join(FOLDERS['blogs'], f)
                new = upload_if_exists(p, "mlc/blogs/og")
                if new:
                    b.og_image = new
                    b.save()

        print("=== FIX COMPLETE ===")
