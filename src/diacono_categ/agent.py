from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from diacono_categ.schemas import Transacao
from dotenv import load_dotenv
from diacono_categ.extractor import extrair_nome
from diacono_categ.get_file_s3 import load_json_config

load_dotenv()

LISTA_CATEGORIAS_FILE = 'lista_categorias.json'
REGRAS_CATEGORIAS_FILE = 'regras_categorias.json'


def carregar_regras() -> dict:
    try:
        return load_json_config(REGRAS_CATEGORIAS_FILE)
    except Exception:
        return {}


def consultar_regras(texto: str, regras: dict) -> str | None:
    for chave, categoria in regras.items():
        if chave.lower() in texto.lower():
            return categoria
    return None


def carregar_categorias() -> list:
    data = load_json_config(LISTA_CATEGORIAS_FILE)
    return data.get('tipo_custo', [])


def load_prompt(categorias: list, regras: dict) -> ChatPromptTemplate:
    categorias_str = '\n'.join(f'- {cat}' for cat in categorias)
    regras_str = '\n'.join(f'  "{k}" -> {v}' for k, v in list(regras.items())[:30])

    prompt = f"""
    Você é um assistente que classifica estabelecimentos pelo nome fantasia.
    Use a lista de categorias abaixo para classificar. Caso não se encaixe exatamente,
    retorne a categoria mais equivalente.

    Categorias possíveis:
    {categorias_str}

    Para referência de nomenclatura, exemplos de regras já mapeadas:
    {regras_str}

    Transação: {{texto}}

    Responda apenas com o nome da categoria.
    """
    return ChatPromptTemplate.from_template(prompt)


def load_llm() -> ChatOpenAI:
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)


def classificar_com_ia(textos: list[str]) -> list[dict]:
    regras = carregar_regras()
    categorias = carregar_categorias()
    chain = load_prompt(categorias, regras) | load_llm()

    resultado = []
    for texto in textos:
        nome_extraido = extrair_nome(texto)
        categoria = consultar_regras(texto, regras)

        if not categoria:
            categoria = chain.invoke({"texto": nome_extraido}).content.strip()

        resultado.append(Transacao(
            original=texto,
            nome_extraido=nome_extraido,
            categoria=categoria
        ).model_dump())

    return resultado
