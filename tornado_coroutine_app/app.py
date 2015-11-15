import tornado.web
import tornado.gen
import tornado.httpclient


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

        yield list(map(client.fetch, data))

        self.write('some closing\n')
        self.finish()

    def on_chunk(self, chunk):
        self.write('some chunk\n')
        self.flush()


app = tornado.web.Application([
    (r"/lists", StreamingHandler)
])
