#!/bin/bash

# CONFIG
STREAMLIT_PORT=8501
OLLAMA_PORT=11434
MAX_RETRIES=10
OLLAMA_MODELS=("llama3" "mistral")

echo "🧠 macRAG SecCopilot Setup Initializing..."

# FAST MODE
if [[ "$1" == "--fast" ]]; then
  echo "🚀 Fast mode enabled — skipping teardown, launching containers..."
  docker-compose up -d
  echo "⏳ Waiting for Streamlit..."
  sleep 3
  xdg-open http://localhost:$STREAMLIT_PORT || open http://localhost:$STREAMLIT_PORT
  exit 0
fi

# TEARDOWN EXISTING CONTAINERS
for cname in ollama_service macrag_streamlit_app; do
  if docker ps -a --format '{{.Names}}' | grep -Eq "^${cname}$"; then
    echo "🛑 Removing container: $cname"
    docker rm -f "$cname" >/dev/null 2>&1 || true
  fi
done

# FREE PORTS IF NEEDED
for port in $STREAMLIT_PORT $OLLAMA_PORT; do
  pid=$(lsof -iTCP:"$port" -sTCP:LISTEN -t 2>/dev/null)
  if [ -n "$pid" ]; then
    echo "🔪 Killing process on port $port (PID: $pid)"
    kill -9 "$pid" || true
  fi
done

# START OLLAMA
if ! lsof -iTCP:$OLLAMA_PORT -sTCP:LISTEN &>/dev/null; then
  if command -v ollama &>/dev/null; then
    echo "🔁 Starting Ollama..."
    nohup ollama serve > ollama.log 2>&1 &
    sleep 3
  else
    echo "❌ Ollama CLI not found. Install from https://ollama.com/download"
    exit 1
  fi
fi

# VERIFY OLLAMA HEALTH
if curl -s http://localhost:$OLLAMA_PORT | grep -q 'Ollama'; then
  echo "✅ Ollama is running on port $OLLAMA_PORT"
else
  echo "❌ Ollama health check failed"
  exit 1
fi

# PRELOAD LLM MODELS
for model in "${OLLAMA_MODELS[@]}"; do
  echo "📦 Preloading model: $model"
  nohup ollama run "$model" >/dev/null 2>&1 &
done

# CLEANUP DOCKER AND REBUILD
echo "🧹 Docker cleanup..."
docker-compose down -v --remove-orphans

echo "🔧 Building containers..."
docker-compose build

# LAUNCH CONTAINERS
echo "🚀 Starting containers..."
docker-compose up -d

# HEALTH CHECK STREAMLIT
echo "⏳ Waiting for Streamlit..."
for ((i=1;i<=$MAX_RETRIES;i++)); do
  if curl -s "http://localhost:$STREAMLIT_PORT" | grep -q "<html"; then
    echo "✅ Streamlit is live at: http://localhost:$STREAMLIT_PORT"
    xdg-open http://localhost:$STREAMLIT_PORT || open http://localhost:$STREAMLIT_PORT
    exit 0
  fi
  echo "🔁 Retry $i/$MAX_RETRIES..."
  sleep 3
done

echo "❌ Streamlit failed to respond. Use 'docker-compose logs' to debug."
exit 1