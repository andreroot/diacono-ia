import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from diacono_categ.schemas import Transacao

from dotenv import load_dotenv
from diacono_categ.extractor import extrair_nome

load_dotenv()

def load_prompt():
    prompt = """
    Você é um assistente que deve classificar e categorizar estbalecimentos, ao receber a informação do nome
    fantasia do estabelecimento. 
    A classificação deve ser feita com base da listagem de categorias fornecida.

    Categorias possíveis:
    - farmacia
    - mercado
    - padaria
    - alimentacao
    - banco
    - posto
    - servicos

    Transação: {texto}

    Responda apenas com o nome da categoria, mas, caso não se encaixe retorno o texto original.
    """
    prompt = ChatPromptTemplate.from_template(prompt)
    return prompt

def load_llm():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return llm


def classificar_com_ia(texto: str) -> str:
    
    texto = extrair_nome(texto)

    prompt = load_prompt()
    llm = load_llm()
    
    chain = prompt | llm
    return chain.invoke({"texto": texto}).content.strip()