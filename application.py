import os
import sys

project_home = '/home/YOUR_CPANEL_USERNAME/mlc_project'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MLC1.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
