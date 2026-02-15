import streamlit as st
import pandas as pd
import random
import json
from datetime import datetime, timedelta

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
    
    # Tworzenie drużyny
    st.session_state.players = [
        {"id": 1, "imie": "Jakub", "nazwisko": "Kowalski", "pozycja": "Atakujący", "wiek": 24, "umiejetnosci": {"atak": 85, "obrona": 70, "zagrywka": 75, "blok": 72}, "forma": 80, "kontuzja": 0, "pensja": 15000},
        {"id": 2, "imie": "Piotr", "nazwisko": "Nowak", "pozycja": "Środkowy", "wiek": 27, "umiejetnosci": {"atak": 78, "obrona": 65, "zagrywka": 68, "blok": 88}, "forma": 75, "kontuzja": 0, "pensja": 12000},
        {"id": 3, "imie": "Marcin", "nazwisko": "Wiśniewski", "pozycja": "Rozgrywający", "wiek": 26, "umiejetnosci": {"atak": 65, "obrona": 80, "zagrywka": 72, "blok": 68}, "forma": 82, "kontuzja": 0, "pensja": 14000},
        {"id": 4, "imie": "Tomasz", "nazwisko": "Lewandowski", "pozycja": "Atakujący", "wiek": 22, "umiejetnosci": {"atak": 82, "obrona": 68, "zagrywka": 77, "blok": 70}, "forma": 85, "kontuzja": 0, "pensja": 13000},
        {"id": 5, "imie": "Kamil", "nazwisko": "Wójcik", "pozycja": "Libero", "wiek": 29, "umiejetnosci": {"atak": 55, "obrona": 92, "zagrywka": 78, "blok": 60}, "forma": 78, "kontuzja": 0, "pensja": 11000},
        {"id": 6, "imie": "Adam", "nazwisko": "Kamiński", "pozycja": "Przyjmujący", "wiek": 25, "umiejetnosci": {"atak": 80, "obrona": 82, "zagrywka": 80, "blok": 75}, "forma": 83, "kontuzja": 0, "pensja": 16000},
        {"id": 7, "imie": "Michał", "nazwisko": "Zieliński", "pozycja": "Środkowy", "wiek": 23, "umiejetnosci": {"atak": 75, "obrona": 62, "zagrywka": 65, "blok": 85}, "forma": 77, "kontuzja": 0, "pensja": 10000},
        {"id": 8, "imie": "Paweł", "nazwisko": "Szymański", "pozycja": "Przyjmujący", "wiek": 28, "umiejetnosci": {"atak": 83, "obrona": 79, "zagrywka": 82, "blok": 73}, "forma": 80, "kontuzja": 0, "pensja": 15500},
        {"id": 9, "imie": "Krzysztof", "nazwisko": "Dąbrowski", "pozycja": "Atakujący", "wiek": 21, "umiejetnosci": {"atak": 76, "obrona": 64, "zagrywka": 70, "blok": 68}, "forma": 88, "kontuzja": 0, "pensja": 9000},
        {"id": 10, "imie": "Bartosz", "nazwisko": "Jankowski", "pozycja": "Rozgrywający", "wiek": 30, "umiejetnosci": {"atak": 62, "obrona": 85, "zagrywka": 75, "blok": 65}, "forma": 72, "kontuzja": 0, "pensja": 13500},
    ]
    
    # Rynek transferowy
    st.session_state.transfer_market = [
        {"id": 101, "imie": "Jan", "nazwisko": "Mazur", "pozycja": "Atakujący", "wiek": 26, "umiejetnosci": {"atak": 88, "obrona": 72, "zagrywka": 78, "blok": 74}, "cena": 120000, "pensja": 18000},
        {"id": 102, "imie": "Łukasz", "nazwisko": "Krawczyk", "pozycja": "Środkowy", "wiek": 24, "umiejetnosci": {"atak": 80, "obrona": 68, "zagrywka": 70, "blok": 90}, "cena": 100000, "pensja": 16000},
        {"id": 103, "imie": "Damian", "nazwisko": "Górski", "pozycja": "Libero", "wiek": 27, "umiejetnosci": {"atak": 58, "obrona": 94, "zagrywka": 80, "blok": 62}, "cena": 90000, "pensja": 14000},
        {"id": 104, "imie": "Sebastian", "nazwisko": "Pawlak", "pozycja": "Przyjmujący", "wiek": 25, "umiejetnosci": {"atak": 85, "obrona": 84, "zagrywka": 83, "blok": 77}, "cena": 140000, "pensja": 19000},
        {"id": 105, "imie": "Wojciech", "nazwisko": "Sikora", "pozycja": "Rozgrywający", "wiek": 23, "umiejetnosci": {"atak": 68, "obrona": 82, "zagrywka": 74, "blok": 70}, "cena": 85000, "pensja": 15000},
    ]
    
    # Wyniki meczów
    st.session_state.matches = []
    st.session_state.next_match = {"przeciwnik": "AZS Kraków", "dzien": 7}

