# Anp City Extract
Auxiliador para obter preço de combustivel para cada municipio em http://preco.anp.gov.br/include/Resumo_Por_Estado_Municipio.asp

# Como usar

1: Vá até a página de síntese dos preços praticados no estado que deseja analisar.
A pagina ficara no indereço indicado acima, porém deves configurar para
o estado e combustível de interesse.
2: Salve a página como html (Pode excluir a pasta de informação que vem junto)
3: Altere no código o `state_name` e o `file_path` para corresponder ao seu
caso de uso
4: Será salvo um arquivo `anp.data.csv` com os dados referentes ao estado

Tips:
Modifique o código para ler de todos os estados necessários e juntar todos
em um grande df (`dfs`). Gerando apenas um csv

