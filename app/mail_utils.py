import os
from zerobouncesdk import ZeroBounce, ZBException
from dotenv import load_dotenv

API = os.getenv("ZEROBOUNCE_API_KEY")
if API is not None and API.strip():
    zero_bounce = ZeroBounce(API)

def validate_email(email):
    """
    Validates an email address using the ZeroBounce API.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    try:
        response = zero_bounce.validate(email)
        if response.status == "valid":
            return True
        else:
            return False
    except ZBException as e:
        print("ZeroBounce validate error: " + str(e))
