import random
import datetime
from locate import search_local
dialogue_state = {
    'name': None,
    'location': None,
    'date': None,
}

def verify_name(ner_classifier, text, type='Pessoa'):
    entities = ner_classifier(text)
    names = []
    for entity in entities:
        if entity['entity'] == f'B-{type}' or entity['entity'] == f'I-{type}':
            names.append(entity)
    
    if names:
        complete_name = ""
        ultimo_end = -1
        for ent in names:
            if ent['word'].startswith('##'):
                complete_name += ent['word'][2:]
            else:
                if ent['start'] >= ultimo_end + 1:
                    complete_name += ' '
                complete_name += ent['word']
            ultimo_end = ent['end']

        complete_name = complete_name.replace('##', '')
        return complete_name
    return False

def name_pipeline(intent, ner_classifier, text, df):
    name = False
    if dialogue_state['name']:
        name = dialogue_state['name']
    else:
        name = verify_name(ner_classifier,text, "Pessoa")
    if name:
        dialogue_state['name'] = name
        df_responses = df[['responses', 'intent']]
        responses=df_responses.explode('responses')
        responses=responses[responses['intent']==intent]
        responses = responses.reset_index()
        response=responses.iloc[random.randint(0, len(responses)-1)]['responses']
        response = response.replace('<HUMANO>', name)
        print("Bot: ", response)
    else:
        print("Bot: Não entendi seu nome, poderia repetir?")

def date_pipeline(intent, ner_classifier, text, df):
    date = False
    if dialogue_state['date']:
        date = dialogue_state['date']
    else:
        date = verify_name(ner_classifier,text, "Data")
    if date:
        dialogue_state['date'] = date
        df_responses = df[['responses', 'intent']]
        responses=df_responses.explode('responses')
        responses=responses[responses['intent']==intent]
        response=responses.iloc[random.randint(0, len(responses)-1)]['responses']
        response = response.replace('<HORARIO_DATA>', date)
        print("Bot: ", response)
    else:
        print("Bot: Não entendi a data, poderia repetir?")
        
def local_pipeline(intent, ner_classifier, text, df):
    local = False
    if dialogue_state['location']:
        local = dialogue_state['location']
    else:
        local_lower = text.lower()
        tem_bairro = 'bairro' in local_lower
        tem_rua = 'rua' in local_lower
        if tem_bairro and tem_rua:
            local = verify_name(ner_classifier,text, "Local")
            if local:
                local = search_local(text)
                print(local)
                if local['places']:
                    local_url = local['places'][0]['googleMapsUri']
                    print("Bot: O link pra url google maps", local_url)
        else:
            print("Bot: Você não informou a localização corretamente, poderia informar o bairro e a rua?")
            return
    
    if local:
        dialogue_state['location'] = local
        df_responses = df[['responses', 'intent']]
        responses=df_responses.explode('responses')
        responses=responses[responses['intent']==intent]
        response=responses.iloc[random.randint(0, len(responses)-1)]['responses']
        response = response.replace('<LOCALIZACAO>', local)
        print("Bot: ", response)
    else:
        print("Bot: Não entendi a localização, poderia repetir?")
                     
def match_case(x,ner_classifier,text,df):
    match x:
        case "RespostaSaudação":
            name_pipeline(x, ner_classifier, text, df)
        case "RespostaSaudaçãoCortesia":
            name_pipeline(x, ner_classifier, text, df)
        case "ConsultaHumanoAtual":
            if dialogue_state['name']:
                df_responses = df[['responses', 'intent']]
                responses=df_responses.explode('responses')
                responses=responses[responses['intent']==x]
                response=responses.iloc[random.randint(0, len(responses)-1)]['responses']
                response = response.replace('<HUMANO>', dialogue_state['name'])
                print("Bot: ", response)
            else:
                print("Bot: Você não informou seu nome, poderia repetir?")
        case "QuemSouEu":
            if dialogue_state['name']: 
                df_responses = df[['responses', 'intent']]
                responses=df_responses.explode('responses')
                responses=responses[responses['intent']==x]
                response=responses.iloc[random.randint(0, len(responses)-1)]['responses']
                response = response.replace('<HUMANO>', dialogue_state['name'])
                print("Bot: ", response)
        case "ConsultaHora":
            df_responses = df[['responses', 'intent']]
            responses=df_responses.explode('responses')
            responses=responses[responses['intent']==x]
            response=responses.iloc[random.randint(0, len(responses)-1)]['responses']
            # get hour
            hour = datetime.datetime.now().strftime('%H:%M')
            response = response.replace('%%TIME%%', hour)
            print("Bot: ", response)
        case "PedidoDeAjuda":
            df_responses = df[['responses', 'intent']]
            responses=df_responses.explode('responses')
            responses=responses[responses['intent']==x]
            response=responses.iloc[random.randint(0, len(responses)-1)]['responses']
            print("Bot: ", response)
            print("Bot: Você pode me perguntar sobre a hora, fazer uma denúncia, pedir uma piada ou fofocar comigo.")
        case "FazerDenuncia":
            df_responses = df[['responses', 'intent']]
            responses=df_responses.explode('responses')
            responses=responses[responses['intent']==x]
            response=responses.iloc[random.randint(0, len(responses)-1)]['responses']
            print("Bot: ", response)
            print("Bot:  Me informe a data do acontecimento")
        
        case "InformacaoDeHorarioData":
            date_pipeline(x, ner_classifier, text, df)
        case "RecebimentoDeLocalizacao":
            local_pipeline(x, ner_classifier, text, df)
        case "AnuncioDeMedoOuPerigo":
            if dialogue_state['location']:
                df_responses = df[['responses', 'intent']]
                responses=df_responses.explode('responses')
                responses=responses[responses['intent']==x]
                response=responses.iloc[random.randint(0, len(responses)-1)]['responses']
                response = response.replace('%%LOCALIZACAO%%', dialogue_state['location'])
            else:
                print("Bot: Iremos enviar ajuda para sua localização")
                print("Bot: Mas você não informou a localização corretamente, poderia informar o bairro e a rua?")
                
        case "ConsultaUltimosIntents":
            return "ConsultaUltimosIntents"
        case "ConsultaDialogueState":
            if dialogue_state['name']:
                df_responses = df[['responses', 'intent']]
                responses=df_responses.explode('responses')
                responses=responses[responses['intent']==x]
                response=responses.iloc[random.randint(0, len(responses)-1)]['responses']
                print("Bot:  ", dialogue_state)
            else:
                print("Bot: Não temos informações sobre o estado do diálogo")
        case _:
            df_responses = df[['responses', 'intent']]
            responses=df_responses.explode('responses')
            responses=responses[responses['intent']==x]
            if(len(responses)):
                response=responses.iloc[random.randint(0, len(responses)-1)]['responses']
                print("Bot: ", response)
            else:
                print("Bot: Desculpe, não entendi o que você disse. Pode falar resumidamente e de forma clara?")
     