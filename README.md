# Motor de Decisões

## 🚀 Funcionalidades

Este projeto implementa um motor de decisões baseado em JsonLogic com funcionalidades estendidas, incluindo **suporte completo para funções assíncronas**.

### ✨ Novidade: JsonLogic Assíncrono

**Nova funcionalidade implementada!** O projeto agora suporta execução assíncrona de regras com funções que fazem I/O, consultas de banco de dados, chamadas de API, etc.

📖 **[Documentação Completa do Suporte Assíncrono](README_ASYNC.md)**

## 📋 Características Principais

### JsonLogic Clássico (Síncrono)
- ✅ Implementação completa do JsonLogic padrão
- ✅ Operações matemáticas, lógicas e de comparação
- ✅ Manipulação de arrays e strings
- ✅ Suporte a funções personalizadas síncronas
- ✅ Acesso a dados aninhados

### 🆕 JsonLogic Assíncrono
- ✅ **Execução assíncrona de regras** (`jsonLogicAsync`)
- ✅ **Suporte a funções síncronas e assíncronas** na mesma regra
- ✅ **Detecção automática** de execução sync/async (`jsonLogicAuto`)
- ✅ **Operações paralelas otimizadas** para melhor performance
- ✅ **Backward compatibility** total com JsonLogic original
- ✅ **Chamadas de API, I/O, banco de dados** sem bloquear execução
- ✅ **Melhor performance** para operações I/O-bound

## 🛠️ Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd poc-jsonlogic

# Instale as dependências
poetry install

# Ou usando pip
pip install -e .
```

## 🚀 Uso Rápido

### JsonLogic Clássico

```python
from src.lib.json_logic import jsonLogic

# Dados
dados = {
    "usuario": {"nome": "João", "idade": 25},
    "produto": {"preco": 100}
}

# Regra
regra = {
    "and": [
        {">": [{"var": "usuario.idade"}, 18]},
        {"<": [{"var": "produto.preco"}, 200]}
    ]
}

# Execução
resultado = jsonLogic(regra, dados)
print(resultado)  # True
```

### 🆕 JsonLogic Assíncrono

```python
import asyncio
from src.lib.json_logic import jsonLogicAsync

# Função assíncrona personalizada
async def consultar_score_credito(cpf):
    # Simula consulta a API externa
    await asyncio.sleep(0.2)
    return 750

# Função síncrona
def calcular_limite(score):
    return score * 10

# Registro de funções
funcoes = {
    "get_score": consultar_score_credito,
    "calc_limite": calcular_limite,
}

# Dados
dados = {"cpf": "12345678901", "valor_solicitado": 5000}

# Regra que combina sync e async
regra = {
    ">=": [
        {"apply": [
            "calc_limite",
            {"apply": ["get_score", {"var": "cpf"}]}
        ]},
        {"var": "valor_solicitado"}
    ]
}

# Execução assíncrona
async def main():
    resultado = await jsonLogicAsync(regra, dados, funcoes)
    print(f"Crédito aprovado: {resultado}")

asyncio.run(main())
```

### 🤖 Detecção Automática

```python
from src.lib.json_logic import jsonLogicAuto

# Detecta automaticamente se deve usar sync ou async
resultado = jsonLogicAuto(regra, dados, funcoes)

if asyncio.iscoroutine(resultado):
    # Tem funções async - execute com await
    final_result = await resultado
else:
    # Apenas funções sync - resultado direto
    final_result = resultado
```

## 📚 Exemplos Avançados

### Caso de Uso: Sistema de Aprovação de Crédito

```python
import asyncio
from src.lib.json_logic import jsonLogic_async

# Funções de negócio assíncronas
async def consultar_serasa(cpf):
    await asyncio.sleep(0.3)  # Simula latência
    return {"score": 720, "restricoes": False}

async def verificar_renda(user_id):
    await asyncio.sleep(0.2)
    return {"valor": 5000, "comprovada": True}

# Função síncrona
def calcular_limite_credito(renda, score):
    if score > 700:
        return renda * 3
    elif score > 600:
        return renda * 2
    return renda * 0.5

# Registro de funções
funcoes = {
    "get_serasa": consultar_serasa,
    "get_renda": verificar_renda,
    "calc_limite": calcular_limite_credito,
}

# Dados da solicitação
dados = {
    "cpf": "12345678901",
    "user_id": 123,
    "valor_solicitado": 10000
}

# Regra complexa de aprovação
regra_aprovacao = {
    "and": [
        # Score > 600 e sem restrições
        {">": [
            {"apply_async": ["get_serasa", {"var": "cpf"}]},
            {"score": 600}
        ]},
        {"==": [
            {"apply_async": ["get_serasa", {"var": "cpf"}]},
            {"restricoes": False}
        ]},
        # Renda comprovada
        {"==": [
            {"apply_async": ["get_renda", {"var": "user_id"}]},
            {"comprovada": True}
        ]},
        # Valor <= limite calculado
        {"<=": [
            {"var": "valor_solicitado"},
            {"apply": [
                "calc_limite",
                {"apply_async": ["get_renda", {"var": "user_id"}]},
                {"apply_async": ["get_serasa", {"var": "cpf"}]}
            ]}
        ]}
    ]
}

