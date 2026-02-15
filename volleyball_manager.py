import streamlit as st
import pandas as pd
import random
import time

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Volleyball Manager 2026", page_icon="🏐", layout="wide")

# --- STYLE CSS (BOISKO I ANIMACJE) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .court-container {
        background: #2e7d32; padding: 20px; border-radius: 15px;
        position: relative; min-height: 500px; border: 8px solid #f9a825; overflow: hidden;
    }
    .net { 
        position: absolute; left: 50%; top: 0; bottom: 0; 
        width: 6px; background: rgba(255,255,255,0.8); z-index: 10; 
    }
    .player-dot {
        position: absolute; width: 42px; height: 42px; border-radius: 50%;
        display: flex; justify-content: center; align-items: center;
        color: white; font-weight: bold; font-size: 0.75em;
        transition: all 0.5s ease-in-out; z-index: 20; border: 2px solid white;
        text-align: center; line-height: 1;
    }
    .ball-dot {
        position: absolute; width: 22px; height: 22px; background: radial-gradient(circle, #fff, #ddd);
        border-radius: 50%; z-index: 50; box-shadow: 0 0 15px #fff;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid #ccc;
    }
    .stMetric { background-color: #1f2937; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INICJALIZACJA STANU GRY ---
if 'initialized' not in st.session_state:
    st.session_state.update({
        'initialized': True,
        'budget': 500000,
        'current_day': 1,
        'morale': 80,
        'league_table': {
            "MKS Warszawa": {"M": 0, "W": 0, "P": 0, "PKT": 0},
            "Jastrzębski Węgiel": {"M": 0, "W": 0, "P": 0, "PKT": 0},
            "ZAKSA": {"M": 0, "W": 0, "P": 0, "PKT": 0},
            "Projekt Warszawa": {"M": 0, "W": 0, "P": 0, "PKT": 0}
        },
        'players': [
            {"id": 1, "n": "Kowalski", "p": "Rozgrywający", "at": 65, "bl": 70, "sr": 85},
            {"id": 2, "n": "Nowak", "p": "Atakujący", "at": 92, "bl": 75, "sr": 88},
            {"id": 3, "n": "Zieliński", "p": "Środkowy", "at": 80, "bl": 95, "sr": 70},
            {"id": 4, "n": "Wiśniewski", "p": "Środkowy", "at": 78, "bl": 92, "sr": 65},
            {"id": 5, "n": "Wójcik", "p": "Przyjmujący", "at": 84, "bl": 70, "sr": 80},
            {"id": 6, "n": "Kamiński", "p": "Przyjmujący", "at": 82, "bl": 72, "sr": 78},
            {"id": 7, "n": "Lewandowski", "p": "Libero", "at": 10, "bl": 5, "sr": 0},
            {"id": 8, "n": "Bąk", "p": "Rezerwowy", "at": 70, "bl": 65, "sr": 60},
            {"id": 9, "n": "Mazur", "p": "Rezerwowy", "at": 68, "bl": 60, "sr": 72}
        ],
        # Ustawienie "na skos": I-IV, II-V, III-VI
        'lineup': { "I": 1, "II": 3, "III": 5, "IV": 2, "V": 4, "VI": 6 },
        'match_in_progress': False,
        'score_us': 0,
        'score_opp': 0
    })

# --- MAPOWANIE POZYCJI NA BOISKU ---
# Lewa strona (My)
POS_US = {
    "I":   {"l": "12%", "t": "72%"}, "VI":  {"l": "12%", "t": "48%"}, "V":   {"l": "12%", "t": "22%"},
    "II":  {"l": "35%", "t": "72%"}, "III": {"l": "35%", "t": "48%"}, "IV":  {"l": "35%", "t": "22%"}
}
# Prawa strona (Przeciwnik)
POS_OPP = {
    "I":   {"l": "85%", "t": "25%"}, "VI":  {"l": "85%", "t": "50%"}, "V":   {"l": "85%", "t": "75%"},
    "II":  {"l": "62%", "t": "25%"}, "III": {"l": "62%", "t": "50%"}, "IV":  {"l": "62%", "t": "75%"}
}

def draw_court(ball_pos, comment):
    players_html = ""
    # Rysuj naszą drużynę
    for pos, pid in st.session_state.lineup.items():
        p = next(x for x in st.session_state.players if x['id'] == pid)
        
        # Logika Libero: Jeśli Środkowy jest w 2. linii (I, VI, V), wchodzi Libero (id: 7)
        display_name = p['n']
        color = "#1565c0" # Niebieski
        
        if p['p'] == "Środkowy" and pos in ["I", "VI", "V"]:
            libero = next(x for x in st.session_state.players if x['p'] == "Libero")
            display_name = libero['n']
            color = "#fbc02d" # Żółty dla Libero

        players_html += f"""
        <div class='player-dot' style='left:{POS_US[pos]['l']}; top:{POS_US[pos]['t']}; background:{color};'>
            {display_name[:3].upper()}<br><span style='font-size:8px'>{pos}</span>
        </div>"""
    
    # Rysuj przeciwnika
    for pos, coords in POS_OPP.items():
        players_html += f"""
        <div class='player-dot' style='left:{coords['l']}; top:{coords['t']}; background:#c62828;'>
            CPU<br><span style='font-size:8px'>{pos}</span>
        </div>"""

    ball_html = f"<div class='ball-dot' style='left:{ball_pos[0]}; top:{ball_pos[1]};'></div>"
    
    st.markdown(f"<div class='court-container'><div class='net'></div>{players_html}{ball_html}</div>", unsafe_allow_html=True)
    st.info(f"🗨️ {comment}")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📊 BIURO", "📋 SKŁAD & TRANSFERY", "🎮 MECZ LIVE"])

with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Budżet", f"{st.session_state.budget} PLN")
    c2.metric("Morale", f"{st.session_state.morale}%")
    c3.metric("Dzień", st.session_state.current_day)
    
    st.subheader("Tabela Ekstraklasy 2026")
    st.table(pd.DataFrame.from_dict(st.session_state.league_table, orient='index'))

with tab2:
    st.subheader("Ustawienie wyjściowe (Rotacja)")
    st.caption("Pamiętaj: Rozgrywający i Atakujący powinni być na skos (np. pozycje I i IV).")
    
    player_options = {f"{p['n']} ({p['p']})": p['id'] for p in st.session_state.players}
    
    col_a, col_b = st.columns(2)
    for i, pos in enumerate(["I", "II", "III", "IV", "V", "VI"]):
        with col_a if i < 3 else col_b:
            current_id = st.session_state.lineup[pos]
            current_name = next(k for k, v in player_options.items() if v == current_id)
            sel = st.selectbox(f"Pozycja {pos}", list(player_options.keys()), index=list(player_options.keys()).index(current_name), key=f"sel_{pos}")
            st.session_state.lineup[pos] = player_options[sel]

    st.divider()
    st.subheader("Rynek Transferowy")
    if st.button("Szukaj talentów (Koszt: 10 000 PLN)"):
        if st.session_state.budget >= 10000:
            st.session_state.budget -= 10000
            new_id = len(st.session_state.players) + 1
            new_p = {"id": new_id, "n": "Młody", "p": "Perspektywiczny", "at": random.randint(60, 80), "bl": random.randint(60, 80), "sr": random.randint(60, 80)}
            st.session_state.players.append(new_p)
            st.success(f"Znaleziono nowego gracza: {new_p['n']}!")
        else:
            st.error("Brak funduszy!")

with tab3:
    if not st.session_state.match_in_progress:
        if st.button("ROZPOCZNIJ TRANSMISJĘ MECZU", type="primary"):
            st.session_state.match_in_progress = True
            st.session_state.score_us = 0
            st.session_state.score_opp = 0
            st.rerun()
    else:
        st.subheader(f"MECZ LIVE: {st.session_state.club_name} vs CPU")
        match_placeholder = st.empty()
        
        # Prosta symulacja punkt po punkcie
        while st.session_state.score_us < 25 and st.session_state.score_opp < 25:
            # Faza 1: Serwis
            with match_placeholder.container():
                draw_court(["15%", "72%"], "Serwis Kowalskiego!")
            time.sleep(0.6)
            
            # Faza 2: Piłka leci na stronę CPU
            with match_placeholder.container():
                draw_court(["75%", "50%"], "Przeciwnik przyjmuje...")
            time.sleep(0.6)
            
            # Faza 3: Atak (losowanie wyniku)
            if random.random() > 0.45:
                st.session_state.score_us += 1
                msg = "PUNKT! Potężny atak Nowaka po skosie!"
                ball = ["90%", "30%"]
            else:
                st.session_state.score_opp += 1
                msg = "BLOK! Zatrzymali nas na siatce..."
                ball = ["10%", "50%"]
            
            with match_placeholder.container():
                st.write(f"### WYNIK: {st.session_state.score_us} - {st.session_state.score_opp}")
                draw_court(ball, msg)
            time.sleep(1.0)

        # Koniec meczu
        st.session_state.match_in_progress = False
        st.balloons()
        if st.session_state.score_us > st.session_state.score_opp:
            st.success("ZWYCIĘSTWO! +3 PKT do tabeli.")
            st.session_state.league_table["MKS Warszawa"]["PKT"] += 3
        else:
            st.error("Porażka. Popracuj nad blokiem!")
        
        if st.button("WRÓĆ DO BIURA"):
            st.session_state.current_day += 1
            st.rerun()
