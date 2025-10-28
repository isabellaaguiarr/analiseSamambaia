# Análise de Imóveis em Samambaia - DF

Este projeto realiza uma análise automatizada de imóveis à venda em Samambaia (Distrito Federal), utilizando técnicas de web scraping, geolocalização, limpeza de dados e regressão estatística para entender os fatores que influenciam o preço dos imóveis.

## Objetivo

Extrair dados de imóveis do site [DF Imóveis](https://www.dfimoveis.com.br), geocodificar os endereços, calcular distâncias até estações de metrô, limpar e transformar os dados, e aplicar regressão linear múltipla para identificar variáveis que impactam o preço.

---

## Tecnologias Utilizadas

- **Python**
- **Selenium** – Automação de navegador para web scraping
- **Pandas & NumPy** – Manipulação e análise de dados
- **Geopy** – Cálculo de distâncias geográficas
- **Statsmodels** – Modelagem estatística e regressão
- **Matplotlib & Seaborn** – Visualizações
- **Requests** – Geocodificação via API Nominatim (OpenStreetMap)

---

## Estrutura do Projeto

analiseImoveis/
├── dados/
│   ├── imoveis_samambaia.csv
│   └── imoveis_samambaia_coordenadas.csv
├── main.py
└── README.md

---

## Etapas do Processo

### 1. Coleta de Dados (Web Scraping)
- Acessa o site DF Imóveis via Selenium  
- Realiza busca por apartamentos à venda em Samambaia  
- Extrai endereço, preço, metragem e número de quartos  

### 2. Limpeza e Padronização
- Converte preços e metragem para valores numéricos  
- Padroniza endereços e remove duplicatas  
- Salva os dados em CSV  

### 3. Geocodificação
- Utiliza a API Nominatim para obter latitude e longitude dos imóveis  
- Calcula a menor distância até as estações de metrô de Samambaia  

### 4. Tratamento Estatístico
- Remove outliers de preço e imóveis com mais de 5 quartos ou acima de R$ 3 milhões  
- Aplica transformações logarítmicas para normalizar variáveis  

### 5. Análise Estatística
- Regressão linear múltipla para prever o preço com base em:
  - Metragem  
  - Número de quartos  
  - Distância até o metrô  
- Avaliação de multicolinearidade via VIF (Variance Inflation Factor)

## Colaboradores
Isabella Aguiar   ()

Liz de Albuquerque ()
