import re
import unicodedata

def normalizar(texto: str) -> str:
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

def extrair_nome(texto: str) -> str:
    for palavra in ("ELECTRON", "PIX"):
        texto = texto.replace(palavra, "").strip()
    texto = re.sub(r"\d{4}$", "", texto).strip()
    texto = re.sub(r"[^a-zA-Z\s]", "", texto)
    return normalizar(texto).strip()