from ratelimit import limits, RateLimitException, sleep_and_retry

import requests

MINUTES = 60


@sleep_and_retry
@limits(calls=5, period=MINUTES)
def call_api(url: str):
    response = requests.get(url)

    print(response)
    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response


while True:
    url = 'https://www.cloudflare.com/rate-limit-test/'
    try:
        call_api(url)
    except RateLimitException as e:
        print(e)
