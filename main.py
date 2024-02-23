from flask import Flask, render_template, request
from wtforms import Form, IntegerField, SelectMultipleField, SubmitField, validators
from flask_restful import Api
from api import UmarellId, CantiereId, Clean
from umarell_gcp import Umarell
from cantiere_gcp import Cantiere

umarell_dao = Umarell()
cantiere_dao = Cantiere()

app = Flask(__name__,
            static_url_path='/static', 
            static_folder='static')

api = Api(app)
basePath = '/api/v1'

class SearchForm(Form):
    cap = IntegerField('CAP', [validators.input_required()])
    choice = SelectMultipleField('Cosa cercare', choices=[('um', 'Umarell'), ('ca', 'Cantieri')])
    submit= SubmitField('Submit')

# Create object to encapsulate model (for form)
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

api.add_resource(UmarellId, f'{basePath}/umarell/<int:idumarell>')
api.add_resource(CantiereId, f'{basePath}/cantiere/<int:idcantiere>')
api.add_resource(Clean, f'{basePath}/clean')

@app.route('/', methods=['GET', 'POST'])
def index():
    cantieri = []
    umarell = []
    cap = -1
    msg = ''

    if request.method == 'POST':
        form = SearchForm(request.form)
        cap = form.cap.data
        print(f"cap {cap}, choice {form.choice.data}")

        if 'um' in form.choice.data:
            umarell = umarell_dao.search(cap)
        if 'ca' in form.choice.data:
            cantieri = cantiere_dao.search(cap)

        if not form.choice.data:
            msg = 'Nessuna opzione selezionata!'
        elif not cantieri and not umarell:
            msg = 'Nessun risultato trovato!'

        print(f"cantieri: {cantieri}")
        print(f"umarell: {umarell}")

    return render_template('index.html', form=SearchForm(obj=Struct(**{'cap': '', 'choice': ''})), umarell=umarell, cantieri=cantieri, cap=cap, msg=msg), 200

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', path=request.path), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
