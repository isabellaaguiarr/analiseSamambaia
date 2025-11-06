from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from geopy.distance import geodesic
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt 
import statsmodels.api as sm
import seaborn as sns
import pandas as pd
import numpy as np
import requests
import re 

# PARTE 1 - Pegando os dados (web scraping)
options = Options() 
url = 'https://www.dfimoveis.com.br/'
driver = webdriver.Chrome(options=options)
driver.get(url)
wait = WebDriverWait(driver, 10)

# Parametros de busca
opcao_modelo = "VENDA"
opcao_imovel = "APARTAMENTO"
# opcao_imovel = "CASA"
opcao_estado = "DF"
opcao_cidade = "SAMAMBAIA"
# opcao_bairro = "TODOS"
# opcao_quarto = "QUARTO (TODOS)"


# Compra ou venda 
xpath = "/html/body/main/section[1]/div[1]/div[1]/form/div[1]/span[1]/span[1]/span"
element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
element.click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'select2-search__field')))
element.send_keys(opcao_modelo)
element.send_keys(Keys.ENTER)

# Casa ou apartamento 
xpath = "/html/body/main/section[1]/div[1]/div[1]/form/div[1]/span[2]/span[1]/span"
element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
element.click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'select2-search__field')))
element.send_keys(opcao_imovel)
element.send_keys(Keys.ENTER)

# Estado  
xpath = "/html/body/main/section[1]/div[1]/div[1]/form/div[1]/span[3]/span[1]/span"
element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
element.click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'select2-search__field')))
element.send_keys(opcao_estado)
element.send_keys(Keys.ENTER)

# Cidade  
xpath = "/html/body/main/section[1]/div[1]/div[1]/form/div[1]/span[4]/span[1]/span"
element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
element.click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'select2-search__field')))
element.send_keys(opcao_cidade)
element.send_keys(Keys.ENTER)

# # Bairro  
# xpath = "/html/body/main/section[1]/div[1]/div[1]/form/div[1]/span[5]/span[1]/span"
# element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
# element.click()
# element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'select2-search__field')))
# element.send_keys(opcao_bairro)
# element.send_keys(Keys.ENTER)

# # Quartos por ID
# element = wait.until(EC.element_to_be_clickable((By.ID, 'select2-quartos-container')))
# element.click()
# opcoesQuartos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'select2-results__option')))
# for opcao in opcoesQuartos:
#     if opcao.text.strip() == opcao_quarto:  
#         opcao.click()
#         break

# Realiza busca por ID
botao_busca = wait.until(EC.element_to_be_clickable((By.ID,"botaoDeBusca")))
botao_busca.click()

lst_imoveis = []   # Lista para armazenar os imoveis

# Resultados por ID 
while True:
    resultado = wait.until(EC.presence_of_element_located((By.ID, "resultadoDaBuscaDeImoveis")))
    elementos = resultado.find_elements(By.TAG_NAME, 'a')

    for elem in elementos:
        try:
            endereco = elem.find_element(By.CLASS_NAME, 'ellipse-text').text
            preco = elem.find_element(By.CLASS_NAME, 'body-large.bold').text
            metragem = elem.find_element(By.CLASS_NAME, 'border-1').text
            try:
                quartos = elem.find_element(By.XPATH, './div[2]/div[2]/div[3]/div[2]').text
            except:
                quartos = ''
            try: 
                vaga = elem.find_element(By.XPATH, './div[2]/div[2]/div[3]').text
            except:
                vaga = ''
# Variavel vaga em boleana / se tiver 1 e nao 0 
            # Dicionario do imovel
            imovel = {
                'endereco': endereco,
                'preco': preco,
                'metragem': metragem,
                'quartos': quartos,
                'vaga': vaga,
            }

            lst_imoveis.append(imovel)

        except:
            continue


    botao_proximo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.btn.next')))
    if "disabled" in botao_proximo.get_attribute("class"):
        print("Última página alcançada.")
        break
    

    driver.execute_script("arguments[0].click();", botao_proximo)
    sleep(2)

driver.quit()   # Fechar o robo 
df = pd.DataFrame(lst_imoveis)

