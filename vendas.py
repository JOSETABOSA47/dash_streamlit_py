import streamlit as st
import pandas as pd
import numpy as np
import http.client
import json
import time

from operator import sub
from datetime import datetime, date, timedelta
from streamlit_card import card

# Obtém a data e hora atual
data_hora_atual = datetime.now()
# Subtrair 3 horas usando timedelta
data_hora_modificada = data_hora_atual - timedelta(hours=3)
# Formatar a data e hora no formato desejado
data_formatada = data_hora_modificada.strftime("%d/%m/%Y %H:%M:%S")
dataatual = date.today()
dataantiga = sub(date.today(), timedelta(60))
# dataatual_api = f"{dataatual.day}/{dataatual.month}/{dataatual.year}"
dataatual_api = f"{dataatual.year}-{dataatual.month}-{dataatual.day}"
dataantiga_api = f"{dataantiga.day}/{dataantiga.month}/{dataantiga.year}"

# st.title(':orange[VENDAS DE HOJE NO BLING]')
# st.markdown(
#     """
#     <style>
#     .title {
#         text-align: center;
#         color: #7f4307;
#     }
#     </style>
#     <h1 class="title">VENDAS DE HOJE NO BLING</h1>
#     """,
#     unsafe_allow_html=True
# )

lista_pedidos_mamoeiroce = []
lista_produtos_mamoeiroce = []
totalvendas_mamoeiroce = 0

@st.cache_data
def load_data(nrows):
#     # data = pd.read_csv(DATA_URL, nrows=nrows)
#     # lowercase = lambda x: str(x).lower()
#     # data.rename(lowercase, axis='columns', inplace=True)
#     # data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])

    apimemoeiroce = f"/Api/v3/pedidos/vendas?pagina=1&limite=200&dataInicial={dataatual_api}"
    conn_mamoeiroce = http.client.HTTPSConnection("api.bling.com.br")
    payload = ''
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer 444c1e677ebe0e68b745144e48545e9017a5c4bb',
        'Cookie': 'PHPSESSID=5rduhjhej10cvkb8a6jgljkorv'
    }
    conn_mamoeiroce.request("GET", apimemoeiroce, payload, headers)
    res = conn_mamoeiroce.getresponse()
    databling_mamoeiroce = json.loads(res.read())
    conn_mamoeiroce.close()
    for tem_mamoeiroce in databling_mamoeiroce["data"]:
        # totalvendas_mamoeiroce = totalvendas_mamoeiroce + tem_mamoeiroce["total"]
        lista_pedidos_mamoeiroce.append(tem_mamoeiroce["id"])

    CONTA = 0
    for pedidos in lista_pedidos_mamoeiroce:
        CONTA = CONTA + 1
        print(pedidos)
        apipedidos= f"/Api/v3/pedidos/vendas/{pedidos}"
        conn_pedidos = http.client.HTTPSConnection("api.bling.com.br")
        payload = ''
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer 444c1e677ebe0e68b745144e48545e9017a5c4bb',
            'Cookie': 'PHPSESSID=5rduhjhej10cvkb8a6jgljkorv'
        }
        conn_pedidos.request("GET", apipedidos, payload, headers)
        res = conn_pedidos.getresponse()
        print(f"{CONTA} - STATUS - ", res.status, "E CONECÇÃO - ", res.reason)
        data_mamoeiroce = json.loads(res.read())
        conn_pedidos.close()
        time.sleep(0.5)

        try:
            for produtos in data_mamoeiroce["data"]["itens"]:
                print(produtos)
                lista_produtos_mamoeiroce.append(produtos)
        except:
            print("ERRRRRRROOOOOO ", pedidos)
            continue
        # print(data_mamoeiroce)
        # print(apipedidos)
        # break
    return lista_produtos_mamoeiroce

data_load_state = st.text('Carregando dados...')
data = load_data(10000)
data_load_state.text(f"ATUALIZAÇAO {data_formatada}")

for tem in lista_produtos_mamoeiroce:
    totalvendas_mamoeiroce = totalvendas_mamoeiroce + tem["valor"]

# Dados para gerar cartões
data_list = [
    {"title": "MAMOEIRO SP", "value": 12345.67},
    {"title": "MAMOEIRO CE", "value": totalvendas_mamoeiroce},
    {"title": "WEB GLAMOUR CE", "value": 23456.78},
    {"title": "LUCAS FREE SHOP SP", "value": 23456.78},
]

# Criar colunas dinamicamente
cols = st.columns(4)  # Supondo que você quer 3 colunas

for i, data in enumerate(data_list):
    formatted_value = format(f"{data['value']:,.2f}")
    with cols[i % 4]:  # Distribuir os cartões entre as colunas
        card(
            key=f"card_{i}",
            title=data["title"],
            text=formatted_value,
            styles={
                "card": {
                    "width": "120px",
                    "height": "80px",
                    "background-color": "#FFA500",  # Cor laranja
                    "color": "white",  # Cor do texto
                    "border-radius": "20px",  # Bordas arredondadas
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)"  # Sombra
                },
                "title": {
                    "font-size": "8px",  # Ajusta o tamanho do texto do título
                    "font-weight": "bold",  # Negrito (opcional)
                }
            }
        )


# Loop para exibir cada produto
for produto in lista_produtos_mamoeiroce:
    # Criar uma linha para cada produto
    col1, col2, col3 = st.columns([1, 3, 2])  # Ajuste a proporção das colunas conforme necessário
    
    with col1:
        # Exibir a imagem do produto
        st.image(f"https://midia.mamoeiro.com.br/{produto['codigo']}-1.jpg", width=100)
        
    with col2:
        # Exibir o nome e quantidade de vendas
        st.subheader(produto["descricao"])
        st.subheader(produto["codigo"])
        
    with col3:
        # Exibir o preço formatado
        st.write(" ")
        st.write(f"Quantidade: {produto['quantidade']}")
        st.write(f"Preço: R$ {produto['valor']:.2f}")
        st.write(f"MAMOEIRO CE")
    
    # Adicionar uma linha divisória entre os produtos (opcional)
    st.markdown("---")

