CATEGORIAS = {
    "farmacia": ["drogaria", "farmacia"],
    "mercado": ["mercado", "extra", "frigomundo"],
    "padaria": ["padaria"],
    "alimentacao": ["restaurante", "lanchonete"],
    "posto": ["posto","FDI FERNAO"],
    "banco": ["itau", "bradesco"],
    "servicos": ["servicos"]
}

def classificar(nome: str) -> str:
    nome = nome.lower()
    
    for categoria, palavras in CATEGORIAS.items():
        for palavra in palavras:
            if palavra in nome:
                return categoria
    
    return "outros"