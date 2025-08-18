import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime

# --- Adiciona o diretório 'src' ao caminho do Python ---
# Isso é necessário para que possamos importar nosso módulo 'db'
SRC_DIR = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(SRC_DIR)

from db import get_engine

# --- Page Configuration ---
st.set_page_config(
    page_title="Coffee & Currency Dashboard",
    page_icon="☕",
    layout="wide"
)

# --- Função de Carregamento de Dados ---
@st.cache_data
def load_data_from_db(query, _engine):
    """Loads data from the database using a SQL query."""
    try:
        return pd.read_sql(query, _engine, parse_dates=['date'])
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# --- Conexão e Queries ---
engine = get_engine()
# Query para buscar os dados recentes para os Big Numbers
latest_rates_query = "SELECT date, currency, rate FROM latest_currency_rates"
# Query para buscar os dados históricos para o gráfico
historical_rates_query = "SELECT date, currency, rate FROM currency_rates"

# --- Carregamento dos Dados ---
df_latest_rates = load_data_from_db(latest_rates_query, engine)
df_historical_rates = load_data_from_db(historical_rates_query, engine)

# --- Título do Dashboard ---
st.title("☕ Coffee & Currency Analytics Dashboard")

# --- Verificação de Dados ---
if df_latest_rates is None or df_historical_rates is None or df_latest_rates.empty or df_historical_rates.empty:
    st.error("Data not found in the database. Please run the full pipeline with 'python main.py' first.")
    st.stop()

# --- Barra Lateral para Filtros ---
with st.sidebar:
    st.header("Filters")

    # Filtro de Data
    min_date = df_historical_rates['date'].min().date()
    max_date = df_historical_rates['date'].max().date()

    selected_start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
    selected_end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

    # Filtro de Moedas
    all_currencies = df_historical_rates['currency'].unique().tolist()
    if "USD" not in all_currencies and "USD" in df_latest_rates['currency'].unique().tolist():
        all_currencies.append("USD")
    
    selected_currencies = st.multiselect(
        "Select Currencies",
        options=all_currencies,
        default=['BRL', 'EUR', 'CLP']
    )

# --- Lógica de Filtragem dos Dados ---
start_datetime = pd.to_datetime(selected_start_date)
end_datetime = pd.to_datetime(selected_end_date)

df_filtered = df_historical_rates[
    (df_historical_rates['date'] >= start_datetime) &
    (df_historical_rates['date'] <= end_datetime) &
    (df_historical_rates['currency'].isin(selected_currencies))
]

# --- Seção de Métricas (Big Numbers) ---
st.header("Latest Exchange Rates (vs USD)")

latest_date = df_latest_rates['date'].max()
latest_data = df_latest_rates[df_latest_rates['date'] == latest_date]

col1, col2, col3 = st.columns(3)

def display_metric(column, currency_code):
    rate_data = latest_data[latest_data['currency'] == currency_code]
    if not rate_data.empty:
        rate = rate_data['rate'].iloc[0]
        column.metric(label=f"**{currency_code} / USD**", value=f"{rate:.4f}")
    else:
        column.metric(label=f"**{currency_code} / USD**", value="N/A")

display_metric(col1, "BRL")
display_metric(col2, "EUR")
display_metric(col3, "CLP")

# --- Seção de Gráficos Históricos ---
st.header("Historical Exchange Rate Charts")

if df_filtered.empty or not selected_currencies:
    st.warning("No data available for the selected period or currencies. Please adjust the filters.")
else:
    # Cria um gráfico separado para cada moeda selecionada
    for currency in selected_currencies:
        st.subheader(f"{currency} / USD Exchange Rate")
        df_currency_chart = df_filtered[df_filtered['currency'] == currency]
        st.line_chart(df_currency_chart.set_index('date')['rate'])

# --- Seção da Tabela de Dados Históricos Completos ---
st.header("Complete Historical Data")

if df_filtered.empty:
    st.warning("Select filters to see data.")
else:
    # Calcula a coluna de variação percentual
    df_filtered = df_filtered.sort_values(by=['currency', 'date'])
    df_filtered['pct_change'] = df_filtered.groupby('currency')['rate'].pct_change()

    # Pivota a tabela para o formato desejado
    df_pivot = df_filtered.pivot(
        index='date', 
        columns='currency', 
        values=['rate', 'pct_change']
    )

    # Reorganiza as colunas para agrupar por moeda
    df_pivot = df_pivot.swaplevel(0, 1, axis=1).sort_index(axis=1)
    
    # Exibe o DataFrame com formatação
    st.dataframe(df_pivot.style.format({
        (currency, 'pct_change'): '{:.2%}' for currency in selected_currencies
    }, na_rep="-"))