from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealer_by_id, get_dealers_from_cf, get_dealers_by_state, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json


# Get an instance of a logger
logger = logging.getLogger(__name__)

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/ce5e7331-ecda-4c59-93e7-e273cf8c4a1d/dealership-package/get-dealership"
        # Get dealers from the URL
        context = {"dealerships": get_dealers_from_cf(url)}
        # Concat all dealer's short name
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('/djangoapp')

def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
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
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("/djangoapp/")
        else:
            return render(request, 'djangoapp/registration.html', context)

def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('/djangoapp/')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

def aboutUs(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

def contactUs(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# View to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = 'https://us-south.functions.appdomain.cloud/api/v1/web/ce5e7331-ecda-4c59-93e7-e273cf8c4a1d/dealership-package/get-reviews-on-delarship'
        reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        context = {
            "reviews":  reviews, 
            "dealer_id": dealer_id
        }

        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
    # User must be logged in before posting a review
    if request.user.is_authenticated:
        # GET request renders the page with the form for filling out a review
        if request.method == "GET":
            url = f"https://us-south.functions.appdomain.cloud/api/v1/web/ce5e7331-ecda-4c59-93e7-e273cf8c4a1d/dealership-package/get-reviews-on-delarship?dealerId={dealer_id}"
            # Get dealer details from the API
            context = {
                "cars": CarModel.objects.all(),
                "dealer": get_dealer_by_id(url, dealer_id=dealer_id),
            }
            return render(request, 'djangoapp/add_review.html', context)

        # POST request posts the content in the review submission form to the Cloudant DB using the post_review Cloud Function
        if request.method == "POST":
            form = request.POST
            review = dict()
            review["name"] = f"{request.user.first_name} {request.user.last_name}"
            review["dealership"] = dealer_id
            review["review"] = form["content"]
            review["purchase"] = form.get("purchasecheck")
            if review["purchase"]:
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"] = car.year
            
            # If the user bought the car, get the purchase date
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
            else: 
                review["purchase_date"] = None

            url = "https://us-south.functions.appdomain.cloud/api/v1/web/ce5e7331-ecda-4c59-93e7-e273cf8c4a1d/dealership-package/post-review-on-delarship"  # API Cloud Function route
            json_payload = {"review": review}  # Create a JSON payload that contains the review data

            # Performing a POST request with the review
            result = post_request(url, json_payload, dealerId=dealer_id)
            if int(result.status_code) == 200:
                print("Review posted successfully.")

            # After posting the review the user is redirected back to the dealer details page
            return redirect("djangoapp:dealer_details", dealerId=dealer_id)

    else:
        # If user isn't logged in, redirect to login page
        print("User must be authenticated before posting a review. Please log in.")
        return redirect("/djangoapp/login")