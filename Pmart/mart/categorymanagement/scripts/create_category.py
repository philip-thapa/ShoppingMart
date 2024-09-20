import sys
import os

from categorymanagement.models import ProductCategory

sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mart.settings')

import django
django.setup()


def create_category():
    ProductCategory.objects.create(
        name='Electronics',
        created_by='script'
    )


if __name__ == "__main__":
    create_category()
