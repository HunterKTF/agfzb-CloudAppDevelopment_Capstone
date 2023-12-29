from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

authenticator = IAMAuthenticator(os.getenv("IAM_API_KEY"))

service = CloudantV1(authenticator=authenticator)

service.set_service_url(os.getenv("COUCH_URL"))

# response = service.get_all_dbs().get_result()
# response = service.post_all_docs(db='dealerships', include_docs=True, start_key='abc', limit=2).get_result()
response = service.post_find(
    db='dealerships',
    selector={
        "state": {
            "$regex": "California"
        }
    },
    fields=[
        "id",
        "city",
        "state",
        "st",
        "address",
        "zip",
        "lat",
        "long"
    ]
).get_result()


print(response)