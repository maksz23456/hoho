import streamlit as st
import pandas as pd
import random
import time

# Konfiguracja
st.set_page_config(page_title="Volleyball Manager 2024", page_icon="🏐", layout="wide")

# Inicjalizacja
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_season = 1
    st.session_state.budget = 500000
    st.session_state.club_name = "MKS Warszawa"
    st.session_state.current_day = 1
    st.session_state.morale = 75
    
    # Drużyny ligowe
    st.session_state.league_teams = [
        "MKS Warszawa",  # My
        "Jastrzębski Węgiel",
        "ZAKSA Kędzierzyn-Koźle",
        "Projekt Warszawa",
        "Aluron Zawiercie",
        "Trefl Gdańsk",
        "PGE Skra Bełchatów",
        "AZS Kraków",
        "Indykpol AZS Olsztyn",
        "Bogdanka LUK Lublin"
    ]
    
    # Tabela ligowa
    st.session_state.league_table = {}
    for team in st.session_state.league_teams:
        st.session_state.league_table[team] = {
            "mecze": 0,
            "wygrane": 0,
            "przegrane": 0,
            "sety_plus": 0,
            "sety_minus": 0,
            "punkty": 0
        }
    
    # Pierwsza drużyna
    st.session_state.first_team = [
        {"id": 1, "imie": "Jakub", "nazwisko": "Kowalski", "pozycja": "Przyjmujący", "numer": 10, "wiek": 24, "umiejetnosci": {"atak": 85, "obrona": 82, "zagrywka": 75, "blok": 72}, "forma": 80, "kontuzja": 0, "pensja": 15000},
        {"id": 2, "imie": "Piotr", "nazwisko": "Nowak", "pozycja": "Środkowy", "numer": 2, "wiek": 27, "umiejetnosci": {"atak": 78, "obrona": 65, "zagrywka": 68, "blok": 88}, "forma": 75, "kontuzja": 0, "pensja": 12000},
        {"id": 3, "imie": "Marcin", "nazwisko": "Wiśniewski", "pozycja": "Rozgrywający", "numer": 1, "wiek": 26, "umiejetnosci": {"atak": 65, "obrona": 80, "zagrywka": 85, "blok": 68}, "forma": 82, "kontuzja": 0, "pensja": 14000},
        {"id": 4, "imie": "Tomasz", "nazwisko": "Lewandowski", "pozycja": "Atakujący", "numer": 11, "wiek": 22, "umiejetnosci": {"atak": 88, "obrona": 68, "zagrywka": 77, "blok": 82}, "forma": 85, "kontuzja": 0, "pensja": 16000},
        {"id": 5, "imie": "Kamil", "nazwisko": "Wójcik", "pozycja": "Libero", "numer": 8, "wiek": 29, "umiejetnosci": {"atak": 55, "obrona": 92, "zagrywka": 78, "blok": 60}, "forma": 78, "kontuzja": 0, "pensja": 11000},
        {"id": 6, "imie": "Adam", "nazwisko": "Kamiński", "pozycja": "Przyjmujący", "numer": 12, "wiek": 25, "umiejetnosci": {"atak": 80, "obrona": 84, "zagrywka": 80, "blok": 75}, "forma": 83, "kontuzja": 0, "pensja": 15000},
        {"id": 7, "imie": "Michał", "nazwisko": "Zieliński", "pozycja": "Środkowy", "numer": 19, "wiek": 23, "umiejetnosci": {"atak": 75, "obrona": 62, "zagrywka": 65, "blok": 85}, "forma": 77, "kontuzja": 0, "pensja": 10000},
    ]
    
    # Cała reszta zawodników (ławka + akademia = poza składem)
    st.session_state.reserve_players = [
        {"id": 8, "imie": "Paweł", "nazwisko": "Szymański", "pozycja": "Przyjmujący", "numer": 13, "wiek": 28, "umiejetnosci": {"atak": 76, "obrona": 78, "zagrywka": 72, "blok": 70}, "forma": 80, "kontuzja": 0, "pensja": 13000},
        {"id": 9, "imie": "Krzysztof", "nazwisko": "Dąbrowski", "pozycja": "Atakujący", "numer": 9, "wiek": 21, "umiejetnosci": {"atak": 82, "obrona": 64, "zagrywka": 70, "blok": 78}, "forma": 88, "kontuzja": 0, "pensja": 11000},
        {"id": 10, "imie": "Bartosz", "nazwisko": "Jankowski", "pozycja": "Rozgrywający", "numer": 5, "wiek": 30, "umiejetnosci": {"atak": 62, "obrona": 82, "zagrywka": 80, "blok": 65}, "forma": 72, "kontuzja": 0, "pensja": 12000},
        {"id": 11, "imie": "Mateusz", "nazwisko": "Kozłowski", "pozycja": "Środkowy", "numer": 18, "wiek": 26, "umiejetnosci": {"atak": 72, "obrona": 60, "zagrywka": 63, "blok": 82}, "forma": 75, "kontuzja": 0, "pensja": 9500},
        {"id": 12, "imie": "Łukasz", "nazwisko": "Wojciechowski", "pozycja": "Libero", "numer": 6, "wiek": 27, "umiejetnosci": {"atak": 52, "obrona": 88, "zagrywka": 75, "blok": 58}, "forma": 76, "kontuzja": 0, "pensja": 10000},
        {"id": 13, "imie": "Rafał", "nazwisko": "Kwiatkowski", "pozycja": "Przyjmujący", "numer": 4, "wiek": 24, "umiejetnosci": {"atak": 74, "obrona": 76, "zagrywka": 70, "blok": 68}, "forma": 79, "kontuzja": 0, "pensja": 11500},
        {"id": 14, "imie": "Daniel", "nazwisko": "Kaczmarek", "pozycja": "Atakujący", "numer": 28, "wiek": 29, "umiejetnosci": {"atak": 80, "obrona": 66, "zagrywka": 73, "blok": 76}, "forma": 74, "kontuzja": 0, "pensja": 12500},
        # Młodzież
        {"id": 201, "imie": "Filip", "nazwisko": "Młody", "pozycja": "Przyjmujący", "numer": 31, "wiek": 18, "umiejetnosci": {"atak": 65, "obrona": 62, "zagrywka": 60, "blok": 58}, "forma": 85, "kontuzja": 0, "pensja": 3000, "potencjal": 88},
        {"id": 202, "imie": "Kacper", "nazwisko": "Talent", "pozycja": "Środkowy", "numer": 32, "wiek": 17, "umiejetnosci": {"atak": 62, "obrona": 55, "zagrywka": 58, "blok": 68}, "forma": 82, "kontuzja": 0, "pensja": 2500, "potencjal": 85},
        {"id": 203, "imie": "Szymon", "nazwisko": "Przyszłość", "pozycja": "Atakujący", "numer": 33, "wiek": 19, "umiejetnosci": {"atak": 70, "obrona": 58, "zagrywka": 62, "blok": 65}, "forma": 88, "kontuzja": 0, "pensja": 3500, "potencjal": 90},
        {"id": 204, "imie": "Dominik", "nazwisko": "Obiecujący", "pozycja": "Rozgrywający", "numer": 34, "wiek": 18, "umiejetnosci": {"atak": 58, "obrona": 68, "zagrywka": 72, "blok": 60}, "forma": 80, "kontuzja": 0, "pensja": 3000, "potencjal": 86},
        {"id": 205, "imie": "Oskar", "nazwisko": "Nadzieja", "pozycja": "Libero", "numer": 35, "wiek": 17, "umiejetnosci": {"atak": 48, "obrona": 78, "zagrywka": 65, "blok": 52}, "forma": 83, "kontuzja": 0, "pensja": 2500, "potencjal": 92},
    ]
    
    st.session_state.starting_lineup = {
        "I": 6, "II": 7, "III": 4, "IV": 1, "V": 2, "VI": 3, "Libero": 5
    }
    
    st.session_state.matches = []
    st.session_state.next_match = {"przeciwnik": "Jastrzębski Węgiel", "dzien": 7}
    st.session_state.match_in_progress = False

