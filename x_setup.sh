#!/bin/bash

# CONFIG
STREAMLIT_PORT=8501
OLLAMA_PORT=11434
MAX_RETRIES=10

echo "🧠 macRAG SecCopilot Setup Initializing..."

# Kill Docker containers
for cname in ollama_service macrag_streamlit_app; do
    if docker ps -a --format '{{.Names}}' | grep -Eq "^${cname}$"; then
        echo "🛑 Removing container: $cname"
        docker rm -f "$cname" >/dev/null 2>&1 || true
    fi
done

# Force free ports 11434 and 8501
for port in $STREAMLIT_PORT $OLLAMA_PORT; do
    pid=$(lsof -iTCP:"$port" -sTCP:LISTEN -t 2>/dev/null)
    if [ -n "$pid" ]; then
        echo "🔪 Killing process on port $port (PID: $pid)"
        kill -9 "$pid" || true
    fi
done

# Start Ollama if not running
if ! lsof -iTCP:$OLLAMA_PORT -sTCP:LISTEN &>/dev/null; then
    if command -v ollama &>/dev/null; then
        echo "🚀 Starting Ollama in background..."
        ollama serve > /dev/null 2>&1 &
        sleep 3
    else
        echo "❌ Ollama CLI not found. Please install Ollama: https://ollama.com/download"
        exit 1
    fi
fi

# Docker cleanup
echo "🧹 Cleaning up Docker environment..."
docker-compose down -v --remove-orphans
docker system prune -af --volumes

# Build and start
echo "🔧 Building Docker containers..."
docker-compose build --no-cache
docker-compose up -d

# Health check for Streamlit
echo "⏳ Waiting for Streamlit to start..."
for ((i=1;i<=$MAX_RETRIES;i++)); do
    if curl -s "http://localhost:$STREAMLIT_PORT" | grep -q "html"; then
        echo "✅ Streamlit is live at: http://localhost:$STREAMLIT_PORT"
        exit 0
    fi
    echo "🔁 Waiting ($i/$MAX_RETRIES)..."
    sleep 3
done

echo "❌ Streamlit failed to respond. Use: docker-compose logs"
exit 1