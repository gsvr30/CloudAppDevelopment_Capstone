from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf

# Get an instance of a logger
logger = logging.getLogger(__name__)


def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


def contact(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html')


def login_request(request):
    context = {}
    # Handles POST request
    if request.method == 'POST':
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
    #         return redirect('djangoapp:index')
    #     else:
    #         # If not, return to login page again
    #         return render(request, 'djangoapp/user_login.html', context)
    # else:
    #     return render(request, 'djangoapp/user_login.html', context)
    return redirect('djangoapp:index')


def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')


def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['psw']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name,
                last_name=last_name, password=password)
            login(request, user)
            # redirect to course list page
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://2df84b44.eu-gb.apigw.appdomain.cloud/api/dealership/"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://2df84b44.eu-gb.apigw.appdomain.cloud/api/review"
        # Get dealers from the URL        
        reviews = get_dealer_reviews_from_cf(url, dealer_id)        
        # Concat all dealer's short name
        review_comments = ' '.join([review.review for review in reviews])
        # Return a list of dealer short name
        context = dict()
        context['dealer_id'] = dealer_id
        context['reviews'] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id):
    if request.method == "POST":
        url = "https://2df84b44.eu-gb.apigw.appdomain.cloud/api/review"
        # review = { "id": 1114, "name": "Upkar Lidder", "dealership": 15, "review": "Great service!", 
        # "purchase": False, "another": "field", "purchase_date": "02/16/2021", 
        # "car_make": "Audi", "car_model": "Car", "car_year": 2021 }
        review = dict()
        review['id'] = int(datetime.strftime(datetime.utcnow(), "%Y%m%d%H%M%S"))
        review['name'] = request.user.first_name + ' ' + request.user.last_name
        review['dealership'] = dealer_id
        review["time"] = datetime.utcnow().isoformat()
        review["review"] = request.POST['content']
        review['purchase'] = 'purchasecheck' in request.POST['purchasecheck'] and request.POST['purchasecheck'] == 'on'
        review['purchase_date'] = request.POST['purchasedate']

        car = CarModel.objects.get(id=request.POST['car'])
        review['car_make'] = car.make.name
        review['car_model'] = car.name
        review['car_year'] = str(car.year)
        
        json_payload = {'review': review}
        response = post_request(url, json_payload, dealerId=dealer_id)
        print(response)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        url = "https://2df84b44.eu-gb.apigw.appdomain.cloud/api/dealership/"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        first_or_default = next((x for x in dealerships if x.id == dealer_id), None)        
        cars = CarModel.objects.filter(dealerID=dealer_id)
        context = dict()
        context['cars'] = cars
        context['dealer'] = first_or_default
        return render(request, 'djangoapp/add_review.html', context)
