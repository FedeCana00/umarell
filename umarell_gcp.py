from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

class Umarell(object):
    def __init__(self):
        self.db = firestore.Client()

    def addUmarell(self, id, body):
        try:
            int(id) # check id is integer
            nome = body['nome']
            cognome = body['cognome']
            cap = int(body['cap'])
            id = str(id)

            if cap < 0 or cap > 99999:
                raise Exception('Cap errror!')
        except:
            return None, 400
        
        # conflict
        if self.db.collection('umarell').document(id).get().exists:
            return None, 409
        
        res = {'nome': nome, 'cognome': cognome, 'cap': cap}
        self.db.collection('umarell').document(id).set(res)
        return res, 201
    
    def getUmarell(self, id):
        doc = self.db.collection('umarell').document(str(id)).get()

        if doc.exists:
            return doc.to_dict(), 200
    
        return None, 404
    
    def search(self, cap):
        res = []
        for doc in self.db.collection("umarell").where(filter=FieldFilter("cap", "==", cap)).get():
            um = doc.to_dict()
            um['id'] = doc.id
            res.append(um)
        
        return res

    def clean(self):
        for doc in self.db.collection('umarell').stream():
            doc_ref = doc.reference
            doc_ref.delete()