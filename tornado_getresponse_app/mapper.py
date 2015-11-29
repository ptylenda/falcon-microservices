from .domain import Campaign
from .domain import List
from .domain import Member


def json_newsletter_to_campaign(data):
    if 'newsletterId' in data:
        return Campaign(esp_id=data['newsletterId'],
                        name=data['name'],
                        subject=data['subject'])
    return data


def json_campaign_to_list(data):
    return List(esp_id=data['campaignId'],
                name=data['name'])


def json_contact_to_member(data):
    if 'contactId' in data:
        return Member(esp_id=data['contactId'],
                      name=data['name'],
                      email=data['email'])
    return data
