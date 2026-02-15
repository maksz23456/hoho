import streamlit as st
import pandas as pd
import random
import time

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Volleyball Manager 2026", page_icon="🏐", layout="wide")

# --- STYLE CSS DLA BOISKA I UI ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    .court-container {
        background: #2e7d32; 
        padding: 20px; 
        border-radius: 15px; 
        position: relative; 
        min-height: 550px; 
        border: 8px solid #f9a825;
        overflow: hidden;
    }
    .net {
        position: absolute; left: 50%; top: 0; bottom: 0; 
        width: 6px; background: rgba(255,255,255,0.8); 
        z-index: 10; border-left: 2px solid #333;
    }
    .attack-line {
        position: absolute; top: 0; bottom: 0; width: 2px; 
        border-left: 3px dashed rgba(255,255,255,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICJALIZACJA DANYCH ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.budget = 500000
    st.session_state.club_name = "MKS Warszawa"
    st.session_state.current_day = 1
    st.session_state.morale = 75
    
    st.session_state.league_teams = ["MKS Warszawa", "Jastrzębski Węgiel", "ZAKSA Kędzierzyn", "Projekt Warszawa", "Aluron Zawiercie", "Trefl Gdańsk"]
    st.session_state.league_table = {team: {"M": 0, "W": 0, "P": 0, "PKT": 0} for team in st.session_state.league_teams}
    
    # Kadra (7 zawodników)
    st.session_state.first_team = [
        {"id": 1, "imie": "Jakub", "nazwisko": "Kowalski", "poz": "Przyjmujący", "nr": 10, "stats": {"atk": 85, "def": 80, "ser": 78, "blk": 70}, "forma": 90},
        {"id": 2, "imie": "Piotr", "nazwisko": "Nowak", "poz": "Środkowy", "nr": 2, "stats": {"atk": 75, "def": 60, "ser": 65, "blk": 92}, "forma": 85},
        {"id": 3, "imie": "Marcin", "nazwisko": "Wiśniewski", "poz": "Rozgrywający", "nr": 1, "stats": {"atk": 60, "def": 85, "ser": 82, "blk": 65}, "forma": 88},
        {"id": 4, "imie": "Tomasz", "nazwisko": "Lewandowski", "poz": "Atakujący", "nr": 11, "stats": {"atk": 92, "def": 65, "ser": 85, "blk": 75}, "forma": 82},
        {"id": 5, "imie": "Kamil", "nazwisko": "Wójcik", "poz": "Libero", "nr": 8, "stats": {"atk": 20, "def": 95, "ser": 0, "blk": 10}, "forma": 90},
        {"id": 6, "imie": "Adam", "nazwisko": "Kamiński", "poz": "Przyjmujący", "nr": 12, "stats": {"atk": 82, "def": 82, "ser": 75, "blk": 74}, "forma": 85},
        {"id": 7, "imie": "Michał", "nazwisko": "Zieliński", "poz": "Środkowy", "nr": 19, "stats": {"atk": 70, "def": 55, "ser": 60, "blk": 88}, "forma": 80},
    ]
    
    st.session_state.starting_lineup = {"IV": 1, "III": 2, "II": 4, "V": 6, "VI": 5, "I": 3}
    st.session_state.next_match = {"przeciwnik": "Jastrzębski Węgiel", "dzien": 2}
    st.session_state.match_in_progress = False

# --- POMOCNICZE ---
def get_player(pid):
    return next((p for p in st.session_state.first_team if p["id"] == pid), None)

# --- WIDOK BOISKA 2D ---
def draw_court(score_us, score_opp, comment, ball=None):
    st.markdown(f"<h1 style='text-align:center;'>🔵 {st.session_state.club_name} {score_us} : {score_opp} 🟡</h1>", unsafe_allow_html=True)
    
    # Mapa pozycji zawodników (nasza strona - lewa)
    pos_coords = {
        "IV": {"l": "40%", "t": "20%"}, "III": {"l": "40%", "t": "48%"}, "II": {"l": "40%", "t": "75%"},
        "V": {"l": "15%", "t": "20%"}, "VI": {"l": "15%", "t": "48%"}, "I": {"l": "15%", "t": "75%"}
    }
    
    players_html = ""
    for pos, c in pos_coords.items():
        p = get_player(st.session_state.starting_lineup[pos])
        players_html += f"""
        <div style='position: absolute; left: {c['l']}; top: {c['t']}; width: 45px; height: 45px; 
             background: #1565c0; border: 3px solid white; border-radius: 50%; z-index: 20;
             display: flex; justify-content: center; align-items: center; color: white; font-weight: bold;'>
             {p['nr']}
        </div>"""

    # Piłka
    ball_html = ""
    if ball:
        ball_html = f"""<div style='position: absolute; left: {ball['l']}; top: {ball['t']}; 
                        width: 25px; height: 25px; background: #fff; border-radius: 50%; 
                        z-index: 50; box-shadow: 0 0 15px white; transition: all 0.4s ease;'></div>"""

    st.markdown(f"""
    <div class="court-container">
        <div class="net"></div>
        <div class="attack-line" style="left: 30%;"></div>
        <div class="attack-line" style="left: 70%;"></div>
        {players_html}
        {ball_html}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""<div style='background: #000; color: #0f0; padding: 15px; border-radius: 5px; 
                 font-family: monospace; font-size: 1.2rem; margin-top: 10px; border-left: 5px solid #0f0;'>
                 > {comment}</div>""", unsafe_allow_html=True)

# --- SILNIK MECZOWY ---
def play_rally(opp_level=80):
    phases = []
    
    # 1. ZAGRYWKA
    server = get_player(st.session_state.starting_lineup["I"])
    skill = server["stats"]["ser"]
    
    if random.randint(1, 100) > skill + 10:
        phases.append({"msg": f"Błąd serwisowy: {server['nazwisko']} w siatkę!", "ball": {"l": "50%", "t": "50%"}, "win": False})
        return False, phases
    
    phases.append({"msg": f"Potężna zagrywka: {server['nazwisko']}", "ball": {"l": "85%", "t": "75%"}, "win": None})
    
    # 2. PRZYJĘCIE I WYSTAWA (Uproszczone)
    phases.append({"msg": "Dobre przyjęcie, piłka do rozgrywającego...", "ball": {"l": "35%", "t": "48%"}, "win": None})
    
    # 3. ATAK (Szczegółowa logika: Mocny, Kiwka, Po Bloku)
    attacker = get_player(random.choice([st.session_state.starting_lineup["IV"], st.session_state.starting_lineup["II"]]))
    atk_type = random.choice(["POWER", "TIP", "BLOCK_OUT"])
    
    if atk_type == "TIP":
        phases.append({"msg": f"Sprytna kiwka {attacker['nazwisko']}!", "ball": {"l": "55%", "t": "48%"}, "win": True})
        return True, phases
    
    elif atk_type == "BLOCK_OUT":
        phases.append({"msg": f"Atak {attacker['nazwisko']} po taśmie i bloku!", "ball": {"l": "50%", "t": "10%"}, "win": None})
        phases.append({"msg": "Piłka ląduje na aucie! Punkt dla nas.", "ball": {"l": "95%", "t": "-5%"}, "win": True})
        return True, phases
    
    else: # MOCNY ATAK
        if attacker["stats"]["atk"] + random.randint(-10, 10) > opp_level:
            phases.append({"msg": f"GWÓŹDŹ! {attacker['nazwisko']} wbija piłkę w parkiet!", "ball": {"l": "80%", "t": "30%"}, "win": True})
            return True, phases
        else:
            phases.append({"msg": "ZATRZYMANY! Potrójny blok przeciwnika!", "ball": {"l": "48%", "t": "48%"}, "win": False})
            return False, phases

# --- INTERFEJS GŁÓWNY ---
st.title("🏐 Volleyball Manager 2026")

t1, t2, t3 = st.tabs(["📊 BIURO", "📋 SKŁAD", "🎮 MECZ LIVE"])

with t1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Budżet", f"{st.session_state.budget:,} PLN")
    c2.metric("Morale", f"{st.session_state.morale}%")
    c3.metric("Dzień", st.session_state.current_day)
    
    st.subheader("Tabela Ligowa")
    df = pd.DataFrame.from_dict(st.session_state.league_table, orient='index').sort_values("PKT", ascending=False)
    st.table(df)

with t2:
    st.subheader("Ustawienie na mecz (Rotacja początkowa)")
    col_l, col_r = st.columns(2)
    
    players_list = {f"{p['imie']} {p['nazwisko']} ({p['poz']})": p["id"] for p in st.session_state.first_team}
    
    for i, pos in enumerate(["IV", "III", "II", "V", "VI", "I"]):
        with (col_l if i < 3 else col_r):
            curr_val = next(k for k, v in players_list.items() if v == st.session_state.starting_lineup[pos])
            sel = st.selectbox(f"Pozycja {pos}", list(players_list.keys()), index=list(players_list.keys()).index(curr_val))
            st.session_state.starting_lineup[pos] = players_list[sel]

with t3:
    if st.session_state.current_day < st.session_state.next_match["dzien"]:
        st.info(f"Oczekiwanie na mecz z {st.session_state.next_match['przeciwnik']} (Dzień {st.session_state.next_match['dzien']})")
        if st.button("Kontynuuj do dnia meczu"):
            st.session_state.current_day = st.session_state.next_match["dzien"]
            st.rerun()
    else:
        st.warning(f"DZISIAJ MECZ: {st.session_state.club_name} vs {st.session_state.next_match['przeciwnik']}")
        
        if not st.session_state.match_in_progress:
            if st.button("ROZPOCZNIJ TRANSMISJĘ", type="primary"):
                st.session_state.match_in_progress = True
                st.rerun()
        
        if st.session_state.match_in_progress:
            board = st.empty()
            s_us, s_opp = 0, 0
            
            # Symulacja punkt po punkcie
            while s_us < 25 and s_opp < 25:
                win, phases = play_rally()
                for p in phases:
                    with board.container():
                        draw_court(s_us, s_opp, p["msg"], p["ball"])
                    time.sleep(0.7)
                
                if win: s_us += 1
                else: s_opp += 1
                time.sleep(0.5)
            
            # Koniec seta
            st.session_state.match_in_progress = False
            st.session_state.league_table[st.session_state.club_name]["M"] += 1
            st.session_state.league_table[st.session_state.club_name]["PKT"] += 3 if s_us > s_opp else 0
            
            st.balloons()
            st.success(f"Koniec meczu! Wynik: {s_us}:{s_opp}")
            
            if st.button("Wróć do biura"):
                st.session_state.current_day += 1
                st.session_state.next_match["dzien"] += 7
                st.rerun()
