import os
import hmac
import hashlib


def generateHmac(params: dict) -> str:
    paramsString = ""
    for key, value in params.items():
        paramsString += f"{key}={value}&"
    paramsString = paramsString[:-1].encode()
    keySignature = os.getenv("SIGNATURE").encode()
    digest = hmac.new(
        key=keySignature,
        msg=paramsString,
        digestmod=hashlib.sha256
    ).hexdigest()
    return f"{digest}"
