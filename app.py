#!/usr/bin/env python3
import requests
import os
from datetime import datetime

# Basis-URLs
env_name = 'idleoutpostclaimer'
BASE_STORE = 'https://store.xsolla.com'
USERID_SERVICE = 'https://sb-user-id-service.xsolla.com/api/v1/user-id'
LOG_FILE = 'claim_rewards.log'

# Konfiguriere hier deine Game-ID
USER_GAME_ID = os.environ.get('USER_GAME_ID')

# Payload für den User-ID-Service
USER_ID_PAYLOAD = {
    "settings": {"projectId":256000, "merchantId":329415},
    "loginId":"048e3522-75bd-43f5-95da-6ec145b9723a",
    "webhookUrl":"https://vd.appquantum.tech/webhook/user_validation",
    "user": {"id":USER_GAME_ID, "country":"DE"},
    "isUserIdFromWebhook": False
}

# Claim-Endpunkte
ENDPOINTS = {
    'shovels': '/api/v2/project/256000/free/item/com.rockbite.zombieoutpost.webshop.dailyshovels',
    'tickets': '/api/v2/project/256000/free/item/com.rockbite.zombieoutpost.webshop.dailyadtickets',
    'legendary': '/api/v2/project/256000/free/item/com.rockbite.zombieoutpost.webshop.weeklylegendarychest'
}


def log(message: str):
    """
    Protokolliert eine Nachricht mit Zeitstempel in eine Log-Datei und auf der Konsole.
    """
    timestamp = datetime.now().strftime("%d.%m.%y-%H:%M")
    line = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line)
    print(line, end='')


def setup_session():
    session = requests.Session()
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }
    # 1) Token vom User-ID-Service holen
    resp = session.post(USERID_SERVICE, json=USER_ID_PAYLOAD, headers=headers)
    resp.raise_for_status()
    token = resp.json().get('token')
    if not token:
        log('❗ Token konnte nicht vom User-ID-Service abgerufen werden.')
        raise RuntimeError('Kein Token erhalten vom User-ID-Service')
    log('🔑 Token erfolgreich erhalten.')
    # 2) Authorization-Header setzen
    session.headers.update({
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    })
    return session


def claim(session, key: str):
    item_name = key.capitalize()
    url = BASE_STORE + ENDPOINTS[key]
    log(f"Versuche, '{item_name}' zu claimen...")
    resp = session.post(url, json={})

    if resp.status_code in (200, 204):
        log(f"✅ '{item_name}' erfolgreich geclaimed.")
    elif resp.status_code == 422:
        log(f"🔒 '{item_name}' wurde heute bereits geclaimed (Kauflimit erreicht).")
    else:
        log(f"❗ Fehler beim Claimen von '{item_name}'. Status-Code: {resp.status_code}")
        log(f"   Server-Antwort: {resp.text}")


if __name__ == '__main__':
    if not USER_GAME_ID:
        print("Fehler: Die Umgebungsvariable USER_GAME_ID wurde nicht gesetzt.")
        print("Bitte setze sie und starte den Container neu.")
        exit(1)

    log("🚀 Starte Idle Outpost Claimer")
    # Session initialisieren
    sess = setup_session()

    log("\n--- Tägliche Belohnungen ---")
    for k in ('shovels', 'tickets'):
        claim(sess, k)

    log("\n--- Wöchentliche Belohnungen ---")
    claim(sess, 'legendary')

    log("\n🏁 Alle Aktionen abgeschlossen.")