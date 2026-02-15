import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="Volleyball Manager 2024", page_icon="🏐", layout="wide")

# Inicjalizacja
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_season = 1
    st.session_state.budget = 500000
    st.session_state.club_name = "MKS Warszawa"
    st.session_state.current_day = 1
    st.session_state.morale = 75
    
    st.session_state.league_teams = [
        "MKS Warszawa", "Jastrzębski Węgiel", "ZAKSA Kędzierzyn-Koźle",
        "Projekt Warszawa", "Aluron Zawiercie", "Trefl Gdańsk",
        "PGE Skra Bełchatów", "AZS Kraków", "Indykpol AZS Olsztyn", "Bogdanka LUK Lublin"
    ]
    
    st.session_state.league_table = {}
    for team in st.session_state.league_teams:
        st.session_state.league_table[team] = {
            "mecze": 0, "wygrane": 0, "przegrane": 0,
            "sety_plus": 0, "sety_minus": 0, "punkty": 0
        }
    
    st.session_state.first_team = [
        {"id": 1, "imie": "Jakub", "nazwisko": "Kowalski", "pozycja": "Przyjmujący", "numer": 10, "wiek": 24, "umiejetnosci": {"atak": 85, "obrona": 82, "zagrywka": 75, "blok": 72}, "forma": 80, "kontuzja": 0, "pensja": 15000},
        {"id": 2, "imie": "Piotr", "nazwisko": "Nowak", "pozycja": "Środkowy", "numer": 2, "wiek": 27, "umiejetnosci": {"atak": 78, "obrona": 65, "zagrywka": 68, "blok": 88}, "forma": 75, "kontuzja": 0, "pensja": 12000},
        {"id": 3, "imie": "Marcin", "nazwisko": "Wiśniewski", "pozycja": "Rozgrywający", "numer": 1, "wiek": 26, "umiejetnosci": {"atak": 65, "obrona": 80, "zagrywka": 85, "blok": 68}, "forma": 82, "kontuzja": 0, "pensja": 14000},
        {"id": 4, "imie": "Tomasz", "nazwisko": "Lewandowski", "pozycja": "Atakujący", "numer": 11, "wiek": 22, "umiejetnosci": {"atak": 88, "obrona": 68, "zagrywka": 77, "blok": 82}, "forma": 85, "kontuzja": 0, "pensja": 16000},
        {"id": 5, "imie": "Kamil", "nazwisko": "Wójcik", "pozycja": "Libero", "numer": 8, "wiek": 29, "umiejetnosci": {"atak": 55, "obrona": 92, "zagrywka": 78, "blok": 60}, "forma": 78, "kontuzja": 0, "pensja": 11000},
        {"id": 6, "imie": "Adam", "nazwisko": "Kamiński", "pozycja": "Przyjmujący", "numer": 12, "wiek": 25, "umiejetnosci": {"atak": 80, "obrona": 84, "zagrywka": 80, "blok": 75}, "forma": 83, "kontuzja": 0, "pensja": 15000},
        {"id": 7, "imie": "Michał", "nazwisko": "Zieliński", "pozycja": "Środkowy", "numer": 19, "wiek": 23, "umiejetnosci": {"atak": 75, "obrona": 62, "zagrywka": 65, "blok": 85}, "forma": 77, "kontuzja": 0, "pensja": 10000},
    ]
    
    st.session_state.reserve_players = [
        {"id": 8, "imie": "Paweł", "nazwisko": "Szymański", "pozycja": "Przyjmujący", "numer": 13, "wiek": 28, "umiejetnosci": {"atak": 76, "obrona": 78, "zagrywka": 72, "blok": 70}, "forma": 80, "kontuzja": 0, "pensja": 13000},
        {"id": 9, "imie": "Krzysztof", "nazwisko": "Dąbrowski", "pozycja": "Atakujący", "numer": 9, "wiek": 21, "umiejetnosci": {"atak": 82, "obrona": 64, "zagrywka": 70, "blok": 78}, "forma": 88, "kontuzja": 0, "pensja": 11000},
        {"id": 10, "imie": "Bartosz", "nazwisko": "Jankowski", "pozycja": "Rozgrywający", "numer": 5, "wiek": 30, "umiejetnosci": {"atak": 62, "obrona": 82, "zagrywka": 80, "blok": 65}, "forma": 72, "kontuzja": 0, "pensja": 12000},
        {"id": 11, "imie": "Mateusz", "nazwisko": "Kozłowski", "pozycja": "Środkowy", "numer": 18, "wiek": 26, "umiejetnosci": {"atak": 72, "obrona": 60, "zagrywka": 63, "blok": 82}, "forma": 75, "kontuzja": 0, "pensja": 9500},
        {"id": 12, "imie": "Łukasz", "nazwisko": "Wojciechowski", "pozycja": "Libero", "numer": 6, "wiek": 27, "umiejetnosci": {"atak": 52, "obrona": 88, "zagrywka": 75, "blok": 58}, "forma": 76, "kontuzja": 0, "pensja": 10000},
    ]
    
    st.session_state.starting_lineup = {
        "I": 6, "II": 7, "III": 4, "IV": 1, "V": 2, "VI": 3, "Libero": 5
    }
    
    # Na boisku podczas meczu (6 zawodników - bez środkowych i libero)
    st.session_state.on_court = []
    st.session_state.off_court_middle = []  # Środkowi poza
    st.session_state.off_court_libero = None  # Libero poza
    
    st.session_state.matches = []
    st.session_state.next_match = {"przeciwnik": "Jastrzębski Węgiel", "dzien": 7}
    st.session_state.match_in_progress = False

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
    our_team = st.session_state.club_name
    opponent = st.session_state.next_match["przeciwnik"]
    
    st.session_state.league_table[our_team]["mecze"] += 1
    st.session_state.league_table[our_team]["sety_plus"] += our_sets
    st.session_state.league_table[our_team]["sety_minus"] += opp_sets
    
    if our_sets > opp_sets:
        st.session_state.league_table[our_team]["wygrane"] += 1
        if our_sets == 3 and opp_sets <= 1:
            st.session_state.league_table[our_team]["punkty"] += 3
        else:
            st.session_state.league_table[our_team]["punkty"] += 2
    else:
        st.session_state.league_table[our_team]["przegrane"] += 1
        if our_sets == 2:
            st.session_state.league_table[our_team]["punkty"] += 1
    
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

