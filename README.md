# Diacono-IA

Primeiro lib usando recursos IA

- diacono-categ: recebe um texto e categoriza uma tipagem, que sera alimentada com uma listagem de categoria.

instalação do pacote: 
> pip install git+https://github.com/andreroot/diacono-ia.git

python-test:
```
    from diacono_categ.agent import classificar_com_ia

    if __name__ == "__main__":
        print("Classificando transação...")
        lista=['ELECTRON MINI EXTRA-51502','ELECTRON FRIGOMUNDO C1502','ELECTRON FDI FERNAO D1502','ELECTRON NSAI POSTO D1602','ELECTRON DROGARIA SAO1602','ELECTRON RP SERVICOS 1702','ELECTRON RP SERVICOS 1702','ELECTRON IvoneteMaria1702']
        categoria = [classificar_com_ia(l) for l in lista]
        print(categoria)
```
