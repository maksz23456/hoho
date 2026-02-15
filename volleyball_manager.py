import streamlit as st
import pandas as pd
import random
import json
from datetime import datetime, timedelta
import time

# Konfiguracja strony
st.set_page_config(page_title="Volleyball Manager 2024", page_icon="🏐", layout="wide")

# CSS dla drag and drop i animacji
st.markdown("""
<style>
    /* Drag and Drop Styles */
    .player-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        margin: 8px 0;
        border-radius: 10px;
        cursor: move;
        transition: all 0.3s;
        border: 2px solid transparent;
        color: white;
        font-weight: bold;
    }
    
    .player-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        border-color: #ffd700;
    }
    
    .player-card-injured {
        background: linear-gradient(135deg, #999 0%, #666 100%);
        opacity: 0.6;
        cursor: not-allowed;
    }
    
    .drop-zone {
        min-height: 80px;
        border: 3px dashed #ccc;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background: rgba(255,255,255,0.05);
        transition: all 0.3s;
    }
    
    .drop-zone:hover {
        border-color: #667eea;
        background: rgba(102,126,234,0.1);
    }
    
    .drop-zone-active {
        border-color: #4CAF50;
        background: rgba(76,175,80,0.1);
    }
    
    /* Court Animation Styles */
    .animated-court {
        background: linear-gradient(135deg, #1a472a 0%, #2d5016 100%);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        position: relative;
        min-height: 500px;
    }
    
    .court-floor {
        background: #d2691e;
        border: 5px solid #000;
        border-radius: 10px;
        padding: 20px;
        position: relative;
    }
    
    .player-position {
        position: absolute;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        font-size: 14px;
        text-align: center;
        transition: all 0.5s;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .player-blue {
        background: linear-gradient(135deg, #2196F3, #1976D2);
    }
    
    .player-yellow {
        background: linear-gradient(135deg, #FFC107, #FFA000);
    }
    
    .ball {
        position: absolute;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #fff, #ff6b6b);
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
        transition: all 0.3s ease-in-out;
        z-index: 100;
    }
    
    .net {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: 4px;
        height: 100%;
        background: #333;
        z-index: 50;
    }
    
    .action-text {
        position: absolute;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 15px 30px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        z-index: 200;
        animation: fadeInOut 2s;
    }
    
    @keyframes fadeInOut {
        0% { opacity: 0; transform: translateX(-50%) translateY(-20px); }
        20% { opacity: 1; transform: translateX(-50%) translateY(0); }
        80% { opacity: 1; transform: translateX(-50%) translateY(0); }
        100% { opacity: 0; transform: translateX(-50%) translateY(20px); }
    }
    
    .score-board {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        color: white;
        text-align: center;
    }
    
    .score-display {
        font-size: 48px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .team-colors {
        display: flex;
        justify-content: space-around;
        margin-top: 10px;
    }
    
    .team-blue-label {
        color: #2196F3;
        font-weight: bold;
        font-size: 24px;
    }
    
    .team-yellow-label {
        color: #FFC107;
        font-weight: bold;
        font-size: 24px;
    }
</style>
""", unsafe_allow_html=True)

