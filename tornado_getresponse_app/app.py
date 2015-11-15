import json
import tornado.web
import tornado.gen
import tornado.httpclient
import requests


class GetResponseConnector(object):
    token = "b60399e794d52b82957dd62a4fa4c2b9"  # Some dead test account

    def get(self, path):
        """
        :type path: str
        :param path: str
        :return:
        :rtype: requests.Response
        """
        return requests.get(self._url(path), headers={'X-Auth-Token': 'api-key ' + self.token})

    @staticmethod
    def _url(path):
        """
        :type path: str
        :param path: str
        :return:
        :rtype: str
        """
        return 'http://api.getresponse.com/v3' + path


class CampaignToListsMapper(object):
    def map(self, campaigns_json):
        return campaigns_json

'''
class BaseResource(object):
    def __init__(self, path, connector, mapper):
        self.path = path
        self.connector = connector
        self.mapper = mapper

    def on_get(self, req, resp):
        """
        :type req: falcon.Request
        :param req:
        :type resp: falcon.Response
        :param resp:
        :return:
        """
        api_resp = self.connector.get(self.path)
        # parse errors here
        mapped_json = self.mapper.map(api_resp.json())
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(mapped_json)


class ListsResource(BaseResource):
    def __init__(self, connector=GetResponseConnector(), mapper=CampaignToListsMapper()):
        super().__init__("/campaigns/", connector, mapper)

'''


class StreamingHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()

        self.write('some opening\n')
        self.flush()

        data = [
            tornado.httpclient.HTTPRequest(
                url='http://httpbin.org/delay/' + str(delay),
                streaming_callback=self.on_chunk
            ) for delay in [5, 4, 3, 2, 1]
        ]

        # `map()` doesn't return a list in Python 3
        yield list(map(client.fetch, data))

        self.write('some closing\n')
        self.finish()

    def on_chunk(self, chunk):
        self.write('some chunk\n')
        self.flush()


app = tornado.web.Application([
    (r"/lists", StreamingHandler)
])