# PARTE 2 - Tratando os dados  
# Trasformando vaga em booleano 
df['vaga'] = df['vaga'].str.contains(r'\b1\s*VAGA\b|\bVAGA\b', flags=re.IGNORECASE, regex=True).astype(int)

# Convertendo o preco para numero
df["preco"] = pd.to_numeric(
    df["preco"].str.extract(r"(\d[\d\.,]*)")[0].str.replace(".", "").str.replace(",", "")
)
# Aparecer apenas a metragem 
df['metragem'] = df['metragem'].str.extract(r'(\d+)[^a-zA-Z]*')

# Aparecer apenas o numero de quartos 
df['quartos'] = df['quartos'].str.extract(r'(\d+)')

# Padronizando e completando os enderecos
df["endereco"] = df["endereco"].str.upper().str.strip()
df["endereco"] = df["endereco"].apply(
    lambda x: x if "SAMAMBAIA" in x else f"{x}, SAMAMBAIA SUL, SAMAMBAIA"
)

# Extraindo padroes validos de endereco
padrao_endereco = r"(Q[RN]\s?\d{3}(?:\s?CONJUNTO\s?\d+)?(?:,\s?SAMAMBAIA (?:SUL|NORTE), SAMAMBAIA)?)"
df["endereco"] = df["endereco"].str.extract(padrao_endereco)

# Removendo enderecos invalidos e ruidos
df = df.dropna(subset=["endereco"])
df["endereco"] = df["endereco"].str.replace(r",\s?\d+[\.,]?\d*", "", regex=True)

# Transformando espacos vazios em NaN
df.replace(r'^\s*$', np.nan, regex=True, inplace=True)

# Removendo duplicatas e ordenando por preco
df = df.drop_duplicates().sort_values(by="preco", ascending=False)

# Salvando em csv 
# df.to_csv("C:/Users/isabe/Documents/PROVA/analiseImoveis/dados/imoveis_samambaia.csv", index=False, encoding="utf-8")
df = pd.read_csv("C:/Users/isabe/Documents/PROVA/analiseImoveis/dados/imoveis_samambaia.csv")
print(df)

# PARTE 3 - Transformando os dados em coordenadas 
# Função de geocodificacao
def geocodificar_nominatim(endereco):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": endereco,
        "format": "json",
        "addressdetails": 1,
        "limit": 1,
        "countrycodes": "br"
    }
    headers = {"User-Agent": "ProjetoImoveisSamambaia/1.0"}
    try:
        resposta = requests.get(url, params=params, headers=headers).json()
        if resposta:
            lat = float(resposta[0]["lat"])
            lon = float(resposta[0]["lon"])
            print(f"Coordenadas consumidas com sucesso: {endereco}")
            return lat, lon
    except Exception as e:
        print(f"Erro ao geocodificar {endereco}: {e}")
    return None, None

# Aplicando geocodificacao (achando lat e lng)
df["lat"], df["lng"] = zip(*df["endereco"].apply(lambda x: geocodificar_nominatim(x)))
sleep(1)

# Filtrando imoveis com coordenadas validas
df_localizados = df.dropna(subset=["lat", "lng"]).copy()

# Coordenadas das estacoes de metro em Samambaia
estacoes_metro = {
    "Samambaia Sul": (-15.8755, -48.0601),
    "Terminal Samambaia": (-15.8902, -48.0636),
    "Furnas": (-15.8623, -48.0581),
}

# Funcao para calcular a distancia dos imoveis ate a estacao de metro
def menor_distancia_metro(coord):
    return min(geodesic(coord, estacao).km for estacao in estacoes_metro.values())

# Calculo de distancia
df_localizados["distancia_metro_km"] = df_localizados.apply(
    lambda row: menor_distancia_metro((row["lat"], row["lng"])), axis=1
)

# Salvando em csv
# df_localizados.to_csv("C:/Users/isabe/Documents/PROVA/analiseImoveis/dados/imoveis_samambaia_coordenadas.csv", index=False, encoding="utf-8")
df_localizados = pd.read_csv("C:/Users/isabe/Documents/PROVA/analiseImoveis/dados/imoveis_samambaia_coordenadas.csv")

