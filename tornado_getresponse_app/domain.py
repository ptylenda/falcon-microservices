class Campaign(object):
    def __init__(self, esp_id, name, subject):
        self.esp_id = esp_id
        self.name = name
        self.subject = subject


class List(object):
    def __init__(self, esp_id, name):
        self.esp_id = esp_id
        self.name = name


class Member(object):
    def __init__(self, esp_id, name, email):
        self.esp_id = esp_id
        self.name = name
        self.email = email