# Funkcje
def get_all_players():
    return st.session_state.first_team + st.session_state.reserve_players

def get_player_by_id(player_id):
    for p in get_all_players():
        if p["id"] == player_id:
            return p
    return None

def oblicz_ocena(player):
    avg = sum(player["umiejetnosci"].values()) / 4
    return round(avg * (player["forma"] / 100), 1)

def update_league_table(our_sets, opp_sets):
    """Aktualizuje tabelę ligową po meczu"""
    our_team = st.session_state.club_name
    opponent = st.session_state.next_match["przeciwnik"]
    
    # Nasz wynik
    st.session_state.league_table[our_team]["mecze"] += 1
    st.session_state.league_table[our_team]["sety_plus"] += our_sets
    st.session_state.league_table[our_team]["sety_minus"] += opp_sets
    
    if our_sets > opp_sets:
        st.session_state.league_table[our_team]["wygrane"] += 1
        if our_sets == 3 and opp_sets <= 1:
            st.session_state.league_table[our_team]["punkty"] += 3  # Wygrana 3:0 lub 3:1
        else:
            st.session_state.league_table[our_team]["punkty"] += 2  # Wygrana 3:2
    else:
        st.session_state.league_table[our_team]["przegrane"] += 1
        if our_sets == 2:
            st.session_state.league_table[our_team]["punkty"] += 1  # Porażka 2:3
    
    # Przeciwnik (symulacja)
    st.session_state.league_table[opponent]["mecze"] += 1
    st.session_state.league_table[opponent]["sety_plus"] += opp_sets
    st.session_state.league_table[opponent]["sety_minus"] += our_sets
    
    if opp_sets > our_sets:
        st.session_state.league_table[opponent]["wygrane"] += 1
        if opp_sets == 3 and our_sets <= 1:
            st.session_state.league_table[opponent]["punkty"] += 3
        else:
            st.session_state.league_table[opponent]["punkty"] += 2
    else:
        st.session_state.league_table[opponent]["przegrane"] += 1
        if opp_sets == 2:
            st.session_state.league_table[opponent]["punkty"] += 1

