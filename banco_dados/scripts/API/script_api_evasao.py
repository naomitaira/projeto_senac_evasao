import requests
import pandas as pd
import datetime

url_api = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
response = requests.get(url_api)

print("--------------------------------------------")

print("Status:", response.status_code)

if response.status_code == 200:
    print("\nOperacao bem sucedida\n")
else:
    print("\nDeu algum erro na operacao\n")

print("--------------------------------------------")

result = response.json()

# validar status da api antes de iterar
try: 
    requests.get(url_api).raise_for_status()

except:
    print("Erro ao acessar a API")
    exit()

for i in result:
    print(i["sigla"], "-", i["nome"], "-", i["regiao"]["nome"])


#exemplo de autenticacao

headers = {"Authorization" : "Bearer MEU_TOKEN"}

response = requests.get(url_api, headers=headers)


# # transformar resposta em Data Frame e normalizar os dados

# df = pd.json_normalize(result)

# # Modificar o formato de data para "dia-mes-ano e hora:minuto:segundo"

# df["inicio_operacao"] = pd.to_datetime(df["inicio_operacao"]).dt.strftime("%d-%m-%Y %H:%M:%S")

# # remover as colunas nome reduzido e modalidade_participacao

# df = df.drop(columns=["nome_reduzido", "modalidade_participacao"])

# # formatar o cnpj para ficar mais legivel, no formato "XX.XXX.XXX/XXXX-XX"

# df["cnpj"] = df["cnpj"].str[:2] + "." + df["cnpj"].str[2:5] + "." + df["cnpj"].str[5:8] + "/" + df["cnpj"].str[8:12] + "-" + df["cnpj"].str[12:]

# # filtrar os participantes que possuem o nome banco 

# df["nome"] = df["nome"].str.capitalize()

# filtro_bancos = print(df[df["nome"].str.startswith("Banco")])

# # transformar o Data Frame em arquivo CSV

# df.to_csv("pix.csv", index=False)

# # checar se o arquivo foi criado com sucesso

# print("Operação completa!")