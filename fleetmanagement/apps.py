from django.apps import AppConfig
from faker import Faker
from faker_vehicle import VehicleProvider

import sys
import random

class FleetmanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fleetmanagement'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        from fleetmanagement.models import Auto, STATUSES
        if (len(Auto.objects.all()) != 0):
            return

        fake = Faker()
        fake.add_provider(VehicleProvider)
        for i in range(542):
            try:
                car = fake.vehicle_object()
                status = "BESTELLT" if car["Year"] == 2022 else random.choice(STATUSES)[0]
                auto = Auto(hersteller=car["Make"], modell=car["Model"], baujahr=car["Year"], status=status)
                if auto.status != "BESTELLT":
                    auto.nummernschild = f"ME-IQ-{i}"
                auto.save()
            except Exception as e:
                print(e)
                print("Failed to create fake vehicle. Skipping.")
