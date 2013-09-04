import json, requests, urllib

class OpenClassAPI(object):
    """
        OpenClassAPI class handles all requests to and from Pearson's OpenClass.com API. 

        Example: get info on a course.

        >>> oc_api = OpenClassAPI('sam@classowl.com', 'password', 'openclass_api_key')
        >>> r = oc_api.make_request('GET', '{}/v1/campus/coursesections/8303682'.format(oc_api.BASE_API_URL))
        >>> r
        { 'courseTitle': 'Math 51', 'courseCode': 'MATH 51', ......... }
    """

    # ====================================================
    # static-ish variables
    # ====================================================

    BASE_API_URL = 'https://api.openclasslabs.com'

    # For fetching the authentication token
    IDENTITY_URL         = '{}/v1/identities/login/basic'.format(BASE_API_URL)
    IDENTITY_REFRESH_URL = '{}/v1/identities/login/refresh'.format(BASE_API_URL)

    """
        OpenClassAPI

        Purpose: establishes a connection with the OpenClass API, saves API key for later use

        Returns: __init__ functions can't return anything! derrrrr

        Required parameters:
            - admin_email: email of OpenClass admin
            - admin_pw:    password of OpenClass admin
            - api_key:     OpenClass API key

        Optional parameters:
            - auth_token:    authentication token (if you cached it)
            - refresh_token: refresh token (if you cached it)
    """
    def __init__(
        self,
        admin_email,
        admin_pw,
        api_key,
        auth_token    = None,
        refresh_token = None,
        debug         = False
    ):
        self.api_key = api_key
        self.debug   = debug

        if auth_token and refresh_token:
            if self.debug:
                print 'Auth tokens passed in at instantiation'

            self.auth_token    = auth_token
            self.refresh_token = refresh_token
        else:
            if self.debug:
                print 'Getting auth tokens at instantiation'
            self.set_auth_tokens(admin_email, admin_pw)
        
        if self.debug:
            print 'Auth tokens: {}'.format({'auth_token': self.auth_token, 'refresh_token': self.refresh_token})
    
    # ====================================================
    # authenticating with OpenClass
    # ====================================================

    """
        set_auth_tokens

        Purpose: sets auth tokens from an admin email and password

        Returns: None
    """
    def set_auth_tokens(self, admin_email, admin_pw):
        tokens = self.get_auth_tokens(admin_email, admin_pw)

        self.auth_token    = tokens['auth_token']
        self.refresh_token = tokens['refresh_token']

    """
        get_auth_tokens

        Purpose: gets an auth token from OpenClass in order to make valid requests to their API

        Returns: {'auth_token': <auth_token>, 'refresh_token': <refresh_token>}

        Required parameters:
            - admin_email: email address of OpenClass admin
            - admin_pw:    password of OpenClass admin
    """
    def get_auth_tokens(self, admin_email, admin_pw):
        url = '{}?apiKey={}'.format(self.IDENTITY_URL, self.api_key)

        payload = {'email': admin_email, 'password': admin_pw}
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        r           = requests.post(url, data = payload, headers = headers)
        status_code = r.status_code

        # http status code != 200? raise an error!
        r.raise_for_status()
        data = r.json()['data']

        return {'auth_token': data['authToken'], 'refresh_token': data['refreshToken']}

    """
        refresh_auth_tokens

        Purpose: refreshes the OpenClass auth_token we need to make requests to their API

        Returns: None
    """
    def refresh_auth_tokens(self):
        tokens = self.get_refreshed_auth_tokens()
        
        if self.debug:
            print 'Auth tokens: {}'.format(tokens)

        self.auth_token    = tokens['auth_token']
        self.refresh_token = tokens['refresh_token']

    """
        get_refreshed_auth_tokens

        Purpose: gets the new auth tokens by using the refresh token

        Returns: {'auth_token': <auth_token>, 'refresh_token': <refresh_token>}
    """
    def get_refreshed_auth_tokens(self):
        url     = self.IDENTITY_REFRESH_URL
        payload = {'apiKey': self.api_key, 'refreshToken': self.refresh_token}

        r = requests.get(url, params = payload)

        data = r.json()['data']

        return {'auth_token': data['authnToken'], 'refresh_token': data['refreshToken']}

    # ====================================================
    # do you take requests? now we do!
    # ====================================================

    """
        make_request

        Purpose: creates a request to the OpenClass API

        Returns: json response from OpenClass API

        Required parameters:
            - request_type: must be 'GET', 'POST', 'PUT', or 'DELETE'
            - url:             valid OpenClass API url

        Optional parameters:
            - payload: dictionary of extra parameters that will be encoded in request URL as GET vars
            - headers: dictionary of extra headers you may need in the request
            - data:    dictionary of data that will be json'ed and sent in body of POST or PUT
    """
    def make_request(self, request_type, url, payload = {}, headers = {}, data = {}):
        xauth   = {'X-Authorization': self.auth_token}
        api_key = {'apiKey': self.api_key}

        headers.update(xauth)
        payload.update(api_key)

        if request_type == 'POST':
            r = requests.post(url,   headers = headers, params = payload, data = json.dumps(data))
        elif request_type == 'PUT':
            r = requests.put(url,    headers = headers, params = payload, data = json.dumps(data))
        elif request_type == 'DELETE':
            r = requests.delete(url, headers = headers, params = payload)
        else:
            r = requests.get(url,    headers = headers, params = payload)

        if self.debug:
            print 'Requested URL: {}&token={}'.format(r.url, urllib.quote_plus(self.auth_token))
            
            if payload: print 'Payload: {}'.format(payload)
            if headers: print 'Headers: {}'.format(headers)
            if data:    print 'Data: {}'.format(data)

        # If we don't have the latest auth token, refresh it on the fly and re-run the request.
        if r.status_code == 401:
            self.refresh_auth_tokens()
            return self.make_request(request_type, url, payload = payload, headers = headers, data = data)

        data = r.json()
        
        if self.debug: print 'Response: {}'.format(data)

        return data