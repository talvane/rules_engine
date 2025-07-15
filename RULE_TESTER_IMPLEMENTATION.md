# Testador de Regras - Implementação Completa

## ✅ O que foi implementado

### 1. Componente RuleTester (Frontend)
- **Localização**: `src/frontend/motor-regras-frontend/src/RuleTester.js`
- **Funcionalidades**:
  - Processamento de regras via JavaScript (local)
  - Processamento de regras via API Python (backend)
  - Geração automática de dados de exemplo
  - Interface para entrada de dados JSON
  - Validação e exibição de resultados

### 2. Servidor API Python
- **Localização**: `src/api_server.py`
- **Endpoints**:
  - `GET /api/health` - Verificar status do servidor
  - `POST /api/process-rule` - Processar regra com dados
  - `POST /api/validate-rule` - Validar regra
- **Funcionalidades**:
  - Processamento completo usando `json_logic.py`
  - Suporte a CORS para requisições do frontend
  - Tratamento de erros robusto

### 3. Scripts de Utilitários
- **`start_server.sh`**: Script para iniciar o servidor com instalação automática de dependências
- **`test_backend.py`**: Script para testar o backend com exemplos
- **`README_RULE_TESTER.md`**: Documentação completa de uso

## 🚀 Como usar

### Opção 1: Apenas Frontend (Mais Simples)
1. O componente RuleTester já está integrado ao App.js
2. Construa uma regra no FlowBuilder
3. Clique em "Gerar JSON da Regra"
4. Use o RuleTester com a opção "Frontend (JavaScript)"
5. Digite seus dados JSON e clique em "Testar Regra"

### Opção 2: Com Backend Python (Mais Robusto)
1. Execute o servidor: `./start_server.sh`
2. No RuleTester, selecione "Backend (Python)"
3. O status do backend será mostrado (🟢 online / 🔴 offline)
4. Teste suas regras com processamento Python completo

## 🎯 Exemplos de Uso

### Exemplo 1: Regra de Idade
```json
// Regra
{
  ">": [
    {"var": "idade"},
    18
  ]
}

// Dados
{
  "idade": 25
}

// Resultado: true
```

### Exemplo 2: Aprovação de Empréstimo
```json
// Regra
{
  "and": [
    {">": [{"var": "score"}, 600]},
    {">": [{"var": "renda"}, 3000]},
    {"!": {"var": "possui_divida"}}
  ]
}

// Dados
{
  "score": 750,
  "renda": 5000,
  "possui_divida": false
}

// Resultado: true
```

### Exemplo 3: Categoria do Cliente
```json
// Regra
{
  "if": [
    {">": [{"var": "score"}, 800]},
    "Premium",
    {
      "if": [
        {">": [{"var": "score"}, 600]},
        "Regular",
        "Básico"
      ]
    }
  ]
}

// Dados
{
  "score": 720
}

// Resultado: "Regular"
```

## 🛠️ Comandos Úteis

### Iniciar apenas o servidor Python
```bash
# Opção 1: Usando o script
./start_server.sh

# Opção 2: Manualmente
poetry install
poetry run python src/api_server.py
```

### Testar o backend
```bash
# Instalar dependências se necessário
poetry install

# Executar testes
poetry run python test_backend.py
```

### Executar frontend React
```bash
cd src/frontend/motor-regras-frontend
npm start
```

## 📋 Dependências Adicionadas

### Python (`pyproject.toml`)
- `flask`: Servidor web
- `flask-cors`: Suporte a CORS
- `requests`: Cliente HTTP para testes

### Frontend (já existente)
- React Flow para construção visual
- Componentes React existentes

## 🔧 Arquitetura

```
FlowBuilder (React)
    ↓
Gera JSON Logic
    ↓
RuleTester Component
    ↓
┌─────────────────────┬─────────────────────┐
│   Frontend (JS)     │   Backend (Python)  │
│   - Rápido          │   - Robusto         │
│   - Simplificado    │   - Completo        │
└─────────────────────┴─────────────────────┘
    ↓
Resultado da Regra
```

## 🎉 Pronto para uso!

A implementação está completa e pronta para uso. O RuleTester já está integrado ao App.js e oferece duas opções de processamento:

1. **Frontend**: Processamento local, sem necessidade de configuração
2. **Backend**: Processamento Python completo, requer servidor rodando

Você pode testar suas regras imediatamente usando a opção Frontend, ou configurar o backend para ter acesso à implementação completa do JSON Logic.
