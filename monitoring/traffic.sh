#!/usr/bin/env bash
set -euo pipefail

BANQUE_URL="${BANQUE_URL:-http://localhost:5003}"
PANIER_URL="${PANIER_URL:-http://localhost:5002}"

USERNAME="thomas"
TOKEN="thomas_token_123"

echo "[traffic] Health checks"
curl -fsS "$BANQUE_URL/health" >/dev/null
curl -fsS "$PANIER_URL/health" >/dev/null

echo "[traffic] Trafic normal banque"
for i in $(seq 1 5); do
  curl -s -X POST "$BANQUE_URL/banque" \
    -d "nom=$USERNAME" \
    -d "token=$TOKEN" \
    >/dev/null
done

echo "[traffic] Trafic normal panier"
curl -s -X POST "$PANIER_URL/panier" \
  -d "token=$TOKEN" \
  -d "film=Inception" \
  >/dev/null

curl -s -X POST "$PANIER_URL/panier" \
  -d "token=$TOKEN" \
  -d "film=Interstellar" \
  >/dev/null

# ===== Mode suspect (tests sécurité) =====
if [ "${SUSPECT_MODE:-0}" = "1" ]; then
  echo "[traffic] ⚠️ Trafic suspect"

  # Banque : nom manquant
  curl -s -X POST "$BANQUE_URL/banque" \
    -d "token=$TOKEN" \
    >/dev/null || true

  # Panier : token mal formé
  curl -s -X POST "$PANIER_URL/panier" \
    -d "token=invalidtoken" \
    -d "film=<script>alert(1)</script>" \
    >/dev/null || true
fi

echo "[traffic] ✅ terminé"