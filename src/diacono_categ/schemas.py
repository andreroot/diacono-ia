from pydantic import BaseModel

class Transacao(BaseModel):
    original: str
    nome_extraido: str
    categoria: str