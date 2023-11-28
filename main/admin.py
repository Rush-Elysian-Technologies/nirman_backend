from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Vendor)
admin.site.register(models.Customer)
admin.site.register(models.serviceCategory)

admin.site.register(models.Rating)
admin.site.register(models.vendorAddAddress)
admin.site.register(models.customerAddAddress)
admin.site.register(models.Order)
admin.site.register(models.OrderItems)

admin.site.register(models.ServiceImage)

class ServiceImagesInline(admin.StackedInline):
    model = models.ServiceImage  # Use 'model' instead of 'models'

class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServiceImagesInline,]

admin.site.register(models.Service, ServiceAdmin)