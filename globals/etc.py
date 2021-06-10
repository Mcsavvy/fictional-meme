import requests


def pos(integer: int) -> str:
    raw = str(integer)
    if integer > 3 and integer < 21:
        return raw + "th"
    elif raw.endswith("1"):
        return raw + "st"
    elif raw.endswith("2"):
        return raw + "nd"
    elif raw.endswith("3"):
        return raw + "rd"
    else:
        return raw + "th"


def Connection(output=lambda x: x):
    url = "http://www.google.com"
    timeout = 5
    for _ in range(1, 6):
        output(f"Trying to connect for the {pos(_)} time...")
        try:
            requests.get(url, timeout=timeout)
            output(
                "Connected To The Internet Successfully.")
            return True
        except (requests.ConnectionError, requests.Timeout):
            if _ != 5:
                output(
                    "Connection Refused. Trying Again...")
            else:
                output("Connection Refused. Aborting...")
    return False


def If(true, returnThis, elseThis):
    return returnThis if true else elseThis
