import streamlit as st
import pandas as pd
import sqlite3
from datetime import date, timedelta

# -------------------------------
# Configurazione pagina
# -------------------------------
st.set_page_config(page_title="Gestionale Palestre", layout="wide")
st.title("Gestionale Palestre")

# -------------------------------
# Colori palestre
# -------------------------------
PALESTRE_COLORI = {
    "NEXUS": "#9EC9FF",      # blu chiaro
    "ELISIR": "#E8D9C0",     # beige
    "YOUNIQUE": "#D9B3FF",   # viola chiaro
    "AVENUE": "#A6DAD9"      # azzurro ottanio
}

# -------------------------------
# Connessione database
# -------------------------------
conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

# -------------------------------
# Creazione tabelle
# -------------------------------
c.execute("""CREATE TABLE IF NOT EXISTS dipendenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    cognome TEXT,
    data_inizio TEXT,
    data_fine TEXT,
    tipo_contratto TEXT,
    telefono TEXT,
    email TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS fornitori (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_azienda TEXT,
    partita_iva TEXT,
    indirizzo TEXT,
    email TEXT,
    telefono TEXT,
    persona_riferimento TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS contabilita (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    tipo TEXT,
    descrizione TEXT,
    importo REAL,
    stato TEXT,
    fornitore_cliente TEXT,
    palestra TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS appuntamenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    ora TEXT,
    titolo TEXT,
    descrizione TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS todo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attivita TEXT,
    scadenza TEXT,
    completata INTEGER
)""")
conn.commit()

# -------------------------------
# Funzioni comuni
# -------------------------------
def aggiungi_riga(tabella, dati):
    placeholders = ",".join("?"*len(dati))
    c.execute(f"INSERT INTO {tabella} VALUES (NULL,{placeholders})", dati)
    conn.commit()

def leggi_tabella(tabella):
    return pd.read_sql(f"SELECT * FROM {tabella}", conn)

# -------------------------------
# Sidebar / Menu principale
# -------------------------------
menu = ["Dashboard", "Dipendenti", "Fornitori", "Contabilità", "Appuntamenti", "To-Do List"]
scelta = st.sidebar.selectbox("Sezioni", menu)

# -------------------------------
# DASHBOARD
# -------------------------------
if scelta == "Dashboard":
    st.header("Dashboard riepilogativa")
    df_dip = leggi_tabella("dipendenti")
    df_cont = leggi_tabella("contabilita")
    df_app = leggi_tabella("appuntamenti")
    df_todo = leggi_tabella("todo")

    st.metric("Dipendenti", len(df_dip))
    fatture_sospese = len(df_cont[df_cont["stato"]=="Non Pagato"])
    st.metric("Fatture in sospeso", fatture_sospese)
    incassi = df_cont[df_cont["tipo"]=="Incasso"]["importo"].sum()
    pagamenti = df_cont[df_cont["tipo"].isin(["Fattura Fornitore","Pagamento"])]["importo"].sum()
    st.metric("Saldo attuale", f"€ {incassi - pagamenti:,.2f}")

    st.subheader("Prossimi 3 appuntamenti")
    df_app["data"] = pd.to_datetime(df_app["data"])
    prossimi = df_app.sort_values("data").head(3)
    st.dataframe(prossimi)

    st.subheader("To-Do in scadenza")
    oggi = date.today()
    df_todo["scadenza"] = pd.to_datetime(df_todo["scadenza"])
    imminenti = df_todo[(df_todo["scadenza"] <= oggi + timedelta(days=15)) & (df_todo["completata"]==0)]
    st.dataframe(imminenti)

# -------------------------------
# DIPENDENTI
# -------------------------------
elif scelta == "Dipendenti":
    st.header("Gestione Dipendenti")
    df = leggi_tabella("dipendenti")

    ricerca = st.text_input("🔍 Cerca dipendente per nome o cognome")
    if ricerca:
        df = df[df["nome"].str.contains(ricerca, case=False) | df["cognome"].str.contains(ricerca, case=False)]

    st.dataframe(df, use_container_width=True)

    st.subheader("Aggiungi nuovo dipendente")
    nome = st.text_input("Nome")
    cognome = st.text_input("Cognome")
    data_inizio = st.date_input("Data inizio contratto")
    data_fine = st.date_input("Data fine contratto")
    tipo_contratto = st.selectbox("Tipo contratto", ["Determinato","Indeterminato","Part-time"])
    telefono = st.text_input("Telefono")
    email = st.text_input("Email")

    if st.button("Salva Dipendente"):
        if nome and cognome:
            aggiungi_riga("dipendenti",(nome,cognome,str(data_inizio),str(data_fine),tipo_contratto,telefono,email))
            st.success("Dipendente aggiunto!")
        else:
            st.error("Compila Nome e Cognome")

# -------------------------------
# FORNITORI
# -------------------------------
elif scelta == "Fornitori":
    st.header("Gestione Fornitori")
    df = leggi_tabella("fornitori")

    ricerca = st.text_input("🔍 Cerca fornitore per nome o partita IVA")
    if ricerca:
        df = df[df["nome_azienda"].str.contains(ricerca, case=False) | df["partita_iva"].str.contains(ricerca, case=False)]

    st.dataframe(df, use_container_width=True)

    st.subheader("Aggiungi nuovo fornitore")
    nome_azienda = st.text_input("Nome Azienda")
    partita_iva = st.text_input("Partita IVA")
    indirizzo = st.text_input("Indirizzo")
    email = st.text_input("Email")
    telefono = st.text_input("Telefono")
    persona_rif = st.text_input("Persona di riferimento")

    if st.button("Salva Fornitore"):
        if nome_azienda:
            aggiungi_riga("fornitori",(nome_azienda,partita_iva,indirizzo,email,telefono,persona_rif))
            st.success("Fornitore aggiunto!")
        else:
            st.error("Inserisci Nome Azienda")

# -------------------------------
# CONTABILITÀ
# -------------------------------
elif scelta == "Contabilità":
    st.header("Gestione Contabilità")
    df = leggi_tabella("contabilita")

    # Barra ricerca globale
    ricerca = st.text_input("🔍 Cerca descrizione, fornitore/cliente o palestra")
    if ricerca:
        df = df[df["descrizione"].str.contains(ricerca, case=False) |
                df["fornitore_cliente"].str.contains(ricerca, case=False) |
                df["palestra"].str.contains(ricerca, case=False)]

    st.dataframe(df, use_container_width=True)

    st.subheader("Aggiungi transazione")
    data_trans = st.date_input("Data", date.today())
    tipo = st.selectbox("Tipo", ["Fattura Fornitore","Incasso","Pagamento"])
    descrizione = st.text_input("Descrizione")
    importo = st.number_input("Importo", min_value=0.0)
    stato = st.selectbox("Stato", ["Pagato","Non Pagato"])
    fornitore_cliente = st.text_input("Fornitore/Cliente")
    palestra = st.selectbox("Palestra", list(PALESTRE_COLORI.keys()))

    if st.button("Salva transazione"):
        if descrizione and importo>0:
            aggiungi_riga("contabilita",(str(data_trans),tipo,descrizione,importo,stato,fornitore_cliente,palestra))
            st.success("Transazione salvata!")
        else:
            st.error("Compila tutti i campi obbligatori")
