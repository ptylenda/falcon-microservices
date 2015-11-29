import json

import tornado.gen
import tornado.httpclient
import tornado.ioloop
import tornado.queues
import tornado.web

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

import time

class GetResponseApiHandler(tornado.web.RequestHandler):
    def __init__(self, path, connector, mapper_function, max_clients, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.path = path
        self.connector = connector
        self.mapper = mapper_function
        self.client = tornado.httpclient.AsyncHTTPClient(max_clients=max_clients)
        self.response_queue = tornado.queues.Queue(maxsize=256)
        self.flush_interval = 128

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        self.write("[")
        yield self._write_data()
        self.write("]")
        self.finish()

    @tornado.gen.coroutine
    def _write_data(self):
        tornado.ioloop.IOLoop.current().spawn_callback(self._json_dumper)
        count = yield self._get_page_count()
        #count = 1
        yield [self._process_page(page) for page in range(1, count + 1)]
        yield self.response_queue.join()

    @tornado.gen.coroutine
    def _get_page_count(self):
        req = self.connector.head(path="{0}?perPage={1}".format(self.path, 1000))
        resp = yield self.client.fetch(req)
        return int(resp.headers['TotalPages'])

    @tornado.gen.coroutine
    def _process_page(self, page):
        req = self.connector.get(path="{0}?perPage={1}&page={2}".format(self.path, 1000, page))
        resp = yield self.client.fetch(req)
        start = time.time()
        for l in json.loads(resp.body.decode("utf-8"), object_hook=self.mapper):
            yield self.response_queue.put(l)
        end = time.time()
        print(end - start)

    @tornado.gen.coroutine
    def _json_dumper(self):
        current = 1
        while True:
            obj = yield self.response_queue.get()
            try:
                if current > 1:
                    self.write(",")
                self.write(json.dumps(obj.__dict__))
                if current % self.flush_interval == 0:
                    self.flush()
                current += 1
            finally:
                self.response_queue.task_done()
