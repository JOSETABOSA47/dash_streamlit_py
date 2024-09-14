import streamlit as st
import pandas as pd
import numpy as np
import http.client
import json

from streamlit_card import card

# st.title(':orange[VENDAS DE HOJE NO BLING]')
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: #7f4307;
    }
    </style>
    <h1 class="title">VENDAS DE HOJE NO BLING</h1>
    """,
    unsafe_allow_html=True
)

conn_mamoeiroce = http.client.HTTPSConnection("api.bling.com.br")
payload = ''
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer 31fbc75b555ef5b18d19c1938ef6d8a1476b0c9d',
  'Cookie': 'PHPSESSID=qv71pbm1mutnjkint5g7dtte6p'
}
conn_mamoeiroce.request("GET", "/Api/v3/pedidos/vendas?pagina=1&limite=100", payload, headers)
res = conn_mamoeiroce.getresponse()
databling_mamoeiroce = json.loads(res.read())
conn_mamoeiroce.close()
totalvendas_mamoeiroce = 0
for tem_mamoeiroce in databling_mamoeiroce["data"]:
    totalvendas_mamoeiroce = totalvendas_mamoeiroce + tem_mamoeiroce["total"]

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



# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#             'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# @st.cache_data
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

# data_load_state = st.text('Loading data...')
# data = load_data(10000)
# data_load_state.text("Done! (using st.cache_data)")

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(databling_mamoeiroce)

# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# # Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)