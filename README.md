# Análise de Imóveis em Samambaia - DF

Este projeto realiza uma análise automatizada de imóveis à venda em Samambaia (Distrito Federal), utilizando técnicas de **web scraping**, **geolocalização**, **limpeza de dados** e **regressão estatística** para entender os principais fatores que influenciam o preço dos imóveis na região.

---

## Objetivo

Extrair dados de imóveis do site [DF Imóveis](https://www.dfimoveis.com.br), geocodificar os endereços, calcular distâncias até estações de metrô, tratar e transformar os dados, e aplicar regressão linear múltipla para identificar as variáveis que mais impactam o valor dos imóveis.

---

## Tecnologias Utilizadas

- **Python**
- **Selenium** – Automação de navegador para coleta de dados
- **Pandas & NumPy** – Manipulação e análise de dados
- **Geopy** – Cálculo de distâncias geográficas
- **Statsmodels** – Modelagem estatística e regressão
- **Matplotlib & Seaborn** – Visualizações gráficas
- **Requests** – Geocodificação via API Nominatim (OpenStreetMap)

---

## Etapas do Processo

### 1. Coleta de Dados (Web Scraping)
- Acessa o site DF Imóveis via Selenium  
- Realiza busca por apartamentos à venda em Samambaia  
- Extrai informações como endereço, preço, metragem e número de quartos  

### 2. Limpeza e Padronização
- Converte preços e metragem para valores numéricos  
- Padroniza os endereços e remove duplicatas  
- Salva os dados tratados em arquivo CSV  

### 3. Geocodificação
- Utiliza a API Nominatim para obter latitude e longitude dos imóveis  
- Calcula a menor distância até as estações de metrô de Samambaia  

### 4. Tratamento Estatístico
- Remove outliers de preço com base no intervalo interquartil (IQR)  
- Exclui imóveis com mais de 5 quartos ou com preço acima de R$ 3 milhões  
- Aplica transformações logarítmicas para normalizar variáveis  

### 5. Análise Estatística
- Aplica regressão linear múltipla para prever o preço com base em:
  - Metragem  
  - Número de quartos  
  - Distância até o metrô  
- Avalia multicolinearidade entre variáveis explicativas usando VIF (Variance Inflation Factor)

---

## Colaboradores
Isabella Aguiar   ()

Liz de Albuquerque ()