async def processar_credito():
    inicio = time.time()
    aprovado = await jsonLogic_async(regra_aprovacao, dados, funcoes)
    fim = time.time()
    
    print(f"Crédito {'APROVADO' if aprovado else 'NEGADO'}")
    print(f"Processamento: {fim - inicio:.2f}s")

asyncio.run(processar_credito())
```

## 🧪 Testando

### Testes Unitários

```bash
# Testes do JsonLogic original
python -m pytest src/tests/test_json_logic.py -v

# Testes de suporte assíncrono
python -m pytest src/tests/test_async_support.py -v

# Todos os testes
python -m pytest src/tests/ -v
```

### Testes de Performance e Carga

```bash
# Teste de carga rápido - Comparação Sync vs Async
python src/tests/test_quick_load_performance.py

# Teste de carga completo com múltiplos cenários
python src/tests/test_load_performance_comparison.py

# Benchmark detalhado de performance
python src/tests/test_benchmark_complete.py

# Teste de melhores práticas
python src/tests/test_best_practices.py

# Teste de carga original
python src/tests/test_load_test.py
```

### Exemplo Completo

```bash
# Exemplo assíncrono
python exemplo_async.py
```

## 📊 Performance

### Comparação de Performance: Sync vs Async

#### 🎯 Resultados dos Testes de Carga

**Cenário 1: Operações Matemáticas Simples (200 iterações)**
- **🔄 Sync**: 14.532,7 ops/s (⌀ 0.07ms) - ✅ **Mais eficiente**
- **⚡ Async**: 554,2 ops/s (⌀ 1.80ms) - 96.2% mais lento
- **🚀 Concurrent**: 2.030,1 ops/s (⌀ 2.45ms) - 86.0% mais lento

**Cenário 2: Operações Computacionais Pesadas (100 iterações)**
- **🔄 Sync**: 52.217,1 ops/s (⌀ 0.02ms) - ✅ **Mais eficiente**
- **⚡ Async**: 169,3 ops/s (⌀ 5.90ms) - 99.7% mais lento
- **🚀 Concurrent**: 842,2 ops/s (⌀ 5.93ms) - 98.4% mais lento

#### 📈 Análise dos Resultados

| Tipo de Operação | Melhor Escolha | Motivo |
|-------------------|----------------|---------|
| **CPU-bound** (matemática, lógica) | **Sync** | Sem overhead de async |
| **I/O-bound** (API, DB, rede) | **Async** | Paralelização de I/O |
| **Misto** | **Auto** | Detecção automática |

### Comparação de Performance (Operações I/O Simuladas)

| Cenário | JsonLogic Sync | JsonLogic Async | Melhoria |
|---------|----------------|-----------------|----------|
| 3 consultas sequenciais | ~0.9s | ~0.4s | **55% mais rápido** |
| 5 validações paralelas | ~1.5s | ~0.6s | **60% mais rápido** |
| Regras complexas | ~2.1s | ~0.8s | **62% mais rápido** |

*Dados baseados em simulações com latência de rede de 200ms*

### 🎯 Recomendações de Uso

```python
# ✅ Use SYNC para operações CPU-bound
regra_matematica = {"+": [{"var": "a"}, {"var": "b"}]}
resultado = jsonLogic(regra_matematica, dados)

# ✅ Use ASYNC para operações I/O-bound
regra_com_api = {"apply": ["consultar_api", {"var": "id"}]}
resultado = await jsonLogicAsync(regra_com_api, dados, funcoes_async)

# ✅ Use AUTO para detecção automática
resultado = jsonLogicAuto(regra, dados, funcoes_mistas)
if asyncio.iscoroutine(resultado):
    resultado = await resultado
```

## 📝 Insights dos Testes de Performance

### 🔍 Descobertas Importantes

1. **Overhead Async é Significativo para CPU-bound**
   - Async pode ser **96-99% mais lento** para operações puras de CPU
   - Event loop e context switching adicionam latência considerável
   - Para matemática/lógica pura, prefira sempre **sync**

2. **Concorrência Melhora Async mas Não Vence Sync**
   - Concurrent async é **60-80% mais lento** que sync puro
   - Benefício real apenas com I/O blocking genuíno
   - Use concurrent para operações independentes com I/O

3. **Detecção Automática (`jsonLogicAuto`) é Inteligente**
   - Detecta presença de funções async automaticamente
   - Escolhe a melhor estratégia sem intervenção manual
   - **Recomendado para aplicações mistas**

4. **Throughput Varia Drasticamente por Cenário**
   - **Sync**: 14.000-52.000 ops/s (operações simples)
   - **Async**: 169-554 ops/s (com sleep simulado)
   - **Concurrent**: 842-2.030 ops/s (melhor que async sequencial)

### ⚖️ Decisão Arquitetural

| Se sua aplicação tem... | Use... | Motivo |
|-------------------------|--------|---------|
| Apenas regras matemáticas | `jsonLogic()` | Máxima performance |
| APIs/DB externos | `jsonLogicAsync()` | Paralelização de I/O |
| Mistura de ambos | `jsonLogicAuto()` | Detecção automática |
| Milhares de regras/seg | `jsonLogic()` | Throughput superior |

## 🔄 Migração

### De JsonLogic para JsonLogic Async

**1. Substituir chamada de função:**
```python
# Antes
resultado = jsonLogic(regra, dados, funcoes)

