import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
import matplotlib.pyplot as plt

# -------------------------------
# Configurazione pagina
# -------------------------------
st.set_page_config(page_title="Gestionale Palestre NiceFit Group", layout="wide")
st.title("Gestionale Palestre NiceFit Group")

# -------------------------------
# Logo NiceFit (da file nel repo)
# -------------------------------
try:
    st.image("logo_nicefit.png", width=200)
except Exception as e:
    st.warning("Logo non trovato. Assicurati che 'logo_nicefit.png' sia nella stessa cartella dello script.")

# -------------------------------
# Colori palestre
# -------------------------------
PALESTRE_COLORI = {
    "NEXUS": "#9EC9FF",
    "ELISIR": "#E8D9C0",
    "YOUNIQUE": "#D9B3FF",
    "AVENUE": "#A6DAD9"
}

# -------------------------------
# Connessione database
# -------------------------------
conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

# -------------------------------
# Creazione tabelle (se non esistono)
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
    return pd
