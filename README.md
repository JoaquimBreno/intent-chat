# Chatbot em Português com Reconhecimento de Intenção

Este projeto implementa um chatbot em Português que utiliza modelos de classificação BERT para reconhecimento de intenções e extrai entidades nomeadas (como nomes de pessoas, datas e localizações) das mensagens do usuário. O sistema é capaz de responder com base na intenção detectada e entidades extraídas.

## Pré-requisitos

Antes de rodar o chatbot, é necessário:

* Python 3.x instalado
* Bibliotecas `numpy`, `pandas`, `torch`, `transformers`, e `requests` instaladas. Você pode instalar todas as dependências necessárias utilizando o comando:
  ```python
  pip install -r requirements.txt
  ```
* Um modelo treinado BERT para classificação de intenções, salvo na pasta `checkpoints/`.
* Um arquivo JSON (`labels.json`) contendo as labels das intenções.
* Um arquivo JSON (`IntentPortuguese.json`) com as intenções e respostas do bot.

## Como executar

1. Clone ou baixe este repositório em seu sistema.
2. Garanta que todas as dependências listadas em "Pré-requisitos" estão instaladas.
3. Certifique-se de ter os arquivos necessários em `checkpoints/`, `data/labels.json`, e `data/IntentPortuguese.json`.
4. Execute o script da seguinte forma:

<pre><div class="mantine-Prism-root mantine-7c7vou" translate="no"><button class="mantine-UnstyledButton-root mantine-ActionIcon-root mantine-Prism-copy mantine-1iop4ht" type="button" aria-label="Copy code"><svg width="1rem" height="1rem" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 2V1H10V2H5ZM4.75 0C4.33579 0 4 0.335786 4 0.75V1H3.5C2.67157 1 2 1.67157 2 2.5V12.5C2 13.3284 2.67157 14 3.5 14H11.5C12.3284 14 13 13.3284 13 12.5V2.5C13 1.67157 12.3284 1 11.5 1H11V0.75C11 0.335786 10.6642 0 10.25 0H4.75ZM11 2V2.25C11 2.66421 10.6642 3 10.25 3H4.75C4.33579 3 4 2.66421 4 2.25V2H3.5C3.22386 2 3 2.22386 3 2.5V12.5C3 12.7761 3.22386 13 3.5 13H11.5C11.7761 13 12 12.7761 12 12.5V2.5C12 2.22386 11.7761 2 11.5 2H11Z" fill="currentColor" fill-rule="evenodd" clip-rule="evenodd"></path></svg></button><div class="mantine-ScrollArea-root mantine-Prism-scrollArea mantine-xa9bso" dir="ltr"><div data-radix-scroll-area-viewport="" class="mantine-b6zkvl mantine-ScrollArea-viewport"><div><pre class="mantine-1uy1lj2 mantine-Prism-code prism-code language-bash" dir="ltr"><div class="mantine-1wkdfe1 mantine-Prism-line token-line"><div class="mantine-1dq8pan mantine-Prism-lineContent"><span class="token plain">python src/chat.py -c </span><span class="token string">"checkpoints/model_best_val_loss.pth"</span><span class="token plain"> -l </span><span class="token string">"data/labels.json"</span><span class="token plain"> -d </span><span class="token string">"data/IntentPortuguese.json"</span></div></div></pre></div></div></div></div></pre>

Substitua `"checkpoints/model_best_val_loss.pth"` pelo caminho do seu arquivo de checkpoint do modelo BERT, se diferente.

5. Interaja com o chatbot através do terminal. Para encerrar a sessão, digite "quit".

## Funcionalidades

* **Classificação de intenções** : O chatbot analisa a intenção por trás da mensagem do usuário e responde de acordo.
* **Extracção de entidades nomeadas** : Identifica e processa entidades nomeadas como nomes, datas e locais nas mensagens do usuário.
* **Respostas Contextuais** : Baseado na intenção e entidades identificadas, o chatbot gera respostas adequadas ao contexto.

---

Este é apenas um exemplo básico e pode ser expandido de acordo com as especificidades e funcionalidades adicionais do seu projeto. Certifique-se de adaptar os caminhos dos arquivos e qualquer instrução de instalação conforme necessário.

# Entity recognition classes

"id2label": {

    "0": "O",

    "1": "B-Organizacao",

    "2": "I-Local",

    "3": "B-Local",

    "4": "B-Pessoa",

    "5": "I-Profissao",

    "6": "B-Profissao",

    "7": "B-Data",

    "8": "I-Data",

    "9": "I-Pessoa",

    "10": "I-Organizacao"

  },

B = BEGIN, I=INSIDE

[WikiNEuRal: Combined Neural and Knowledge-based Silver Data Creation for Multilingual NER](https://aclanthology.org/2021.findings-emnlp.215) (Tedeschi et al., Findings 2021)

Fábio Souza, Rodrigo Nogueira, Roberto Lotufo. "Portuguese Named Entity Recognition using BERT-CRF", *arXiv:1909.10649 [cs.CL]*, Sep 2019, revisado em Fev 2020. Disponível em: https://doi.org/10.48550/arXiv.1909.10649