# Depois  
resultado = await jsonLogic_async(regra, dados, funcoes)
```

**2. Adicionar funções assíncronas:**
```python
# Mantenha funções existentes
funcoes_sync = {"calc": lambda x, y: x + y}

# Adicione novas funções async
async def fetch_data(id):
    return await api_call(id)

# Combine ambas
funcoes_completas = {
    **funcoes_sync,
    "fetch": fetch_data,
}

# Use operações específicas
regra = {
    "apply": ["calc", 10, 20],        # Síncrona
    "apply_async": ["fetch", "123"]   # Assíncrona
}
```

## 🏗️ Arquitetura

```
src/
├── lib/
│   └── json_logic.py      # Core: JsonLogic + JsonLogic Async
├── tests/
│   ├── test_async_support.py        # Testes para o suporte a funções assíncronas
│   ├── test_best_practices.py       # Demonstração de melhores práticas
│   ├── test_benchmark_complete.py   # Benchmark completo de performance
│   ├── test_json_logic.py          # Testes originais do JsonLogic
│   ├── test_load_performance_comparison.py # Teste de carga: Sync vs Async
│   ├── test_load_test.py           # Testes de carga originais
│   ├── test_performance_quick.py    # Teste de performance rápido
│   ├── test_performance_sync_async.py # Comparação detalhada sync/async
│   └── test_quick_load_performance.py # Teste de carga rápido
├── motor_regras.py        # Motor de regras
├── regras.py             # Definições de regras
└── acoes.py              # Ações do sistema
```

## 🔍 Operações Suportadas

### Operações Base (Compatíveis com JsonLogic original)
- **Lógicas:** `and`, `or`, `!`, `?:`
- **Comparação:** `==`, `!=`, `>`, `>=`, `<`, `<=`
- **Matemáticas:** `+`, `-`, `*`, `/`, `%`, `min`, `max`
- **Dados:** `var`, `in`, `count`
- **Arrays:** `some`, `every`, `map`, `filter`, `merge`
- **Strings:** `cat`
- **Sistema:** `log`

### 🆕 Novas Operações Assíncronas
- **`apply_async`:** Executa função assíncrona
- **`apply`:** Executa função síncrona (com validação de tipo)
- **Operações lógicas assíncronas:** `and`, `or` com suporte a async
- **Operações de array assíncronas:** `map`, `filter`, `some`, `every`

## 📈 Casos de Uso Ideais

### ✅ Quando usar JsonLogic Async
- 🌐 Regras que fazem consultas HTTP/API
- 🗄️ Validações que acessam banco de dados
- 📊 Cálculos que dependem de múltiplas fontes externas
- ⚡ Cenários que se beneficiam de paralelismo
- 🔄 Sistemas que processam muitas regras simultaneamente

### ✅ Quando usar JsonLogic Clássico
- 🧮 Regras puramente matemáticas/lógicas
- 💾 Operações apenas com dados em memória
- 🏃 Cenários onde latência mínima é crítica
- 🔒 Ambientes que não suportam async/await
- ⚡ **High-throughput CPU-bound operations** (conforme testes de carga)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🏷️ Tags

`jsonlogic` `async` `motor-decisoes` `regras-negocio` `python` `asyncio` `performance` `poc`

## 🔬 Testes de Performance Incluídos

### 1. Teste de Carga Rápido (`test_quick_load_performance.py`)
- **Propósito**: Comparação rápida entre sync, async e concurrent
- **Cenários**: Operações matemáticas simples e computação pesada
- **Métricas**: Throughput, latência média, taxa de sucesso

### 2. Teste de Carga Completo (`test_load_performance_comparison.py`)
- **Propósito**: Análise detalhada sob diferentes cargas de trabalho
- **Cenários**: Light Load, Medium Load, Heavy Load
- **Métricas**: Performance completa com estatísticas detalhadas

### 3. Benchmark Completo (`test_benchmark_complete.py`)
- **Propósito**: Benchmark em diferentes tipos de operação
- **Cenários**: CPU-bound, I/O simulation, lógica complexa
- **Métricas**: Análise comparativa profunda

### 4. Teste de Melhores Práticas (`test_best_practices.py`)
- **Propósito**: Demonstra padrões corretos vs anti-patterns
- **Foco**: Evitar objetos literais, usar operações lógicas puras
- **Objetivo**: Educacional e validação de qualidade

### 📊 Como Executar os Testes

```bash
# Teste rápido (2-3 segundos)
python src/tests/test_quick_load_performance.py

# Teste completo (1-2 minutos)
python src/tests/test_load_performance_comparison.py

# Benchmark profundo (3-5 minutos)
python src/tests/test_benchmark_complete.py

# Validação de práticas
python src/tests/test_best_practices.py
```
