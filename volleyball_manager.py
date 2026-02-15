import streamlit as st
import pandas as pd
import random
import json
from datetime import datetime, timedelta
import time

# Konfiguracja strony
st.set_page_config(page_title="Volleyball Manager 2024", page_icon="🏐", layout="wide")

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
        {"id": 1, "imie": "Jakub", "nazwisko": "Kowalski", "pozycja": "Przyjmujący", "wiek": 24, "umiejetnosci": {"atak": 85, "obrona": 82, "zagrywka": 75, "blok": 72}, "forma": 80, "kontuzja": 0, "pensja": 15000},
        {"id": 2, "imie": "Piotr", "nazwisko": "Nowak", "pozycja": "Środkowy", "wiek": 27, "umiejetnosci": {"atak": 78, "obrona": 65, "zagrywka": 68, "blok": 88}, "forma": 75, "kontuzja": 0, "pensja": 12000},
        {"id": 3, "imie": "Marcin", "nazwisko": "Wiśniewski", "pozycja": "Rozgrywający", "wiek": 26, "umiejetnosci": {"atak": 65, "obrona": 80, "zagrywka": 85, "blok": 68}, "forma": 82, "kontuzja": 0, "pensja": 14000},
        {"id": 4, "imie": "Tomasz", "nazwisko": "Lewandowski", "pozycja": "Atakujący", "wiek": 22, "umiejetnosci": {"atak": 88, "obrona": 68, "zagrywka": 77, "blok": 82}, "forma": 85, "kontuzja": 0, "pensja": 16000},
        {"id": 5, "imie": "Kamil", "nazwisko": "Wójcik", "pozycja": "Libero", "wiek": 29, "umiejetnosci": {"atak": 55, "obrona": 92, "zagrywka": 78, "blok": 60}, "forma": 78, "kontuzja": 0, "pensja": 11000},
        {"id": 6, "imie": "Adam", "nazwisko": "Kamiński", "pozycja": "Przyjmujący", "wiek": 25, "umiejetnosci": {"atak": 80, "obrona": 84, "zagrywka": 80, "blok": 75}, "forma": 83, "kontuzja": 0, "pensja": 15000},
        {"id": 7, "imie": "Michał", "nazwisko": "Zieliński", "pozycja": "Środkowy", "wiek": 23, "umiejetnosci": {"atak": 75, "obrona": 62, "zagrywka": 65, "blok": 85}, "forma": 77, "kontuzja": 0, "pensja": 10000},
    ]
    
    # Ławka rezerwowych (7 zawodników)
    st.session_state.bench = [
        {"id": 8, "imie": "Paweł", "nazwisko": "Szymański", "pozycja": "Przyjmujący", "wiek": 28, "umiejetnosci": {"atak": 76, "obrona": 78, "zagrywka": 72, "blok": 70}, "forma": 80, "kontuzja": 0, "pensja": 13000},
        {"id": 9, "imie": "Krzysztof", "nazwisko": "Dąbrowski", "pozycja": "Atakujący", "wiek": 21, "umiejetnosci": {"atak": 82, "obrona": 64, "zagrywka": 70, "blok": 78}, "forma": 88, "kontuzja": 0, "pensja": 11000},
        {"id": 10, "imie": "Bartosz", "nazwisko": "Jankowski", "pozycja": "Rozgrywający", "wiek": 30, "umiejetnosci": {"atak": 62, "obrona": 82, "zagrywka": 80, "blok": 65}, "forma": 72, "kontuzja": 0, "pensja": 12000},
        {"id": 11, "imie": "Mateusz", "nazwisko": "Kozłowski", "pozycja": "Środkowy", "wiek": 26, "umiejetnosci": {"atak": 72, "obrona": 60, "zagrywka": 63, "blok": 82}, "forma": 75, "kontuzja": 0, "pensja": 9500},
        {"id": 12, "imie": "Łukasz", "nazwisko": "Wojciechowski", "pozycja": "Libero", "wiek": 27, "umiejetnosci": {"atak": 52, "obrona": 88, "zagrywka": 75, "blok": 58}, "forma": 76, "kontuzja": 0, "pensja": 10000},
        {"id": 13, "imie": "Rafał", "nazwisko": "Kwiatkowski", "pozycja": "Przyjmujący", "wiek": 24, "umiejetnosci": {"atak": 74, "obrona": 76, "zagrywka": 70, "blok": 68}, "forma": 79, "kontuzja": 0, "pensja": 11500},
        {"id": 14, "imie": "Daniel", "nazwisko": "Kaczmarek", "pozycja": "Atakujący", "wiek": 29, "umiejetnosci": {"atak": 80, "obrona": 66, "zagrywka": 73, "blok": 76}, "forma": 74, "kontuzja": 0, "pensja": 12500},
    ]
    
    # Akademia (młodzież)
    st.session_state.academy = [
        {"id": 201, "imie": "Filip", "nazwisko": "Młody", "pozycja": "Przyjmujący", "wiek": 18, "umiejetnosci": {"atak": 65, "obrona": 62, "zagrywka": 60, "blok": 58}, "forma": 85, "kontuzja": 0, "pensja": 3000, "potencjal": 88},
        {"id": 202, "imie": "Kacper", "nazwisko": "Talent", "pozycja": "Środkowy", "wiek": 17, "umiejetnosci": {"atak": 62, "obrona": 55, "zagrywka": 58, "blok": 68}, "forma": 82, "kontuzja": 0, "pensja": 2500, "potencjal": 85},
        {"id": 203, "imie": "Szymon", "nazwisko": "Przyszłość", "pozycja": "Atakujący", "wiek": 19, "umiejetnosci": {"atak": 70, "obrona": 58, "zagrywka": 62, "blok": 65}, "forma": 88, "kontuzja": 0, "pensja": 3500, "potencjal": 90},
        {"id": 204, "imie": "Dominik", "nazwisko": "Obiecujący", "pozycja": "Rozgrywający", "wiek": 18, "umiejetnosci": {"atak": 58, "obrona": 68, "zagrywka": 72, "blok": 60}, "forma": 80, "kontuzja": 0, "pensja": 3000, "potencjal": 86},
        {"id": 205, "imie": "Oskar", "nazwisko": "Nadzieja", "pozycja": "Libero", "wiek": 17, "umiejetnosci": {"atak": 48, "obrona": 78, "zagrywka": 65, "blok": 52}, "forma": 83, "kontuzja": 0, "pensja": 2500, "potencjal": 92},
    ]
    
    # Ustawienie podstawowe (pozycje na boisku według numeracji I-VI)
    st.session_state.starting_lineup = {
        "I": 6,      # Pozycja I (Przyjmujący/Atakujący w zagrywce)
        "II": 7,     # Pozycja II (Środkowy przy siatce)
        "III": 4,    # Pozycja III (Atakujący przy siatce)
        "IV": 1,     # Pozycja IV (Przyjmujący przy siatce)
        "V": 2,      # Pozycja V (Środkowy z tyłu - ZMIENIA SIĘ Z LIBERO)
        "VI": 3,     # Pozycja VI (Rozgrywający z tyłu)
        "Libero": 5  # Libero (poza boiskiem, zmienia się z pozycją V)
    }
    
    # Rynek transferowy
    st.session_state.transfer_market = [
        {"id": 101, "imie": "Jan", "nazwisko": "Mazur", "pozycja": "Atakujący", "wiek": 26, "umiejetnosci": {"atak": 88, "obrona": 72, "zagrywka": 78, "blok": 84}, "cena": 120000, "pensja": 18000},
        {"id": 102, "imie": "Łukasz", "nazwisko": "Krawczyk", "pozycja": "Środkowy", "wiek": 24, "umiejetnosci": {"atak": 80, "obrona": 68, "zagrywka": 70, "blok": 90}, "cena": 100000, "pensja": 16000},
        {"id": 103, "imie": "Damian", "nazwisko": "Górski", "pozycja": "Libero", "wiek": 27, "umiejetnosci": {"atak": 58, "obrona": 94, "zagrywka": 80, "blok": 62}, "cena": 90000, "pensja": 14000},
        {"id": 104, "imie": "Sebastian", "nazwisko": "Pawlak", "pozycja": "Przyjmujący", "wiek": 25, "umiejetnosci": {"atak": 85, "obrona": 86, "zagrywka": 83, "blok": 77}, "cena": 140000, "pensja": 19000},
        {"id": 105, "imie": "Wojciech", "nazwisko": "Sikora", "pozycja": "Rozgrywający", "wiek": 23, "umiejetnosci": {"atak": 68, "obrona": 82, "zagrywka": 86, "blok": 70}, "cena": 85000, "pensja": 15000},
    ]
    
    # Wyniki meczów
    st.session_state.matches = []
    st.session_state.next_match = {"przeciwnik": "AZS Kraków", "dzien": 7}
    st.session_state.match_in_progress = False
    st.session_state.simulation_mode = "fast"  # "fast" lub "detailed"

