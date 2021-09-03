from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return "Car name: " + self.name + ", " + \
               "Description: " + self.description


class CarModel(models.Model):
    car_make = models.ForeignKey('CarMake', on_delete=models.CASCADE)
    dealerID = models.IntegerField()

    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    MODEL_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon')
    ]
    car_type = models.CharField(
        null=False,
        max_length=20,
        choices=MODEL_CHOICES,
        default=SEDAN
    )
    year = models.DateField()

    def __str__(self):
        return "Dealer ID: " + self.dealerID + ", " + \
               "Car type: " + self.car_type + ", " + \
               "Year: " + self.year

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
