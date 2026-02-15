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
    
    # Ustawienie podstawowe (6 zawodników na boisku)
    st.session_state.starting_lineup = {
        "Przyjmujący 1": 1,  # ID zawodnika
        "Przyjmujący 2": 6,
        "Atakujący": 4,
        "Środkowy 1": 2,
        "Środkowy 2": 7,
        "Rozgrywający": 3,
        "Libero": 5
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

def symuluj_set(team_strength, opponent_strength, is_tiebreak=False):
    """Symuluje pojedynczy set"""
    max_points = 15 if is_tiebreak else 25
    team_score = 0
    opponent_score = 0
    
    # Obliczanie prawdopodobieństwa wygrania punktu
    strength_diff = team_strength - opponent_strength
    win_prob = 0.5 + (strength_diff / 200)
    win_prob = max(0.3, min(0.7, win_prob))
    
    while True:
        if random.random() < win_prob:
            team_score += 1
        else:
            opponent_score += 1
        
        # Sprawdzanie warunków wygranej
        if team_score >= max_points and team_score - opponent_score >= 2:
            return team_score, opponent_score, True
        elif opponent_score >= max_points and opponent_score - team_score >= 2:
            return team_score, opponent_score, False

def symuluj_mecz_szczegolowy(lineup_players):
    """Symuluje mecz z detalami"""
    # Obliczanie siły drużyny
    team_strength = sum(oblicz_ocena_zawodnika(p) for p in lineup_players) / len(lineup_players)
    opponent_strength = random.randint(70, 85)
    
    sets_won_team = 0
    sets_won_opponent = 0
    sets_detail = []
    
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
        team_score, opp_score, team_won = symuluj_set(team_strength, opponent_strength, is_tiebreak)
        
        # Generowanie statystyk dla seta
        for player in lineup_players:
            # Punkty bazowane na ataku i formie
            if player["pozycja"] in ["Atakujący", "Przyjmujący"]:
                punkty = random.randint(3, 8)
            elif player["pozycja"] == "Środkowy":
                punkty = random.randint(2, 6)
            else:
                punkty = random.randint(0, 2)
            
            player_stats[player["id"]]["punkty"] += punkty
            
            # Asy serwisowe
            if random.random() < (player["umiejetnosci"]["zagrywka"] / 150):
                player_stats[player["id"]]["asy"] += random.randint(0, 2)
            
            # Bloki dla środkowych i atakujących
            if player["pozycja"] in ["Środkowy", "Atakujący"]:
                if random.random() < (player["umiejetnosci"]["blok"] / 120):
                    player_stats[player["id"]]["bloki"] += random.randint(0, 3)
            
            # Obrony dla libero i przyjmujących
            if player["pozycja"] in ["Libero", "Przyjmujący"]:
                obrony = int(player["umiejetnosci"]["obrona"] / 10)
                player_stats[player["id"]]["obrony"] += random.randint(obrony-2, obrony+2)
        
        if team_won:
            sets_won_team += 1
        else:
            sets_won_opponent += 1
        
        sets_detail.append(f"{team_score}:{opp_score}")
        set_number += 1
    
    return {
        "wynik": f"{sets_won_team}:{sets_won_opponent}",
        "sety": sets_detail,
        "wygrana": sets_won_team > sets_won_opponent,
        "statystyki": player_stats
    }

def trenuj_druzyne(squad_type="first_team"):
    """Trening zwiększa umiejętności i formę"""
    squad = st.session_state.first_team if squad_type == "first_team" else st.session_state.academy
    
    for player in squad:
        if player["kontuzja"] == 0:
            # Wzrost umiejętności (młodzież rośnie szybciej)
            growth_chance = 0.4 if squad_type == "academy" else 0.3
            max_skill = player.get("potencjal", 95) if squad_type == "academy" else 95
            
            if random.random() < growth_chance:
                skill = random.choice(list(player["umiejetnosci"].keys()))
                if player["umiejetnosci"][skill] < max_skill:
                    wzrost = random.randint(1, 2) if squad_type == "academy" else 1
                    player["umiejetnosci"][skill] = min(max_skill, player["umiejetnosci"][skill] + wzrost)
            
            # Zmiana formy
            player["forma"] = max(60, min(95, player["forma"] + random.randint(-2, 6)))
        else:
            # Leczenie kontuzji
            player["kontuzja"] = max(0, player["kontuzja"] - 1)

def next_day():
    """Przechodzi do następnego dnia"""
    st.session_state.current_day += 1
    
    # Koszty pensji (raz w tygodniu)
    if st.session_state.current_day % 7 == 0:
        total_salary = (sum(p["pensja"] for p in st.session_state.first_team) + 
                       sum(p["pensja"] for p in st.session_state.bench) +
                       sum(p["pensja"] for p in st.session_state.academy))
        st.session_state.budget -= total_salary
    
    # Losowe kontuzje (tylko dla pierwszej drużyny i ławki)
    all_players = get_all_players()
    for player in all_players:
        if player["kontuzja"] == 0 and random.random() < 0.015:
            player["kontuzja"] = random.randint(3, 14)

def validate_lineup():
    """Sprawdza czy ustawienie jest prawidłowe"""
    lineup = st.session_state.starting_lineup
    required_positions = {
        "Przyjmujący": 2,
        "Atakujący": 1,
        "Środkowy": 2,
        "Rozgrywający": 1,
        "Libero": 1
    }
    
    position_count = {}
    for role, player_id in lineup.items():
        if player_id is None:
            return False, "Wszystkie pozycje muszą być wypełnione"
        
        player = get_player_by_id(player_id)
        if player is None:
            return False, f"Nie znaleziono zawodnika o ID {player_id}"
        
        if player["kontuzja"] > 0:
            return False, f"{player['imie']} {player['nazwisko']} jest kontuzjowany"
        
        pos = player["pozycja"]
        position_count[pos] = position_count.get(pos, 0) + 1
    
    for pos, count in required_positions.items():
        if position_count.get(pos, 0) != count:
            return False, f"Wymagana liczba pozycji {pos}: {count}, obecnie: {position_count.get(pos, 0)}"
    
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
    "👥 Kadra", 
    "⚙️ Ustawienie", 
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
    st.header("Kadra zawodników")
    
    # Pierwsza drużyna
    st.subheader("🏆 Pierwsza drużyna (7 zawodników)")
    players_data = []
    for p in st.session_state.first_team:
        ocena = oblicz_ocena_zawodnika(p)
        status = "🤕 Kontuzja" if p["kontuzja"] > 0 else "✅ Gotowy"
        players_data.append({
            "ID": p["id"],
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
            "ID": p["id"],
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
    
    st.markdown("---")
    
    # Przenoszenie zawodników
    st.subheader("🔄 Zarządzanie kadrą")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Awansuj z ławki do pierwszej drużyny**")
        if len(st.session_state.first_team) < 7:
            bench_options = [f"{p['id']}: {p['imie']} {p['nazwisko']} ({p['pozycja']})" 
                           for p in st.session_state.bench]
            if bench_options:
                promote_player = st.selectbox("Wybierz zawodnika", bench_options, key="promote")
                if st.button("⬆️ Awansuj", key="promote_btn"):
                    player_id = int(promote_player.split(":")[0])
                    player = next(p for p in st.session_state.bench if p["id"] == player_id)
                    st.session_state.bench.remove(player)
                    st.session_state.first_team.append(player)
                    st.success(f"✅ {player['imie']} {player['nazwisko']} awansował do pierwszej drużyny!")
                    st.rerun()
        else:
            st.info("Pierwsza drużyna jest pełna (7/7)")
    
    with col2:
        st.write("**Przenieś do ławki rezerwowych**")
        if len(st.session_state.bench) < 7:
            first_team_options = [f"{p['id']}: {p['imie']} {p['nazwisko']} ({p['pozycja']})" 
                                for p in st.session_state.first_team]
            if first_team_options:
                demote_player = st.selectbox("Wybierz zawodnika", first_team_options, key="demote")
                if st.button("⬇️ Przenieś", key="demote_btn"):
                    player_id = int(demote_player.split(":")[0])
                    player = next(p for p in st.session_state.first_team if p["id"] == player_id)
                    st.session_state.first_team.remove(player)
                    st.session_state.bench.append(player)
                    st.success(f"✅ {player['imie']} {player['nazwisko']} przeniesiony na ławkę!")
                    st.rerun()
        else:
            st.info("Ławka jest pełna (7/7)")
    
    st.markdown("---")
    st.subheader("📋 Szczegóły zawodnika")
    
    all_players = get_all_players()
    player_names = [f"{p['imie']} {p['nazwisko']} ({p['pozycja']})" for p in all_players]
    selected_player_name = st.selectbox("Wybierz zawodnika", player_names)
    
    if selected_player_name:
        selected_player = next(p for p in all_players if f"{p['imie']} {p['nazwisko']} ({p['pozycja']})" == selected_player_name)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Pozycja:** {selected_player['pozycja']}")
            st.write(f"**Wiek:** {selected_player['wiek']}")
            st.write(f"**Forma:** {selected_player['forma']}%")
            st.write(f"**Ocena ogólna:** {oblicz_ocena_zawodnika(selected_player)}")
            if selected_player["kontuzja"] > 0:
                st.error(f"🤕 Kontuzja: {selected_player['kontuzja']} dni")
        
        with col2:
            st.write("**Umiejętności:**")
            for skill, value in selected_player['umiejetnosci'].items():
                st.progress(value / 100, text=f"{skill.capitalize()}: {value}")

with tab3:
    st.header("⚙️ Ustawienie drużyny")
    
    st.info("""
    **Zasady ustawienia:**
    - 2 Przyjmujący
    - 1 Atakujący  
    - 2 Środkowy
    - 1 Rozgrywający
    - 1 Libero
    
    **Libero zmienia się ze środkowymi w drugiej linii podczas meczu.**
    """)
    
    # Dostępni zawodnicy (tylko z pierwszej drużyny)
    available_players = [p for p in st.session_state.first_team if p["kontuzja"] == 0]
    
    if len(available_players) < 7:
        st.error(f"❌ Za mało zdrowych zawodników w pierwszej drużynie! ({len(available_players)}/7)")
    
    st.subheader("🏐 Skład wyjściowy")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Przyjmujący**")
        przyjmujacy = [p for p in available_players if p["pozycja"] == "Przyjmujący"]
        if przyjmujacy:
            options = [f"{p['id']}: {p['imie']} {p['nazwisko']} (Ocena: {oblicz_ocena_zawodnika(p)})" 
                      for p in przyjmujacy]
            options.insert(0, "Nie wybrano")
            
            current_p1 = st.session_state.starting_lineup.get("Przyjmujący 1")
            current_index_p1 = 0
            if current_p1:
                for i, opt in enumerate(options):
                    if opt.startswith(f"{current_p1}:"):
                        current_index_p1 = i
                        break
            
            selected_p1 = st.selectbox("Przyjmujący 1", options, index=current_index_p1, key="p1")
            if selected_p1 != "Nie wybrano":
                st.session_state.starting_lineup["Przyjmujący 1"] = int(selected_p1.split(":")[0])
            else:
                st.session_state.starting_lineup["Przyjmujący 1"] = None
            
            current_p2 = st.session_state.starting_lineup.get("Przyjmujący 2")
            current_index_p2 = 0
            if current_p2:
                for i, opt in enumerate(options):
                    if opt.startswith(f"{current_p2}:"):
                        current_index_p2 = i
                        break
            
            selected_p2 = st.selectbox("Przyjmujący 2", options, index=current_index_p2, key="p2")
            if selected_p2 != "Nie wybrano":
                st.session_state.starting_lineup["Przyjmujący 2"] = int(selected_p2.split(":")[0])
            else:
                st.session_state.starting_lineup["Przyjmujący 2"] = None
        else:
            st.warning("Brak dostępnych przyjmujących!")
        
        st.write("**Atakujący**")
        atakujacy = [p for p in available_players if p["pozycja"] == "Atakujący"]
        if atakujacy:
            options = [f"{p['id']}: {p['imie']} {p['nazwisko']} (Ocena: {oblicz_ocena_zawodnika(p)})" 
                      for p in atakujacy]
            options.insert(0, "Nie wybrano")
            
            current_a = st.session_state.starting_lineup.get("Atakujący")
            current_index_a = 0
            if current_a:
                for i, opt in enumerate(options):
                    if opt.startswith(f"{current_a}:"):
                        current_index_a = i
                        break
            
            selected_a = st.selectbox("Atakujący", options, index=current_index_a, key="a")
            if selected_a != "Nie wybrano":
                st.session_state.starting_lineup["Atakujący"] = int(selected_a.split(":")[0])
            else:
                st.session_state.starting_lineup["Atakujący"] = None
        else:
            st.warning("Brak dostępnych atakujących!")
        
        st.write("**Środkowi**")
        srodkowi = [p for p in available_players if p["pozycja"] == "Środkowy"]
        if srodkowi:
            options = [f"{p['id']}: {p['imie']} {p['nazwisko']} (Ocena: {oblicz_ocena_zawodnika(p)})" 
                      for p in srodkowi]
            options.insert(0, "Nie wybrano")
            
            current_s1 = st.session_state.starting_lineup.get("Środkowy 1")
            current_index_s1 = 0
            if current_s1:
                for i, opt in enumerate(options):
                    if opt.startswith(f"{current_s1}:"):
                        current_index_s1 = i
                        break
            
            selected_s1 = st.selectbox("Środkowy 1", options, index=current_index_s1, key="s1")
            if selected_s1 != "Nie wybrano":
                st.session_state.starting_lineup["Środkowy 1"] = int(selected_s1.split(":")[0])
            else:
                st.session_state.starting_lineup["Środkowy 1"] = None
            
            current_s2 = st.session_state.starting_lineup.get("Środkowy 2")
            current_index_s2 = 0
            if current_s2:
                for i, opt in enumerate(options):
                    if opt.startswith(f"{current_s2}:"):
                        current_index_s2 = i
                        break
            
            selected_s2 = st.selectbox("Środkowy 2", options, index=current_index_s2, key="s2")
            if selected_s2 != "Nie wybrano":
                st.session_state.starting_lineup["Środkowy 2"] = int(selected_s2.split(":")[0])
            else:
                st.session_state.starting_lineup["Środkowy 2"] = None
        else:
            st.warning("Brak dostępnych środkowych!")
    
    with col2:
        st.write("**Rozgrywający**")
        rozgrywajacy = [p for p in available_players if p["pozycja"] == "Rozgrywający"]
        if rozgrywajacy:
            options = [f"{p['id']}: {p['imie']} {p['nazwisko']} (Ocena: {oblicz_ocena_zawodnika(p)})" 
                      for p in rozgrywajacy]
            options.insert(0, "Nie wybrano")
            
            current_r = st.session_state.starting_lineup.get("Rozgrywający")
            current_index_r = 0
            if current_r:
                for i, opt in enumerate(options):
                    if opt.startswith(f"{current_r}:"):
                        current_index_r = i
                        break
            
            selected_r = st.selectbox("Rozgrywający", options, index=current_index_r, key="r")
            if selected_r != "Nie wybrano":
                st.session_state.starting_lineup["Rozgrywający"] = int(selected_r.split(":")[0])
            else:
                st.session_state.starting_lineup["Rozgrywający"] = None
        else:
            st.warning("Brak dostępnych rozgrywających!")
        
        st.write("**Libero**")
        libero = [p for p in available_players if p["pozycja"] == "Libero"]
        if libero:
            options = [f"{p['id']}: {p['imie']} {p['nazwisko']} (Ocena: {oblicz_ocena_zawodnika(p)})" 
                      for p in libero]
            options.insert(0, "Nie wybrano")
            
            current_l = st.session_state.starting_lineup.get("Libero")
            current_index_l = 0
            if current_l:
                for i, opt in enumerate(options):
                    if opt.startswith(f"{current_l}:"):
                        current_index_l = i
                        break
            
            selected_l = st.selectbox("Libero", options, index=current_index_l, key="l")
            if selected_l != "Nie wybrano":
                st.session_state.starting_lineup["Libero"] = int(selected_l.split(":")[0])
            else:
                st.session_state.starting_lineup["Libero"] = None
        else:
            st.warning("Brak dostępnych libero!")
    
    st.markdown("---")
    
    # Podsumowanie ustawienia
    st.subheader("📋 Aktualne ustawienie")
    is_valid, message = validate_lineup()
    
    if is_valid:
        st.success("✅ Ustawienie jest prawidłowe!")
        
        lineup_summary = []
        for role, player_id in st.session_state.starting_lineup.items():
            if player_id:
                player = get_player_by_id(player_id)
                lineup_summary.append({
                    "Rola": role,
                    "Zawodnik": f"{player['imie']} {player['nazwisko']}",
                    "Ocena": oblicz_ocena_zawodnika(player),
                    "Forma": f"{player['forma']}%"
                })
        
        df_lineup = pd.DataFrame(lineup_summary)
        st.dataframe(df_lineup, use_container_width=True, hide_index=True)
    else:
        st.error(f"❌ {message}")

with tab4:
    st.header("🎓 Akademia młodzieżowa")
    
    st.info("""
    **Akademia to przyszłość klubu!**
    - Młodzi zawodnicy mają niższe umiejętności, ale większy potencjał wzrostu
    - Trenuj akademię regularnie, aby rozwijać talenty
    - Możesz promować najlepszych zawodników do ławki rezerwowych
    - Akademicy mają niższe pensje
    """)
    
    # Tabela akademii
    academy_data = []
    for p in st.session_state.academy:
        ocena = oblicz_ocena_zawodnika(p)
        potencjal = p.get("potencjal", 85)
        academy_data.append({
            "ID": p["id"],
            "Imię": p["imie"],
            "Nazwisko": p["nazwisko"],
            "Pozycja": p["pozycja"],
            "Wiek": p["wiek"],
            "Ocena": ocena,
            "Potencjał": potencjal,
            "Forma": f"{p['forma']}%",
            "Pensja": f"{p['pensja']:,} zł"
        })
    
    df_academy = pd.DataFrame(academy_data)
    st.dataframe(df_academy, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Promowanie z akademii
    st.subheader("⬆️ Promuj zawodnika do ławki rezerwowych")
    
    if len(st.session_state.bench) < 7:
        academy_options = [f"{p['id']}: {p['imie']} {p['nazwisko']} ({p['pozycja']}) - Ocena: {oblicz_ocena_zawodnika(p)}" 
                         for p in st.session_state.academy]
        if academy_options:
            selected_academy = st.selectbox("Wybierz zawodnika z akademii", academy_options)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Awans oznacza:**")
                st.write("- Zawodnik dołącza do ławki rezerwowych")
                st.write("- Może być wybrany do pierwszej drużyny")
                st.write("- Może grać w meczach ligowych")
            
            with col2:
                if st.button("⬆️ Awansuj do ławki", type="primary"):
                    player_id = int(selected_academy.split(":")[0])
                    player = next(p for p in st.session_state.academy if p["id"] == player_id)
                    
                    # Usuwamy potencjał przy awansie (już nie jest w akademii)
                    if "potencjal" in player:
                        del player["potencjal"]
                    
                    st.session_state.academy.remove(player)
                    st.session_state.bench.append(player)
                    st.success(f"✅ {player['imie']} {player['nazwisko']} awansował do ławki rezerwowych!")
                    st.rerun()
        else:
            st.info("Brak zawodników w akademii")
    else:
        st.warning("⚠️ Ławka rezerwowych jest pełna (7/7). Zwolnij miejsce, aby awansować zawodnika z akademii.")

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
                
                # Usuń z odpowiedniej listy
                if player_to_sell in st.session_state.first_team:
                    st.session_state.first_team.remove(player_to_sell)
                else:
                    st.session_state.bench.remove(player_to_sell)
                
                # Usuń z ustawienia jeśli był w składzie
                for role, pid in st.session_state.starting_lineup.items():
                    if pid == player_to_sell["id"]:
                        st.session_state.starting_lineup[role] = None
                
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
        st.info("Ustaw skład w zakładce 'Ustawienie' i trenuj drużynę!")
    else:
        st.success(f"🏐 Dzisiaj grasz z {st.session_state.next_match['przeciwnik']}!")
        
        # Sprawdzenie ustawienia
        is_valid, message = validate_lineup()
        
        if not is_valid:
            st.error(f"❌ {message}")
            st.warning("Przejdź do zakładki 'Ustawienie' i skompletuj skład!")
        else:
            st.success("✅ Skład jest gotowy do meczu!")
            
            # Wyświetl ustawienie
            st.subheader("📋 Wyjściowy skład")
            lineup_players = []
            lineup_display = []
            
            for role, player_id in st.session_state.starting_lineup.items():
                player = get_player_by_id(player_id)
                lineup_players.append(player)
                lineup_display.append({
                    "Pozycja": role,
                    "Zawodnik": f"{player['imie']} {player['nazwisko']}",
                    "Ocena": oblicz_ocena_zawodnika(player),
                    "Forma": f"{player['forma']}%"
                })
            
            df_lineup_match = pd.DataFrame(lineup_display)
            st.dataframe(df_lineup_match, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            if st.button("🏐 ROZPOCZNIJ MECZ!", type="primary", use_container_width=True):
                st.session_state.match_in_progress = True
                st.rerun()
            
            # Symulacja meczu
            if st.session_state.match_in_progress:
                st.markdown("---")
                st.subheader("⚡ Trwa mecz...")
                
                opponent_name = st.session_state.next_match['przeciwnik']
                
                # Kontener na live aktualizacje
                match_container = st.empty()
                stats_container = st.empty()
                
                with match_container.container():
                    st.write(f"### {st.session_state.club_name} vs {opponent_name}")
                    
                    # Symulacja meczu
                    result = symuluj_mecz_szczegolowy(lineup_players)
                    
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
                
                with stats_container.container():
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
                        st.session_state.budget += 10000  # Premia za udział
                    
                    # Nowy następny mecz
                    opponents = ["AZS Kraków", "Jastrzębski Węgiel", "Projekt Warszawa", "Aluron Zawiercie", 
                                "ZAKSA Kędzierzyn-Koźle", "Trefl Gdańsk", "PGE Skra Bełchatów", "Indykpol AZS Olsztyn"]
                    st.session_state.next_match = {
                        "przeciwnik": random.choice([o for o in opponents if o != opponent_name]),
                        "dzien": st.session_state.current_day + 7
                    }
                    
                    # Losowe kontuzje po meczu (10% szans)
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
