#!/usr/bin/env python3
import asyncio
import aiohttp
import socket
import concurrent.futures
import os
import requests
from typing import List
from colorama import Fore, Style
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, number_type
from prettytable import PrettyTable

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ───────────────────────────────
# Banner
# ───────────────────────────────
banner = r"""
  __    __   ____  ____  _____  ___  ___________  ______     _______  ___________  __      ______    _____  ___           
 /" |  | "\ ("  _||_ " |(\"   \|"  \("     _   ")/    " \   /"      \("     _   ")|" \    /    " \  (\"   \|"  \   |      ___  __________________  ___  ______________  _  __  ____  _________  ________
(:  (__)  :)|   (  ) : ||.\\   \    |)__/  \\__/// ____  \ |:        |)__/  \\__/ ||  |  // ____  \ |.\\   \    |  |  	 / _ \/  _/ __/_  __/ __ \/ _ \/_  __/  _/ __ \/ |/ / / __ \/ __/  _/ |/ /_  __/
 \/      \/ (:  |  | . )|: \.   \\  |   \\_ /  /  /    ) :)|_____/   )   \\_ /    |:  | /  /    ) :)|: \.   \\  |  |    / // // /_\ \  / / / /_/ / , _/ / / _/ // /_/ /    / / /_/ /\ \_/ //    / / /   
 //  __  \\  \\ \__/ // |.  \    \. |   |.  | (: (____/ //  //      /    |.  |    |.  |(: (____/ // |.  \    \. |  |   /____/___/___/ /_/  \____/_/|_| /_/ /___/\____/_/|_/  \____/___/___/_/|_/ /_/    
(:  (  )  :) /\\ __ //\ |    \    \ |   \:  |  \        /  |:  __   \    \:  |    /\  |\\        /  |    \    \ |  |                                                                                 
 \__|  |__/ (__________) \___|\____\)    \__|   \"_____/   |__|  \___)    \__|   (__\_|_)\"_____/    \___|\____\)  |  
      
TIKTOK: @rootgosint
DISCORD: @rootgosint
INSTAGRAM: @rootgosint
SERVER DISCORD: Distortion | OSINT
       

ROOTGOSINT | V1.0 - MULTITOOL
----------------------------------------------------
⚠️  DISCLAIMER: Strumento a scopo educativo.
   Usare solo su propri sistemi o con permesso.
  Non mi assumo responsabilià per usi impropri
  di questo tool. Buon proseguimento
────────────────────────────────────────────────────
"""

def print_banner():
    MAGENTA = "\033[1;35m"
    RESET = "\033[0m"
    print(MAGENTA + banner + RESET)

