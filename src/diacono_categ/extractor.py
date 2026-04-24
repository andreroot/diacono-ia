import re
import unicodedata

_PREFIXOS = r"(?:PIX TRANSF|ELECTRON|ELCSS)\s*"

def normalizar(texto: str) -> str:
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

def extrair_nome(texto: str) -> str:
    # remove prefixo e captura tudo até o primeiro dígito
    # cobre: "PIX TRANSF Ademar 02/03" e "ELECTRON BENETON PARK2103"
    match = re.search(r"(?:PIX TRANSF|ELECTRON|ELCSS)\s+([^\d]+)", texto)
    if match:
        return normalizar(match.group(1).strip())

    # fallback: corta no primeiro dígito
    texto = re.sub(_PREFIXOS, "", texto).strip()
    texto = re.split(r"\d", texto)[0]
    return normalizar(texto).strip()
