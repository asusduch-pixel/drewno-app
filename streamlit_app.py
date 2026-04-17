import streamlit as st
import pandas as pd
from datetime import datetime

# Konfiguracja strony
st.set_page_config(page_title="Sprzedaż Drewna", layout="wide")
st.title("🌲 System Zamówień Drewna")

# Prosta baza danych w pamięci (dla testu)
if 'orders' not in st.session_state:
    st.session_state.orders = pd.DataFrame(columns=[
        "Klient", "Telefon", "Adres", "Gatunek", "Ilość", "Długość", "Termin", "Status"
    ])

# BOCZNY PANEL - Dodawanie zamówienia
st.sidebar.header("➕ Dodaj nowe zamówienie")
with st.sidebar.form("order_form", clear_on_submit=True):
    name = st.text_input("Imię i Nazwisko")
    phone = st.text_input("Telefon")
    address = st.text_input("Adres dostawy")
    wood_type = st.selectbox("Gatunek", ["Buk", "Dąb", "Grab", "Sosna", "Brzoza"])
    amount = st.number_input("Ilość (mp/m3)", min_value=0.5, step=0.5)
    length = st.selectbox("Długość (cm)", ["25", "33", "40", "50"])
    date = st.date_input("Termin dostawy", datetime.now())
    status = st.selectbox("Status", ["Do realizacji", "Pocięte", "Transport", "Zakończone"])
    
    submitted = st.form_submit_button("Zapisz zamówienie")
    
    if submitted:
        new_data = {
            "Klient": name, "Telefon": phone, "Adres": address, 
            "Gatunek": wood_type, "Ilość": amount, "Długość": length, 
            "Termin": str(date), "Status": status
        }
        st.session_state.orders = pd.concat([st.session_state.orders, pd.DataFrame([new_data])], ignore_index=True)
        st.sidebar.success("Zapisano!")

# GŁÓWNY PANEL - Lista zamówień
st.header("📋 Aktualne zamówienia")
if not st.session_state.orders.empty:
    # Filtrowanie po statusie
    filter_status = st.multiselect("Filtruj status:", ["Do realizacji", "Pocięte", "Transport", "Zakończone"], default=["Do realizacji", "Pocięte", "Transport"])
    
    display_df = st.session_state.orders[st.session_state.orders['Status'].isin(filter_status)]
    st.dataframe(display_df, use_container_width=True)
    
    # Przycisk do pobrania bazy do Excela
    csv = st.session_state.orders.to_csv(index=False).encode('utf-8')
    st.download_button("Pobierz listę (CSV)", csv, "zamowienia.csv", "text/csv")
else:
    st.info("Brak zamówień. Dodaj pierwsze w panelu bocznym.")
