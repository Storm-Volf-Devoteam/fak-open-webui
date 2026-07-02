#!/usr/bin/env python3
"""FAK seed script — omdøber 3 Mistral-modeller og disabler resten.

Køres én gang efter første admin-login:
    docker exec open-webui python3 /app/scripts/fak-seed.py

Idempotent: eksisterende ændringer bevares medmindre --force angives.
"""
import argparse
import json
import os
import sqlite3
import sys
import time
import urllib.request
from pathlib import Path

DB_PATH = Path("/app/backend/data/webui.db")

ENABLED_MODELS = {
    "mistral-small-latest": {
        "name": "Hurtig",
        "meta": {"description": "Til simple opgaver"},
    },
    "mistral-medium-latest": {
        "name": "Balanceret",
        "meta": {"description": "Anbefalet til de fleste opgaver"},
    },
    "mistral-large-latest": {
        "name": "Kompleks",
        "meta": {"description": "Grundigt svar, tager længere tid"},
    },
}


def fetch_provider_models():
    """Henter alle model-ID'er fra konfigurerede LLM-providers."""
    api_urls = os.environ.get("OPENAI_API_BASE_URLS", "")
    api_keys = os.environ.get("OPENAI_API_KEYS", "")

    if not api_urls or not api_keys:
        print("  Advarsel: OPENAI_API_BASE_URLS/KEYS ikke sat — kan ikke hente modelliste.")
        return []

    model_ids = []
    for url, key in zip(api_urls.split(";"), api_keys.split(";")):
        url = url.strip()
        key = key.strip()
        if not url or not key:
            continue
        try:
            req = urllib.request.Request(f"{url}/models")
            req.add_header("Authorization", f"Bearer {key}")
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read())
            for model in data.get("data", []):
                model_ids.append(model["id"])
            print(f"  Hentet {len(data.get('data', []))} modeller fra {url}")
        except Exception as e:
            print(f"  Advarsel: Kunne ikke hente modeller fra {url}: {e}")

    return model_ids


def seed(force=False):
    if not DB_PATH.exists():
        print(f"Database ikke fundet: {DB_PATH}")
        print("Start containeren først, og kør derefter dette script.")
        sys.exit(1)

    db = sqlite3.connect(str(DB_PATH))

    admin = db.execute(
        "SELECT id FROM user WHERE role='admin' ORDER BY created_at LIMIT 1"
    ).fetchone()
    if not admin:
        print("Ingen admin-bruger fundet. Opret en admin via browseren først.")
        db.close()
        sys.exit(1)
    admin_id = admin[0]

    now = int(time.time())
    renamed = 0
    disabled = 0
    skipped = 0

    print("\n--- Omdøber FAK-modeller ---")
    for model_id, config in ENABLED_MODELS.items():
        existing = db.execute(
            "SELECT id, name FROM model WHERE id=?", [model_id]
        ).fetchone()

        if existing:
            if existing[1] == config["name"] and not force:
                print(f"  {model_id}: allerede '{config['name']}'")
                skipped += 1
                continue
            db.execute(
                "UPDATE model SET name=?, meta=?, is_active=1, updated_at=? WHERE id=?",
                [config["name"], json.dumps(config["meta"]), now, model_id],
            )
        else:
            db.execute(
                "INSERT INTO model (id, user_id, base_model_id, name, params, meta, is_active, updated_at, created_at) VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)",
                [model_id, admin_id, None, config["name"], "{}", json.dumps(config["meta"]), now, now],
            )
        print(f"  {model_id} → '{config['name']}'")
        renamed += 1

    print("\n--- Disabler øvrige modeller ---")
    provider_models = fetch_provider_models()

    for model_id in provider_models:
        if model_id in ENABLED_MODELS:
            continue

        existing = db.execute(
            "SELECT id, is_active FROM model WHERE id=?", [model_id]
        ).fetchone()

        if existing:
            if existing[1] == 0 and not force:
                continue
            db.execute(
                "UPDATE model SET is_active=0, updated_at=? WHERE id=?", [now, model_id]
            )
        else:
            db.execute(
                "INSERT INTO model (id, user_id, base_model_id, name, params, meta, is_active, updated_at, created_at) VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?)",
                [model_id, admin_id, None, model_id, "{}", "{}", now, now],
            )
        print(f"  {model_id}: disabled")
        disabled += 1

    db.commit()
    db.close()

    print(f"\nFAK seed: {renamed} omdøbt, {disabled} disabled, {skipped} uændrede.")
    if renamed > 0 or disabled > 0:
        print("Genindlæs siden i browseren for at se ændringerne.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FAK Open WebUI database seed")
    parser.add_argument("--force", action="store_true", help="Overskriv eksisterende ændringer")
    args = parser.parse_args()
    seed(force=args.force)
