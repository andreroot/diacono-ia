import re
import unicodedata

def normalizar(texto: str) -> str:
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

def extrair_nome(texto: str) -> str:
    texto = texto.replace("ELECTRON", "").strip()
    texto = re.sub(r"\d{4}$", "", texto).strip()
    texto = re.sub(r"[^a-zA-Z\s]", "", texto)
    return normalizar(texto).strip()