# Funkcje pomocnicze
def get_all_players():
    """Zwraca wszystkich zawodników"""
    return st.session_state.first_team + st.session_state.bench

def get_player_by_id(player_id):
    """Znajduje zawodnika po ID"""
    all_players = get_all_players() + st.session_state.academy
    for player in all_players:
        if player["id"] == player_id:
            return player
    return None

def oblicz_ocena_zawodnika(player):
    """Oblicza ogólną ocenę zawodnika"""
    umiejetnosci = player["umiejetnosci"]
    srednia = sum(umiejetnosci.values()) / len(umiejetnosci)
    return round(srednia * (player["forma"] / 100), 1)

def get_position_name(position_key):
    """Konwertuje numer pozycji na nazwę"""
    if position_key == "Libero":
        return "Libero (poza)"
    return f"Pozycja {position_key}"

def display_court_lineup():
    """Wyświetla wizualizację boiska z ustawieniem zawodników"""
    
    st.markdown("""
    <style>
    .court-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
    }
    .court-title {
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .court-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        background: white;
        padding: 20px;
        border-radius: 10px;
        border: 4px solid #333;
    }
    .position-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #333;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .position-label {
        font-weight: bold;
        font-size: 18px;
        color: white;
        margin-bottom: 5px;
    }
    .player-name {
        font-size: 14px;
        color: white;
        font-weight: 600;
    }
    .player-rating {
        font-size: 12px;
        color: rgba(255,255,255,0.9);
        margin-top: 3px;
    }
    .libero-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        grid-column: span 3;
        margin-top: 10px;
    }
    .net-line {
        grid-column: span 3;
        height: 5px;
        background: #333;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    lineup = st.session_state.starting_lineup
    
    # Przygotuj dane zawodników
    positions_data = {}
    for pos_key in ["IV", "III", "II", "V", "VI", "I", "Libero"]:
        player_id = lineup.get(pos_key)
        if player_id:
            player = get_player_by_id(player_id)
            if player:
                positions_data[pos_key] = {
                    "name": f"{player['imie']} {player['nazwisko']}",
                    "position": player['pozycja'],
                    "rating": oblicz_ocena_zawodnika(player)
                }
    
    st.markdown('<div class="court-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="court-title">🏐 USTAWIENIE BOISKA - {st.session_state.club_name}</div>', unsafe_allow_html=True)
    
    # Linia ataku (przy siatce)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if "IV" in positions_data:
            st.markdown(f"""
            <div class="position-box">
                <div class="position-label">IV</div>
                <div class="player-name">{positions_data['IV']['name']}</div>
                <div class="player-rating">{positions_data['IV']['position']} • {positions_data['IV']['rating']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if "III" in positions_data:
            st.markdown(f"""
            <div class="position-box">
                <div class="position-label">III</div>
                <div class="player-name">{positions_data['III']['name']}</div>
                <div class="player-rating">{positions_data['III']['position']} • {positions_data['III']['rating']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if "II" in positions_data:
            st.markdown(f"""
            <div class="position-box">
                <div class="position-label">II</div>
                <div class="player-name">{positions_data['II']['name']}</div>
                <div class="player-rating">{positions_data['II']['position']} • {positions_data['II']['rating']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Siatka
    st.markdown('<div style="text-align:center; font-size:20px; margin:10px 0; color:white;">═══════ SIATKA ═══════</div>', unsafe_allow_html=True)
    
    # Linia obrony (z tyłu)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if "V" in positions_data:
            libero_info = ""
            if "Libero" in positions_data:
                libero_info = f"<br><small style='color:rgba(255,255,255,0.8);'>↔️ Zmienia się z {positions_data['Libero']['name']}</small>"
            st.markdown(f"""
            <div class="position-box">
                <div class="position-label">V</div>
                <div class="player-name">{positions_data['V']['name']}</div>
                <div class="player-rating">{positions_data['V']['position']} • {positions_data['V']['rating']}</div>
                {libero_info}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if "VI" in positions_data:
            st.markdown(f"""
            <div class="position-box">
                <div class="position-label">VI</div>
                <div class="player-name">{positions_data['VI']['name']}</div>
                <div class="player-rating">{positions_data['VI']['position']} • {positions_data['VI']['rating']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if "I" in positions_data:
            st.markdown(f"""
            <div class="position-box">
                <div class="position-label">I (⚡)</div>
                <div class="player-name">{positions_data['I']['name']}</div>
                <div class="player-rating">{positions_data['I']['position']} • {positions_data['I']['rating']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Libero (poza boiskiem)
    if "Libero" in positions_data:
        st.markdown(f"""
        <div class="position-box libero-box">
            <div class="position-label">LIBERO (poza boiskiem)</div>
            <div class="player-name">{positions_data['Libero']['name']}</div>
            <div class="player-rating">{positions_data['Libero']['position']} • {positions_data['Libero']['rating']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def symuluj_set(team_strength, opponent_strength, is_tiebreak=False):
    """Symuluje pojedynczy set"""
    max_points = 15 if is_tiebreak else 25
    team_score = 0
    opponent_score = 0
    
    strength_diff = team_strength - opponent_strength
    win_prob = 0.5 + (strength_diff / 200)
    win_prob = max(0.3, min(0.7, win_prob))
    
    while True:
        if random.random() < win_prob:
            team_score += 1
        else:
            opponent_score += 1
        
        if team_score >= max_points and team_score - opponent_score >= 2:
            return team_score, opponent_score, True
        elif opponent_score >= max_points and opponent_score - team_score >= 2:
            return team_score, opponent_score, False

def symuluj_akcje(team_strength, opponent_strength, lineup_players):
    """Symuluje pojedynczą akcję z detalami"""
    strength_diff = team_strength - opponent_strength
    win_prob = 0.5 + (strength_diff / 200)
    win_prob = max(0.3, min(0.7, win_prob))
    
    team_wins = random.random() < win_prob
    
    # Wybierz losowego zawodnika odpowiedzialnego za punkt
    player = random.choice(lineup_players)
    
    akcje_rodzaje = []
    
    if team_wins:
        if player["pozycja"] in ["Atakujący", "Przyjmujący"]:
            akcje_rodzaje = [
                f"⚡ AS serwisowy {player['imie']} {player['nazwisko']}!",
                f"🔥 ATAK! {player['imie']} {player['nazwisko']} przebija blok!",
                f"💪 Silny atak {player['imie']} {player['nazwisko']}!"
            ]
        elif player["pozycja"] == "Środkowy":
            akcje_rodzaje = [
                f"🧱 BLOK! {player['imie']} {player['nazwisko']}!",
                f"⚡ Szybka piłka! {player['imie']} {player['nazwisko']}!",
                f"💥 As blokowy {player['imie']} {player['nazwisko']}!"
            ]
        elif player["pozycja"] == "Libero":
            akcje_rodzaje = [
                f"🛡️ Świetna obrona {player['imie']} {player['nazwisko']}! Drużyna kończy kontrę!",
                f"👏 Perfekcyjne przyjęcie {player['imie']} {player['nazwisko']}!"
            ]
        else:  # Rozgrywający
            akcje_rodzaje = [
                f"🎯 Idealne zagranie {player['imie']} {player['nazwisko']}!",
                f"✨ Asystuje {player['imie']} {player['nazwisko']}!"
            ]
    else:
        akcje_rodzaje = [
            "❌ Błąd w ataku przeciwnika",
            "❌ Faul przy bloku rywala",
            "❌ Piłka wylatuje za boisko",
            "❌ Błąd w zagrywce przeciwnika"
        ]
    
    return team_wins, random.choice(akcje_rodzaje)

def symuluj_mecz_szczegolowy(lineup_players, mode="fast"):
    """Symuluje mecz z detalami - tryb szybki lub szczegółowy"""
    team_strength = sum(oblicz_ocena_zawodnika(p) for p in lineup_players) / len(lineup_players)
    opponent_strength = random.randint(70, 85)
    
    sets_won_team = 0
    sets_won_opponent = 0
    sets_detail = []
    all_actions = [] if mode == "detailed" else None
    
    set_number = 1
    
    # Statystyki zawodników
    player_stats = {}
    for player in lineup_players:
        player_stats[player["id"]] = {
            "imie": player["imie"],
            "nazwisko": player["nazwisko"],
            "pozycja": player["pozycja"],
            "punkty": 0,
            "asy": 0,
            "bloki": 0,
            "obrony": 0
        }
    
    # Rozgrywka do 3 wygranych setów
    while sets_won_team < 3 and sets_won_opponent < 3:
        is_tiebreak = (set_number == 5)
        
        if mode == "detailed":
            # Szczegółowa symulacja set po punkcie
            max_points = 15 if is_tiebreak else 25
            team_score = 0
            opponent_score = 0
            set_actions = []
            
            while True:
                team_wins, action = symuluj_akcje(team_strength, opponent_strength, lineup_players)
                
                if team_wins:
                    team_score += 1
                    # Aktualizuj statystyki
                    for player in lineup_players:
                        if player["imie"] in action and player["nazwisko"] in action:
                            if "AS serwisowy" in action or "As blokowy" in action:
                                player_stats[player["id"]]["asy"] += 1
                            if "BLOK" in action or "As blokowy" in action:
                                player_stats[player["id"]]["bloki"] += 1
                            if "obrona" in action or "przyjęcie" in action:
                                player_stats[player["id"]]["obrony"] += 1
                            if any(word in action for word in ["ATAK", "atak", "piłka", "kontrę"]):
                                player_stats[player["id"]]["punkty"] += 1
                else:
                    opponent_score += 1
                
                set_actions.append(f"{team_score}:{opponent_score} - {action}")
                
                if team_score >= max_points and team_score - opponent_score >= 2:
                    team_won = True
                    break
                elif opponent_score >= max_points and opponent_score - team_score >= 2:
                    team_won = False
                    break
            
            all_actions.append({
                "set_number": set_number,
                "actions": set_actions,
                "final_score": f"{team_score}:{opponent_score}"
            })
            
        else:
            # Szybka symulacja
            team_score, opponent_score, team_won = symuluj_set(team_strength, opponent_strength, is_tiebreak)
            
            # Generowanie statystyk dla seta
            for player in lineup_players:
                if player["pozycja"] in ["Atakujący", "Przyjmujący"]:
                    punkty = random.randint(3, 8)
                elif player["pozycja"] == "Środkowy":
                    punkty = random.randint(2, 6)
                else:
                    punkty = random.randint(0, 2)
                
                player_stats[player["id"]]["punkty"] += punkty
                
                if random.random() < (player["umiejetnosci"]["zagrywka"] / 150):
                    player_stats[player["id"]]["asy"] += random.randint(0, 2)
                
                if player["pozycja"] in ["Środkowy", "Atakujący"]:
                    if random.random() < (player["umiejetnosci"]["blok"] / 120):
                        player_stats[player["id"]]["bloki"] += random.randint(0, 3)
                
                if player["pozycja"] in ["Libero", "Przyjmujący"]:
                    obrony = int(player["umiejetnosci"]["obrona"] / 10)
                    player_stats[player["id"]]["obrony"] += random.randint(max(0, obrony-2), obrony+2)
        
        if team_won:
            sets_won_team += 1
        else:
            sets_won_opponent += 1
        
        sets_detail.append(f"{team_score}:{opponent_score}")
        set_number += 1
    
    return {
        "wynik": f"{sets_won_team}:{sets_won_opponent}",
        "sety": sets_detail,
        "wygrana": sets_won_team > sets_won_opponent,
        "statystyki": player_stats,
        "actions": all_actions
    }

def trenuj_druzyne(squad_type="first_team"):
    """Trening zwiększa umiejętności i formę"""
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
    """Przechodzi do następnego dnia"""
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
    """Sprawdza czy ustawienie jest prawidłowe"""
    lineup = st.session_state.starting_lineup
    
    # Sprawdź czy wszystkie pozycje są wypełnione
    required_positions = ["I", "II", "III", "IV", "V", "VI", "Libero"]
    for pos in required_positions:
        if lineup.get(pos) is None:
            return False, f"Pozycja {pos} nie jest wypełniona"
    
    # Sprawdź kontuzje
    for pos, player_id in lineup.items():
        player = get_player_by_id(player_id)
        if player is None:
            return False, f"Nie znaleziono zawodnika o ID {player_id}"
        if player["kontuzja"] > 0:
            return False, f"{player['imie']} {player['nazwisko']} jest kontuzjowany"
    
    return True, "OK"

# Interfejs główny
st.title("🏐 Volleyball Manager 2024")
st.markdown("---")

# Górny pasek informacji
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏠 Główna", 
    "👥 Zarządzanie kadrą", 
    "⚙️ Ustawienie boiska", 
    "🎓 Akademia", 
    "💰 Transfery", 
    "📊 Statystyki", 
    "⚽ Mecz"
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
                st.write(f"Sety: {', '.join(last_match['sety'])}")
            else:
                st.error(f"❌ Przegraliśmy z {last_match['przeciwnik']} {last_match['wynik']}")
                st.write(f"Sety: {', '.join(last_match['sety'])}")
        else:
            st.info("Jeszcze nie rozegraliśmy żadnego meczu. Powodzenia!")
        
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
            st.success("✅ Trening akademii zakończony!")
            st.rerun()
        
        if st.button("⏭️ Następny dzień", use_container_width=True):
            next_day()
            st.rerun()
        
        st.markdown("---")
        st.subheader("Forma drużyny")
        all_players = get_all_players()
        avg_form = sum(p["forma"] for p in all_players) / len(all_players)
        st.progress(avg_form / 100)
        st.write(f"Średnia forma: {avg_form:.1f}%")

with tab2:
    st.header("👥 Zarządzanie kadrą")
    
    st.info("💡 Łatwe zarządzanie: Przenoś zawodników między pierwszą drużyną, ławką i akademią")
    
    # Szybkie akcje
    st.subheader("⚡ Szybkie zarządzanie")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Awans z ławki → Pierwsza drużyna**")
        if len(st.session_state.first_team) < 7:
            bench_options = [f"{p['imie']} {p['nazwisko']} ({p['pozycja']}) - {oblicz_ocena_zawodnika(p)}" 
                           for p in st.session_state.bench if p["kontuzja"] == 0]
            if bench_options:
                selected = st.selectbox("Wybierz z ławki", ["---"] + bench_options, key="promote_bench")
                if selected != "---" and st.button("⬆️ Awansuj", key="promote_bench_btn"):
                    player_name = selected.split(" (")[0]
                    player = next(p for p in st.session_state.bench 
                                if f"{p['imie']} {p['nazwisko']}" == player_name)
                    st.session_state.bench.remove(player)
                    st.session_state.first_team.append(player)
                    st.success(f"✅ {player['imie']} {player['nazwisko']} w pierwszej drużynie!")
                    st.rerun()
            else:
                st.info("Brak zdrowych zawodników na ławce")
        else:
            st.info("Pierwsza drużyna pełna (7/7)")
    
    with col2:
        st.write("**Degradacja → Ławka**")
        if len(st.session_state.bench) < 7:
            first_team_options = [f"{p['imie']} {p['nazwisko']} ({p['pozycja']}) - {oblicz_ocena_zawodnika(p)}" 
                                for p in st.session_state.first_team]
            if first_team_options:
                selected = st.selectbox("Wybierz z pierwszej", ["---"] + first_team_options, key="demote_first")
                if selected != "---" and st.button("⬇️ Na ławkę", key="demote_first_btn"):
                    player_name = selected.split(" (")[0]
                    player = next(p for p in st.session_state.first_team 
                                if f"{p['imie']} {p['nazwisko']}" == player_name)
                    st.session_state.first_team.remove(player)
                    st.session_state.bench.append(player)
                    # Usuń z ustawienia jeśli był w składzie
                    for pos, pid in st.session_state.starting_lineup.items():
                        if pid == player["id"]:
                            st.session_state.starting_lineup[pos] = None
                    st.success(f"✅ {player['imie']} {player['nazwisko']} na ławce!")
                    st.rerun()
        else:
            st.info("Ławka pełna (7/7)")
    
    with col3:
        st.write("**Akademia → Ławka**")
        if len(st.session_state.bench) < 7:
            academy_options = [f"{p['imie']} {p['nazwisko']} ({p['pozycja']}) - Pot: {p.get('potencjal', 85)}" 
                             for p in st.session_state.academy if p["kontuzja"] == 0]
            if academy_options:
                selected = st.selectbox("Wybierz z akademii", ["---"] + academy_options, key="promote_academy")
                if selected != "---" and st.button("⬆️ Do ławki", key="promote_academy_btn"):
                    player_name = selected.split(" (")[0]
                    player = next(p for p in st.session_state.academy 
                                if f"{p['imie']} {p['nazwisko']}" == player_name)
                    if "potencjal" in player:
                        del player["potencjal"]
                    st.session_state.academy.remove(player)
                    st.session_state.bench.append(player)
                    st.success(f"✅ {player['imie']} {player['nazwisko']} awansował na ławkę!")
                    st.rerun()
            else:
                st.info("Brak zdrowych talentów w akademii")
        else:
            st.info("Ławka pełna (7/7)")
    
    st.markdown("---")
    
    # Pierwsza drużyna
    st.subheader("🏆 Pierwsza drużyna (7 zawodników)")
    players_data = []
    for p in st.session_state.first_team:
        ocena = oblicz_ocena_zawodnika(p)
        status = "🤕 Kontuzja" if p["kontuzja"] > 0 else "✅ Gotowy"
        players_data.append({
            "Imię": p["imie"],
            "Nazwisko": p["nazwisko"],
            "Pozycja": p["pozycja"],
            "Wiek": p["wiek"],
            "Ocena": ocena,
            "Forma": f"{p['forma']}%",
            "Status": status,
            "Pensja": f"{p['pensja']:,} zł"
        })
    
    df_first_team = pd.DataFrame(players_data)
    st.dataframe(df_first_team, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Ławka rezerwowych
    st.subheader("🪑 Ławka rezerwowych (7 zawodników)")
    bench_data = []
    for p in st.session_state.bench:
        ocena = oblicz_ocena_zawodnika(p)
        status = "🤕 Kontuzja" if p["kontuzja"] > 0 else "✅ Gotowy"
        bench_data.append({
            "Imię": p["imie"],
            "Nazwisko": p["nazwisko"],
            "Pozycja": p["pozycja"],
            "Wiek": p["wiek"],
            "Ocena": ocena,
            "Forma": f"{p['forma']}%",
            "Status": status,
            "Pensja": f"{p['pensja']:,} zł"
        })
    
    df_bench = pd.DataFrame(bench_data)
    st.dataframe(df_bench, use_container_width=True, hide_index=True)

with tab3:
    st.header("⚙️ Ustawienie boiska")
    
    # Wizualizacja boiska
    display_court_lineup()
    
    st.markdown("---")
    
    st.info("""
    **Zasady ustawienia:**
    - Pozycje I-VI według numeracji siatkarskiej
    - Libero zmienia się z pozycją V (środkowy z tyłu) i jest poza boiskiem
    - Pozycja I (⚡) - zagrywka
    - Pozycje II, III, IV - linia ataku (przy siatce)
    - Pozycje V, VI, I - linia obrony (z tyłu)
    """)
    
    st.subheader("🔧 Edycja ustawienia")
    
    # Dostępni zawodnicy (tylko z pierwszej drużyny)
    available_players = [p for p in st.session_state.first_team if p["kontuzja"] == 0]
    
    if len(available_players) < 7:
        st.error(f"❌ Za mało zdrowych zawodników w pierwszej drużynie! ({len(available_players)}/7)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Linia ataku (przy siatce)**")
        
        for pos in ["IV", "III", "II"]:
            options = [f"{p['id']}: {p['imie']} {p['nazwisko']} ({p['pozycja']}) - {oblicz_ocena_zawodnika(p)}" 
                      for p in available_players]
            options.insert(0, "Nie wybrano")
            
            current_id = st.session_state.starting_lineup.get(pos)
            current_index = 0
            if current_id:
                for i, opt in enumerate(options):
                    if opt.startswith(f"{current_id}:"):
                        current_index = i
                        break
            
            selected = st.selectbox(f"Pozycja {pos}", options, index=current_index, key=f"pos_{pos}")
            if selected != "Nie wybrano":
                st.session_state.starting_lineup[pos] = int(selected.split(":")[0])
            else:
                st.session_state.starting_lineup[pos] = None
    
    with col2:
        st.write("**Linia obrony (z tyłu)**")
        
        for pos in ["V", "VI", "I"]:
            options = [f"{p['id']}: {p['imie']} {p['nazwisko']} ({p['pozycja']}) - {oblicz_ocena_zawodnika(p)}" 
                      for p in available_players]
            options.insert(0, "Nie wybrano")
            
            current_id = st.session_state.starting_lineup.get(pos)
            current_index = 0
            if current_id:
                for i, opt in enumerate(options):
                    if opt.startswith(f"{current_id}:"):
                        current_index = i
                        break
            
            label = f"Pozycja {pos}"
            if pos == "V":
                label += " (zmienia się z Libero)"
            elif pos == "I":
                label += " (zagrywka ⚡)"
            
            selected = st.selectbox(label, options, index=current_index, key=f"pos_{pos}")
            if selected != "Nie wybrano":
                st.session_state.starting_lineup[pos] = int(selected.split(":")[0])
            else:
                st.session_state.starting_lineup[pos] = None
    
    st.markdown("---")
    
    st.write("**Libero (poza boiskiem)**")
    libero_players = [p for p in available_players if p["pozycja"] == "Libero"]
    if libero_players:
        options = [f"{p['id']}: {p['imie']} {p['nazwisko']} - {oblicz_ocena_zawodnika(p)}" 
                  for p in libero_players]
        options.insert(0, "Nie wybrano")
        
        current_id = st.session_state.starting_lineup.get("Libero")
        current_index = 0
        if current_id:
            for i, opt in enumerate(options):
                if opt.startswith(f"{current_id}:"):
                    current_index = i
                    break
        
        selected = st.selectbox("Libero", options, index=current_index, key="pos_libero")
        if selected != "Nie wybrano":
            st.session_state.starting_lineup["Libero"] = int(selected.split(":")[0])
        else:
            st.session_state.starting_lineup["Libero"] = None
    else:
        st.warning("Brak dostępnych libero w pierwszej drużynie!")
    
    st.markdown("---")
    
    # Walidacja
    is_valid, message = validate_lineup()
    if is_valid:
        st.success("✅ Ustawienie jest prawidłowe i gotowe do meczu!")
    else:
        st.error(f"❌ {message}")

with tab4:
    st.header("🎓 Akademia młodzieżowa")
    
    st.info("""
    **Akademia to przyszłość klubu!**
    - Młodzi zawodnicy mają niższe umiejętności, ale większy potencjał wzrostu
    - Trenuj akademię regularnie, aby rozwijać talenty
    - Promuj najlepszych do ławki rezerwowych (powyżej w zakładce "Zarządzanie kadrą")
    - Akademicy mają niższe pensje
    """)
    
    academy_data = []
    for p in st.session_state.academy:
        ocena = oblicz_ocena_zawodnika(p)
        potencjal = p.get("potencjal", 85)
        status = "🤕 Kontuzja" if p["kontuzja"] > 0 else "✅ Gotowy"
        academy_data.append({
            "Imię": p["imie"],
            "Nazwisko": p["nazwisko"],
            "Pozycja": p["pozycja"],
            "Wiek": p["wiek"],
            "Ocena": ocena,
            "Potencjał": potencjal,
            "Forma": f"{p['forma']}%",
            "Status": status,
            "Pensja": f"{p['pensja']:,} zł"
        })
    
    df_academy = pd.DataFrame(academy_data)
    st.dataframe(df_academy, use_container_width=True, hide_index=True)

with tab5:
    st.header("💰 Rynek transferowy")
    
    st.subheader("Dostępni zawodnicy")
    
    transfer_data = []
    for p in st.session_state.transfer_market:
        avg_skill = sum(p["umiejetnosci"].values()) / len(p["umiejetnosci"])
        transfer_data.append({
            "Imię": p["imie"],
            "Nazwisko": p["nazwisko"],
            "Pozycja": p["pozycja"],
            "Wiek": p["wiek"],
            "Umiejętności": round(avg_skill, 1),
            "Cena": f"{p['cena']:,} zł",
            "Pensja": f"{p['pensja']:,} zł/tydz"
        })
    
    df_transfers = pd.DataFrame(transfer_data)
    st.dataframe(df_transfers, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Kup zawodnika")
        if st.session_state.transfer_market:
            buy_options = [f"{p['imie']} {p['nazwisko']} ({p['pozycja']}) - {p['cena']:,} zł" 
                          for p in st.session_state.transfer_market]
            selected_buy = st.selectbox("Wybierz zawodnika do kupienia", buy_options)
            
            if st.button("💰 Kup zawodnika", type="primary"):
                player_to_buy = st.session_state.transfer_market[buy_options.index(selected_buy)]
                
                if st.session_state.budget >= player_to_buy["cena"]:
                    if len(st.session_state.bench) < 7:
                        st.session_state.budget -= player_to_buy["cena"]
                        new_player = player_to_buy.copy()
                        new_player["forma"] = 75
                        new_player["kontuzja"] = 0
                        st.session_state.bench.append(new_player)
                        st.session_state.transfer_market.remove(player_to_buy)
                        st.success(f"✅ Kupiono {player_to_buy['imie']} {player_to_buy['nazwisko']}! Dodano do ławki rezerwowych.")
                        st.rerun()
                    else:
                        st.error("❌ Ławka rezerwowych jest pełna! Zwolnij miejsce przed zakupem.")
                else:
                    st.error(f"❌ Niewystarczający budżet! Potrzebujesz {player_to_buy['cena']:,} zł, masz {st.session_state.budget:,} zł")
        else:
            st.info("Brak dostępnych zawodników na rynku.")
    
    with col2:
        st.subheader("Sprzedaj zawodnika")
        all_sellable = st.session_state.first_team + st.session_state.bench
        
        if len(all_sellable) > 6:
            sell_options = [f"{p['imie']} {p['nazwisko']} ({p['pozycja']})" for p in all_sellable]
            selected_sell = st.selectbox("Wybierz zawodnika do sprzedania", sell_options)
            
            if st.button("💸 Sprzedaj zawodnika"):
                player_to_sell = next(p for p in all_sellable 
                                     if f"{p['imie']} {p['nazwisko']} ({p['pozycja']})" == selected_sell)
                sell_price = int(oblicz_ocena_zawodnika(player_to_sell) * 1200)
                st.session_state.budget += sell_price
                
                if player_to_sell in st.session_state.first_team:
                    st.session_state.first_team.remove(player_to_sell)
                else:
                    st.session_state.bench.remove(player_to_sell)
                
                for pos, pid in st.session_state.starting_lineup.items():
                    if pid == player_to_sell["id"]:
                        st.session_state.starting_lineup[pos] = None
                
                st.success(f"✅ Sprzedano {player_to_sell['imie']} {player_to_sell['nazwisko']} za {sell_price:,} zł!")
                st.rerun()
        else:
            st.warning("Musisz mieć przynajmniej 6 zawodników w klubie!")

with tab6:
    st.header("📊 Statystyki")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bilans meczów")
        if st.session_state.matches:
            wins = sum(1 for m in st.session_state.matches if m["wygrana"])
            losses = len(st.session_state.matches) - wins
            st.metric("Zwycięstwa", wins)
            st.metric("Porażki", losses)
            st.metric("Procent wygranych", f"{(wins/len(st.session_state.matches)*100):.1f}%")
        else:
            st.info("Brak rozegranych meczów")
    
    with col2:
        st.subheader("Top 5 zawodników klubu")
        all_players = get_all_players() + st.session_state.academy
        sorted_players = sorted(all_players, key=oblicz_ocena_zawodnika, reverse=True)[:5]
        for i, p in enumerate(sorted_players, 1):
            squad = "📚" if p in st.session_state.academy else "🏆" if p in st.session_state.first_team else "🪑"
            st.write(f"{i}. {squad} **{p['imie']} {p['nazwisko']}** ({p['pozycja']}) - Ocena: {oblicz_ocena_zawodnika(p)}")
    
    st.markdown("---")
    st.subheader("Historia meczów")
    if st.session_state.matches:
        matches_data = []
        for m in st.session_state.matches:
            matches_data.append({
                "Przeciwnik": m["przeciwnik"],
                "Wynik": m["wynik"],
                "Sety": ", ".join(m["sety"]),
                "Rezultat": "Wygrana ✅" if m["wygrana"] else "Porażka ❌"
            })
        df_matches = pd.DataFrame(matches_data)
        st.dataframe(df_matches, use_container_width=True, hide_index=True)
    else:
        st.info("Brak rozegranych meczów")

with tab7:
    st.header("🏐 Rozgrywka meczowa")
    
    days_to_match = st.session_state.next_match["dzien"] - st.session_state.current_day
    
    if days_to_match > 0:
        st.warning(f"⏳ Następny mecz za {days_to_match} dni przeciwko {st.session_state.next_match['przeciwnik']}")
        st.info("Ustaw skład w zakładce 'Ustawienie boiska' i trenuj drużynę!")
    else:
        st.success(f"🏐 Dzisiaj grasz z {st.session_state.next_match['przeciwnik']}!")
        
        # Sprawdzenie ustawienia
        is_valid, message = validate_lineup()
        
        if not is_valid:
            st.error(f"❌ {message}")
            st.warning("Przejdź do zakładki 'Ustawienie boiska' i skompletuj skład!")
        else:
            # Wybór trybu symulacji
            st.subheader("🎮 Wybierz tryb symulacji")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("⚡ Szybka symulacja", use_container_width=True, type="primary"):
                    st.session_state.simulation_mode = "fast"
                    st.session_state.match_in_progress = True
                    st.rerun()
                st.info("Natychmiastowy wynik bez szczegółów akcji")
            
            with col2:
                if st.button("🎬 Szczegółowa symulacja", use_container_width=True, type="secondary"):
                    st.session_state.simulation_mode = "detailed"
                    st.session_state.match_in_progress = True
                    st.rerun()
                st.info("Pełna symulacja z każdą akcją i komentarzem")
            
            st.markdown("---")
            
            # Wyświetl ustawienie przed meczem
            st.subheader("📋 Twoje ustawienie na mecz")
            display_court_lineup()
            
            # Symulacja meczu
            if st.session_state.match_in_progress:
                st.markdown("---")
                
                opponent_name = st.session_state.next_match['przeciwnik']
                
                # Przygotuj skład
                lineup_players = []
                for pos in ["I", "II", "III", "IV", "V", "VI", "Libero"]:
                    player_id = st.session_state.starting_lineup[pos]
                    player = get_player_by_id(player_id)
                    if player and pos != "Libero":  # Libero nie gra na boisku, tylko się zmienia
                        lineup_players.append(player)
                
                # Dodaj libero do składu dla statystyk
                libero_id = st.session_state.starting_lineup["Libero"]
                if libero_id:
                    libero = get_player_by_id(libero_id)
                    if libero:
                        lineup_players.append(libero)
                
                mode = st.session_state.simulation_mode
                
                if mode == "detailed":
                    st.subheader("🎬 Trwa szczegółowa symulacja meczu...")
                    st.write(f"### {st.session_state.club_name} vs {opponent_name}")
                    
                    result = symuluj_mecz_szczegolowy(lineup_players, mode="detailed")
                    
                    # Wyświetl akcje dla każdego seta
                    for set_data in result["actions"]:
                        with st.expander(f"📊 Set {set_data['set_number']} - Wynik końcowy: {set_data['final_score']}", expanded=(set_data['set_number']==1)):
                            for action in set_data['actions']:
                                st.write(action)
                                time.sleep(0.05)  # Krótka pauza dla efektu
                    
                    st.markdown("---")
                    
                else:  # fast mode
                    st.subheader("⚡ Wynik meczu")
                    st.write(f"### {st.session_state.club_name} vs {opponent_name}")
                    
                    result = symuluj_mecz_szczegolowy(lineup_players, mode="fast")
                
                # Wyświetlanie wyników setów
                st.write("#### Wyniki setów:")
                sets_display = []
                for i, set_score in enumerate(result["sety"], 1):
                    is_tiebreak = (i == 5)
                    team_score, opp_score = map(int, set_score.split(":"))
                    won = team_score > opp_score
                    
                    sets_display.append({
                        "Set": f"Set {i}" + (" (Tie-break)" if is_tiebreak else ""),
                        "Wynik": set_score,
                        "Status": "✅ Wygrany" if won else "❌ Przegrany"
                    })
                
                df_sets = pd.DataFrame(sets_display)
                st.dataframe(df_sets, use_container_width=True, hide_index=True)
                
                # Wynik końcowy
                if result["wygrana"]:
                    st.success(f"### 🎉 ZWYCIĘSTWO! {result['wynik']}")
                else:
                    st.error(f"### 😞 Porażka... {result['wynik']}")
                
                st.markdown("---")
                st.write("#### 📊 Statystyki zawodników")
                
                stats_display = []
                for pid, stats in result["statystyki"].items():
                    stats_display.append({
                        "Zawodnik": f"{stats['imie']} {stats['nazwisko']}",
                        "Pozycja": stats['pozycja'],
                        "Punkty": stats['punkty'],
                        "Asy": stats['asy'],
                        "Bloki": stats['bloki'],
                        "Obrony": stats['obrony']
                    })
                
                df_stats = pd.DataFrame(stats_display)
                df_stats = df_stats.sort_values("Punkty", ascending=False)
                st.dataframe(df_stats, use_container_width=True, hide_index=True)
                
                # MVP meczu
                mvp = df_stats.iloc[0]
                st.success(f"🏆 MVP meczu: **{mvp['Zawodnik']}** ({mvp['Punkty']} punktów)")
                
                st.markdown("---")
                
                if st.button("✅ Zakończ mecz i zapisz wynik", type="primary", use_container_width=True):
                    # Zapisanie wyniku
                    match_result = {
                        "przeciwnik": opponent_name,
                        "wynik": result["wynik"],
                        "sety": result["sety"],
                        "wygrana": result["wygrana"],
                        "statystyki": result["statystyki"]
                    }
                    st.session_state.matches.append(match_result)
                    
                    # Aktualizacja morale i budżetu
                    if result["wygrana"]:
                        st.session_state.morale = min(100, st.session_state.morale + 5)
                        st.session_state.budget += 25000
                    else:
                        st.session_state.morale = max(50, st.session_state.morale - 3)
                        st.session_state.budget += 10000
                    
                    # Nowy następny mecz
                    opponents = ["AZS Kraków", "Jastrzębski Węgiel", "Projekt Warszawa", "Aluron Zawiercie", 
                                "ZAKSA Kędzierzyn-Koźle", "Trefl Gdańsk", "PGE Skra Bełchatów", "Indykpol AZS Olsztyn"]
                    st.session_state.next_match = {
                        "przeciwnik": random.choice([o for o in opponents if o != opponent_name]),
                        "dzien": st.session_state.current_day + 7
                    }
                    
                    # Losowe kontuzje po meczu
                    for p in lineup_players:
                        if random.random() < 0.1:
                            p["kontuzja"] = random.randint(3, 10)
                    
                    # Zmiana formy po meczu
                    for p in lineup_players:
                        if result["wygrana"]:
                            p["forma"] = min(95, p["forma"] + random.randint(1, 3))
                        else:
                            p["forma"] = max(60, p["forma"] - random.randint(0, 2))
                    
                    st.session_state.match_in_progress = False
                    st.success("✅ Mecz zakończony! Wynik zapisany.")
                    time.sleep(2)
                    st.rerun()

st.markdown("---")
st.markdown("*Volleyball Manager 2024 - Zostań najlepszym menedżerem siatkówki!* 🏐")
