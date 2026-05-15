"""Pytest configuration for Todo API tests."""

import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_api.settings')
django.setup()

# Pytest fixtures can be added here