# Funkcje pomocnicze
def oblicz_ocena_zawodnika(player):
    """Oblicza ogólną ocenę zawodnika"""
    umiejetnosci = player["umiejetnosci"]
    srednia = sum(umiejetnosci.values()) / len(umiejetnosci)
    return round(srednia * (player["forma"] / 100), 1)

def symuluj_mecz(team_strength):
    """Symuluje wynik meczu"""
    opponent_strength = random.randint(65, 85)
    
    # Obliczanie prawdopodobieństwa wygranej
    strength_diff = team_strength - opponent_strength
    win_prob = 0.5 + (strength_diff / 200)
    win_prob = max(0.2, min(0.8, win_prob))
    
    # Symulacja setów
    team_sets = 0
    opponent_sets = 0
    sets_detail = []
    
    while team_sets < 3 and opponent_sets < 3:
        if random.random() < win_prob:
            team_score = random.randint(25, 30)
            opp_score = random.randint(20, team_score - 2)
            team_sets += 1
        else:
            opp_score = random.randint(25, 30)
            team_score = random.randint(20, opp_score - 2)
            opponent_sets += 1
        sets_detail.append(f"{team_score}:{opp_score}")
    
    return {
        "wynik": f"{team_sets}:{opponent_sets}",
        "sety": ", ".join(sets_detail),
        "wygrana": team_sets > opponent_sets
    }

def trenuj_druzyne():
    """Trening zwiększa umiejętności i formę"""
    for player in st.session_state.players:
        if player["kontuzja"] == 0:
            # Niewielki wzrost umiejętności
            if random.random() < 0.3:
                skill = random.choice(list(player["umiejetnosci"].keys()))
                if player["umiejetnosci"][skill] < 95:
                    player["umiejetnosci"][skill] += 1
            
            # Zmiana formy
            player["forma"] = max(60, min(95, player["forma"] + random.randint(-3, 5)))
        else:
            # Leczenie kontuzji
            player["kontuzja"] = max(0, player["kontuzja"] - 1)

def next_day():
    """Przechodzi do następnego dnia"""
    st.session_state.current_day += 1
    
    # Koszty pensji (raz w tygodniu)
    if st.session_state.current_day % 7 == 0:
        total_salary = sum(p["pensja"] for p in st.session_state.players)
        st.session_state.budget -= total_salary
    
    # Losowe kontuzje
    for player in st.session_state.players:
        if player["kontuzja"] == 0 and random.random() < 0.02:
            player["kontuzja"] = random.randint(3, 14)
            st.warning(f"⚕️ {player['imie']} {player['nazwisko']} doznał kontuzji! ({player['kontuzja']} dni)")

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
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Główna", "👥 Kadra", "💰 Transfery", "📊 Statystyki", "⚽ Mecz"])

with tab1:
    st.header("Panel główny")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Ostatnie aktualności")
        
        if st.session_state.matches:
            last_match = st.session_state.matches[-1]
            if last_match["wygrana"]:
                st.success(f"✅ Wygraliśmy z {last_match['przeciwnik']} {last_match['wynik']} ({last_match['sety']})")
            else:
                st.error(f"❌ Przegraliśmy z {last_match['przeciwnik']} {last_match['wynik']} ({last_match['sety']})")
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
        
        if st.button("🏃 Przeprowadź trening", use_container_width=True):
            trenuj_druzyne()
            next_day()
            st.success("✅ Trening zakończony!")
            st.rerun()
        
        if st.button("⏭️ Następny dzień", use_container_width=True):
            next_day()
            st.rerun()
        
        st.markdown("---")
        st.subheader("Forma drużyny")
        avg_form = sum(p["forma"] for p in st.session_state.players) / len(st.session_state.players)
        st.progress(avg_form / 100)
        st.write(f"Średnia forma: {avg_form:.1f}%")

