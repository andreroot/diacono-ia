# Diacono-IA

Primeiro lib usando recursos IA - openia

- diacono-categ: recebe um texto e categoriza uma tipagem, que sera alimentada com uma listagem de categoria.

instalação do pacote: 
> pip install git+https://github.com/andreroot/diacono-ia.git

python-test:
```
    from diacono_categ.agent import classificar_com_ia

    if __name__ == "__main__":
        print("Classificando transação...")

        # lista fake
        lista=['ELECTRON MINI EXTRA-51502','ELECTRON FRIGOMUNDO C1502','ELECTRON FDI FERNAO D1502','ELECTRON NSAI POSTO D1602','ELECTRON DROGARIA SAO1602','ELECTRON RP SERVICOS 1702','ELECTRON RP SERVICOS 1702','ELECTRON IvoneteMaria1702']

        categoria = [classificar_com_ia(l) for l in lista]
        lista_dict = [[ item['original'], item['categoria']] for item in categoria]
        print(lista_dict)
```

Criar um arquivo .env e colocar o token do OpenIA

Recebe uma lista de texto e retorna um json com modelo validado pydantic que pode ser convertido para outros tipos de objeto

Alimentado via json - listagem de categorias 
Aplicação de regras de exceção via json - regras de categorias add novas regras

* mudar a forma de incluir novas regras