def display_court_simple(set_team, set_opp, action_text, ball_emoji=""):
    """Proste wyświetlanie boiska bez HTML"""
    
    # Wynik
    st.markdown(f"## 🔵 {st.session_state.club_name}  **{set_team} : {set_opp}**  🟡 {st.session_state.next_match['przeciwnik']}")
    
    if action_text:
        st.success(f"### {ball_emoji} {action_text}")
    
    st.markdown("---")
    
    # Boisko
    lineup = st.session_state.starting_lineup
    
    st.write("**BOISKO:**")
    st.write("")
    
    # Linia ataku
    col1, col2, col3 = st.columns(3)
    for i, (col, pos) in enumerate(zip([col1, col2, col3], ["IV", "III", "II"])):
        pid = lineup.get(pos)
        if pid:
            p = get_player_by_id(pid)
            with col:
                st.info(f"**Poz {pos}**\n#{p.get('numer', '?')} {p['nazwisko']}\n{p['pozycja']}")
    
    st.markdown("### ═══════ SIATKA ═══════")
    
    # Linia obrony
    col1, col2, col3 = st.columns(3)
    for i, (col, pos) in enumerate(zip([col1, col2, col3], ["V", "VI", "I"])):
        pid = lineup.get(pos)
        if pid:
            p = get_player_by_id(pid)
            with col:
                extra = "⚡" if pos == "I" else ""
                st.info(f"**Poz {pos} {extra}**\n#{p.get('numer', '?')} {p['nazwisko']}\n{p['pozycja']}")
    
    st.write("")
    
    # Poza boiskiem
    col1, col2 = st.columns(2)
    
    with col1:
        # Środkowi poza
        srodkowi_poza = []
        for pos in ["II", "V"]:
            pid = lineup.get(pos)
            if pid:
                p = get_player_by_id(pid)
                if p["pozycja"] == "Środkowy":
                    srodkowi_poza.append(p)
        
        if srodkowi_poza:
            st.warning(f"**ŚRODKOWI (poza):** " + ", ".join([f"#{p['numer']} {p['nazwisko']}" for p in srodkowi_poza]))
    
    with col2:
        # Libero poza
        lib_id = lineup.get("Libero")
        if lib_id:
            lib = get_player_by_id(lib_id)
            st.warning(f"**LIBERO (poza):** #{lib.get('numer', '?')} {lib['nazwisko']}")

