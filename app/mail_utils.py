
import os
from zerobouncesdk import ZeroBounce, ZBException
from dotenv import load_dotenv

API = os.getenv("ZEROBOUNCE_API_KEY")
zero_bounce = ZeroBounce("API")
def validate_email(email):
    try:
        response = zero_bounce.validate(email)
        print(response)
        if response.status == "valid":
            return True
        else:
            return False
    except ZBException as e:
        print("ZeroBounce validate error: " + str(e))
