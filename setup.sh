#!/bin/bash

# CONFIG
STREAMLIT_PORT=8501
OLLAMA_PORT=11434
MAX_RETRIES=10
OLLAMA_MODELS=("llama3" "mistral")  # preload these models

echo "🧠 macRAG SecCopilot Setup Initializing..."

# FAST MODE: skip cleanup and relaunch
if [[ "$1" == "--fast" ]]; then
  echo "🚀 Fast mode enabled — skipping teardown, launching containers..."
  docker-compose up -d
  echo "⏳ Waiting for Streamlit..."
  sleep 3
  xdg-open http://localhost:$STREAMLIT_PORT || open http://localhost:$STREAMLIT_PORT
  exit 0
fi

# Kill Docker containers if running
for cname in ollama_service macrag_streamlit_app; do
    if docker ps -a --format '{{.Names}}' | grep -Eq "^${cname}$"; then
        echo "🛑 Removing container: $cname"
        docker rm -f "$cname" >/dev/null 2>&1 || true
    fi
done

# Free ports 11434 and 8501 if in use
for port in $STREAMLIT_PORT $OLLAMA_PORT; do
    pid=$(lsof -iTCP:"$port" -sTCP:LISTEN -t 2>/dev/null)
    if [ -n "$pid" ]; then
        echo "🔪 Killing process on port $port (PID: $pid)"
        kill -9 "$pid" || true
    fi
done

# Start Ollama if not already running
if ! lsof -iTCP:$OLLAMA_PORT -sTCP:LISTEN &>/dev/null; then
    if command -v ollama &>/dev/null; then
        echo "🔁 Starting Ollama..."
        ollama serve > /dev/null 2>&1 &
        sleep 3
    else
        echo "❌ Ollama CLI not found. Install from https://ollama.com/download"
        exit 1
    fi
fi

# Preload Ollama models to avoid first-use delay
echo "📦 Preloading LLMs: ${OLLAMA_MODELS[*]}"
for model in "${OLLAMA_MODELS[@]}"; do
    ollama run "$model" >/dev/null 2>&1 &
done

# Docker cleanup (retain cache for fast rebuild)
echo "🧹 Docker cleanup..."
docker-compose down -v --remove-orphans

# Build containers with caching
echo "🔧 Building Docker containers (cached)..."
docker-compose build

# Start containers in background
echo "🚀 Launching app in background..."
docker-compose up -d

# Streamlit health check
echo "⏳ Waiting for Streamlit to respond..."
for ((i=1;i<=$MAX_RETRIES;i++)); do
    if curl -s "http://localhost:$STREAMLIT_PORT" | grep -q "<html"; then
        echo "✅ Streamlit is live: http://localhost:$STREAMLIT_PORT"
        xdg-open http://localhost:$STREAMLIT_PORT || open http://localhost:$STREAMLIT_PORT
        exit 0
    fi
    echo "🔁 Retry $i/$MAX_RETRIES..."
    sleep 3
done

echo "❌ Streamlit failed to respond. Use 'docker-compose logs' to debug."
exit 1