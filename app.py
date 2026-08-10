import streamlit as st
import pandas as pd

# Seitentitel & Icon festlegen
st.set_page_config(page_title="Mein Browser-Prototyp", page_icon="🚀", layout="wide")

st.title("🚀 Mein kostenloser Python-Prototyp")
st.write("Diese App wurde zu 100 % im Browser entwickelt und gehostet.")

# Interaktive Seitenleiste
st.sidebar.header("Filter & Optionen")
kategorie = st.sidebar.selectbox("Wähle eine Region:", ["Vorarlberg", "Tirol", "Salzburg"])

# Beispieldaten erzeugen
data = {
    "Region": ["Vorarlberg", "Vorarlberg", "Tirol", "Tirol", "Salzburg"],
    "Projekt": ["Projekt Alpha", "Projekt Beta", "Projekt Gamma", "Projekt Delta", "Projekt Epsilon"],
    "Status": ["Aktiv", "In Planung", "Aktiv", "Abgeschlossen", "Aktiv"],
    "Wert (€)": [15000, 23000, 18500, 42000, 9500]
}
df = pd.DataFrame(data)

# Daten filtern
filtered_df = df[df["Region"] == kategorie]

# Kennzahlen (KPIs) anzeigen
col1, col2 = st.columns(2)
col1.metric(label="Anzahl Projekte", value=len(filtered_df))
col2.metric(label="Gesamtwert (€)", value=f"{filtered_df['Wert (€)'].sum():,} €")

st.subheader(f"Übersicht für {kategorie}")
st.dataframe(filtered_df, use_container_width=True)

# Interaktiver Button
if st.button("Aktion ausführen"):
    st.success(f"Daten für {kategorie} wurden erfolgreich verarbeitet!")