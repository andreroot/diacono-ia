
import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from diacono_categ.schemas import Transacao
from dotenv import load_dotenv
from diacono_categ.extractor import extrair_nome

load_dotenv()

# Caminho absoluto para o depara.json
DEPARA_PATH = os.path.join(os.path.dirname(__file__), 'lista_categorias.json')
REGRAS_PATH = os.path.join(os.path.dirname(__file__), 'regras_categorias.json')

def consultar_regras(texto):
    try:
        with open(REGRAS_PATH, 'r', encoding='utf-8') as f:
            regras = json.load(f)
        for chave, categoria in regras.items():
            if chave.lower() in texto.lower():
                return categoria
    except Exception:
        pass
    return None
    
def carregar_categorias():
    with open(DEPARA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('tipo_custo', [])

def load_prompt(categorias):
    categorias_str = '\n'.join(f'- {cat}' for cat in categorias)

    # print(categorias_str)
    
    prompt = f"""
    Você é um assistente que deve classificar e categorizar estabelecimentos, ao receber a informação do nome
    fantasia do estabelecimento. 
    A classificação deve ser feita com base na listagem de categorias fornecida.

    Categorias possíveis:
    {categorias_str}

    Transação: {{texto}}

    Responda apenas com o nome da categoria, mas, caso não se encaixe, retorne o texto original.
    """
    prompt = ChatPromptTemplate.from_template(prompt)
    return prompt

def load_llm():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return llm


def classificar_com_ia(texto: str) -> str:
    
    # Consulta regras associativas primeiro
    categoria_regra = consultar_regras(texto)
    nome_extraido = extrair_nome(texto)
    if categoria_regra:
        transacao = Transacao(
            original=texto,
            nome_extraido=nome_extraido,
            categoria=categoria_regra
        )
    else:
        categorias = carregar_categorias()
        prompt = load_prompt(categorias)
        llm = load_llm()
        chain = prompt | llm
        categoria = chain.invoke({"texto": nome_extraido}).content.strip()
        transacao = Transacao(
            original=texto,
            nome_extraido=nome_extraido,
            categoria=categoria
        )
    return transacao.model_dump()