DEFAULT_SITES = [
    # ───── Social & General ─────
    ("GitHub", "https://github.com/{username}"),
    ("Twitter", "https://twitter.com/{username}"),
    ("Instagram", "https://www.instagram.com/{username}/"),
    ("Reddit", "https://www.reddit.com/user/{username}"),
    ("TikTok", "https://www.tiktok.com/@{username}"),
    ("YouTube", "https://www.youtube.com/{username}"),
    ("Twitch", "https://www.twitch.tv/{username}"),
    ("Pinterest", "https://www.pinterest.com/{username}"),
    ("Snapchat", "https://www.snapchat.com/add/{username}"),
    ("Threads", "https://www.threads.net/@{username}"),
    ("Mastodon", "https://mastodon.social/@{username}"),
    ("TruthSocial", "https://truthsocial.com/@{username}"),
    ("Gettr", "https://gettr.com/user/{username}"),
    ("Gab", "https://gab.com/{username}"),
    ("VK", "https://vk.com/{username}"),
    ("Odysee", "https://odysee.com/@{username}"),
    ("Rumble", "https://rumble.com/user/{username}"),
    ("Dailymotion", "https://www.dailymotion.com/{username}"),
    ("Telegram", "https://t.me/{username}"),
    ("Keybase", "https://keybase.io/{username}"),
    ("AboutMe", "https://about.me/{username}"),
    ("Patreon", "https://www.patreon.com/{username}"),
    ("OnlyFans", "https://onlyfans.com/{username}"),
    ("KoFi", "https://ko-fi.com/{username}"),
    ("BuyMeACoffee", "https://www.buymeacoffee.com/{username}"),

    # ───── Developer / Tech ─────
    ("GitLab", "https://gitlab.com/{username}"),
    ("Bitbucket", "https://bitbucket.org/{username}"),
    ("SourceForge", "https://sourceforge.net/u/{username}"),
    ("StackOverflow", "https://stackoverflow.com/users/{username}"),
    ("Kaggle", "https://www.kaggle.com/{username}"),
    ("Replit", "https://replit.com/@{username}"),
    ("CodePen", "https://codepen.io/{username}"),
    ("Dev.to", "https://dev.to/{username}"),
    ("Hashnode", "https://hashnode.com/@{username}"),
    ("HuggingFace", "https://huggingface.co/{username}"),
    ("JSFiddle", "https://jsfiddle.net/user/{username}"),
    ("HackerRank", "https://www.hackerrank.com/{username}"),
    ("LeetCode", "https://leetcode.com/{username}"),
    ("TopCoder", "https://www.topcoder.com/members/{username}"),
    ("Codewars", "https://www.codewars.com/users/{username}"),
    ("Exercism", "https://exercism.org/profiles/{username}"),
    ("StackExchange", "https://stackexchange.com/users/{username}"),
    ("npm", "https://www.npmjs.com/~{username}"),
    ("PyPI", "https://pypi.org/user/{username}"),
    ("DockerHub", "https://hub.docker.com/u/{username}"),
    ("RubyGems", "https://rubygems.org/profiles/{username}"),
    ("CPAN", "https://metacpan.org/author/{username}"),
    ("Arduino", "https://create.arduino.cc/users/{username}"),
    ("Hackaday", "https://hackaday.io/{username}"),

    # ───── Gaming ─────
    ("Steam", "https://steamcommunity.com/id/{username}"),
    ("EpicGames", "https://www.epicgames.com/id/{username}"),
    ("Xbox", "https://xboxgamertag.com/search/{username}"),
    ("PlayStation", "https://psnprofiles.com/{username}"),
    ("Roblox", "https://www.roblox.com/user.aspx?username={username}"),
    ("Minecraft", "https://namemc.com/profile/{username}"),
    ("Speedrun", "https://www.speedrun.com/user/{username}"),
    ("Chess.com", "https://www.chess.com/member/{username}"),
    ("Lichess", "https://lichess.org/@/{username}"),
    ("GameJolt", "https://gamejolt.com/@{username}"),
    ("ModDB", "https://www.moddb.com/members/{username}"),
    ("Itch.io", "https://itch.io/profile/{username}"),
    ("Valorant", "https://tracker.gg/valorant/profile/riot/{username}/overview"),
    ("Fortnite", "https://fortnitetracker.com/profile/all/{username}"),
    ("ApexLegends", "https://apex.tracker.gg/apex/profile/origin/{username}/overview"),
    ("PUBG", "https://pubg.op.gg/user/{username}"),
    ("CSGO", "https://csgostats.gg/player/{username}"),
    ("Dota2", "https://www.dotabuff.com/players/{username}"),
    ("Overwatch", "https://overbuff.com/players/{username}"),
    ("Hearthstone", "https://www.hearthstonetopdecks.com/player/{username}"),
    ("GOG", "https://www.gog.com/u/{username}"),

    # ───── Blogging / Writing ─────
    ("Medium", "https://medium.com/@{username}"),
    ("WordPress", "https://{username}.wordpress.com"),
    ("Blogger", "https://{username}.blogspot.com"),
    ("Tumblr", "https://{username}.tumblr.com"),
    ("Wattpad", "https://www.wattpad.com/user/{username}"),
    ("Substack", "https://{username}.substack.com"),
    ("Ghost", "https://{username}.ghost.io"),
    ("LiveJournal", "https://{username}.livejournal.com"),

    # ───── Community & Misc ─────
    ("Quora", "https://www.quora.com/profile/{username}"),
    ("Goodreads", "https://www.goodreads.com/{username}"),
    ("Letterboxd", "https://letterboxd.com/{username}"),
    ("MyAnimeList", "https://myanimelist.net/profile/{username}"),
    ("AniList", "https://anilist.co/user/{username}"),
    ("LastFM", "https://www.last.fm/user/{username}"),
    ("Discogs", "https://www.discogs.com/user/{username}"),
    ("SoundCloud", "https://soundcloud.com/{username}"),
    ("Bandcamp", "https://{username}.bandcamp.com"),
    ("Mixcloud", "https://www.mixcloud.com/{username}"),
    ("Spotify", "https://open.spotify.com/user/{username}"),
    ("Genius", "https://genius.com/{username}"),
]



HEADERS = {"User-Agent": "rootgosint-multitool/1.0"}