def symuluj_akcje(team_str, opp_str, lineup_players):
    """Symuluje akcję z opisem"""
    diff = team_str - opp_str
    prob = 0.5 + (diff / 200)
    prob = max(0.3, min(0.7, prob))
    
    team_wins = random.random() < prob
    
    phases = []
    
    # Zagrywka
    server = random.choice([p for p in lineup_players if p["pozycja"] != "Libero"])
    phases.append(("⚡", f"ZAGRYWKA: #{server.get('numer', '?')} {server['nazwisko']}"))
    
    if team_wins:
        # Przyjęcie
        receiver = random.choice([p for p in lineup_players if p["pozycja"] in ["Libero", "Przyjmujący"]])
        phases.append(("🛡️", f"PRZYJĘCIE: #{receiver.get('numer', '?')} {receiver['nazwisko']}"))
        
        # Rozegranie
        setter = next((p for p in lineup_players if p["pozycja"] == "Rozgrywający"), None)
        if setter:
            phases.append(("🎯", f"ROZEGRANIE: #{setter.get('numer', '?')} {setter['nazwisko']}"))
        
        # Atak
        attacker = random.choice([p for p in lineup_players if p["pozycja"] in ["Atakujący", "Przyjmujący", "Środkowy"]])
        phases.append(("💥", f"ATAK! #{attacker.get('numer', '?')} {attacker['nazwisko']} - PUNKT!"))
    else:
        phases.append(("❌", "Błąd przeciwnika - PUNKT dla nas!"))
    
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
            return False, f"Brak na poz. {pos}"
        p = get_player_by_id(lineup[pos])
        if not p:
            return False, "Błąd"
        if p["kontuzja"] > 0:
            return False, f"{p['nazwisko']} kontuzja"
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

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Główna",
    "📊 Tabela",
    "👥 Kadra",
    "⚙️ Skład",
    "📈 Stats",
    "🏐 Mecz"
])

with tab1:
    st.header("Panel")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.matches:
            last = st.session_state.matches[-1]
            if last["wygrana"]:
                st.success(f"✅ Wygrana {last['wynik']} z {last['przeciwnik']}")
            else:
                st.error(f"❌ Porażka {last['wynik']} z {last['przeciwnik']}")
        
        days = st.session_state.next_match["dzien"] - st.session_state.current_day
        if days > 0:
            st.info(f"🏐 Mecz za {days} dni: {st.session_state.next_match['przeciwnik']}")
        else:
            st.warning("🏐 MECZ DZISIAJ!")
    
    with col2:
        if st.button("🏃 Trening", use_container_width=True):
            trenuj_druzyne(True)
            next_day()
            st.success("✅")
            st.rerun()
        
        if st.button("⏭️ Dzień", use_container_width=True):
            next_day()
            st.rerun()

