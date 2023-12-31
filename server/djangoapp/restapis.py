from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions

import requests
import json
import os

load_dotenv()
IAM_API_KEY=os.getenv('IAM_API_KEY')
COUCH_URL=os.getenv('COUCH_URL')


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, params, **kwargs):
    # print(kwargs)
    # print(f"GET from {url}")

    if "api_key" in kwargs:
        try:
            authenticator = IAMAuthenticator(kwargs['api_key'])
            natural_language_understanding = NaturalLanguageUnderstandingV1(
                version=kwargs["version"],
                authenticator=authenticator
            )

            natural_language_understanding.set_service_url(url)

            # Basic authentication GET
            response = natural_language_understanding.analyze(
                text=kwargs["text"],
                features=Features(sentiment=SentimentOptions())
            )

            status_code = response.status_code
            print("With status {}".format(status_code))
            json_data = response.get_result()
            return json_data

        except:
            # If any error occurs
            print("Network exception occured")
    else:
        try:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'})

            status_code = response.status_code
            print("With status {}".format(status_code))
            json_data = json.loads(response.text)
            return json_data
        except:
            # If any error occurs
            print("Network exception occured")
    

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    params={
        "IAM_API_KEY":IAM_API_KEY,
        "COUCH_URL":COUCH_URL,
        "dealership":json_payload["dealership"],
        "name":json_payload["name"],
        "purchase":json_payload["purchase"],
        "review":json_payload["review"],
        "purchase_date":json_payload["purchase_date"],
        "car_make":json_payload["car_make"],
        "car_model":json_payload["car_model"],
        "car_year":json_payload["car_year"],
        "id":json_payload["id"],
        "time":json_payload["time"]
    }
    response = requests.post(url, params=params, headers={'Content-Type': 'application/json'})

    status_code = response.status_code
    print("With status {}".format(status_code))
    return response


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
                                      sentiment=analyze_review_sentiments(docs["review"]),
                                      id_r=docs["id"])
            # Append results from review_obj
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text, **kwargs):
    watson_url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/ed632029-bb7b-4780-a954-194a6b348a4f"

    version = "2022-04-07"
    return_analyzed_text = True
    api_key = os.getenv('api_key')

    params = {}

    json_result = get_request(watson_url, params=params, text=text, version=version, return_analyzed_text=return_analyzed_text, api_key=api_key)
    
    if json_result:
        sentiment_value = json_result["sentiment"]["document"]["label"]

    else:
        sentiment_value = "neutral"

    return sentiment_value
    