async def check_site(session: aiohttp.ClientSession, service: str, url_template: str, username: str, timeout: int):
    url = url_template.format(username=username)
    try:
        async with session.get(url, timeout=timeout, allow_redirects=True) as resp:
            status = resp.status
            exists = status in (200, 301, 302)
            return {"service": service, "url": url, "status": status, "exists": exists}
    except asyncio.TimeoutError:
        return {"service": service, "url": url, "status": "timeout", "exists": False}
    except Exception as e:
        return {"service": service, "url": url, "status": f"error: {e}", "exists": False}

async def run_checks(username: str, sites: List, concurrency: int, timeout: int):
    connector = aiohttp.TCPConnector(limit_per_host=concurrency, ssl=False)
    timeout_obj = aiohttp.ClientTimeout(total=None, sock_connect=timeout, sock_read=timeout)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout_obj, headers=HEADERS) as session:
        sem = asyncio.Semaphore(concurrency)
        tasks = []

        async def sem_task(service, url_template):
            async with sem:
                return await check_site(session, service, url_template, username, timeout)

        for service, url_template, *_ in sites:
            tasks.append(asyncio.create_task(sem_task(service, url_template)))

        results = await asyncio.gather(*tasks)
        return results

def pretty_print(results):
    for r in results:
        mark = "FOUND" if r.get("exists") else "----"
        print(f"[{mark}] {r['service']:<10} {r['status']:>6} {r['url']}")

def userhunter():
    username = input(Fore.LIGHTMAGENTA_EX + "[+] Insert target username: ").strip()
    if not username:
        print("⚠️ Nessun username inserito, uscita...")
        return
    results = asyncio.run(run_checks(username, DEFAULT_SITES, concurrency=20, timeout=10))
    pretty_print(results)

# ───────────────────────────────
# Port Scanner
# ───────────────────────────────
def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            result = sock.connect_ex((ip, port))
            return port if result == 0 else None
    except:
        return None

def portscanner():
    target = input(Fore.LIGHTMAGENTA_EX + "[+] Insert target IP: ").strip()
    print(f"\n[🔎] Scanning all 65535 ports on {target}...\n")

    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2000) as executor:
        futures = {executor.submit(scan_port, target, port): port for port in range(1, 65536)}
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port:
                print(f"[OPEN] Port {port}")
                open_ports.append(port)

    print("\n──────────────────────────────")
    print("   ✅ SCAN COMPLETED")
    print("──────────────────────────────")
    if open_ports:
        print(f"[+] Open ports found: {', '.join(map(str, sorted(open_ports)))}")
    else:
        print("[!] No open ports found.")

# ───────────────────────────────
# GitHub Mail Puller
# ───────────────────────────────
def github_mail_puller():
    Username = input(Fore.LIGHTMAGENTA_EX + "Inserisci il nome utente GitHub --> ")
    repos = input(Fore.LIGHTMAGENTA_EX + "Inserisci il nome del repository --> ")

    try:
        res = requests.get(f"https://api.github.com/repos/{Username}/{repos}/commits")
        data = res.json()

        first_commit = data[0]
        author = first_commit.get('commit', {}).get('author', {})
        Email = author.get('email', 'N/A')
        User = author.get('name', 'N/A')

        print(Fore.CYAN + "\n+----+----------------------+---------------------------+")
        print("| ID | Username             | Email                     |")
        print("+----+----------------------+---------------------------+")
        print(f"| 1  | {User:<20} | {Email:<25} |")
        print("+----+----------------------+---------------------------+\n")

    except Exception as e:
        print(Fore.RED + f"[ERRORE] {e}")

    input(Fore.WHITE + "Premi Invio per tornare al menu...")

# ───────────────────────────────
# PhoneHunter
# ───────────────────────────────
PHONE_SITES = [
    ("WhatsApp", "https://wa.me/{number}"),
    ("Facebook", "https://www.facebook.com/search/top?q={number}"),
    ("Twitter", "https://twitter.com/search?q={number}"),
    ("Instagram", "https://www.instagram.com/{number}"),
]