with tab2:
    st.header("📊 Liga")
    
    table_data = []
    for team, stats in st.session_state.league_table.items():
        table_data.append({
            "Drużyna": "🏆 " + team if team == st.session_state.club_name else team,
            "M": stats["mecze"],
            "W": stats["wygrane"],
            "P": stats["przegrane"],
            "Sety": f"{stats['sety_plus']}:{stats['sety_minus']}",
            "Bil": stats['sety_plus'] - stats['sety_minus'],
            "Pkt": stats["punkty"]
        })
    
    table_data.sort(key=lambda x: (x["Pkt"], x["Bil"]), reverse=True)
    
    for i, row in enumerate(table_data, 1):
        row["#"] = i
    
    df = pd.DataFrame(table_data)
    df = df[["#", "Drużyna", "M", "W", "P", "Sety", "Bil", "Pkt"]]
    
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab3:
    st.header("👥 Kadra")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Pierwsza (7)")
        
        for p in st.session_state.first_team:
            c = st.columns([5, 1])
            with c[0]:
                s = "🤕" if p["kontuzja"] > 0 else "✅"
                pot = f"⭐{p['potencjal']}" if p.get("potencjal") else ""
                st.write(f"{s} #{p['numer']} **{p['nazwisko']}** {pot}")
                st.caption(f"{p['pozycja']} • {oblicz_ocena(p)}")
            with c[1]:
                if st.button("→", key=f"o{p['id']}"):
                    st.session_state.first_team.remove(p)
                    st.session_state.reserve_players.append(p)
                    for pos, pid in st.session_state.starting_lineup.items():
                        if pid == p["id"]:
                            st.session_state.starting_lineup[pos] = None
                    st.rerun()
            st.divider()
    
    with col2:
        st.subheader("🪑 Poza")
        
        for p in st.session_state.reserve_players:
            c = st.columns([4, 1, 1])
            with c[0]:
                s = "🤕" if p["kontuzja"] > 0 else "✅"
                pot = f"⭐{p['potencjal']}" if p.get("potencjal") else ""
                st.write(f"{s} #{p['numer']} {p['nazwisko']} {pot}")
                st.caption(f"{p['pozycja']}")
            with c[1]:
                if len(st.session_state.first_team) < 7:
                    if st.button("←", key=f"i{p['id']}"):
                        st.session_state.reserve_players.remove(p)
                        st.session_state.first_team.append(p)
                        if "potencjal" in p:
                            del p["potencjal"]
                        st.rerun()
            with c[2]:
                if st.button("🗑", key=f"d{p['id']}"):
                    pr = int(oblicz_ocena(p) * 1000)
                    st.session_state.budget += pr
                    st.session_state.reserve_players.remove(p)
                    st.rerun()
            st.divider()

with tab4:
    st.header("⚙️ Skład")
    
    lineup = st.session_state.starting_lineup
    available = [p for p in st.session_state.first_team if p["kontuzja"] == 0]
    
    st.subheader("Wizualizacja")
    
    c = st.columns(3)
    for i, pos in enumerate(["IV", "III", "II"]):
        pid = lineup.get(pos)
        if pid:
            p = get_player_by_id(pid)
            with c[i]:
                st.info(f"**{pos}**\n#{p['numer']} {p['nazwisko']}")
    
    st.write("### ═══ SIATKA ═══")
    
    c = st.columns(3)
    for i, pos in enumerate(["V", "VI", "I"]):
        pid = lineup.get(pos)
        if pid:
            p = get_player_by_id(pid)
            with c[i]:
                ex = "⚡" if pos == "I" else ""
                st.info(f"**{pos} {ex}**\n#{p['numer']} {p['nazwisko']}")
    
    lid = lineup.get("Libero")
    if lid:
        lib = get_player_by_id(lid)
        st.warning(f"LIBERO: #{lib['numer']} {lib['nazwisko']}")
    
    st.divider()
    st.subheader("Edycja")
    
    for pos in ["I", "II", "III", "IV", "V", "VI", "Libero"]:
        opts = [f"#{p['numer']} {p['nazwisko']} ({p['pozycja']})" for p in available]
        opts.insert(0, "---")
        
        curr = lineup.get(pos)
        idx = 0
        if curr:
            pl = get_player_by_id(curr)
            if pl:
                for i, o in enumerate(opts):
                    if f"#{pl['numer']}" in o:
                        idx = i
                        break
        
        sel = st.selectbox(f"Poz {pos}", opts, index=idx, key=f"s{pos}")
        
        if sel != "---":
            num = sel.split("#")[1].split(" ")[0]
            pl = next((p for p in available if str(p['numer']) == num), None)
            if pl:
                st.session_state.starting_lineup[pos] = pl["id"]
        else:
            st.session_state.starting_lineup[pos] = None
    
    v, m = validate_lineup()
    if v:
        st.success("✅ OK")
    else:
        st.error(f"❌ {m}")

