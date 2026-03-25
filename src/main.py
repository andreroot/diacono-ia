from diacono_categ.agent import classificar_com_ia

if __name__ == "__main__":
    print("Classificando transação...")
    lista=['PAGTO FINANC VEIC 01/48','PIX QRS MULTIDISPLA18/02','ELECTRON AdolfoOchsen1802','ELECTRON JULIO BUONO 1902','ELECTRON MP  ORIEL   2102','ELECTRON OrielPereira2102','ELECTRON MP ORIEL    2102','ELECTRON RosileneDaSi2102','ELECTRON CarlosDiyodi2102','ELECTRON VERA C VIEIR2102','ELECTRON KUNIKO KOHAK2102','ELECTRON RenanMoraesD2102','ELECTRON OrielPereira2802','ELECTRON MP PKF      2802','ELECTRON ArianaDias  2802','ELECTRON MP ORIEL    2802','ELECTRON LUIZ ANTONIO2802','PIX QRS TUNA PAGAME01/03','ELECTRON LUIZ ANTONIO0203','ELECTRON JulianeLimaD0203','ELECTRON LUIZ ANTONIO0503','ELECTRON MP IFECO    0603','ELECTRON CarlosDiyodi0703','ELECTRON LuizaDeFatim0703','ELECTRON MP PKF      0703','ELECTRON MP ORIEL    0703','ELECTRON LUIZ ANTONIO0703','ELECTRON LUIZ ANTONIO0703']
    categoria = [classificar_com_ia(l) for l in lista]
    print(categoria)

    # with open('saida.json', 'r', encoding='utf-8') as f:
    # dados = json.load(categoria)
    lista_dict = [[ item['original'], item['categoria']] for item in categoria]
    print(lista_dict)