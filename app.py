import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Heizwerke & FirmenABC Live-Daten", layout="wide")

st.title("🔥 Nahwärme-Tarife & FirmenABC Live-Daten")
st.caption("Datenquelle: Live-Scraping aus dem Web (Wärmepreise.at & FirmenABC.at)")

@st.cache_data
def load_data():
    conn = sqlite3.connect("meine_datenbank.db")
    df = pd.read_sql_query("SELECT * FROM heizwerke", conn)
    conn.close()
    return df

df = load_data()

st.dataframe(
    df,
    column_config={
        "name": "Heizwerk / Anbieter",
        "ort": "Ort",
        "arbeitspreis_netto_mwh": st.column_config.NumberColumn("Arbeitspreis (€/MWh)", format="%.2f €"),
        "gesamtpreis_brutto_eur": st.column_config.NumberColumn("Gesamtpreis Brutto (€)", format="%.2f €"),
        "firmenbuchnummer": "Firmenbuchnummer (FN)",
        "firmenabc_url": st.column_config.LinkColumn("FirmenABC Live-Profil", display_text="🔗 Auf FirmenABC öffnen")
    },
    hide_index=True,
    use_container_width=True
)