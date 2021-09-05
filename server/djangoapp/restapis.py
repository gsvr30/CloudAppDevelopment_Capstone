import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


def get_request(url, api_key=None, **kwargs):
    print("GET from {} ".format(url))
    print(kwargs)
    try:
        if api_key:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        auth=HTTPBasicAuth('apikey', api_key),
                                        params=kwargs)
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['body']['rows']
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result['reviews']
        # For each review object
        for review_doc in reviews:
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                   id=review_doc["id"], review=review_doc["review"], purchase_date=review_doc["purchase_date"],
                                   car_make=review_doc["car_make"], car_model=review_doc["car_model"],
                                   car_year=review_doc["car_year"], sentiment=review_doc.get("sentiment"))
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results


def analyze_review_sentiments(dealerreview):
    authenticator = IAMAuthenticator('1jhQUGS2rnvg64JptID2YvZ3JeZhjmaETMnYv1yqhSpZ')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2020-08-01',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url('https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/c7b538cf-8226-4a33-b7a4-5067b4f6143e')
    try:
        response = natural_language_understanding.analyze(
            text=dealerreview,
            features=Features(sentiment=SentimentOptions())).get_result()

        print(json.dumps(response, indent=2))
        return response['sentiment']['document']['label']
    except:
        return 'neutral'


def post_request(url, json_payload, **kwargs):
    print(json_payload)
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, json=json_payload)
    except:
        # If any error occurs        
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
