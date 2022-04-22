import random
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from faker_vehicle import VehicleProvider

from fleetmanagement.models import Auto, STATUSES


class Command(BaseCommand):
    help = 'Creates some fake entries'

    def handle(self, *args, **options):
        fake = Faker()
        fake.add_provider(VehicleProvider)
        a = Auto(hersteller="BMW", modell="M1", baujahr=1978, status="FAHRBEREIT")
        a.nummernschild = "M-JB-007"
        a.save()
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
        self.stdout.write(self.style.SUCCESS("Created fake vehicles"))
