import pandas as pd
import numpy as np
import lxml.html as LH
import requests
import argparse


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


def get_city_data(city, info):
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
  data = requests.post(url, data = form_data)
  df_city = pd.read_html(data.text, decimal=',', thousands='.')[1]
  df_city.columns = df_city.columns.droplevel(0)
  df_city['CIDADE'] = name_city
  df_city['COD_CIDADE'] = cod_city
  df_city['ESTADO'] = info['NOME_ESTADO']
  df_city['COD_ESTADO'] = info['COD_ESTADO']

  return df_city


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("echo", help="echo the string you use here")
    args = parser.parse_args()
    print(args.echo)

    return

    state_name = "Bahia"
    file_path = "Bahia_cidades.html"
    info, citys = get_state_info(file_path, state_name)
    dfs = []
    for city in citys:
      print(f"Loading city {city.split('*')[1]}")
      dfs.append(get_city_data(city, info))

    df = pd.concat(dfs)
    df.to_csv("anp_data.csv")
    print(df.head())
    print(f"========> Successfully extract data from {state_name}") 

