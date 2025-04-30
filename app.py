
import streamlit as st
import requests
import pandas as pd
from config import API_KEY

st.title("Value Bet Finder - Partite Future")

st.write("Questa app mostra partite future con value bet su 1X2 e Over/Under.")

# Parametri iniziali
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

# Recupero partite future
st.subheader("Prossime partite")
url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&season=2023&next=10"
res = requests.get(url, headers=headers)

if res.status_code == 200:
    data = res.json()
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
    st.error("Errore nel recupero dati API.")
