import pandas as pd
import lxml.html as LH
import requests
from unidecode import unidecode 


def get_state_info(file_path, state_name):
    state_file = open(file_path, 'rb').read()
    state_content = LH.fromstring(state_file)

    citys = [
    c.split("('")[1].split("')")[0]
    for c in state_content.xpath('//tr/td/a/@href')
    ]

    base_info = state_content.xpath('//input/@*[name()="name" or name()="value"]')
    info = {
      base_info[i]: base_info[i+1]
      for i in range(0, len(base_info)-1)
    }
    info['NOME_ESTADO'] = state_name
    return info, citys


def get_city_data(city, info, hierarquia_map):
    cod_city, name_city = city.split("*")
    url = 'http://preco.anp.gov.br/include/Relatorio_Excel_Semanal_Posto.asp'
    form_data = { 
    "DESC_MUNICIPIO": name_city,
    "COD_MUNICIPIO": cod_city,
    "DESC_COMBUSTIVEL": info['desc_combustivel'],
    "COD_COMBUSTIVEL": info['cod_combustivel'],
    "DESC_SEMANA": info['desc_semana'],
    "COD_SEMANA": info['cod_semana'],
    "COD_ESTADO": info['COD_ESTADO']
    }

    # Made request
    name_city = unidecode(name_city).lower().replace('@', ' ')
    data = requests.post(url, data = form_data)
    df_city = pd.read_html(data.text, decimal=',', thousands='.')[1]
    df_city.columns = df_city.columns.droplevel(0)
    df_city['CIDADE'] = name_city
    df_city['COD_CIDADE'] = cod_city
    df_city['ESTADO'] = info['NOME_ESTADO']
    df_city['COD_ESTADO'] = info['COD_ESTADO']
    df_city['REGIÂO_ESTADO'] = hierarquia_map.loc[name_city]['hierarquia']
    return df_city


def load_hierarquia(file_path):
    df = ( 
        pd
        .read_html(file_path)
        [0]
        .rename(columns={'Municípios':'cidade', 'Gentílico':'gentilico', 'Hierarquia urbana':'hierarquia'})
        .assign(cidade=lambda x: x['cidade'].apply(unidecode).str.lower())
        .set_index('cidade')
        .iloc[:-1,:]
    )
    return df


def generate_state_data(state_name, anp_file_path, hierarquia_file_path):
    info, citys = get_state_info(anp_file_path, state_name)
    hierarquia_map = load_hierarquia(hierarquia_file_path)
    dfs = []
    print(f"=========={state_name}============")
    for city in citys:
      print(f"Loading city {city.split('*')[1]}")
      dfs.append(get_city_data(city, info, hierarquia_map))

    df = pd.concat(dfs)
    df.to_csv(f"data/anp_{state_name.lower()}_data.csv")
    print(df.head())
    print(f"========> Successfully extract data from {state_name} to data/anp_{state_name.lower()}_data.csv")


if __name__ == "__main__":
    state_name = "Bahia"
    anp_file_path = "data/anp_bahia.html"
    hierarquia_file_path = "data/hierarquia_bahia.html"
    generate_state_data(state_name, anp_file_path, hierarquia_file_path)

