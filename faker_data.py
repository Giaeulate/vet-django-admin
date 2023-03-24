import random
from django.db import models
from faker import Faker
from core.models import (
    SubscriptionPlan,
    Service,
    AffiliatedVeterinary,
    VeterinaryService,
    VeterinaryPromotion,
    Owner,
)
from django.utils import timezone

from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from django.core.files import File
from django.conf import settings
from PIL import Image
from io import BytesIO

fake = Faker()
total = 1000

def generate_image():
    img = Image.new('RGB', (300, 300), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    buffer = BytesIO()
    img.save(buffer, 'jpeg')
    buffer.seek(0)
    return buffer

# Generar objetos aleatorios para SubscriptionPlan
for i in range(total):
    plan = SubscriptionPlan(
        name=fake.word(),
        description=fake.text(max_nb_chars=255),
        price=fake.pydecimal(left_digits=3, right_digits=2, positive=True)
    )
    plan.save()
subscription_plans = SubscriptionPlan.objects.all()

# Generar objetos aleatorios para Service
for i in range(total):
    service = Service(
        name=fake.word(),
        description=fake.text(max_nb_chars=255),
        price=fake.pydecimal(left_digits=3, right_digits=2, positive=True)
    )
    service.save()
services = Service.objects.all()


# Generar objetos aleatorios para Owner
owners = []
for i in range(total):
    owner = Owner(
        document_id=fake.uuid4(),
        name=fake.first_name(),
        lastname=fake.last_name(),
        phone=fake.phone_number(),
        email=fake.email(),
        birthdate=fake.date_time_between(start_date='-30y', end_date='-18y', tzinfo=timezone.utc),
    )
    owner.save()

     # Creamos una imagen aleatoria
    image = Image.new('RGB', (100, 100), color=(255, 0, 0))
    image_io = BytesIO()
    image.save(image_io, 'JPEG')
    image_io.seek(0)

    veterinary = AffiliatedVeterinary(
        name=fake.company(),
        # logo=file,
        logo=InMemoryUploadedFile(
            generate_image(),
            'ImageField',
            f'{random.getrandbits(32)}.jpg',
            'image/jpeg',
            None,
            None
        ),
        mission=fake.text(max_nb_chars=255),
        vision=fake.text(max_nb_chars=255),
        owner=owner,
        subscription_plan=random.choice(subscription_plans),
        overdue_payment=fake.boolean(),
        web_page=fake.url(),
        facebook=fake.url(),
        twitter=fake.url(),
        instagram=fake.url(),
        tiktok=fake.url()
    )
    veterinary.save()

    # filename = f'{fake.uuid4()}.jpg'
    # filepath = os.path.join(settings.MEDIA_ROOT, 'core', 'AffiliatedVeterinary', filename)
    # with open(filepath, 'wb') as f:
    #     f.write(image_io.read())
    #     f.close()
    # with open(filepath, 'rb') as f:
    #     veterinary.logo.save(filename, File(f), save=True)
    #     veterinary.save()
owners = Owner.objects.all()
affiliatedVeterinaries = AffiliatedVeterinary.objects.all()


for i in range(total):
    data = VeterinaryService(
        veterinary=random.choice(affiliatedVeterinaries),
        service=random.choice(services)
    )
    data.save()

for i in range(total):
    promotion = VeterinaryPromotion(
        veterinary=random.choice(affiliatedVeterinaries),
        title=fake.sentence(),
        description=fake.text(),
        start_date=fake.date_time_between(
            start_date='-1d', end_date='+7d', tzinfo=timezone.utc),
        end_date=fake.date_time_between(
            start_date='+1d', end_date='+14d', tzinfo=timezone.utc),
    )
    promotion.save()