def display_animated_court(set_team, set_opp, action_text, ball_position=None):
    """Wyświetla animowane boisko z piłką"""
    
    # Tablica wyników
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                padding: 20px; border-radius: 15px; margin: 20px 0; color: white; text-align: center;'>
        <div style='display: flex; justify-content: space-around; align-items: center;'>
            <div style='font-size: 24px; font-weight: bold;'>🔵 {st.session_state.club_name}</div>
            <div style='font-size: 64px; font-weight: bold;'>{set_team} : {set_opp}</div>
            <div style='font-size: 24px; font-weight: bold;'>🟡 {st.session_state.next_match["przeciwnik"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Akcja
    if action_text:
        st.markdown(f"""
        <div style='background: rgba(0,0,0,0.9); color: #00ff00; padding: 20px; 
                    border-radius: 10px; font-size: 24px; font-weight: bold; 
                    text-align: center; margin: 20px 0; font-family: monospace;
                    border: 2px solid #00ff00;'>
            {action_text}
        </div>
        """, unsafe_allow_html=True)
    
    # Boisko z piłką
    lineup = st.session_state.starting_lineup
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); 
                padding: 40px; border-radius: 20px; position: relative;'>
    """, unsafe_allow_html=True)
    
    # Pozycje boiska
    positions_html = """
    <div style='background: #d2691e; border: 6px solid #000; border-radius: 15px; 
                padding: 60px; position: relative; min-height: 600px;'>
    """
    
    # Piłka (jeśli jest)
    if ball_position:
        positions_html += f"""
        <div style='position: absolute; left: {ball_position['left']}; top: {ball_position['top']}; 
                    width: 50px; height: 50px; background: radial-gradient(circle at 30% 30%, #fff, #ff3333);
                    border-radius: 50%; z-index: 1000; 
                    box-shadow: 0 8px 16px rgba(0,0,0,0.5);
                    animation: bounce 0.5s ease-in-out;'>
        </div>
        <style>
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        </style>
        """
    
    # Siatka
    positions_html += """
    <div style='position: absolute; left: 50%; top: 0; bottom: 0; 
                width: 6px; background: repeating-linear-gradient(0deg, #333 0px, #333 10px, transparent 10px, transparent 20px);
                transform: translateX(-50%); z-index: 500;'></div>
    """
    
    # Zawodnicy - linia ataku
    attack_positions = {
        "IV": {"left": "15%", "top": "15%"},
        "III": {"left": "45%", "top": "10%"},
        "II": {"left": "75%", "top": "15%"}
    }
    
    for pos, coords in attack_positions.items():
        pid = lineup.get(pos)
        if pid:
            p = get_player_by_id(pid)
            positions_html += f"""
            <div style='position: absolute; left: {coords["left"]}; top: {coords["top"]}; 
                        transform: translate(-50%, -50%);'>
                <div style='background: linear-gradient(135deg, #2196F3, #1565C0); 
                            width: 90px; height: 90px; border-radius: 50%; 
                            display: flex; flex-direction: column; justify-content: center; 
                            align-items: center; color: white; font-weight: bold;
                            box-shadow: 0 6px 12px rgba(33, 150, 243, 0.5);
                            border: 4px solid #fff;'>
                    <div style='font-size: 32px;'>#{p.get('numer', '?')}</div>
                    <div style='font-size: 11px;'>{p['nazwisko'][:8]}</div>
                </div>
            </div>
            """
    
    # Zawodnicy - linia obrony
    defense_positions = {
        "V": {"left": "15%", "top": "75%"},
        "VI": {"left": "45%", "top": "80%"},
        "I": {"left": "75%", "top": "75%"}
    }
    
    for pos, coords in defense_positions.items():
        pid = lineup.get(pos)
        if pid:
            p = get_player_by_id(pid)
            extra = "⚡" if pos == "I" else "↔️" if pos == "V" else ""
            positions_html += f"""
            <div style='position: absolute; left: {coords["left"]}; top: {coords["top"]}; 
                        transform: translate(-50%, -50%);'>
                <div style='background: linear-gradient(135deg, #2196F3, #1565C0); 
                            width: 90px; height: 90px; border-radius: 50%; 
                            display: flex; flex-direction: column; justify-content: center; 
                            align-items: center; color: white; font-weight: bold;
                            box-shadow: 0 6px 12px rgba(33, 150, 243, 0.5);
                            border: 4px solid #fff;'>
                    <div style='font-size: 32px;'>#{p.get('numer', '?')}</div>
                    <div style='font-size: 11px;'>{p['nazwisko'][:8]} {extra}</div>
                </div>
            </div>
            """
    
    positions_html += "</div></div>"
    
    st.markdown(positions_html, unsafe_allow_html=True)
    
    # Libero info
    lib_id = lineup.get("Libero")
    if lib_id:
        lib = get_player_by_id(lib_id)
        st.info(f"🟡 LIBERO (poza boiskiem): #{lib.get('numer', '?')} {lib['imie']} {lib['nazwisko']}")

def symuluj_akcje_z_animacja(team_str, opp_str, lineup_players):
    """Symuluje akcję z pełną animacją piłki"""
    diff = team_str - opp_str
    prob = 0.5 + (diff / 200)
    prob = max(0.3, min(0.7, prob))
    
    team_wins = random.random() < prob
    
    # Etapy akcji z pozycjami piłki
    phases = []
    
    # 1. Zagrywka
    server = random.choice([p for p in lineup_players if p["pozycja"] != "Libero"])
    phases.append({
        "text": f"⚡ ZAGRYWKA: #{server.get('numer', '?')} {server['nazwisko']}",
        "ball": {"left": "75%", "top": "75%"}
    })
    
    if team_wins:
        # 2. Piłka leci przez siatkę
        phases.append({
            "text": f"🏐 Piłka leci...",
            "ball": {"left": "50%", "top": "45%"}
        })
        
        # 3. Przyjęcie
        receiver = random.choice([p for p in lineup_players if p["pozycja"] in ["Libero", "Przyjmujący"]])
        phases.append({
            "text": f"🛡️ PRZYJĘCIE: #{receiver.get('numer', '?')} {receiver['nazwisko']}",
            "ball": {"left": "30%", "top": "60%"}
        })
        
        # 4. Rozegranie
        setter = next((p for p in lineup_players if p["pozycja"] == "Rozgrywający"), None)
        if setter:
            phases.append({
                "text": f"🎯 ROZEGRANIE: #{setter.get('numer', '?')} {setter['nazwisko']}",
                "ball": {"left": "45%", "top": "35%"}
            })
        
        # 5. Wystawienie do ataku
        phases.append({
            "text": "⬆️ Wystawienie...",
            "ball": {"left": "35%", "top": "20%"}
        })
        
        # 6. Atak
        attacker = random.choice([p for p in lineup_players if p["pozycja"] in ["Atakujący", "Przyjmujący", "Środkowy"]])
        phases.append({
            "text": f"💥 ATAK! #{attacker.get('numer', '?')} {attacker['nazwisko']}",
            "ball": {"left": "30%", "top": "10%"}
        })
        
        # 7. Piłka leci nad siatką
        phases.append({
            "text": "🔥 Piłka leci nad siatką!",
            "ball": {"left": "50%", "top": "5%"}
        })
        
        # 8. Punkt!
        phases.append({
            "text": f"✅ PUNKT! {attacker['nazwisko'].upper()}!",
            "ball": {"left": "70%", "top": "30%"}
        })
    else:
        # Błąd przeciwnika
        phases.append({
            "text": "❌ Błąd przeciwnika",
            "ball": {"left": "65%", "top": "40%"}
        })
        phases.append({
            "text": "✅ PUNKT dla nas!",
            "ball": None
        })
    
    return team_wins, phases

def trenuj_druzyne(all_players=False):
    squad = get_all_players() if all_players else st.session_state.first_team
    
    for p in squad:
        if p["kontuzja"] == 0:
            chance = 0.4 if p.get("potencjal") else 0.3
            max_s = p.get("potencjal", 95)
            
            if random.random() < chance:
                skill = random.choice(list(p["umiejetnosci"].keys()))
                if p["umiejetnosci"][skill] < max_s:
                    p["umiejetnosci"][skill] = min(max_s, p["umiejetnosci"][skill] + 1)
            
            p["forma"] = max(60, min(95, p["forma"] + random.randint(-2, 6)))
        else:
            p["kontuzja"] = max(0, p["kontuzja"] - 1)

def next_day():
    st.session_state.current_day += 1
    
    if st.session_state.current_day % 7 == 0:
        total = sum(p["pensja"] for p in get_all_players())
        st.session_state.budget -= total
    
    for p in get_all_players():
        if p["kontuzja"] == 0 and random.random() < 0.015:
            p["kontuzja"] = random.randint(3, 14)

def validate_lineup():
    lineup = st.session_state.starting_lineup
    for pos in ["I", "II", "III", "IV", "V", "VI", "Libero"]:
        if not lineup.get(pos):
            return False, f"Brak zawodnika na poz. {pos}"
        p = get_player_by_id(lineup[pos])
        if not p:
            return False, "Błąd składu"
        if p["kontuzja"] > 0:
            return False, f"{p['nazwisko']} kontuzjowany"
    return True, "OK"

# UI
st.title("🏐 Volleyball Manager 2024")
st.markdown("---")

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

# Zakładki
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Główna",
    "📊 Tabela Ligi",
    "👥 Kadra",
    "⚙️ Ustawienie",
    "📈 Statystyki",
    "🏐 Mecz LIVE"
])

with tab1:
    st.header("Panel główny")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.matches:
            last = st.session_state.matches[-1]
            if last["wygrana"]:
                st.success(f"✅ Ostatni: Wygrana z {last['przeciwnik']} {last['wynik']}")
            else:
                st.error(f"❌ Ostatni: Porażka z {last['przeciwnik']} {last['wynik']}")
        
        st.markdown("---")
        days = st.session_state.next_match["dzien"] - st.session_state.current_day
        if days > 0:
            st.info(f"🏐 Mecz za {days} dni: {st.session_state.next_match['przeciwnik']}")
        else:
            st.warning("🏐 MECZ DZISIAJ!")
    
    with col2:
        if st.button("🏃 Trening wszystkich", use_container_width=True):
            trenuj_druzyne(all_players=True)
            next_day()
            st.success("✅ Trening!")
            st.rerun()
        
        if st.button("⏭️ Następny dzień", use_container_width=True):
            next_day()
            st.rerun()

with tab2:
    st.header("📊 Tabela Ligi Plus")
    
    # Przygotuj dane tabeli
    table_data = []
    for team, stats in st.session_state.league_table.items():
        table_data.append({
            "Drużyna": "🏆 " + team if team == st.session_state.club_name else team,
            "Mecze": stats["mecze"],
            "Wygrane": stats["wygrane"],
            "Przegrane": stats["przegrane"],
            "Sety": f"{stats['sety_plus']}:{stats['sety_minus']}",
            "Bilans": stats['sety_plus'] - stats['sety_minus'],
            "Punkty": stats["punkty"]
        })
    
    # Sortuj po punktach
    table_data.sort(key=lambda x: (x["Punkty"], x["Bilans"]), reverse=True)
    
    # Dodaj pozycję
    for i, row in enumerate(table_data, 1):
        row["Poz."] = i
    
    # Zmień kolejność kolumn
    df = pd.DataFrame(table_data)
    df = df[["Poz.", "Drużyna", "Mecze", "Wygrane", "Przegrane", "Sety", "Bilans", "Punkty"]]
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Nasza pozycja
    our_pos = next(i for i, row in enumerate(table_data, 1) if row["Drużyna"].endswith(st.session_state.club_name))
    
    if our_pos == 1:
        st.success(f"🥇 Jesteśmy LIDEREM ligi!")
    elif our_pos <= 3:
        st.info(f"🥉 {our_pos}. miejsce - walczymy o podium!")
    elif our_pos <= 6:
        st.warning(f"📊 {our_pos}. miejsce - środek tabeli")
    else:
        st.error(f"⚠️ {our_pos}. miejsce - strefa spadkowa!")

with tab3:
    st.header("👥 Zarządzanie kadrą")
    
    st.info("💡 **UPROSZCZONE ZARZĄDZANIE**: Pierwsza drużyna (7) + Poza składem (wszyscy reszta)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🏆 Pierwsza drużyna (7)")
        
        for p in st.session_state.first_team:
            cols = st.columns([5, 1])
            with cols[0]:
                status = "🤕" if p["kontuzja"] > 0 else "✅"
                pot = f" ⭐Pot:{p['potencjal']}" if p.get("potencjal") else ""
                st.write(f"{status} **#{p.get('numer', '?')} {p['imie']} {p['nazwisko']}**{pot}")
                st.caption(f"{p['pozycja']} • Ocena: {oblicz_ocena(p)} • Forma: {p['forma']}%")
            with cols[1]:
                if st.button("➡️", key=f"out_{p['id']}", help="Poza skład"):
                    st.session_state.first_team.remove(p)
                    st.session_state.reserve_players.append(p)
                    # Usuń z ustawienia
                    for pos, pid in st.session_state.starting_lineup.items():
                        if pid == p["id"]:
                            st.session_state.starting_lineup[pos] = None
                    st.rerun()
            st.markdown("---")
    
    with col2:
        st.subheader("🪑 Poza składem")
        
        for p in st.session_state.reserve_players:
            cols = st.columns([4, 1, 1])
            with cols[0]:
                status = "🤕" if p["kontuzja"] > 0 else "✅"
                pot = f" ⭐{p['potencjal']}" if p.get("potencjal") else ""
                st.write(f"{status} **#{p.get('numer', '?')} {p['nazwisko']}**{pot}")
                st.caption(f"{p['pozycja']} • {oblicz_ocena(p)}")
            with cols[1]:
                if len(st.session_state.first_team) < 7:
                    if st.button("⬅️", key=f"in_{p['id']}", help="Do pierwszej"):
                        st.session_state.reserve_players.remove(p)
                        st.session_state.first_team.append(p)
                        if "potencjal" in p:
                            del p["potencjal"]
                        st.rerun()
            with cols[2]:
                if st.button("🗑️", key=f"del_{p['id']}", help="Zwolnij"):
                    price = int(oblicz_ocena(p) * 1000)
                    st.session_state.budget += price
                    st.session_state.reserve_players.remove(p)
                    st.toast(f"Sprzedano za {price:,} zł!")
                    st.rerun()
            st.markdown("---")

with tab4:
    st.header("⚙️ Ustawienie na mecz")
    
    lineup = st.session_state.starting_lineup
    available = [p for p in st.session_state.first_team if p["kontuzja"] == 0]
    
    # Wizualizacja
    st.subheader("📋 Aktualne")
    
    cols = st.columns(3)
    for i, pos in enumerate(["IV", "III", "II"]):
        pid = lineup.get(pos)
        if pid:
            p = get_player_by_id(pid)
            with cols[i]:
                st.success(f"**{pos}**\n#{p.get('numer', '?')} {p['nazwisko']}\n{p['pozycja']}")
    
    st.markdown("<div style='text-align:center; font-size:18px; margin:15px 0;'>═══ SIATKA ═══</div>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, pos in enumerate(["V", "VI", "I"]):
        pid = lineup.get(pos)
        if pid:
            p = get_player_by_id(pid)
            extra = "⚡" if pos == "I" else "↔️" if pos == "V" else ""
            with cols[i]:
                st.success(f"**{pos} {extra}**\n#{p.get('numer', '?')} {p['nazwisko']}\n{p['pozycja']}")
    
    lid = lineup.get("Libero")
    if lid:
        lib = get_player_by_id(lid)
        st.warning(f"**LIBERO:** #{lib.get('numer', '?')} {lib['nazwisko']}")
    
    st.markdown("---")
    st.subheader("🔧 Zmień skład")
    
    for pos in ["I", "II", "III", "IV", "V", "VI", "Libero"]:
        opts = [f"#{p.get('numer', '?')} {p['nazwisko']} ({p['pozycja']}) - {oblicz_ocena(p)}" for p in available]
        opts.insert(0, "---")
        
        curr = lineup.get(pos)
        idx = 0
        if curr:
            pl = get_player_by_id(curr)
            if pl:
                for i, o in enumerate(opts):
                    if f"#{pl.get('numer', '?')}" in o:
                        idx = i
                        break
        
        sel = st.selectbox(f"Pozycja {pos}", opts, index=idx, key=f"s_{pos}")
        
        if sel != "---":
            num = sel.split("#")[1].split(" ")[0]
            pl = next((p for p in available if str(p.get('numer', '?')) == num), None)
            if pl:
                st.session_state.starting_lineup[pos] = pl["id"]
        else:
            st.session_state.starting_lineup[pos] = None
    
    v, m = validate_lineup()
    if v:
        st.success("✅ Gotowe!")
    else:
        st.error(f"❌ {m}")

with tab5:
    st.header("📈 Statystyki")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bilans sezonu")
        if st.session_state.matches:
            w = sum(1 for m in st.session_state.matches if m["wygrana"])
            st.metric("Wygrane", w)
            st.metric("Przegrane", len(st.session_state.matches) - w)
    
    with col2:
        st.subheader("Top 3 klubu")
        all_p = get_all_players()
        top = sorted(all_p, key=oblicz_ocena, reverse=True)[:3]
        for i, p in enumerate(top, 1):
            st.write(f"{i}. #{p.get('numer', '?')} {p['nazwisko']} - {oblicz_ocena(p)}")

with tab6:
    st.header("🏐 Mecz LIVE")
    
    days = st.session_state.next_match["dzien"] - st.session_state.current_day
    
    if days > 0:
        st.warning(f"Mecz za {days} dni")
    else:
        v, m = validate_lineup()
        
        if not v:
            st.error(m)
        else:
            st.success(f"Mecz: {st.session_state.next_match['przeciwnik']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("⚡ Szybka", use_container_width=True, type="primary"):
                    opp = st.session_state.next_match['przeciwnik']
                    
                    lineup_p = []
                    for pos in ["I", "II", "III", "IV", "V", "VI", "Libero"]:
                        pid = st.session_state.starting_lineup[pos]
                        p = get_player_by_id(pid)
                        if p and pos != "Libero":
                            lineup_p.append(p)
                    
                    sets_us = 0
                    sets_opp = 0
                    sets_det = []
                    
                    while sets_us < 3 and sets_opp < 3:
                        if random.random() < 0.6:
                            sets_us += 1
                            sets_det.append(f"25:{random.randint(20, 23)}")
                        else:
                            sets_opp += 1
                            sets_det.append(f"{random.randint(20, 23)}:25")
                    
                    # Aktualizuj tabelę
                    update_league_table(sets_us, sets_opp)
                    
                    if sets_us > sets_opp:
                        st.balloons()
                        st.success(f"🎉 WYGRANA {sets_us}:{sets_opp}!")
                        st.session_state.budget += 25000
                        st.session_state.morale = min(100, st.session_state.morale + 5)
                    else:
                        st.error(f"😞 Porażka {sets_us}:{sets_opp}")
                        st.session_state.budget += 10000
                        st.session_state.morale = max(50, st.session_state.morale - 3)
                    
                    st.session_state.matches.append({
                        "przeciwnik": opp,
                        "wynik": f"{sets_us}:{sets_opp}",
                        "sety": sets_det,
                        "wygrana": sets_us > sets_opp
                    })
                    
                    # Następny przeciwnik
                    next_opp = random.choice([t for t in st.session_state.league_teams if t != st.session_state.club_name and t != opp])
                    st.session_state.next_match = {"przeciwnik": next_opp, "dzien": st.session_state.current_day + 7}
                    
                    if st.button("✅ OK"):
                        st.rerun()
            
            with col2:
                if st.button("🎬 ANIMACJA!", use_container_width=True, type="secondary"):
                    st.session_state.match_in_progress = True
                    st.rerun()
            
            if st.session_state.match_in_progress:
                opp = st.session_state.next_match['przeciwnik']
                
                lineup_p = []
                for pos in ["I", "II", "III", "IV", "V", "VI"]:
                    pid = st.session_state.starting_lineup[pos]
                    p = get_player_by_id(pid)
                    if p:
                        lineup_p.append(p)
                
                lib_id = st.session_state.starting_lineup["Libero"]
                if lib_id:
                    lineup_p.append(get_player_by_id(lib_id))
                
                team_str = sum(oblicz_ocena(p) for p in lineup_p) / len(lineup_p)
                opp_str = random.randint(70, 85)
                
                court_place = st.empty()
                
                sets_us = 0
                sets_opp = 0
                sets_det = []
                set_n = 1
                
                while sets_us < 3 and sets_opp < 3:
                    max_p = 15 if set_n == 5 else 25
                    
                    st.write(f"### Set {set_n}")
                    
                    s_us = 0
                    s_opp = 0
                    
                    while True:
                        team_wins, phases = symuluj_akcje_z_animacja(team_str, opp_str, lineup_p)
                        
                        for phase in phases:
                            with court_place.container():
                                display_animated_court(s_us, s_opp, phase["text"], phase.get("ball"))
                            time.sleep(0.8)
                        
                        if team_wins:
                            s_us += 1
                        else:
                            s_opp += 1
                        
                        if s_us >= max_p and s_us - s_opp >= 2:
                            sets_us += 1
                            sets_det.append(f"{s_us}:{s_opp}")
                            st.success(f"✅ Wygraliśmy set!")
                            break
                        elif s_opp >= max_p and s_opp - s_us >= 2:
                            sets_opp += 1
                            sets_det.append(f"{s_us}:{s_opp}")
                            st.error(f"❌ Przegraliśmy set")
                            break
                    
                    set_n += 1
                    time.sleep(1.5)
                
                # Aktualizuj tabelę
                update_league_table(sets_us, sets_opp)
                
                if sets_us > sets_opp:
                    st.balloons()
                    st.success(f"### 🎉 ZWYCIĘSTWO {sets_us}:{sets_opp}!")
                    st.session_state.budget += 25000
                    st.session_state.morale = min(100, st.session_state.morale + 5)
                else:
                    st.error(f"### 😞 PORAŻKA {sets_us}:{sets_opp}")
                    st.session_state.budget += 10000
                    st.session_state.morale = max(50, st.session_state.morale - 3)
                
                st.session_state.matches.append({
                    "przeciwnik": opp,
                    "wynik": f"{sets_us}:{sets_opp}",
                    "sety": sets_det,
                    "wygrana": sets_us > sets_opp
                })
                
                next_opp = random.choice([t for t in st.session_state.league_teams if t != st.session_state.club_name and t != opp])
                st.session_state.next_match = {"przeciwnik": next_opp, "dzien": st.session_state.current_day + 7}
                st.session_state.match_in_progress = False
                
                if st.button("✅ Zakończ"):
                    st.rerun()

st.markdown("---")
st.markdown("*Volleyball Manager 2024 - Final Edition* 🏐")