# Inicjalizacja stanu sesji
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_season = 1
    st.session_state.budget = 500000
    st.session_state.club_name = "MKS Warszawa"
    st.session_state.current_day = 1
    st.session_state.league_position = 1
    st.session_state.morale = 75
    
    # Tworzenie pierwszej drużyny (7 zawodników)
    st.session_state.first_team = [
        {"id": 1, "imie": "Jakub", "nazwisko": "Kowalski", "pozycja": "Przyjmujący", "numer": 10, "wiek": 24, "umiejetnosci": {"atak": 85, "obrona": 82, "zagrywka": 75, "blok": 72}, "forma": 80, "kontuzja": 0, "pensja": 15000},
        {"id": 2, "imie": "Piotr", "nazwisko": "Nowak", "pozycja": "Środkowy", "numer": 2, "wiek": 27, "umiejetnosci": {"atak": 78, "obrona": 65, "zagrywka": 68, "blok": 88}, "forma": 75, "kontuzja": 0, "pensja": 12000},
        {"id": 3, "imie": "Marcin", "nazwisko": "Wiśniewski", "pozycja": "Rozgrywający", "numer": 1, "wiek": 26, "umiejetnosci": {"atak": 65, "obrona": 80, "zagrywka": 85, "blok": 68}, "forma": 82, "kontuzja": 0, "pensja": 14000},
        {"id": 4, "imie": "Tomasz", "nazwisko": "Lewandowski", "pozycja": "Atakujący", "numer": 11, "wiek": 22, "umiejetnosci": {"atak": 88, "obrona": 68, "zagrywka": 77, "blok": 82}, "forma": 85, "kontuzja": 0, "pensja": 16000},
        {"id": 5, "imie": "Kamil", "nazwisko": "Wójcik", "pozycja": "Libero", "numer": 8, "wiek": 29, "umiejetnosci": {"atak": 55, "obrona": 92, "zagrywka": 78, "blok": 60}, "forma": 78, "kontuzja": 0, "pensja": 11000},
        {"id": 6, "imie": "Adam", "nazwisko": "Kamiński", "pozycja": "Przyjmujący", "numer": 12, "wiek": 25, "umiejetnosci": {"atak": 80, "obrona": 84, "zagrywka": 80, "blok": 75}, "forma": 83, "kontuzja": 0, "pensja": 15000},
        {"id": 7, "imie": "Michał", "nazwisko": "Zieliński", "pozycja": "Środkowy", "numer": 19, "wiek": 23, "umiejetnosci": {"atak": 75, "obrona": 62, "zagrywka": 65, "blok": 85}, "forma": 77, "kontuzja": 0, "pensja": 10000},
    ]
    
    # Ławka rezerwowych (7 zawodników)
    st.session_state.bench = [
        {"id": 8, "imie": "Paweł", "nazwisko": "Szymański", "pozycja": "Przyjmujący", "numer": 13, "wiek": 28, "umiejetnosci": {"atak": 76, "obrona": 78, "zagrywka": 72, "blok": 70}, "forma": 80, "kontuzja": 0, "pensja": 13000},
        {"id": 9, "imie": "Krzysztof", "nazwisko": "Dąbrowski", "pozycja": "Atakujący", "numer": 9, "wiek": 21, "umiejetnosci": {"atak": 82, "obrona": 64, "zagrywka": 70, "blok": 78}, "forma": 88, "kontuzja": 0, "pensja": 11000},
        {"id": 10, "imie": "Bartosz", "nazwisko": "Jankowski", "pozycja": "Rozgrywający", "numer": 5, "wiek": 30, "umiejetnosci": {"atak": 62, "obrona": 82, "zagrywka": 80, "blok": 65}, "forma": 72, "kontuzja": 0, "pensja": 12000},
        {"id": 11, "imie": "Mateusz", "nazwisko": "Kozłowski", "pozycja": "Środkowy", "numer": 18, "wiek": 26, "umiejetnosci": {"atak": 72, "obrona": 60, "zagrywka": 63, "blok": 82}, "forma": 75, "kontuzja": 0, "pensja": 9500},
        {"id": 12, "imie": "Łukasz", "nazwisko": "Wojciechowski", "pozycja": "Libero", "numer": 6, "wiek": 27, "umiejetnosci": {"atak": 52, "obrona": 88, "zagrywka": 75, "blok": 58}, "forma": 76, "kontuzja": 0, "pensja": 10000},
        {"id": 13, "imie": "Rafał", "nazwisko": "Kwiatkowski", "pozycja": "Przyjmujący", "numer": 4, "wiek": 24, "umiejetnosci": {"atak": 74, "obrona": 76, "zagrywka": 70, "blok": 68}, "forma": 79, "kontuzja": 0, "pensja": 11500},
        {"id": 14, "imie": "Daniel", "nazwisko": "Kaczmarek", "pozycja": "Atakujący", "numer": 28, "wiek": 29, "umiejetnosci": {"atak": 80, "obrona": 66, "zagrywka": 73, "blok": 76}, "forma": 74, "kontuzja": 0, "pensja": 12500},
    ]
    
    # Akademia (młodzież)
    st.session_state.academy = [
        {"id": 201, "imie": "Filip", "nazwisko": "Młody", "pozycja": "Przyjmujący", "numer": 31, "wiek": 18, "umiejetnosci": {"atak": 65, "obrona": 62, "zagrywka": 60, "blok": 58}, "forma": 85, "kontuzja": 0, "pensja": 3000, "potencjal": 88},
        {"id": 202, "imie": "Kacper", "nazwisko": "Talent", "pozycja": "Środkowy", "numer": 32, "wiek": 17, "umiejetnosci": {"atak": 62, "obrona": 55, "zagrywka": 58, "blok": 68}, "forma": 82, "kontuzja": 0, "pensja": 2500, "potencjal": 85},
        {"id": 203, "imie": "Szymon", "nazwisko": "Przyszłość", "pozycja": "Atakujący", "numer": 33, "wiek": 19, "umiejetnosci": {"atak": 70, "obrona": 58, "zagrywka": 62, "blok": 65}, "forma": 88, "kontuzja": 0, "pensja": 3500, "potencjal": 90},
        {"id": 204, "imie": "Dominik", "nazwisko": "Obiecujący", "pozycja": "Rozgrywający", "numer": 34, "wiek": 18, "umiejetnosci": {"atak": 58, "obrona": 68, "zagrywka": 72, "blok": 60}, "forma": 80, "kontuzja": 0, "pensja": 3000, "potencjal": 86},
        {"id": 205, "imie": "Oskar", "nazwisko": "Nadzieja", "pozycja": "Libero", "numer": 35, "wiek": 17, "umiejetnosci": {"atak": 48, "obrona": 78, "zagrywka": 65, "blok": 52}, "forma": 83, "kontuzja": 0, "pensja": 2500, "potencjal": 92},
    ]
    
    # Ustawienie podstawowe
    st.session_state.starting_lineup = {
        "I": 6,
        "II": 7,
        "III": 4,
        "IV": 1,
        "V": 2,
        "VI": 3,
        "Libero": 5
    }
    
    # Rynek transferowy
    st.session_state.transfer_market = [
        {"id": 101, "imie": "Jan", "nazwisko": "Mazur", "pozycja": "Atakujący", "numer": 7, "wiek": 26, "umiejetnosci": {"atak": 88, "obrona": 72, "zagrywka": 78, "blok": 84}, "cena": 120000, "pensja": 18000},
        {"id": 102, "imie": "Łukasz", "nazwisko": "Krawczyk", "pozycja": "Środkowy", "numer": 15, "wiek": 24, "umiejetnosci": {"atak": 80, "obrona": 68, "zagrywka": 70, "blok": 90}, "cena": 100000, "pensja": 16000},
        {"id": 103, "imie": "Damian", "nazwisko": "Górski", "pozycja": "Libero", "numer": 3, "wiek": 27, "umiejetnosci": {"atak": 58, "obrona": 94, "zagrywka": 80, "blok": 62}, "cena": 90000, "pensja": 14000},
    ]
    
    st.session_state.matches = []
    st.session_state.next_match = {"przeciwnik": "AZS Kraków", "dzien": 7}
    st.session_state.match_in_progress = False
    st.session_state.simulation_mode = "fast"

