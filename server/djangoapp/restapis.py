import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()
IAM_API_KEY=os.getenv('IAM_API_KEY')
COUCH_URL=os.getenv('COUCH_URL')


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, params, **kwargs):
    print(kwargs)
    print(f"GET from {url}")

    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occured")
    
    status_code = response.status_code
    print("With status {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []

    params={
        "IAM_API_KEY":IAM_API_KEY,
        "COUCH_URL":COUCH_URL
    }

    # Call get_request with a URL parameters
    json_result = get_request(url, params=params)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        for dealer in dealers:
            # Get its content in 'doc' object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in 'doc' object
            dealer_obj = CarDealer(address=dealer_doc["address"],
                                   city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"],
                                   id_d=dealer_doc["id"],
                                   lat=dealer_doc["lat"],
                                   lon=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"],
                                   zip_c=dealer_doc["zip"])
            # Append results from dealer_obj
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []

    params={
        "IAM_API_KEY":IAM_API_KEY,
        "COUCH_URL":COUCH_URL,
        "dealerId":dealer_id
    }

    # Call get_request with a URL and dealer_id parameters
    json_results = get_request(url, params=params)
    if json_results:
        review_docs = json_results["docs"]
        for docs in review_docs:
            review_obj = DealerReview(dealership=docs["dealership"],
                                      name=docs["name"],
                                      purchase=docs["purchase"],
                                      review=docs["review"],
                                      purchase_date=docs["purchase_date"],
                                      car_make=docs["car_make"],
                                      car_model=docs["car_model"],
                                      car_year=docs["car_year"],
                                      sentiment="positive",
                                      id_r=docs["id"])
            # Append results from review_obj
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
