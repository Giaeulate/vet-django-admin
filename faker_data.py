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
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

import python_avatars as pa
import cairosvg
import string
import os

from web.settings import BASE_DIR


fake = Faker()
total = 10


def convert_svg_to_image(svg_file, output_file, output_format):
    with open(svg_file, 'rb') as f:
        svg_data = f.read()
        if output_format.lower() == 'png':
            cairosvg.svg2png(bytestring=svg_data, write_to=output_file)
        elif output_format.lower() == 'jpg':
            cairosvg.svg2jpg(bytestring=svg_data, write_to=output_file)
        else:
            raise ValueError('Unsupported output format')

    return os.path.isfile(output_file)

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
    avatar = pa.Avatar.random()
    image_name = f'{fake.uuid4()}.svg'
    image_path = os.path.join(BASE_DIR, 'media', 'core', 'Owner', image_name)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    svg_data = avatar.render(path=image_path)

    png_bytes = cairosvg.svg2png(bytestring=svg_data)
    image_file = InMemoryUploadedFile(
        BytesIO(png_bytes),
        None,
        f"{fake.uuid4()}.png",
        "image/png",
        len(png_bytes),
        None,
    )

    owner = Owner(
        image=image_file,
        document_id=fake.uuid4(),
        name=fake.first_name(),
        lastname=fake.last_name(),
        phone=fake.phone_number(),
        email=fake.email(),
        birthdate=fake.date_time_between(start_date='-30y', end_date='-18y', tzinfo=timezone.utc),
    )
    owner.save()
    # owner.image.save(f'{fake.uuid4()}.png', ContentFile(avatar))

    veterinary = AffiliatedVeterinary(
        name=fake.company(),
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

