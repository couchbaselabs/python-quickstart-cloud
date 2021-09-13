import base64
import datetime
import hashlib
import hmac
import requests


class CouchbaseCloud:
    """Couchbase Cloud Requests"""

    def __init__(self, access_key, secret, url) -> None:
        self.access_key = access_key
        self.secret = secret
        self.url = url

    def request(self, endpoint, method, data=None) -> requests.Response:
        """Send requests to the Couchbase Cloud
        Only supports GET, POST, DELETE"""
        # Epoch time in milliseconds
        cbc_api_now = int(datetime.datetime.now().timestamp() * 1000)

        # Form the message string for the Hmac hash
        cbc_api_message = f"{method}\n{endpoint}\n{str(cbc_api_now)}"

        # Calculate the hmac hash value with secret key and message
        cbc_api_signature = base64.b64encode(
            hmac.new(
                bytes(self.secret, "utf-8"),
                bytes(cbc_api_message, "utf-8"),
                digestmod=hashlib.sha256,
            ).digest()
        )

        # Values for the header
        cbc_api_request_headers = {
            "Authorization": f"Bearer {self.access_key}:{cbc_api_signature.decode()}",
            "Couchbase-Timestamp": str(cbc_api_now),
        }
        if method == "GET":
            # print(cbc_api_request_headers)
            res = requests.get(
                f"{self.url}{endpoint}",
                headers=cbc_api_request_headers,
            )

        elif method == "POST":
            res = requests.post(
                f"{self.url}{endpoint}",
                json=data,
                headers=cbc_api_request_headers,
            )

        elif method == "DELETE":
            res = requests.delete(
                f"{self.url}{endpoint}", headers=cbc_api_request_headers
            )
        return res
