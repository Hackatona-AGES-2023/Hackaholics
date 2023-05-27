from django.shortcuts import render
import openai
import json
from .models import Consultas

# Create your views here.

openai.api_key = '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'

def index(request):
    
    return render(request, "antiscam/index.html", {
        "answers":False
    })

def answer(request):
    if request.method=="POST":
        pergunta = request.POST["pergunta"]
        input_text = "O texto da frase seguinte é uma solicitação. Responda com sim ou não, esta mensagem contém algum caráter de urgência ?"  + pergunta
        response1 = openai.Completion.create(
        engine='text-davinci-003',
        prompt=input_text,
        max_tokens=5,
        )

        input_text2 = "O texto da frase seguinte é uma solicitação, digite 'sim' ou 'não' se ele menciona valores ou palavras similares. Considere por valores qualquer índicio de símbolo monetário ou números ou número escrito por extenso."+ pergunta
        response2 = openai.Completion.create(
        engine='text-davinci-003',
        prompt=input_text2,
        max_tokens=5,
        )
        input_text3 = 'O texto da frase seguinte é uma solicitação, responda com sim ou não se o texto contém solicitações de informações pessoais. Considere por menção pessoal qualquer menção a nome pessoal, endereço, email ou telefone. Responda com sim ou não'+ pergunta
        response3 = openai.Completion.create(
        engine='text-davinci-003',
        prompt=input_text3,
        max_tokens=5,
        )
        #input_text4 = "O texto da frase seguinte é uma solicitação. Este texto possui algum link, sim ou não? "+ pergunta
        input_text4 = "Este texto possui algum link ou intuito de mudar de página, sim ou não? "+ pergunta
        response4 = openai.Completion.create(
        engine='text-davinci-003',
        prompt=input_text4,
        max_tokens=5,
        )
        if str(response1).lower().find("sim") != -1:
            boolurge = True
        else:
            boolurge = False

        if str(response2).lower().find("sim") != -1:
            boolvalores = True
        else:
            boolvalores = False

        if str(response3).lower().find("sim") !=-1:
            boolpessoais = True
        else:
            boolpessoais = False

        if str(response4).lower().find("sim") != -1:
            boollink = True
        else:
            boollink = False

        words_link = ["clique","link", "http", "https", ".com", ".br", "saiba mais", "mostrar"]
        
        found_link_word = any(word in str(pergunta).lower() for word in words_link)
        if found_link_word == True:
            boollink = True
        
        consulta = Consultas.objects.create(
        text=request.POST["pergunta"],
        urgencia=response1["choices"][0]["text"],
        valores=response2["choices"][0]["text"],
        pessoal=response3["choices"][0]["text"],
        link=response4["choices"][0]["text"]
)
        return render(request, "antiscam/index.html", {
            "pergunta":pergunta,
            "answers":True,
            "urgencia":"Existe urgência: "+response1["choices"][0]["text"],
            "falavalores":"Existe solicitação de Valores: "+response2["choices"][0]["text"],
            "pedeinfo":"Existe solicitação de informações pessoais:"+response3["choices"][0]["text"],
            "temlink":"Existe um link nesta solicitação:"+response4["choices"][0]["text"],
            "boollink":boollink,
            "boolpessoais":boolpessoais,
            "boolvalores":boolvalores,
            "boolurge":boolurge,
        })



#{ "choices": [ { "finish_reason": "length", "index": 0, "logprobs": null, "text": "\n\nA capital da Fran\u00e7a \u00e9 Paris." } ], "created": 1685171579, "id": "cmpl-7KiOhDGdGnIfvFgyg2YmqCfEY0PBj", "model": "text-davinci-003", "object": "text_completion", "usage": { "completion_tokens": 10, "prompt_tokens": 8, "total_tokens": 18 } }