with tab5:
    st.header("📈 Statystyki")
    
    if st.session_state.matches:
        w = sum(1 for m in st.session_state.matches if m["wygrana"])
        st.metric("Wygrane", w)
        st.metric("Przegrane", len(st.session_state.matches) - w)

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
            st.success(f"Przeciwnik: {st.session_state.next_match['przeciwnik']}")
            
            # Przyciski
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("⚡ SZYBKA", use_container_width=True, type="primary"):
                    opp = st.session_state.next_match['przeciwnik']
                    
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
                    
                    update_league_table(sets_us, sets_opp)
                    
                    if sets_us > sets_opp:
                        st.balloons()
                        st.success(f"🎉 {sets_us}:{sets_opp}!")
                        st.session_state.budget += 25000
                        st.session_state.morale = min(100, st.session_state.morale + 5)
                    else:
                        st.error(f"😞 {sets_us}:{sets_opp}")
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
                    
                    time.sleep(1)
                    st.rerun()
            
            with col2:
                if st.button("🎬 ANIMACJA", use_container_width=True, type="secondary"):
                    st.session_state.match_in_progress = True
                    st.rerun()
            
            # Mecz z animacją
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
                
                # Panel zmian
                st.sidebar.header("🔄 ZMIANY")
                bench_available = [p for p in st.session_state.first_team if p not in lineup_p and p["kontuzja"] == 0]
                
                if bench_available:
                    st.sidebar.write("**Ławka:**")
                    for bp in bench_available:
                        if st.sidebar.button(f"Wpuść #{bp['numer']} {bp['nazwisko']}", key=f"sub_{bp['id']}"):
                            # Wybierz kogo zmienić
                            st.sidebar.write("Kogo zmienić?")
                            for lp in lineup_p:
                                if lp["pozycja"] == bp["pozycja"]:
                                    if st.sidebar.button(f"Zmień #{lp['numer']}", key=f"out_{lp['id']}"):
                                        lineup_p.remove(lp)
                                        lineup_p.append(bp)
                                        st.sidebar.success(f"✅ Zmiana: #{bp['numer']} za #{lp['numer']}")
                                        time.sleep(0.5)
                
                while sets_us < 3 and sets_opp < 3:
                    max_p = 15 if set_n == 5 else 25
                    
                    st.write(f"## Set {set_n}")
                    
                    s_us = 0
                    s_opp = 0
                    
                    while True:
                        team_wins, phases = symuluj_akcje(team_str, opp_str, lineup_p)
                        
                        for emoji, text in phases:
                            with court_place.container():
                                display_court_simple(s_us, s_opp, text, emoji)
                            time.sleep(1)
                        
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
                    time.sleep(1)
                
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
                
                if st.button("✅ Zakończ mecz"):
                    st.rerun()

st.markdown("---")
st.markdown("*Volleyball Manager 2024*")
