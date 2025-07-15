#!/bin/bash

# Script para iniciar o servidor de processamento de regras

echo "🚀 Iniciando servidor de processamento de regras..."
echo "==============================================="

# Verifica se o poetry está instalado
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry não encontrado. Instale o Poetry primeiro:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Instala as dependências
echo "📦 Instalando dependências..."
poetry install

# Verifica se a instalação foi bem-sucedida
if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências."
    exit 1
fi

echo "✅ Dependências instaladas com sucesso!"
echo ""

# Inicia o servidor
echo "🖥️  Iniciando servidor Flask..."
echo "   Servidor será executado em: http://localhost:5000"
echo "   Pressione Ctrl+C para parar o servidor"
echo ""

# Executa o servidor usando poetry
poetry run python src/api_server.py
