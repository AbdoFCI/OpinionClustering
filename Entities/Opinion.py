class Opinion:
    id
    text = ''
    hash_tags = [] #list
    clusterid= None# for Testing

    def __init__(self, id =0, hash_tags = None,text='default',cluster = 1):
        self.id = id
        self.hash_tags = hash_tags
        self.text = text
        self.clusterid = cluster

    def json_to_opinion(self,dec):
        self.id = dec['opId']
        self.text = dec['opinion']
        self.hash_tags = dec['hashtags']

    def get_hash_tags(self):# distncit hashtag
        result = set(self.hash_tags)
        return result;

    def is_in(self,hashtag):
        return hashtag in self.get_hash_tags()

    def opinion_to_json(self):
        return {"opId": self.id, "opinion": self.text, "hashtags": self.hash_tags}

