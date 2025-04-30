
import streamlit as st
import requests
import pandas as pd
from config import API_KEY

st.title("Value Bet Finder - DEBUG")

LEAGUE_IDS = {
    "Premier League": 39,
    "Serie A": 135
}
selected_league = st.selectbox("Scegli campionato:", list(LEAGUE_IDS.keys()))
league_id = LEAGUE_IDS[selected_league]

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "v3.football.api-sports.io"
}

# DEBUG: URL usato
url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&season=2023&next=10"
st.code(f"Richiesta a: {url}")

res = requests.get(url, headers=headers)
st.write(f"Status code: {res.status_code}")

try:
    data = res.json()
    st.subheader("Risposta JSON completa")
    st.json(data)

    if "response" in data and data["response"]:
        st.subheader("Partite trovate:")
        match_list = []
        for match in data["response"]:
            teams = match["teams"]
            date = match["fixture"]["date"]
            match_list.append({
                "Data": date[:10],
                "Squadra Casa": teams["home"]["name"],
                "Squadra Ospite": teams["away"]["name"]
            })
        df = pd.DataFrame(match_list)
        st.dataframe(df)
    else:
        st.warning("Nessuna partita trovata nella risposta dell'API.")

except Exception as e:
    st.error(f"Errore durante il parsing JSON: {e}")
