from flask import Flask, render_template, request
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/',  methods=['GET']) 
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():

    #Leitura de valores vindo do formulário
    original_text = request.form['text']
    target_language = request.form['language']

    #Lê as variáveis ambientais criadas no arquivo .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']


    #Cria o caminho necessário para chamar o serviço de Tradução
    path = '/translate?api-version=3.0'
    target_language_parameter = '&to=' + target_language

    #Cria as informações de cabeçalho
    constructed_url = endpoint + path + target_language_parameter

    #Set do cabeçalho de informações
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    #Cria o corpo da solicitação, ou seja o texto a ser traduzido
    body = [{ 'text': original_text }]

    """Chama post em requests para chamar o serviço de Tradução

       Obs: é possível usar uma das duas linhas de código (a comentada e a fora do comentário) apresentadas abaixo, para a request dentro do post
       translator_request = requests.request('POST', constructed_url, headers=headers, json=body)
    """
    translator_request = requests.post(constructed_url, headers=headers, json=body)

 
    #Recupera a resposta JSON do servidor
    translator_response = translator_request.json()

    #Recupera o texto traduzido
    translated_text = translator_response[0]['translations'][0]['text']

    #Chama render_template para exibir a resposta em outra página
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )

if __name__ == '__main__': 
   app.run(debug = True) 