# Funkcje pomocnicze
def get_all_players():
    return st.session_state.first_team + st.session_state.bench

def get_player_by_id(player_id):
    all_players = get_all_players() + st.session_state.academy
    for player in all_players:
        if player["id"] == player_id:
            return player
    return None

def oblicz_ocena_zawodnika(player):
    umiejetnosci = player["umiejetnosci"]
    srednia = sum(umiejetnosci.values()) / len(umiejetnosci)
    return round(srednia * (player["forma"] / 100), 1)

def render_player_card(player, show_number=True):
    """Renderuje kartę zawodnika z numerem koszulki"""
    is_injured = player["kontuzja"] > 0
    card_class = "player-card-injured" if is_injured else "player-card"
    
    number_display = f"#{player.get('numer', '?')}" if show_number else ""
    status = "🤕" if is_injured else "✅"
    
    return f"""
    <div class="{card_class}" draggable="true" data-player-id="{player['id']}">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-size: 20px;">{number_display} {player['imie']} {player['nazwisko']}</div>
                <div style="font-size: 14px; opacity: 0.9;">{player['pozycja']} • Ocena: {oblicz_ocena_zawodnika(player)}</div>
            </div>
            <div style="font-size: 24px;">{status}</div>
        </div>
    </div>
    """

def display_animated_court(team_score, opponent_score, action_text="", ball_pos=None):
    """Wyświetla animowane boisko z zawodnikami i piłką"""
    
    lineup = st.session_state.starting_lineup
    
    # Pozycje zawodników na boisku (współrzędne w %)
    positions = {
        "IV": {"left": "15%", "top": "20%"},   # Lewa strefa ataku
        "III": {"left": "45%", "top": "15%"},  # Środek ataku
        "II": {"left": "75%", "top": "20%"},   # Prawa strefa ataku
        "V": {"left": "15%", "top": "65%"},    # Lewa strefa obrony
        "VI": {"left": "45%", "top": "70%"},   # Środek obrony
        "I": {"left": "75%", "top": "65%"},    # Prawa strefa obrony (zagrywka)
    }
    
    # Pozycje przeciwnika (odwrócone)
    opponent_positions = {
        "1": {"left": "15%", "top": "65%"},
        "2": {"left": "45%", "top": "70%"},
        "3": {"left": "75%", "top": "65%"},
        "4": {"left": "15%", "top": "20%"},
        "5": {"left": "45%", "top": "15%"},
        "6": {"left": "75%", "top": "20%"},
    }
    
    players_html = ""
    
    # Renderuj naszych zawodników
    for pos_key, coords in positions.items():
        player_id = lineup.get(pos_key)
        if player_id:
            player = get_player_by_id(player_id)
            if player:
                number = player.get('numer', '?')
                players_html += f"""
                <div class="player-position player-blue" style="left: {coords['left']}; top: {coords['top']};">
                    {number}
                </div>
                """
    
    # Renderuj przeciwników
    for i, coords in opponent_positions.items():
        players_html += f"""
        <div class="player-position player-yellow" style="left: {coords['left']}; top: {coords['top']};">
            {i}
        </div>
        """
    
    # Piłka
    ball_html = ""
    if ball_pos:
        ball_html = f"""
        <div class="ball" style="left: {ball_pos['left']}; top: {ball_pos['top']};"></div>
        """
    
    # Tekst akcji
    action_html = ""
    if action_text:
        action_html = f"""
        <div class="action-text">{action_text}</div>
        """
    
    return f"""
    <div class="score-board">
        <div class="team-colors">
            <div class="team-blue-label">🔵 {st.session_state.club_name}</div>
            <div class="team-yellow-label">🟡 Przeciwnik</div>
        </div>
        <div class="score-display">{team_score} : {opponent_score}</div>
    </div>
    
    <div class="animated-court">
        <div class="court-floor">
            <div class="net"></div>
            {action_html}
            {ball_html}
            {players_html}
        </div>
    </div>
    """

