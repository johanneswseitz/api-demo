from django.apps import AppConfig
from faker import Faker
from faker_vehicle import VehicleProvider

import sys
import random

class FleetmanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fleetmanagement'
