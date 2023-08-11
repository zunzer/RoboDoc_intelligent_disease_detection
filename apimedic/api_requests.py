import requests  # https://requests.readthedocs.io/en/master/api/
import hmac  # https://docs.python.org/3/library/hmac.html
import base64
import json

# example api calls
# https://github.com/priaid-eHealth/symptomchecker/blob/master/Python/PriaidDiagnosisClient.py


def get_auth_token(username, password, url):
    """
    Get authentication token from auth api.
    :param username: api_key username
    :param password: api_key password
    :param url: api url
    :return: auth token as string
    """
    # get hashed credentials
    raw_hash_string = hmac.new(bytes(password, encoding='utf-8'), url.encode('utf-8'), digestmod='MD5').digest()
    computed_hash_string = base64.b64encode(raw_hash_string).decode()
    bearer_credentials = username + ':' + computed_hash_string

    # add credentials to header
    header = {
        'Authorization': 'Bearer {}'.format(bearer_credentials)
    }

    # call api
    response = requests.post(url, headers=header)

    # extract token from response
    token = json.loads(response.text)['Token']

    return token


def get_item(item, params, url):
    """
    Get selected item.
    :param item: Item to retrieve from API, e.g. 'symptoms', 'diagnosis'
    :param params: Dictionary object containing key-value pairs to be passed as arguments.
    :param url: api url
    :return: json-response of api
    """
    # attach item to url
    url = url + '/' + item
    response = requests.get(url, params=params)

    return response