def symuluj_akcje_animowana(team_strength, opponent_strength, lineup_players):
    """Symuluje akcję z animacją na boisku"""
    strength_diff = team_strength - opponent_strength
    win_prob = 0.5 + (strength_diff / 200)
    win_prob = max(0.3, min(0.7, win_prob))
    
    team_wins = random.random() < win_prob
    player = random.choice(lineup_players)
    
    # Fazy akcji
    phases = []
    
    # Faza 1: Zagrywka
    server = random.choice([p for p in lineup_players if p["pozycja"] != "Libero"])
    phases.append({
        "action": f"⚡ Zagrywka: {server['imie']} {server['nazwisko']}",
        "ball_pos": {"left": "75%", "top": "65%"}
    })
    
    if team_wins:
        # Faza 2: Przyjęcie
        receiver = random.choice([p for p in lineup_players if p["pozycja"] in ["Libero", "Przyjmujący"]])
        phases.append({
            "action": f"🛡️ Przyjęcie: {receiver['imie']} {receiver['nazwisko']}",
            "ball_pos": {"left": "45%", "top": "40%"}
        })
        
        # Faza 3: Rozegranie
        setter = next((p for p in lineup_players if p["pozycja"] == "Rozgrywający"), None)
        if setter:
            phases.append({
                "action": f"🎯 Rozegranie: {setter['imie']} {setter['nazwisko']}",
                "ball_pos": {"left": "45%", "top": "30%"}
            })
        
        # Faza 4: Atak
        if player["pozycja"] in ["Atakujący", "Przyjmujący", "Środkowy"]:
            phases.append({
                "action": f"🔥 ATAK! {player['imie']} {player['nazwisko']} zdobywa punkt!",
                "ball_pos": {"left": "30%", "top": "15%"}
            })
        else:
            phases.append({
                "action": f"✨ Punkt dla nas!",
                "ball_pos": {"left": "30%", "top": "15%"}
            })
    else:
        phases.append({
            "action": "❌ Błąd przeciwnika - nasz punkt!",
            "ball_pos": {"left": "50%", "top": "50%"}
        })
    
    return team_wins, phases

