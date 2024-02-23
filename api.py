from flask import Flask, request
from flask_restful import Resource, Api
from umarell_gcp import Umarell
from cantiere_gcp import Cantiere

umarell_dao = Umarell()
cantiere_dao = Cantiere()

class Clean(Resource):
    def get(self):
        umarell_dao.clean()
        cantiere_dao.clean()
        return None, 200

class UmarellId(Resource):
    def get(self, idumarell):
       return umarell_dao.getUmarell(idumarell)
    
    def post(self, idumarell):      
        return umarell_dao.addUmarell(idumarell, request.json)

class CantiereId(Resource):
    def get(self, idcantiere):
       return cantiere_dao.getCantiere(idcantiere)
    
    def post(self, idcantiere):      
        return cantiere_dao.addCantiere(idcantiere, request.json)