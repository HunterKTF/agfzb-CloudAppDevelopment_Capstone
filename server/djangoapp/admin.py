from django.contrib import admin
from .models import CarModel, CarMake


# Register your models here.
admin.site.register(CarModel)
# admin.site.register(CarMake)

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# CarModelAdmin class
class CarModelAdmin(admin.StackedInline):
    fields = ['model_name', 'dealer_id', 'year']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

# Register models here
# admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)