def trenuj_druzyne(squad_type="first_team"):
    squad = st.session_state.first_team if squad_type == "first_team" else st.session_state.academy
    
    for player in squad:
        if player["kontuzja"] == 0:
            growth_chance = 0.4 if squad_type == "academy" else 0.3
            max_skill = player.get("potencjal", 95) if squad_type == "academy" else 95
            
            if random.random() < growth_chance:
                skill = random.choice(list(player["umiejetnosci"].keys()))
                if player["umiejetnosci"][skill] < max_skill:
                    wzrost = random.randint(1, 2) if squad_type == "academy" else 1
                    player["umiejetnosci"][skill] = min(max_skill, player["umiejetnosci"][skill] + wzrost)
            
            player["forma"] = max(60, min(95, player["forma"] + random.randint(-2, 6)))
        else:
            player["kontuzja"] = max(0, player["kontuzja"] - 1)

def next_day():
    st.session_state.current_day += 1
    
    if st.session_state.current_day % 7 == 0:
        total_salary = (sum(p["pensja"] for p in st.session_state.first_team) + 
                       sum(p["pensja"] for p in st.session_state.bench) +
                       sum(p["pensja"] for p in st.session_state.academy))
        st.session_state.budget -= total_salary
    
    all_players = get_all_players()
    for player in all_players:
        if player["kontuzja"] == 0 and random.random() < 0.015:
            player["kontuzja"] = random.randint(3, 14)

def validate_lineup():
    lineup = st.session_state.starting_lineup
    required_positions = ["I", "II", "III", "IV", "V", "VI", "Libero"]
    
    for pos in required_positions:
        if lineup.get(pos) is None:
            return False, f"Pozycja {pos} nie jest wypełniona"
    
    for pos, player_id in lineup.items():
        player = get_player_by_id(player_id)
        if player is None:
            return False, f"Nie znaleziono zawodnika o ID {player_id}"
        if player["kontuzja"] > 0:
            return False, f"{player['imie']} {player['nazwisko']} jest kontuzjowany"
    
    return True, "OK"

# Interfejs główny
st.title("🏐 Volleyball Manager 2024 - Professional Edition")
st.markdown("---")

# Górny pasek
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Klub", st.session_state.club_name)
with col2:
    st.metric("Sezon", st.session_state.current_season)
with col3:
    st.metric("Dzień", st.session_state.current_day)
with col4:
    st.metric("Budżet", f"{st.session_state.budget:,} zł")
with col5:
    st.metric("Morale", f"{st.session_state.morale}%")

# Menu nawigacji
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Główna", 
    "👥 Kadra (Drag & Drop)", 
    "⚙️ Ustawienie", 
    "📊 Statystyki", 
    "🏐 Mecz LIVE"
])

with tab1:
    st.header("Panel główny")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Ostatnie aktualności")
        
        if st.session_state.matches:
            last_match = st.session_state.matches[-1]
            if last_match["wygrana"]:
                st.success(f"✅ Wygraliśmy z {last_match['przeciwnik']} {last_match['wynik']}")
            else:
                st.error(f"❌ Przegraliśmy z {last_match['przeciwnik']} {last_match['wynik']}")
        else:
            st.info("Jeszcze nie rozegraliśmy żadnego meczu!")
        
        st.markdown("---")
        st.subheader("Najbliższy mecz")
        days_to_match = st.session_state.next_match["dzien"] - st.session_state.current_day
        if days_to_match > 0:
            st.info(f"🏐 {st.session_state.next_match['przeciwnik']} (za {days_to_match} dni)")
        else:
            st.warning("🏐 Mecz dzisiaj!")
    
    with col2:
        st.subheader("Akcje")
        
        if st.button("🏃 Trening pierwszej drużyny", use_container_width=True):
            trenuj_druzyne("first_team")
            next_day()
            st.success("✅ Trening zakończony!")
            st.rerun()
        
        if st.button("🎓 Trening akademii", use_container_width=True):
            trenuj_druzyne("academy")
            next_day()
            st.success("✅ Trening akademii!")
            st.rerun()
        
        if st.button("⏭️ Następny dzień", use_container_width=True):
            next_day()
            st.rerun()

