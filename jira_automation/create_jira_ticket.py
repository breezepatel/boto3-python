# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import os

url = "https://northeastern-team-n0lxizqj.atlassian.net/rest/api/3/issue"

API_TOKEN=os.environ.get("API_TOKEN_JIRA")
print("API token loaded:", bool(API_TOKEN))

auth = HTTPBasicAuth("patel.bre@northeastern.edu", API_TOKEN)

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

payload = json.dumps( {
  "fields": {
    "description": {
      "content": [
        {
          "content": [
            {
              "text": "My first jira ticket",
              "type": "text"
            }
          ],
          "type": "paragraph"
        }
      ],
      "type": "doc",
      "version": 1
    },
    "project": {
      "key": "AA"
    },
    "issuetype": {
      "id": "10009"
    },
    "summary": "First JIRA Ticket",
  },
  "update": {}
} )

response = requests.request(
   "POST",
   url,
   data=payload,
   headers=headers,
   auth=auth
)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
