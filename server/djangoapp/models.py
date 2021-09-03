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


class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.id = id
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Review: " + self.review
