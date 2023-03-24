from django.db import models


class AutoDateTimeAbstract(models.Model):
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Owner(AutoDateTimeAbstract):
    document_id = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    birthdate = models.DateTimeField()

    class Meta:
        verbose_name = "Owner"
        verbose_name_plural = "Owners"
        ordering = ["name", "lastname"]

    def __str__(self):
        return f"{self.name} {self.lastname}"


class SubscriptionPlan(AutoDateTimeAbstract):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Service(AutoDateTimeAbstract):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ('name',)

    def __str__(self):
        return self.name


class AffiliatedVeterinary(AutoDateTimeAbstract):
    name = models.CharField(max_length=255)
    logo = models.ImageField(
        upload_to='core/AffiliatedVeterinary/', blank=True, null=True)
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.CASCADE)
    overdue_payment = models.BooleanField(default=False)
    web_page = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Affiliated Veterinary'
        verbose_name_plural = 'Affiliated Veterinaries'
        ordering = ('name',)

    def __str__(self):
        return self.name


class VeterinaryService(AutoDateTimeAbstract):
    veterinary = models.ForeignKey(
        AffiliatedVeterinary, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Veterinary Service'
        verbose_name_plural = 'Veterinary Services'
        ordering = ('veterinary',)

    def __str__(self):
        return f'{self.veterinary} - {self.service}'


class VeterinaryPromotion(AutoDateTimeAbstract):
    veterinary = models.ForeignKey(
        AffiliatedVeterinary, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Veterinary Promotion'
        verbose_name_plural = 'Veterinary Promotions'
        ordering = ('veterinary',)

    def __str__(self):
        return f'{self.veterinary} - {self.title}'
