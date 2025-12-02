from .models import SiteSettings

def user_flags(request):
    user = request.user

    if user.is_authenticated:
        return {
            'is_client': user.user_type == 'client',
            'is_advocate': user.user_type == 'advocate',

            # Global default support info
            'support_email': 'support@mylegalconsultants.in',
            'support_contact': '+91-9876543210',
        }

    return {
        'support_email': 'support@mylegalconsultants.in',
        'support_contact': '+91-9876543210',
    }


# ----------------------------------------
# NEW: FOOTER SETTINGS (Admin Controlled)
# ----------------------------------------
def footer_settings(request):
    settings = SiteSettings.objects.first()
    return {
        "footer_settings": settings
    }
