from django.db import models

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class AffiliatedVeterinary(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    overdue_payment = models.BooleanField(default=False)

class VeterinaryService(models.Model):
    veterinary = models.ForeignKey(AffiliatedVeterinary, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

class VeterinaryPromotion(models.Model):
    veterinary = models.ForeignKey(AffiliatedVeterinary, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
