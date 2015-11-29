import json
import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.ioloop
import tornado.locks
import tornado.queues
import requests


def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


class GetResponseConnector(object):
    token = ""  # Some dead test account

    def get(self, path, extra_headers):
        auth_headers = {'X-Auth-Token': 'api-key ' + self.token}
        return requests.get(self._url(path), headers=merge_dicts(auth_headers, extra_headers))

    def head(self, path, extra_headers):
        auth_headers = {'X-Auth-Token': 'api-key ' + self.token}
        return requests.head(self._url(path), headers=merge_dicts(auth_headers, extra_headers))

    @staticmethod
    def _url(path):
        return 'http://api.getresponse.com/v3' + path


class GetResponseConnectorAsync(object):
    token = ""  # Some dead test account

    def get(self, path):
        auth_headers = {'X-Auth-Token': 'api-key ' + self.token}
        return tornado.httpclient.HTTPRequest(url=self._url(path), headers=auth_headers,  connect_timeout=600, request_timeout=600)

    def head(self, path, extra_headers):
        auth_headers = {'X-Auth-Token': 'api-key ' + self.token}
        return tornado.httpclient.HTTPRequest(url=self._url(path), headers=merge_dicts(auth_headers, extra_headers))

    @staticmethod
    def _url(path):
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

    q = tornado.queues.Queue(maxsize=0)
    sem = tornado.locks.BoundedSemaphore(value=10)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):


        # self.write(str(resp.headers))
        # self.flush()





        #resp = yield [self.flush_page(page) for page in range(1, count + 1)]


        tornado.ioloop.IOLoop.current().spawn_callback(self.consumer)
        yield self.producer()     # Wait for producer to put all tasks.
        yield self.q.join()       # Wait for consumer to finish all tasks.




        #for page, response in resp.items():
        #    self.write(response.body)

        # yield list(map(client.fetch, data))

        self.finish()


    @tornado.gen.coroutine
    def producer(self):
        client = tornado.httpclient.AsyncHTTPClient(max_clients=10)
        connector_async = GetResponseConnectorAsync()
        connector = GetResponseConnector()
        resp = connector.head("/contacts", {'perPage': 1000})
        count = int(resp.headers['TotalPages']);

        print(count)

        for page in range(1, count + 1):
            job = client.fetch(connector_async.get(path="/contacts?perPage={0}&page={1}".format(1000, page)))
            yield self.q.put(job)

    @tornado.gen.coroutine
    def consumer(self):
        while True:
            job = yield self.q.get()
            try:
                self.sem.acquire()
                yield self.process(job)
            finally:
                self.q.task_done()

    @tornado.gen.coroutine
    def process(self, job):
        print("processing!")
        response = yield job
        self.write(response.body)
        self.flush()


app = tornado.web.Application([
    (r"/lists", StreamingHandler)
])
