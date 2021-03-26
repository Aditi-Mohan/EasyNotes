class ShareRequest:
    req_from = None
    note_id = None
    sub_name = None
    unit_name = None
    note_title = None
    friend_name = None
    sent_on = None

    def __init__(self, req_from, note_id, sub_name, unit_name, sent_on, note_title, friend_name):
        self.req_from = req_from
        self.note_id = note_id
        self.sub_name = sub_name
        self.unit_name = unit_name
        self.sent_on = sent_on
        self.note_title = note_title
        self.friend_name = friend_name