def phone_lookup():
    number = input(Fore.LIGHTMAGENTA_EX + "[+] Inserisci il numero di telefono (es: +393491234567): ").strip()
    try:
        phone_number = phonenumbers.parse(number)
        if not phonenumbers.is_valid_number(phone_number):
            print(Fore.RED + "[!] Numero non valido.")
            return

        country = geocoder.description_for_number(phone_number, "it")
        sim_carrier = carrier.name_for_number(phone_number, "it")
        line_type = number_type(phone_number)
        timezones = timezone.time_zones_for_number(phone_number)

        line_type_map = {
            0: "FIXED_LINE",
            1: "MOBILE",
            2: "FIXED_LINE_OR_MOBILE",
            3: "TOLL_FREE",
            4: "PREMIUM_RATE",
            5: "SHARED_COST",
            6: "VOIP",
            7: "PERSONAL_NUMBER",
            8: "PAGER",
            9: "UAN",
            10: "VOICEMAIL",
        }
        line_type_str = line_type_map.get(line_type, "Sconosciuto")

        table = PrettyTable()
        table.field_names = ["🔎 Campo", "📌 Valore"]
        table.align["🔎 Campo"] = "l"
        table.align["📌 Valore"] = "l"

        table.add_row(["Numero", number])
        table.add_row(["Paese", country or "N/A"])
        table.add_row(["Carrier", sim_carrier or "N/A"])
        table.add_row(["Tipo linea", line_type_str])
        table.add_row(["Fuso orario", ", ".join(timezones) if timezones else "N/A"])

        print(Fore.CYAN + "\n[📞] Informazioni sul numero:\n" + Style.RESET_ALL)
        print(table)
        
        print(Fore.CYAN + "\n[🌐] Ricerca su Social / Web:\n" + Style.RESET_ALL)

        socials = {
            "WhatsApp": f"https://wa.me/{number.replace('+','')}",
            "Telegram": f"https://t.me/{number}",
            "Facebook": f"https://www.facebook.com/search/top/?q={number}",
            "Instagram": f"https://www.instagram.com/{number}/",
            "Twitter": f"https://twitter.com/search?q={number}",
            "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={number}",
            "Truecaller (search)": f"https://www.truecaller.com/search/{number.replace('+','')}"
        }

        for social, url in socials.items():
            try:
                r = requests.get(url, timeout=5)
                status = "Possibile Match" if r.status_code in [200, 301, 302] else "Nessun risultato"
            except:
                status = "Errore richiesta"
            print(f"- {social:<12}: {status} → {url}")

        # --- Analisi extra: VoIP / temporaneo ---
        if line_type_str in ["VOIP", "TOLL_FREE", "PREMIUM_RATE"]:
            print(Fore.YELLOW + "\n⚠️ Attenzione: il numero potrebbe essere VoIP o temporaneo." + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"[ERRORE] {e}")

    input(Fore.WHITE + "\nPremi Invio per tornare al menu...")
# ───────────────────────────────
# IP Geolocation Lookup
# ───────────────────────────────
def ip_geolocation():
    ip = input(Fore.LIGHTMAGENTA_EX + "Inserisci l'IP da cercare --> ").strip()
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        data = res.json()
        if data.get("status") == "success":
            print(Fore.CYAN + "\n+----------- IP INFO -----------+")
            print(Fore.GREEN + f"IP: {data.get('query', 'N/A')}")
            print(Fore.GREEN + f"Paese: {data.get('country', 'N/A')}")
            print(Fore.GREEN + f"Regione: {data.get('regionName', 'N/A')}")
            print(Fore.GREEN + f"Città: {data.get('city', 'N/A')}")
            print(Fore.GREEN + f"ISP: {data.get('isp', 'N/A')}")
            print(Fore.GREEN + f"Timezone: {data.get('timezone', 'N/A')}")
            print(Fore.GREEN + f"Lat/Lon: {data.get('lat', 'N/A')}/{data.get('lon', 'N/A')}")
            print(Fore.CYAN + "+-------------------------------+\n")
        else:
            print(Fore.RED + f"Errore nella ricerca IP: {data.get('message', 'Unknown')}")
    except Exception as e:
        print(Fore.RED + f"[ERRORE] {e}")
    input(Fore.WHITE + "Premi Invio per tornare al menu...")
# ----------------------------
# menu' palle
# ----------------------------
def main():
    clear_screen()
    print_banner()
    print("Select tool:")
    print("  1) USERHUNTER (username scanner)")
    print("  2) PORT SCANNER")
    print("  3) GITHUB MAIL PULLER")
    print("  4) PHONEHUNTER")
    print("  5) IP GEOLOCATION LOOKUP")
    print("  0) Exit")

    choice = input("\n[>] Enter choice: ").strip()

    if choice == "1":
        userhunter()
    elif choice == "2":
        portscanner()
    elif choice == "3":
        github_mail_puller()
    elif choice == "4":
        phone_lookup()
    elif choice == "5":
        ip_geolocation()
    else:
        print("Bye 👋")

if __name__ == "__main__":
    main()

