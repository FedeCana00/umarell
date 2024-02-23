from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud import pubsub_v1
import json

class Cantiere(object):
    def __init__(self):
        self.db = firestore.Client()
        # pub/sub
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path('generalsac', 'new_cantiere')

    def addCantiere(self, id, body):
        try:
            int(id) # check id is integer
            indirizzo = body['indirizzo']
            cap = int(body['cap'])
            id = str(id)

            if cap < 0 or cap > 99999:
                raise Exception('Cap errror!')
        except:
            return None, 400
        
        # conflict
        if self.db.collection('cantiere').document(id).get().exists:
            return None, 409
        
        res = {'indirizzo': indirizzo, 'cap': cap}
        self.db.collection('cantiere').document(id).set(res)

        # publish to topic
        self.publisher.publish(self.topic_path, json.dumps(res).encode('utf-8'))

        return res, 201
    
    def getCantiere(self, id):
        doc = self.db.collection('cantiere').document(str(id)).get()

        if doc.exists:
            return doc.to_dict(), 200 
        
        return None, 404
    
    def search(self, cap):
        res = []
        for doc in self.db.collection("cantiere").where(filter=FieldFilter("cap", "==", cap)).get():
            um = doc.to_dict()
            um['id'] = doc.id
            res.append(um)

        return res

    def clean(self):
        for doc in self.db.collection('cantiere').stream():
            doc_ref = doc.reference
            doc_ref.delete()