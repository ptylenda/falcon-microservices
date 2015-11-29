from .domain import List
from .domain import Member


def json_campaign_to_list(data):
    return List(data['campaignId'], data['name'])


def json_contact_to_member(data):
    if 'contactId' in data:
        return Member(data['contactId'], data['name'], data['email'])
    return data
