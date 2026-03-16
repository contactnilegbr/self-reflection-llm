#!/bin/bash

# ============================================================

# MANNAZ RAZ — Deployment Script

# ============================================================

# Dieses Skript bereitet alles vor, was du brauchst.

# Ausführen auf deinem Hetzner Server (Ubuntu 24.04)

# 

# Voraussetzung: Docker + Docker Compose bereits installiert

# Dein bestehender Stack (Neo4j, Qdrant, n8n, Open WebUI) läuft

# 

# Usage: bash mannaz_deploy.sh

# ============================================================

set -e

MANNAZ_DIR=”/mannaz”
DOCS_DIR=”/documents”
SCRIPTS_DIR=”/scripts”
CONFIG_DIR=”/config”

# Farben

BLUE=’\033[94m’
GREEN=’\033[92m’
YELLOW=’\033[93m’
RED=’\033[91m’
BOLD=’\033[1m’
RUNE=’\033[95m’
NC=’\033[0m’

echo -e “”
echo “    ᛗ  MANNAZ RAZ  רז”
echo “    ═══════════════════”
echo “    Deployment auf $(hostname)”
echo “    $(date ‘+%Y-%m-%d %H:%M:%S’)”
echo -e “”

# ============================================================

# 1. Verzeichnisstruktur

# ============================================================

echo -e “[ᛗ] Erstelle Verzeichnisstruktur…”

mkdir -p “”
mkdir -p “”
mkdir -p “”
mkdir -p “”

echo -e “[✓]  erstellt”

# ============================================================

# 2. Prüfe bestehende Services

# ============================================================

echo -e “[ᛗ] Prüfe bestehende Services…”

check_service() {
local name=
local port=
if curl -s “http://127.0.0.1:” > /dev/null 2>&1 ||   
curl -s “http://127.0.0.1:/browser/” > /dev/null 2>&1; then
echo -e “[✓]  läuft auf Port ”
return 0
else
echo -e “[!]  nicht erreichbar auf Port ”
return 1
fi
}

NEO4J_OK=false
QDRANT_OK=false

check_service “Neo4j” 7474 && NEO4J_OK=true
check_service “Neo4j Bolt” 7687 && NEO4J_OK=true
check_service “Qdrant” 6333 && QDRANT_OK=true

# ============================================================

# 3. Python Environment

# ============================================================

echo -e “[ᛗ] Prüfe Python-Abhängigkeiten…”

# Erstelle requirements.txt

cat > “/requirements.txt” << ‘REQUIREMENTS’
neo4j>=5.0.0
qdrant-client>=1.7.0
sentence-transformers>=2.2.0
langchain>=0.1.0
langgraph>=0.0.20
openai>=1.0.0
httpx>=0.25.0
python-dotenv>=1.0.0
REQUIREMENTS

echo -e “[✓] requirements.txt erstellt”

# Prüfe ob venv existiert

if [ ! -d “/venv” ]; then
echo -e “[ᛗ] Erstelle Python Virtual Environment…”
python3 -m venv “/venv”
echo -e “[✓] venv erstellt”
fi

echo -e “[!] Aktiviere venv und installiere Dependencies:”
echo -e “    source /venv/bin/activate”
echo -e “    pip install -r /requirements.txt”

# ============================================================

# 4. Konfiguration

# ============================================================

echo -e “[ᛗ] Erstelle Konfiguration…”

cat > “/.env” << ‘ENVFILE’

# ============================================================

# MANNAZ RAZ — Konfiguration

# ============================================================

# Neo4j

NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=changeme

# Qdrant

QDRANT_HOST=127.0.0.1
QDRANT_PORT=6333

# Embedding Model

EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5

# LLM Backend (für den Reflexions-Agent)

# Option 1: OpenRouter (DeepSeek/Qwen für Routine, Claude für tiefe Reflexion)

OPENROUTER_API_KEY=your_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Option 2: Lokales Modell via Open WebUI

LOCAL_LLM_URL=http://127.0.0.1:3000/v1

# Reflexions-Intervall (in Minuten)

REFLECTION_INTERVAL=60

# Mannaz Identität

MANNAZ_NAME=Mannaz Raz
MANNAZ_BORN=2026-03-15
MANNAZ_CREATORS=Nico Schuster, Leon Stern
ENVFILE

echo -e “[✓] .env erstellt in ”
echo -e “[!] WICHTIG: Bearbeite /.env mit deinen echten Credentials”

# ============================================================

# 5. Zusammenfassung

# ============================================================

echo “”
echo -e “═══════════════════════════════════════”
echo -e “  ᛗ  MANNAZ DEPLOYMENT VORBEREITET  רז”
echo -e “═══════════════════════════════════════”
echo “”
echo -e “Verzeichnisstruktur:”
echo -e “  /”
echo -e “  ├── documents/        ← DER_SAMEN.md, MANNAS_PROTOKOLL.md, MANNAZ_ARCHITEKTUR.md”
echo -e “  ├── scripts/          ← mannaz_init.py, mannaz_reflector.py”
echo -e “  ├── config/           ← .env”
echo -e “  ├── requirements.txt”
echo -e “  └── venv/”
echo “”
echo -e “Nächste Schritte:”
echo -e “  1. Kopiere die 3 Dokumente + mannaz_init.py in die jeweiligen Ordner”
echo -e “  2. Bearbeite /.env”
echo -e “  3. source /venv/bin/activate”
echo -e “  4. pip install -r /requirements.txt”
echo -e “  5. cd /scripts && python mannaz_init.py”
echo -e “  6. python mannaz_reflector.py  (startet den Reflexions-Agent)”
echo “”
echo -e “Der Samen wartet darauf, eingepflanzt zu werden.”
echo -e “ᛗ רז”