# PARTE 4 - Limpeza de dados
# 1. Definindo as colunas relevantes para analise
colunas_modelo = ["metragem", "quartos", "distancia_metro_km", "preco", "vaga"]

# 2. Limpando novamente a base e convertendo os dados para o formato float
df_limpo = df_localizados[colunas_modelo + ["endereco", "lat", "lng"]].copy()

# 2.1 Convertendo as colunas numericas individualmente
df_limpo["metragem"] = pd.to_numeric(df_limpo["metragem"], errors="coerce")
df_limpo["quartos"] = pd.to_numeric(df_limpo["quartos"], errors="coerce")
df_limpo["distancia_metro_km"] = pd.to_numeric(df_limpo["distancia_metro_km"], errors="coerce")
df_limpo["preco"] = pd.to_numeric(df_limpo["preco"], errors="coerce")
df_limpo["vaga"] = pd.to_numeric(df_limpo["vaga"], errors="coerce")

# 3. Removendo outliers de preco usando IQR (quartis)
precos = df_limpo["preco"]
iqr = precos.quantile(0.75) - precos.quantile(0.25)
limite_inf = precos.quantile(0.25) - 1.5 * iqr
limite_sup = precos.quantile(0.75) + 1.5 * iqr
df_limpo = df_limpo[precos.between(limite_inf, limite_sup)]

# PARTE 5 - Transformacoes logaritmicas
# 1 Convertendo distancia de km para metros
df_limpo["distancia_metro_m"] = df_limpo["distancia_metro_km"] * 1000

# 1.1 Aplicando logaritmo natural (ln(1 + x)) na distancia em metros e no preco
df_limpo["ln_distancia_metro"] = np.log1p(df_limpo["distancia_metro_m"])
df_limpo["ln_preco"] = np.log1p(df_limpo["preco"])

# PARTE 6 – Analises e visualizacoes
# 1. Histograma da Distribuicao de Precos dos Imoveis
print("\nGerando Histograma: Distribuição de Preços dos Imóveis...")
plt.figure(figsize=(10, 6))
sns.histplot(data=df_limpo, x='preco', bins=30, kde=True, color='ForestGreen')
plt.title('Distribuição de Preços dos Imóveis em Samambaia')
plt.xlabel('Preço do Imóvel (R$)')
plt.ylabel('Contagem')
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. Boxplot por Faixas de Distancia 
df_limpo["faixa_distancia"] = pd.cut(df_limpo["distancia_metro_km"], bins=[0, 0.5, 1, 2, 5], labels=["<500m", "500m–1km", "1–2km", "2–5km"])
sns.boxplot(data=df_limpo, x="faixa_distancia", y="preco", color='ForestGreen')
plt.title("Distribuição de preços por faixa de distância ao metrô")
plt.xlabel("Faixa de distância ao metrô")
plt.ylabel("Preço do imóvel (R$)")
plt.grid(True)
plt.show()

# 3. Grafico de barras sobre preco medio por faixa de distancia
preco_medio_faixa = df_limpo.groupby("faixa_distancia")["preco"].mean().reset_index()
plt.figure(figsize=(8, 6))
sns.barplot(data=preco_medio_faixa, x="faixa_distancia", y="preco", palette="crest")
plt.title("Preço médio dos imóveis por faixa de distância ao metrô")
plt.xlabel("Faixa de distância ao metrô")
plt.ylabel("Preço médio do imóvel (R$)")
plt.grid(axis="y", alpha=0.7)
plt.tight_layout()
plt.show()

# 4. Regressao linear multipla
X = df_limpo[["metragem", "quartos", "vaga", "ln_distancia_metro"]]
y = df_limpo["ln_preco"]
X_const = sm.add_constant(X)
modelo_multiplo = sm.OLS(y, X_const).fit()
print("Regressão linear múltipla:")
print(modelo_multiplo.summary())

# 4.1 Regressao linear multipla (Multicolinearidade)
# Calcula o VIF para cada variavel 
X_vif = sm.add_constant(df_limpo[["metragem", "quartos", "vaga", "ln_distancia_metro"]])
vif = pd.DataFrame()
vif["Variável"] = X_vif.columns
vif["VIF"] = [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
print("Fatores de inflação de variância (VIF):")
print(vif)



