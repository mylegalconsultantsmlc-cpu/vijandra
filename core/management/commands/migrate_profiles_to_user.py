# core/management/commands/migrate_profiles_to_user.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

# Import models dynamically to avoid circular issues
from core.models import User
try:
    from core.models import ClientProfile, AdvocateProfile
except Exception:
    ClientProfile = None
    AdvocateProfile = None

class Command(BaseCommand):
    help = "Copy data from ClientProfile and AdvocateProfile into User fields"

    def handle(self, *args, **options):
        self.stdout.write("Starting profile → user migration...")

        if ClientProfile is None and AdvocateProfile is None:
            self.stdout.write("No profile models found. Nothing to migrate.")
            return

        with transaction.atomic():
            # Clients
            if ClientProfile is not None:
                for cp in ClientProfile.objects.select_related('user').all():
                    user = cp.user
                    # Copy only when target field is empty to avoid overwriting
                    if cp.profile_pic and not user.profile_pic:
                        user.profile_pic = cp.profile_pic
                    if cp.address and (not user.address or user.address == ""):
                        user.address = cp.address
                    if cp.city and (not user.city or user.city == ""):
                        user.city = cp.city
                    if cp.state and (not user.state or user.state == ""):
                        user.state = cp.state
                    user.save()
                self.stdout.write("ClientProfile data copied into User.")

            # Advocates
            if AdvocateProfile is not None:
                for ap in AdvocateProfile.objects.select_related('user').all():
                    user = ap.user
                    if ap.profile_pic and not user.profile_pic:
                        user.profile_pic = ap.profile_pic
                    if ap.enrollment_number and not user.enrollment_number:
                        user.enrollment_number = ap.enrollment_number
                    # bar council id and document - copy if user has none
                    if ap.bar_council_id and not user.bar_council_id:
                        user.bar_council_id = ap.bar_council_id
                    if ap.document and not user.document:
                        user.document = ap.document
                    if ap.expertise and not user.expertise:
                        user.expertise = ap.expertise
                    if ap.experience and (not user.experience or user.experience == 0):
                        try:
                            user.experience = int(ap.experience)
                        except Exception:
                            pass
                    user.save()
                self.stdout.write("AdvocateProfile data copied into User.")

        self.stdout.write(self.style.SUCCESS("Profile → User migration finished."))