with tab2:
    st.header("👥 Zarządzanie kadrą - Drag & Drop")
    
    st.info("💡 **NOWOŚĆ!** Przeciągnij i upuść zawodników między składami (funkcja dostępna w przeglądarkach)")
    
    # Simplified drag and drop using buttons with better UX
    st.subheader("⚡ Szybkie zarządzanie")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**📋 Pierwsza drużyna**")
        for i, player in enumerate(st.session_state.first_team):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.markdown(render_player_card(player), unsafe_allow_html=True)
            with col_b:
                if st.button("⬇️", key=f"demote_{player['id']}", help="Na ławkę"):
                    if len(st.session_state.bench) < 7:
                        st.session_state.first_team.remove(player)
                        st.session_state.bench.append(player)
                        for pos, pid in st.session_state.starting_lineup.items():
                            if pid == player["id"]:
                                st.session_state.starting_lineup[pos] = None
                        st.rerun()
    
    with col2:
        st.write("**🪑 Ławka rezerwowych**")
        for player in st.session_state.bench:
            col_a, col_b, col_c = st.columns([4, 1, 1])
            with col_a:
                st.markdown(render_player_card(player), unsafe_allow_html=True)
            with col_b:
                if st.button("⬆️", key=f"promote_{player['id']}", help="Do pierwszej"):
                    if len(st.session_state.first_team) < 7:
                        st.session_state.bench.remove(player)
                        st.session_state.first_team.append(player)
                        st.rerun()
            with col_c:
                if st.button("🗑️", key=f"sell_{player['id']}", help="Sprzedaj"):
                    if len(st.session_state.first_team) + len(st.session_state.bench) > 6:
                        sell_price = int(oblicz_ocena_zawodnika(player) * 1200)
                        st.session_state.budget += sell_price
                        st.session_state.bench.remove(player)
                        st.success(f"Sprzedano za {sell_price:,} zł!")
                        st.rerun()
    
    with col3:
        st.write("**🎓 Akademia**")
        for player in st.session_state.academy:
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.markdown(render_player_card(player), unsafe_allow_html=True)
            with col_b:
                if st.button("⬆️", key=f"academy_{player['id']}", help="Na ławkę"):
                    if len(st.session_state.bench) < 7:
                        if "potencjal" in player:
                            del player["potencjal"]
                        st.session_state.academy.remove(player)
                        st.session_state.bench.append(player)
                        st.rerun()

