import tornado.gen
import tornado.httpclient
import tornado.ioloop
import tornado.locks
import tornado.queues
import tornado.web

from . import mapper
from .connector import GetResponseConnectorAsync
from .handler import GetResponseApiHandler


class CampaignsHandler(GetResponseApiHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(path="/newsletters",
                         connector=GetResponseConnectorAsync(),
                         mapper_function=mapper.json_newsletter_to_campaign,
                         max_clients=5,
                         application=application,
                         request=request,
                         **kwargs)


class ListsHandler(GetResponseApiHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(path="/campaigns",
                         connector=GetResponseConnectorAsync(),
                         mapper_function=mapper.json_campaign_to_list,
                         max_clients=5,
                         application=application,
                         request=request,
                         **kwargs)


class MembersHandler(GetResponseApiHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(path="/contacts",
                         connector=GetResponseConnectorAsync(),
                         mapper_function=mapper.json_contact_to_member,
                         max_clients=5,
                         application=application,
                         request=request,
                         **kwargs)


app = tornado.web.Application([
    (r"/campaigns", CampaignsHandler),
    (r"/lists", ListsHandler),
    (r"/members", MembersHandler)
])
