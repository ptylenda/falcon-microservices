class List(object):
    def __init__(self, esp_id, name):
        self.esp_id = esp_id
        self.name = name


class Member(object):
    def __init__(self, esp_id, name, email):
        self.esp_id = esp_id
        self.name = name
        self.email = email