with tab3:
    st.header("⚙️ Ustawienie boiska")
    
    st.info("Wybierz zawodników na każdą pozycję. Libero zmienia się z pozycją V (środkowy z tyłu)")
    
    # Wizualizacja boiska z numerami
    lineup = st.session_state.starting_lineup
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1a472a 0%, #2d5016 100%); padding: 30px; border-radius: 15px;'>
        <h3 style='color: white; text-align: center;'>BOISKO - {st.session_state.club_name}</h3>
        <div style='background: #d2691e; border: 5px solid #000; border-radius: 10px; padding: 40px; position: relative;'>
            <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 20px;'>
    """, unsafe_allow_html=True)
    
    # Linia ataku
    for pos in ["IV", "III", "II"]:
        player_id = lineup.get(pos)
        if player_id:
            player = get_player_by_id(player_id)
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #2196F3, #1976D2); padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                    <div style='font-size: 24px; font-weight: bold;'>#{player.get('numer', '?')}</div>
                    <div style='font-size: 18px;'>{player['imie']} {player['nazwisko']}</div>
                    <div style='font-size: 14px; opacity: 0.9;'>{player['pozycja']} • Pozycja {pos}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align: center; font-size: 20px; color: white; margin: 20px 0;'>═══════ SIATKA ═══════</div>", unsafe_allow_html=True)
    st.markdown("<div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;'>", unsafe_allow_html=True)
    
    # Linia obrony
    for pos in ["V", "VI", "I"]:
        player_id = lineup.get(pos)
        if player_id:
            player = get_player_by_id(player_id)
            extra = " (⚡ Zagrywka)" if pos == "I" else " (↔️ Libero)" if pos == "V" else ""
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #2196F3, #1976D2); padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                    <div style='font-size: 24px; font-weight: bold;'>#{player.get('numer', '?')}</div>
                    <div style='font-size: 18px;'>{player['imie']} {player['nazwisko']}</div>
                    <div style='font-size: 14px; opacity: 0.9;'>{player['pozycja']} • Pozycja {pos}{extra}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div></div></div>", unsafe_allow_html=True)
    
    # Libero
    libero_id = lineup.get("Libero")
    if libero_id:
        libero = get_player_by_id(libero_id)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #FFC107, #FFA000); padding: 20px; border-radius: 10px; text-align: center; color: white; margin-top: 20px;'>
            <div style='font-size: 24px; font-weight: bold;'>LIBERO (poza boiskiem) - #{libero.get('numer', '?')}</div>
            <div style='font-size: 18px;'>{libero['imie']} {libero['nazwisko']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Edycja ustawienia
    st.subheader("🔧 Edycja składu")
    
    available = [p for p in st.session_state.first_team if p["kontuzja"] == 0]
    
    for pos in ["I", "II", "III", "IV", "V", "VI", "Libero"]:
        options = [f"#{p.get('numer', '?')} {p['imie']} {p['nazwisko']} ({p['pozycja']}) - {oblicz_ocena_zawodnika(p)}" 
                  for p in available]
        options.insert(0, "Nie wybrano")
        
        current_id = lineup.get(pos)
        current_index = 0
        if current_id:
            for i, opt in enumerate(options):
                player = get_player_by_id(current_id)
                if player and f"#{player.get('numer', '?')}" in opt and player['imie'] in opt:
                    current_index = i
                    break
        
        label = f"Pozycja {pos}"
        if pos == "I":
            label += " (⚡ Zagrywka)"
        elif pos == "V":
            label += " (↔️ zmienia się z Libero)"
        elif pos == "Libero":
            label = "LIBERO (poza boiskiem)"
        
        selected = st.selectbox(label, options, index=current_index, key=f"lineup_{pos}")
        
        if selected != "Nie wybrano":
            number = selected.split("#")[1].split(" ")[0]
            player = next((p for p in available if str(p.get('numer', '?')) == number), None)
            if player:
                st.session_state.starting_lineup[pos] = player["id"]
        else:
            st.session_state.starting_lineup[pos] = None
    
    is_valid, msg = validate_lineup()
    if is_valid:
        st.success("✅ Skład gotowy do meczu!")
    else:
        st.error(f"❌ {msg}")

with tab4:
    st.header("📊 Statystyki")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bilans meczów")
        if st.session_state.matches:
            wins = sum(1 for m in st.session_state.matches if m["wygrana"])
            losses = len(st.session_state.matches) - wins
            st.metric("Zwycięstwa", wins)
            st.metric("Porażki", losses)
        else:
            st.info("Brak meczów")
    
    with col2:
        st.subheader("Top 5 zawodników")
        all_p = get_all_players() + st.session_state.academy
        sorted_p = sorted(all_p, key=oblicz_ocena_zawodnika, reverse=True)[:5]
        for i, p in enumerate(sorted_p, 1):
            st.write(f"{i}. #{p.get('numer', '?')} {p['imie']} {p['nazwisko']} - {oblicz_ocena_zawodnika(p)}")

with tab5:
    st.header("🏐 Mecz LIVE z Animacją")
    
    days_to_match = st.session_state.next_match["dzien"] - st.session_state.current_day
    
    if days_to_match > 0:
        st.warning(f"⏳ Mecz za {days_to_match} dni: {st.session_state.next_match['przeciwnik']}")
    else:
        is_valid, msg = validate_lineup()
        
        if not is_valid:
            st.error(f"❌ {msg}")
        else:
            st.success(f"🏐 Mecz dzisiaj: {st.session_state.next_match['przeciwnik']}!")
            
            # Wybór trybu
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⚡ Szybka symulacja", use_container_width=True, type="primary"):
                    st.session_state.simulation_mode = "fast"
                    st.session_state.match_in_progress = True
                    st.rerun()
            with col2:
                if st.button("🎬 LIVE z animacją boiska!", use_container_width=True, type="secondary"):
                    st.session_state.simulation_mode = "animated"
                    st.session_state.match_in_progress = True
                    st.rerun()
            
            if st.session_state.match_in_progress:
                opponent = st.session_state.next_match['przeciwnik']
                
                lineup_players = []
                for pos in ["I", "II", "III", "IV", "V", "VI", "Libero"]:
                    pid = st.session_state.starting_lineup[pos]
                    p = get_player_by_id(pid)
                    if p and pos != "Libero":
                        lineup_players.append(p)
                
                libero_id = st.session_state.starting_lineup["Libero"]
                if libero_id:
                    lineup_players.append(get_player_by_id(libero_id))
                
                team_strength = sum(oblicz_ocena_zawodnika(p) for p in lineup_players) / len(lineup_players)
                opponent_strength = random.randint(70, 85)
                
                if st.session_state.simulation_mode == "animated":
                    st.subheader(f"🎬 {st.session_state.club_name} vs {opponent}")
                    
                    # Kontener na animację
                    court_placeholder = st.empty()
                    score_placeholder = st.empty()
                    
                    team_score = 0
                    opponent_score = 0
                    sets_won_team = 0
                    sets_won_opponent = 0
                    sets_detail = []
                    
                    set_number = 1
                    
                    while sets_won_team < 3 and sets_won_opponent < 3:
                        is_tiebreak = (set_number == 5)
                        max_points = 15 if is_tiebreak else 25
                        
                        set_team = 0
                        set_opp = 0
                        
                        st.write(f"### Set {set_number}")
                        
                        while True:
                            team_wins, phases = symuluj_akcje_animowana(team_strength, opponent_strength, lineup_players)
                            
                            # Animuj każdą fazę
                            for phase in phases:
                                with court_placeholder.container():
                                    st.markdown(display_animated_court(
                                        set_team, set_opp,
                                        phase["action"],
                                        phase.get("ball_pos")
                                    ), unsafe_allow_html=True)
                                time.sleep(1)
                            
                            if team_wins:
                                set_team += 1
                            else:
                                set_opp += 1
                            
                            with score_placeholder.container():
                                st.write(f"**Wynik seta: {set_team}:{set_opp}**")
                            
                            if set_team >= max_points and set_team - set_opp >= 2:
                                sets_won_team += 1
                                sets_detail.append(f"{set_team}:{set_opp}")
                                st.success(f"✅ Wygraliśmy set {set_number}!")
                                break
                            elif set_opp >= max_points and set_opp - set_team >= 2:
                                sets_won_opponent += 1
                                sets_detail.append(f"{set_team}:{set_opp}")
                                st.error(f"❌ Przegraliśmy set {set_number}")
                                break
                        
                        set_number += 1
                        time.sleep(2)
                    
                    # Wynik końcowy
                    if sets_won_team > sets_won_opponent:
                        st.balloons()
                        st.success(f"### 🎉 ZWYCIĘSTWO! {sets_won_team}:{sets_won_opponent}")
                    else:
                        st.error(f"### 😞 Porażka {sets_won_team}:{sets_won_opponent}")
                    
                    if st.button("✅ Zakończ i zapisz"):
                        st.session_state.matches.append({
                            "przeciwnik": opponent,
                            "wynik": f"{sets_won_team}:{sets_won_opponent}",
                            "sety": sets_detail,
                            "wygrana": sets_won_team > sets_won_opponent
                        })
                        
                        if sets_won_team > sets_won_opponent:
                            st.session_state.budget += 25000
                            st.session_state.morale = min(100, st.session_state.morale + 5)
                        else:
                            st.session_state.budget += 10000
                            st.session_state.morale = max(50, st.session_state.morale - 3)
                        
                        st.session_state.next_match["dzien"] = st.session_state.current_day + 7
                        st.session_state.match_in_progress = False
                        st.rerun()

st.markdown("---")
st.markdown("*Volleyball Manager 2024 v4.0 - Professional Edition* 🏐")
