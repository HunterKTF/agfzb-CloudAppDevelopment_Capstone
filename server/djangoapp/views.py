from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import random

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/466bba81-54b7-4f7d-82a9-b1d1e036b470/dealership-package/get-dealership"

        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

        context["dealership_list"] = dealerships

        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.full_name for dealer in dealerships])

        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        dealer_context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/466bba81-54b7-4f7d-82a9-b1d1e036b470/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        for dealer in dealerships:
            dealer_context[dealer.id] = dealer.full_name

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/466bba81-54b7-4f7d-82a9-b1d1e036b470/dealership-package/review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        context["reviews_list"] = reviews
        for data in reviews:
            context["dealer_name"] = dealer_context[dealer_id]

        context["dealer_id"] = dealer_id
        # reviews_review = ' '.join([review.review for review in reviews])

        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    context["dealer_id"] = dealer_id
    if request.method == "POST":
        # Get user input data
        content = request.POST["content"]
        name = request.POST["first_name"] + " " + request.POST["last_name"]
        if request.POST["purchasecheck"] == "on":
            purchase = True
        else:
            purchase = False
        car_select = request.POST["car"]
        car_data = car_select.split(" -")
        purchase_date = request.POST["purchasedate"]

        print(car_data)

        review = dict()
        url = 'https://us-south.functions.appdomain.cloud/api/v1/web/466bba81-54b7-4f7d-82a9-b1d1e036b470/dealership-package/post-review'

        review["date"] = datetime.utcnow().isoformat()
        review["name"] = name
        review["dealership"] = int(dealer_id)
        review["review"] = content
        review["purchase"] = purchase
        review["purchase_date"] = purchase_date
        review["car_make"] = car_data[1]
        review["car_model"] = car_data[0]
        review["car_year"] = car_data[2]

        result = post_request(url, json_payload=review)

        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

    elif request.method == "GET":
        dealer_context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/466bba81-54b7-4f7d-82a9-b1d1e036b470/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        for dealer in dealerships:
            dealer_context[dealer.id] = dealer.full_name

        context["dealer_fullname"] = dealer_context[dealer_id]

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/466bba81-54b7-4f7d-82a9-b1d1e036b470/dealership-package/review"
        get_cars = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        context["cars"] = get_cars

        return render(request, 'djangoapp/add_review.html', context)
    
    else:
        return HttpResponse("Something went wrong")
