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
        background: #2e7d32; /* Kolor boiska */
        padding: 20px;
        border-radius: 15px;
        position: relative;
        min-height: 550px;
        border: 8px solid #f9a825; /* Linie autowe */
        overflow: hidden;
        margin-top: 15px;
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
    .player-dot {
        position: absolute;
        width: 45px; height: 45px;
        border-radius: 50%;
        display: flex; justify-content: center; align-items: center;
        color: white; font-weight: bold;
        font-size: 0.9em;
        transition: all 0.3s ease-out; /* Płynne przejścia */
        box-shadow: 0 0 8px rgba(0,0,0,0.5);
        z-index: 20;
    }
    .player-us { background: #1565c0; border: 3px solid #add8e6; } /* Nasz zespół - niebieski */
    .player-opp { background: #d32f2f; border: 3px solid #ffccbc; } /* Przeciwnik - czerwony */
    .ball-dot {
        position: absolute;
        width: 25px; height: 25px;
        background: radial-gradient(circle at 30% 30%, #fff, #bbb);
        border-radius: 50%;
        z-index: 50;
        box-shadow: 0 0 10px #ffe082, 0 0 5px #ffeb3b;
        transition: all 0.4s ease-out; /* Płynne przejścia */
        border: 2px solid #fbc02d;
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
        {"id": 1, "imie": "Jakub", "nazwisko": "Kowalski", "poz": "Przyjmujący", "nr": 10, "stats": {"atk": 85, "def": 80, "ser": 78, "blk": 70, "set": 60}, "forma": 90, "fatigue": 0},
        {"id": 2, "imie": "Piotr", "nazwisko": "Nowak", "poz": "Środkowy", "nr": 2, "stats": {"atk": 75, "def": 60, "ser": 65, "blk": 92, "set": 50}, "forma": 85, "fatigue": 0},
        {"id": 3, "imie": "Marcin", "nazwisko": "Wiśniewski", "poz": "Rozgrywający", "nr": 1, "stats": {"atk": 60, "def": 85, "ser": 82, "blk": 65, "set": 90}, "forma": 88, "fatigue": 0},
        {"id": 4, "imie": "Tomasz", "nazwisko": "Lewandowski", "poz": "Atakujący", "nr": 11, "stats": {"atk": 92, "def": 65, "ser": 85, "blk": 75, "set": 55}, "forma": 82, "fatigue": 0},
        {"id": 5, "imie": "Kamil", "nazwisko": "Wójcik", "poz": "Libero", "nr": 8, "stats": {"atk": 20, "def": 95, "ser": 0, "blk": 10, "set": 80}, "forma": 90, "fatigue": 0},
        {"id": 6, "imie": "Adam", "nazwisko": "Kamiński", "poz": "Przyjmujący", "nr": 12, "stats": {"atk": 82, "def": 82, "ser": 75, "blk": 74, "set": 65}, "forma": 85, "fatigue": 0},
        {"id": 7, "imie": "Michał", "nazwisko": "Zieliński", "poz": "Środkowy", "nr": 19, "stats": {"atk": 70, "def": 55, "ser": 60, "blk": 88, "set": 50}, "forma": 80, "fatigue": 0},
    ]
    
    # Przykładowi zawodnicy przeciwnika (uproszczone)
    st.session_state.opp_team = [
        {"id": 101, "imie": "Opp", "nazwisko": "Player1", "nr": 1, "poz": "OH", "stats": {"atk": 80, "def": 75, "ser": 70, "blk": 70, "set": 60}},
        {"id": 102, "imie": "Opp", "nazwisko": "Player2", "nr": 2, "poz": "MB", "stats": {"atk": 70, "def": 60, "ser": 60, "blk": 85, "set": 50}},
        {"id": 103, "imie": "Opp", "nazwisko": "Player3", "nr": 3, "poz": "SET", "stats": {"atk": 55, "def": 80, "ser": 75, "blk": 60, "set": 85}},
        {"id": 104, "imie": "Opp", "nazwisko": "Player4", "nr": 4, "poz": "OPP", "stats": {"atk": 88, "def": 60, "ser": 80, "blk": 70, "set": 55}},
        {"id": 105, "imie": "Opp", "nazwisko": "Player5", "nr": 5, "poz": "LIB", "stats": {"atk": 20, "def": 90, "ser": 0, "blk": 10, "set": 75}},
        {"id": 106, "imie": "Opp", "nazwisko": "Player6", "nr": 6, "poz": "OH", "stats": {"atk": 78, "def": 78, "ser": 70, "blk": 70, "set": 60}},
    ]

    # Początkowe ustawienie na boisku (ID graczy z first_team)
    # Pozycje: I, II, III, IV, V, VI (Zgodnie z rotacją)
    st.session_state.starting_lineup = {
        "I": 3,  # Rozgrywający
        "II": 4, # Atakujący
        "III": 2, # Środkowy
        "IV": 1,  # Przyjmujący
        "V": 6,  # Przyjmujący
        "VI": 5  # Libero (na przyjęciu)
    }

    st.session_state.next_match = {"przeciwnik": "Jastrzębski Węgiel", "dzien": 2}
    st.session_state.match_in_progress = False
    st.session_state.current_set = 1
    st.session_state.sets_won = 0
    st.session_state.sets_lost = 0

# --- POMOCNICZE FUNKCJE ---
def get_player(pid, team="us"):
    if team == "us":
        return next((p for p in st.session_state.first_team if p["id"] == pid), None)
    else:
        return next((p for p in st.session_state.opp_team if p["id"] == pid), None)

def get_player_by_position(pos_key, team="us"):
    if team == "us":
        player_id = st.session_state.starting_lineup[pos_key]
        return get_player(player_id, team="us")
    else:
        # Dla przeciwnika upraszczamy: stałe przypisanie ID do pozycji
        opp_lineup = {
            "I": 103, "II": 104, "III": 102,
            "IV": 101, "V": 106, "VI": 105
        }
        player_id = opp_lineup[pos_key]
        return get_player(player_id, team="opp")

def get_effective_stat(player, stat_name):
    # Oblicz efektywną statystykę uwzględniającą formę i zmęczenie
    base_stat = player["stats"].get(stat_name, 0)
    form_factor = player.get("forma", 100) / 100
    fatigue_penalty = player.get("fatigue", 0) / 2 # Każde 2 punkty zmęczenia to 1% mniej skilla
    
    effective_value = base_stat * form_factor - fatigue_penalty
    return max(10, min(100, int(effective_value))) # Statystyki między 10 a 100

def apply_fatigue(player_id, team="us", amount=1):
    if team == "us":
        for p in st.session_state.first_team:
            if p["id"] == player_id:
                p["fatigue"] = min(p["fatigue"] + amount, 100) # Max 100 zmęczenia
                break
    else:
        # Przeciwnik nie śledzi zmęczenia w tej wersji, ale można by to dodać
        pass

def rotate_team(team_side):
    # Rotacja dla naszej drużyny
    if team_side == "us":
        current_lineup = st.session_state.starting_lineup
        new_lineup = {}
        # Przesuwanie pozycji zgodnie z ruchem wskazówek zegara
        new_lineup["I"] = current_lineup["VI"]
        new_lineup["II"] = current_lineup["I"]
        new_lineup["III"] = current_lineup["II"]
        new_lineup["IV"] = current_lineup["III"]
        new_lineup["V"] = current_lineup["IV"]
        new_lineup["VI"] = current_lineup["V"]
        st.session_state.starting_lineup = new_lineup
    else:
        # Możesz zaimplementować rotację dla przeciwnika w podobny sposób
        pass

# --- WIDOK BOISKA 2D Z ANIMACJĄ ---
def draw_court_live(score_us, score_opp, comment, player_positions, ball_pos=None):
    st.markdown(f"<h1 style='text-align:center;'>🔵 {st.session_state.club_name} {score_us} : {score_opp} 🔴 {st.session_state.next_match['przeciwnik']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center;'>SET {st.session_state.current_set} ({st.session_state.sets_won}:{st.session_state.sets_lost})</h2>", unsafe_allow_html=True)

    players_html = ""
    for team, players_data in player_positions.items():
        for pos_key, player_info in players_data.items():
            player_class = "player-us" if team == "us" else "player-opp"
            players_html += f"""
            <div class='player-dot {player_class}' style='left: {player_info['l']}; top: {player_info['t']};'>
                {player_info['nr']}<br>
                <span style='font-size:0.6em;'>{player_info['nazwisko']}</span>
            </div>"""

    ball_html = ""
    if ball_pos:
        ball_html = f"""<div class='ball-dot' style='left: {ball_pos['l']}; top: {ball_pos['t']};'></div>"""

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
def play_rally(server_team="us"):
    phases = []
    win_point_us = None # True: my punkt, False: przeciwnik punkt

    # Początkowe pozycje na boisku dla 6 na 6 graczy
    # % lewo, % góra
    # Pozycje naszego zespołu (lewa strona boiska)
    us_coords = {
        "I": {"l": "15%", "t": "75%"},    # Rozgrywający
        "II": {"l": "40%", "t": "75%"},   # Atakujący
        "III": {"l": "40%", "t": "48%"},  # Środkowy
        "IV": {"l": "40%", "t": "20%"},   # Przyjmujący
        "V": {"l": "15%", "t": "20%"},    # Przyjmujący
        "VI": {"l": "15%", "t": "48%"}    # Libero
    }
    
    # Pozycje przeciwnika (prawa strona boiska)
    opp_coords = {
        "I": {"l": "85%", "t": "75%"},
        "II": {"l": "60%", "t": "75%"},
        "III": {"l": "60%", "t": "48%"},
        "IV": {"l": "60%", "t": "20%"},
        "V": {"l": "85%", "t": "20%"},
        "VI": {"l": "85%", "t": "48%"}
    }

    # Przygotowanie pełnej struktury pozycji dla draw_court_live
    current_player_positions = {"us": {}, "opp": {}}
    for pos_key, coords in us_coords.items():
        p = get_player_by_position(pos_key, "us")
        current_player_positions["us"][pos_key] = {**coords, "nr": p["nr"], "nazwisko": p["nazwisko"]}
    for pos_key, coords in opp_coords.items():
        p = get_player_by_position(pos_key, "opp")
        current_player_positions["opp"][pos_key] = {**coords, "nr": p["nr"], "nazwisko": p["nazwisko"]}

    # --- 1. ZAGRYWKA ---
    if server_team == "us":
        server = get_player_by_position("I", team="us") # Zawsze I pozycja serwuje
        skill = get_effective_stat(server, "ser")
        apply_fatigue(server["id"], amount=2)
        
        phases.append({"comment": f"Sędzia gwizd! Zagrywka: {server['nazwisko']}.", "players": current_player_positions, "ball": us_coords["I"]})
        time.sleep(0.5)

        if random.randint(1, 100) > skill + 15: # Błąd serwisowy
            phases.append({"comment": f"Błąd serwisowy! {server['nazwisko']} w siatkę/aut.", "players": current_player_positions, "ball": {"l": "50%", "t": "50%"}})
            win_point_us = False
        else:
            phases.append({"comment": f"Potężna zagrywka {server['nazwisko']}!", "players": current_player_positions, "ball": {"l": "85%", "t": "75%"}})
            # Przyjęcie przez przeciwnika
            receiver_skill_opp = get_effective_stat(get_player_by_position("I", "opp"), "def") # Przykładowy receiver
            if random.randint(1, 100) > receiver_skill_opp + 10: # Błąd przyjęcia
                phases.append({"comment": "As serwisowy! Błąd przyjęcia przeciwnika.", "players": current_player_positions, "ball": {"l": "95%", "t": "5%"}})
                win_point_us = True
            else:
                phases.append({"comment": "Dobre przyjęcie przeciwnika, piłka w górze.", "players": current_player_positions, "ball": opp_coords["VI"]})
                phases.append({"comment": "Rozegranie do atakującego przeciwnika.", "players": current_player_positions, "ball": opp_coords["III"]})
                
                # --- Kontratak przeciwnika ---
                attacker_opp = get_player_by_position("II", team="opp") # Przykładowy atakujący przeciwnika
                atk_skill_opp = get_effective_stat(attacker_opp, "atk")
                
                blocker_us = get_player_by_position("III", team="us") # Nasz środkowy
                block_skill_us = get_effective_stat(blocker_us, "blk")
                apply_fatigue(blocker_us["id"], amount=3)

                phases.append({"comment": f"Atak przeciwnika! {attacker_opp['nazwisko']} uderza!", "players": current_player_positions, "ball": {"l": "60%", "t": "48%"}})
                
                if random.randint(1, 100) < block_skill_us - 10: # Udany blok
                    phases.append({"comment": f"BLOK! {blocker_us['nazwisko']} zatrzymuje atak!", "players": current_player_positions, "ball": us_coords["III"]})
                    win_point_us = True
                elif random.randint(1, 100) < atk_skill_opp: # Atak skuteczny
                    phases.append({"comment": "Skuteczny atak przeciwnika! Punkt dla nich.", "players": current_player_positions, "ball": {"l": "10%", "t": "30%"}})
                    win_point_us = False
                else: # Obrona
                    phases.append({"comment": "Piłka w boisku, obrona po naszej stronie!", "players": current_player_positions, "ball": us_coords["VI"]})
                    
                    # --- Nasz kontratak po obronie ---
                    setter_us = get_player_by_position("I", team="us")
                    set_skill_us = get_effective_stat(setter_us, "set")
                    apply_fatigue(setter_us["id"], amount=2)

                    phases.append({"comment": "Rozgrywający ustawia piłkę do ataku.", "players": current_player_positions, "ball": us_coords["I"]})
                    
                    attacker_us = get_player_by_position(random.choice(["II", "IV"]), team="us")
                    atk_skill_us = get_effective_stat(attacker_us, "atk")
                    apply_fatigue(attacker_us["id"], amount=4)
                    
                    blocker_opp = get_player_by_position("III", team="opp")
                    block_skill_opp = get_effective_stat(blocker_opp, "blk")

                    phases.append({"comment": f"GWÓŹDŹ! {attacker_us['nazwisko']} atakuje!", "players": current_player_positions, "ball": {"l": "40%", "t": "48%"}})

                    if random.randint(1, 100) < atk_skill_us + 10:
                        phases.append({"comment": "Piłka wbita w parkiet! Punkt dla nas!", "players": current_player_positions, "ball": {"l": "80%", "t": "30%"}})
                        win_point_us = True
                    elif random.randint(1, 100) < block_skill_opp - 15:
                        phases.append({"comment": "BLOK! Przeciwnik zatrzymuje atak!", "players": current_player_positions, "ball": opp_coords["III"]})
                        win_point_us = False
                    else:
                        phases.append({"comment": "Obrona przeciwnika. Długa wymiana!", "players": current_player_positions, "ball": {"l": "70%", "t": "30%"}})
                        win_point_us = False # Na razie upraszczamy, że długa wymiana kończy się dla przeciwnika
    else: # Serwis przeciwnika
        server_opp = get_player_by_position("I", team="opp")
        skill_opp = get_effective_stat(server_opp, "ser")

        phases.append({"comment": f"Zagrywka przeciwnika: {server_opp['nazwisko']}.", "players": current_player_positions, "ball": opp_coords["I"]})
        time.sleep(0.5)

        if random.randint(1, 100) > skill_opp + 15:
            phases.append({"comment": f"Błąd serwisowy przeciwnika! Piłka w aut.", "players": current_player_positions, "ball": {"l": "50%", "t": "50%"}})
            win_point_us = True
        else:
            phases.append({"comment": f"Mocna zagrywka {server_opp['nazwisko']}!", "players": current_player_positions, "ball": {"l": "15%", "t": "75%"}})
            
            receiver_us = get_player_by_position("I", team="us") # Rozgrywający na przyjęciu
            def_skill_us = get_effective_stat(receiver_us, "def")
            apply_fatigue(receiver_us["id"], amount=2)

            if random.randint(1, 100) > def_skill_us + 10:
                phases.append({"comment": "As serwisowy przeciwnika! Błąd przyjęcia.", "players": current_player_positions, "ball": {"l": "5%", "t": "95%"}})
                win_point_us = False
            else:
                phases.append({"comment": "Perfekcyjne przyjęcie! Piłka do rozgrywającego.", "players": current_player_positions, "ball": us_coords["VI"]})
                
                # --- Nasz atak po przyjęciu ---
                setter_us = get_player_by_position("I", team="us")
                set_skill_us = get_effective_stat(setter_us, "set")
                apply_fatigue(setter_us["id"], amount=2)

                phases.append({"comment": "Rozgrywający: Wiśniewski wystawia piłkę!", "players": current_player_positions, "ball": us_coords["I"]})
                
                attacker_us = get_player_by_position(random.choice(["II", "IV"]), team="us")
                atk_skill_us = get_effective_stat(attacker_us, "atk")
                apply_fatigue(attacker_us["id"], amount=4)

                blocker_opp = get_player_by_position("III", team="opp")
                block_skill_opp = get_effective_stat(blocker_opp, "blk")

                phases.append({"comment": f"Atak: {attacker_us['nazwisko']} uderza z całej siły!", "players": current_player_positions, "ball": {"l": "40%", "t": "48%"}})

                if random.randint(1, 100) < atk_skill_us:
                    phases.append({"comment": "Mocny atak przełamuje blok! Punkt dla nas!", "players": current_player_positions, "ball": {"l": "80%", "t": "30%"}})
                    win_point_us = True
                elif random.randint(1, 100) < block_skill_opp - 10:
                    phases.append({"comment": "Zablokowany! Przeciwnik stawia ścianę!", "players": current_player_positions, "ball": opp_coords["III"]})
                    win_point_us = False
                else:
                    phases.append({"comment": "Obrona przeciwnika, kontratak!", "players": current_player_positions, "ball": {"l": "70%", "t": "30%"}})
                    # Kontynuacja wymiany (upraszczamy na razie do punktu dla przeciwnika)
                    win_point_us = False


    return win_point_us, phases

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
    st.write("Wybierz zawodników na początkowe pozycje rotacji.")
    st.markdown("""
    **I (Rozgrywający/Libero tył)**<br>
    **II (Atakujący/Środkowy przód)**<br>
    **III (Środkowy/Rozgrywający przód)**<br>
    **IV (Przyjmujący/Atakujący przód)**<br>
    **V (Przyjmujący/Środkowy tył)**<br>
    **VI (Libero/Przyjmujący tył)**
    """)
    col_l, col_r = st.columns(2)
    
    players_list_options = {f"{p['imie']} {p['nazwisko']} ({p['poz']})": p["id"] for p in st.session_state.first_team}
    
    # Lista kluczy pozycji w ustalonej kolejności do wyświetlania
    ordered_positions = ["I", "II", "III", "IV", "V", "VI"]

    for i, pos in enumerate(ordered_positions):
        with (col_l if i < 3 else col_r):
            curr_val_id = st.session_state.starting_lineup[pos]
            curr_val_name = next(k for k, v in players_list_options.items() if v == curr_val_id)
            
            sel = st.selectbox(f"Pozycja {pos}", list(players_list_options.keys()), 
                               index=list(players_list_options.keys()).index(curr_val_name), key=f"pos_sel_{pos}")
            st.session_state.starting_lineup[pos] = players_list_options[sel]
    
    st.subheader("Kadra zawodników")
    df_players = pd.DataFrame(st.session_state.first_team)
    df_players_display = df_players[['nr', 'imie', 'nazwisko', 'poz', 'forma', 'fatigue']]
    df_players_display['atk'] = df_players['stats'].apply(lambda x: x['atk'])
    df_players_display['def'] = df_players['stats'].apply(lambda x: x['def'])
    df_players_display['ser'] = df_players['stats'].apply(lambda x: x['ser'])
    df