with tab2:
    st.header("Kadra zawodników")
    
    # Tworzenie tabeli zawodników
    players_data = []
    for p in st.session_state.players:
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
    
    df_players = pd.DataFrame(players_data)
    st.dataframe(df_players, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("Szczegóły zawodnika")
    
    player_names = [f"{p['imie']} {p['nazwisko']}" for p in st.session_state.players]
    selected_player_name = st.selectbox("Wybierz zawodnika", player_names)
    
    if selected_player_name:
        selected_player = next(p for p in st.session_state.players if f"{p['imie']} {p['nazwisko']}" == selected_player_name)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Pozycja:** {selected_player['pozycja']}")
            st.write(f"**Wiek:** {selected_player['wiek']}")
            st.write(f"**Forma:** {selected_player['forma']}%")
            st.write(f"**Ocena ogólna:** {oblicz_ocena_zawodnika(selected_player)}")
        
        with col2:
            st.write("**Umiejętności:**")
            for skill, value in selected_player['umiejetnosci'].items():
                st.progress(value / 100, text=f"{skill.capitalize()}: {value}")

with tab3:
    st.header("Rynek transferowy")
    
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
            "Pensja": f"{p['pensja']:,} zł"
        })
    
    df_transfers = pd.DataFrame(transfer_data)
    st.dataframe(df_transfers, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Kup zawodnika")
        if st.session_state.transfer_market:
            buy_options = [f"{p['imie']} {p['nazwisko']} - {p['cena']:,} zł" for p in st.session_state.transfer_market]
            selected_buy = st.selectbox("Wybierz zawodnika do kupienia", buy_options)
            
            if st.button("Kup zawodnika"):
                player_to_buy = st.session_state.transfer_market[buy_options.index(selected_buy)]
                if st.session_state.budget >= player_to_buy["cena"]:
                    st.session_state.budget -= player_to_buy["cena"]
                    new_player = player_to_buy.copy()
                    new_player["forma"] = 75
                    new_player["kontuzja"] = 0
                    st.session_state.players.append(new_player)
                    st.session_state.transfer_market.remove(player_to_buy)
                    st.success(f"✅ Kupiono {player_to_buy['imie']} {player_to_buy['nazwisko']}!")
                    st.rerun()
                else:
                    st.error("❌ Niewystarczający budżet!")
        else:
            st.info("Brak dostępnych zawodników na rynku.")
    
    with col2:
        st.subheader("Sprzedaj zawodnika")
        if len(st.session_state.players) > 6:
            sell_options = [f"{p['imie']} {p['nazwisko']}" for p in st.session_state.players]
            selected_sell = st.selectbox("Wybierz zawodnika do sprzedania", sell_options)
            
            if st.button("Sprzedaj zawodnika"):
                player_to_sell = next(p for p in st.session_state.players if f"{p['imie']} {p['nazwisko']}" == selected_sell)
                sell_price = int(oblicz_ocena_zawodnika(player_to_sell) * 1000)
                st.session_state.budget += sell_price
                st.session_state.players.remove(player_to_sell)
                st.success(f"✅ Sprzedano za {sell_price:,} zł!")
                st.rerun()
        else:
            st.warning("Musisz mieć przynajmniej 6 zawodników w drużynie!")

with tab4:
    st.header("Statystyki")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bilans meczów")
        if st.session_state.matches:
            wins = sum(1 for m in st.session_state.matches if m["wygrana"])
            losses = len(st.session_state.matches) - wins
            st.write(f"**Zwycięstwa:** {wins}")
            st.write(f"**Porażki:** {losses}")
            st.write(f"**Procent wygranych:** {(wins/len(st.session_state.matches)*100):.1f}%")
        else:
            st.info("Brak rozegranych meczów")
    
    with col2:
        st.subheader("Top 3 zawodnicy")
        sorted_players = sorted(st.session_state.players, key=oblicz_ocena_zawodnika, reverse=True)[:3]
        for i, p in enumerate(sorted_players, 1):
            st.write(f"**{i}. {p['imie']} {p['nazwisko']}** - Ocena: {oblicz_ocena_zawodnika(p)}")
    
    st.markdown("---")
    st.subheader("Historia meczów")
    if st.session_state.matches:
        matches_data = []
        for m in st.session_state.matches:
            matches_data.append({
                "Przeciwnik": m["przeciwnik"],
                "Wynik": m["wynik"],
                "Sety": m["sety"],
                "Rezultat": "Wygrana ✅" if m["wygrana"] else "Porażka ❌"
            })
        df_matches = pd.DataFrame(matches_data)
        st.dataframe(df_matches, use_container_width=True, hide_index=True)
    else:
        st.info("Brak rozegranych meczów")

with tab5:
    st.header("Rozgrywka meczowa")
    
    days_to_match = st.session_state.next_match["dzien"] - st.session_state.current_day
    
    if days_to_match > 0:
        st.warning(f"⏳ Następny mecz za {days_to_match} dni przeciwko {st.session_state.next_match['przeciwnik']}")
        st.info("Trenuj drużynę i przygotuj się na mecz!")
    else:
        st.success(f"🏐 Dzisiaj grasz z {st.session_state.next_match['przeciwnik']}!")
        
        # Skład wyjściowy
        st.subheader("Wybierz skład (6 zawodników)")
        available_players = [p for p in st.session_state.players if p["kontuzja"] == 0]
        
        if len(available_players) < 6:
            st.error("❌ Za mało zdrowych zawodników do rozegrania meczu!")
        else:
            player_names = [f"{p['imie']} {p['nazwisko']} ({p['pozycja']}) - Ocena: {oblicz_ocena_zawodnika(p)}" 
                           for p in available_players]
            
            selected_lineup = st.multiselect(
                "Wybierz 6 zawodników do wyjściowego składu",
                player_names,
                max_selections=6
            )
            
            if len(selected_lineup) == 6:
                st.success("✅ Skład kompletny!")
                
                if st.button("🏐 Rozpocznij mecz!", type="primary", use_container_width=True):
                    # Obliczanie siły drużyny
                    lineup_indices = [player_names.index(name) for name in selected_lineup]
                    lineup_players = [available_players[i] for i in lineup_indices]
                    team_strength = sum(oblicz_ocena_zawodnika(p) for p in lineup_players) / 6
                    
                    # Symulacja meczu
                    result = symuluj_mecz(team_strength)
                    
                    # Zapisanie wyniku
                    match_result = {
                        "przeciwnik": st.session_state.next_match['przeciwnik'],
                        "wynik": result["wynik"],
                        "sety": result["sety"],
                        "wygrana": result["wygrana"]
                    }
                    st.session_state.matches.append(match_result)
                    
                    # Aktualizacja morale
                    if result["wygrana"]:
                        st.session_state.morale = min(100, st.session_state.morale + 5)
                        st.session_state.budget += 20000
                    else:
                        st.session_state.morale = max(50, st.session_state.morale - 3)
                    
                    # Nowy następny mecz
                    opponents = ["AZS Kraków", "Jastrzębski Węgiel", "Projekt Warszawa", "Aluron Zawiercie", 
                                "ZAKSA Kędzierzyn-Koźle", "Trefl Gdańsk", "PGE Skra Bełchatów"]
                    st.session_state.next_match = {
                        "przeciwnik": random.choice(opponents),
                        "dzien": st.session_state.current_day + 7
                    }
                    
                    # Losowe kontuzje po meczu
                    for p in lineup_players:
                        if random.random() < 0.1:
                            p["kontuzja"] = random.randint(3, 10)
                    
                    st.rerun()
            else:
                st.warning(f"⚠️ Wybierz dokładnie 6 zawodników (wybrano: {len(selected_lineup)})")

st.markdown("---")
st.markdown("*Volleyball Manager 2024 - Zostań najlepszym menedżerem siatkówki!* 🏐")
