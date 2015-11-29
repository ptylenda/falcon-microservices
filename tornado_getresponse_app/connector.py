import tornado.httpclient


class GetResponseConnectorAsync(object):
    def __init__(self):
        self.token = ""  # Some dead test account
        self.auth_headers = {'X-Auth-Token': 'api-key ' + self.token}

    def get(self, path):
        return tornado.httpclient.HTTPRequest(url=self._url(path),
                                              method='GET',
                                              headers=self.auth_headers,
                                              connect_timeout=3600,
                                              request_timeout=3600)

    def head(self, path):
        return tornado.httpclient.HTTPRequest(url=self._url(path),
                                              method='HEAD',
                                              headers=self.auth_headers)

    @staticmethod
    def _url(path):
        return 'http://api.getresponse.com/v3' + path