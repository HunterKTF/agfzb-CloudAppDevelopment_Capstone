from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default="")
    description = models.CharField(null=False, max_length=50, default="")

    def __str__(self):
        return self.name + ", " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    COUPE = 'coupe'
    SPORTS_CAR = 'sports car'
    STATION_WAGON = 'station wagon'
    HATCHBACK = 'hatchback'
    CONVERTIBLE = 'convertible'
    MINIVAN = 'minivan'
    PICKUP = 'pickup'

    TYPE_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (COUPE, "Coupe"),
        (SPORTS_CAR, "Sports Car"),
        (STATION_WAGON, "Wagon"),
        (HATCHBACK, "Hatchback"),
        (CONVERTIBLE, "Convertible"),
        (MINIVAN, "Minivan"),
        (PICKUP, "Pickup Truck")
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    model_name = models.CharField(null=False, max_length=30, default="")
    dealer_id = models.IntegerField()
    car_type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
    year = models.DateField(null=True)

    def __str__(self):
        return "Car make: " + self.car_make + ", " \
                "Model name: " + self.model_name + ", " \
                "Dealer id: " + self.dealer_id + ", " \
                "Car type: " + self.car_type + ", " \
                "Year: " + self.year
                

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
