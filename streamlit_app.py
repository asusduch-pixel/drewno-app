import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Sprzedaż Drewna", layout="wide")
st.title("🌲 System Zamówień Drewna")

# Połączenie
conn = st.connection("gsheets", type=GSheetsConnection)

# Odczyt danych
df = conn.read(ttl=0)

st.sidebar.header("➕ Nowe zamówienie")
with st.sidebar.form("order_form", clear_on_submit=True):
    name = st.text_input("Imię i Nazwisko")
    phone = st.text_input("Telefon")
    address = st.text_input("Adres dostawy")
    wood_type = st.selectbox("Gatunek", ["Buk", "Dąb", "Grab", "Sosna", "Brzoza"])
    amount = st.number_input("Ilość (mp/m3)", min_value=0.1, step=0.1)
    length = st.selectbox("Długość (cm)", ["25", "33", "40", "50"])
    date = st.date_input("Termin dostawy")
    price = st.number_input("Cena za m3 (zł)", min_value=0, step=10)
    status = st.selectbox("Status", ["Do realizacji", "Pocięte", "Transport", "Zakończone"])
    
    if st.form_submit_button("Zapisz w bazie"):
        if name and phone: # Prosta walidacja
            new_row = {
                "Klient": name, "Telefon": phone, "Adres dostawy": address,
                "Gatunek": wood_type, "Ilość (mp/m3)": amount, "Długość (cm)": length,
                "Termin": str(date), "Status": status, "Cena za m3": price
            }
            # Dodanie do arkusza
            updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            conn.update(data=updated_df)
            st.sidebar.success("Zapisano!")
            st.rerun()
        else:
            st.sidebar.error("Wpisz imię i telefon!")

st.header("📋 Lista zamówień")
if not df.empty:
    df_display = df.copy()
    # Przeliczanie sumy
    df_display['Suma (zł)'] = df_display['Ilość (mp/m3)'] * df_display['Cena za m3']
    st.dataframe(df_display, use_container_width=True)
    st.metric("Łączna wartość", f"{df_display['Suma (zł)'].sum()} zł")
else:
    st.info("Brak zamówień. Dodaj pierwsze w panelu bocznym.")
