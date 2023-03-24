from django.contrib import admin

from core.models import *


# Owner
# SubscriptionPlan
# Service
# AffiliatedVeterinary
# VeterinaryService
# VeterinaryPromotion

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Owner._meta.fields]
    search_fields = ['',]

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = [x.name for x in SubscriptionPlan._meta.fields]
    search_fields = ['', ]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Service._meta.fields]
    search_fields = ['', ]


@admin.register(AffiliatedVeterinary)
class AffiliatedVeterinaryAdmin(admin.ModelAdmin):
    list_display = [x.name for x in AffiliatedVeterinary._meta.fields]
    search_fields = ['', ]


@admin.register(VeterinaryService)
class VeterinaryServiceAdmin(admin.ModelAdmin):
    list_display = [x.name for x in VeterinaryService._meta.fields]
    search_fields = ['', ]


@admin.register(VeterinaryPromotion)
class VeterinaryPromotionAdmin(admin.ModelAdmin):
    list_display = [x.name for x in VeterinaryPromotion._meta.fields]
    search_fields = ['', ]
