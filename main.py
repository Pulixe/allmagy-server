from flask import Flask, request
from newspaper import Article
from flask_restful import Api, Resource
from transformers  import pipeline
import chatbot
import json
import os

apikey = "000000abc1234ABC"

app = Flask(__name__)
api = Api(app)

nlp = pipeline(
    'question-answering',
    model='mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es',
    tokenizer=(
        'mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es',
        {"use_fast": False}
    )
)


class Bert(Resource):
    @staticmethod
    def post():
        y = request.get_json()
        if y["apikey"] == apikey:
            article = Article(y["url"], language="es")
            article.download()
            article.parse()
            contexto = article.text
            answer = nlp({'question':y["question"], 'context':contexto})
            out = {'Prediction': answer['answer'] }
            return out, 201
        else:
            return "{'msg':'error este no es el origen'", 404

class Bot(Resource):
    @staticmethod
    def post():
        data = request.get_json()
        if data['msg'] != " ":
            message = data['msg']
            bot = chatbot.chatbot_response(message)
            resp = {'msg': str(bot)}
            return resp , 200
        else:
            return "{'msg':'error no hay mensaje'}"



api.add_resource(Bert,  '/api/v1/bert')

api.add_resource(Bot, '/api/v1/chatbot')

if __name__ == '__main__':
    app.run(threaded=False)
    
