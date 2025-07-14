import streamlit as st
import requests
import pandas as pd
import json

#def predict_emprestimo(df):
#    url = 'https://hungry-loraine-jadsonds-543d1ebd.koyeb.app/empresa/predict '
#    header = {'Content-type': 'application/json'}
#
#    data = json.dumps(df.to_dict(orient='records'))  # ✅ Agora está certo!
#
#    r = requests.post(url, data=data, headers=header)
#    prediction = r.json()[0]['prediction']
#    return prediction
def predict_emprestimo(df):
    url = 'https://pretty-verine-jadsonds-15d5f595.koyeb.app/empresa/predict'
    headers = {'Content-type': 'application/json'}

    # Converte o DataFrame para JSON
    data = json.dumps(df.to_dict(orient='records'))

    # Faz a requisição
    r = requests.post(url, data=data, headers=headers)

    # Verifica se a resposta foi bem-sucedida
    if r.status_code == 200:
        try:
            # Tenta converter a resposta para JSON
            response_json = r.json()
            prediction = response_json[0]['prediction']
            return prediction
        except ValueError:
            # Se não conseguir converter para JSON
            st.error("Erro: A resposta da API não é um JSON válido.")
            st.write("Resposta bruta da API:", r.text)
            return None
    else:
        # Se a resposta não foi 200 OK
        st.error(f"Erro na API: Código {r.status_code}")
        st.write("Resposta bruta da API:", r.text)
        return None
    
st.set_page_config(
    layout='wide',
    page_title='Previsão deInadimplência'
)

st.title('Previsão de Inadimplência')

col1, col2, col3, col4 = st.columns(4)

with col1:
    idade = st.number_input('Insira a Idade do Cliente')

with col2:
    renda = st.number_input('Insira a Renda do Cliente')

with col3:
    tempo_emprego = st.number_input('Insira o tempo de emprego do Cliente')

with col4:
    valor_emprestimo = st.number_input('Insira o valor do empréstimo')

col5, col6, col7, col8 = st.columns(4)

with col5:
    taxa_juros_emprestimo = st.number_input('Insira a Taxa de Juros')

with col6:
    relacao_emprestimo_renda = st.number_input('Insira a relação emprestimo renda')

with col7:
    historico_credito = st.number_input('Insira o histórico de Crédito')

with col8:
    posse_casa = st.selectbox('Insira a posse de casa',(['RENT', 'OWN', 'MORTGAGE', 'OTHER']))

col9, col10, col11 = st.columns(3)

with col9:
    finalidade_emprestimo = st.selectbox('Insira a Finalidade do Empréstimo', (['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOMEIMPROVEMENT', 'DEBTCONSOLIDATION']))

with col10:
    grau_risco_emprestimo = st.selectbox('Insira o Grau do Risco do Empréstimo', (['D', 'B', 'C', 'A', 'E', 'F', 'G']))

with col11:
    registro_inadimplencia = st.selectbox('Insira o registro de inadimplência', (['Y', 'N']))

dict_data = {
    'idade': int(idade),
    'renda': int(renda),
    'tempo_emprego': int(tempo_emprego),
    'valor_emprestimo': int(valor_emprestimo),
    'taxa_juros_emprestimo': float(taxa_juros_emprestimo),
    'relacao_emprestimo_renda': float(relacao_emprestimo_renda),
    'historico_credito': int(historico_credito),
    'posse_casa': posse_casa,
    'finalidade_emprestimo': finalidade_emprestimo,
    'registro_inadimplencia': registro_inadimplencia,
    'grau_risco_emprestimo': grau_risco_emprestimo
}

df = pd.DataFrame([dict_data])
data = json.dumps(df.to_dict(orient='records'))

if st.button('Fazer Previsão'):
    with st.spinner('Nosso Modelo de Inteligência Artificial está analisando os dados...'):
        previsao = predict_emprestimo(df)
        if previsao != 0:
            st.markdown("<h4 style='color:red;'>Nosso Modelo de Inteligência Artificial recomenda não disponibilizar crédito para este cliente, pois ele possue uma alta probabilidade de não pagar o empréstimo.</h4>", unsafe_allow_html=True)
        else:
            st.markdown("<h4 style='color:green;'>Nosso Modelo de Inteligência Artificial recomenda disponibilizar crédito para este cliente.</h4>", unsafe_allow_html=True)