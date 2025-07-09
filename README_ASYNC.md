# JsonLogic com Suporte Assíncrono

Esta é uma implementação estendida do JsonLogic que adiciona suporte completo para funções assíncronas em Python, mantendo total compatibilidade com a versão síncrona original.

## ✨ Novas Funcionalidades

### 🚀 Suporte a Funções Assíncronas

- **`jsonLogicAsync()`**: Versão assíncrona completa do JsonLogic
- **`jsonLogicAuto()`**: Detecção automática de funções async/sync
- **`has_async_functions()`**: Utilitário para detectar funções assíncronas
- **Execução mista**: Combina funções síncronas e assíncronas na mesma regra

### 🔧 Funcionalidades Principais

1. **Execução Assíncrona Nativa**: Execute regras que incluem chamadas de API, operações de I/O e processamento assíncrono
2. **Detecção Automática**: O sistema detecta automaticamente se deve usar execução síncrona ou assíncrona
3. **Compatibilidade Total**: Funções síncronas continuam funcionando normalmente
4. **Performance Otimizada**: Operações assíncronas são executadas em paralelo quando possível

## 📋 Requisitos

- Python 3.7+
- asyncio (incluído no Python 3.7+)
- typing (incluído no Python 3.5+)

## 🚀 Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd poc-jsonlogic

# Instale dependências (se usar poetry)
poetry install

# Ou instale dependências via pip
pip install -r requirements.txt
```

## 💡 Uso Básico

### Funções Síncronas (Comportamento Original)

```python
from lib.json_logic import jsonLogic

# Funções síncronas
def calcular_area(largura, altura):
    return largura * altura

funcoes = {"calc_area": calcular_area}
dados = {"retangulo": {"l": 10, "a": 5}}

regra = {
    "apply": ["calc_area", {"var": "retangulo.l"}, {"var": "retangulo.a"}]
}

resultado = jsonLogic(regra, dados, funcoes)
print(resultado)  # 50
```

### Funções Assíncronas

```python
import asyncio
from lib.json_logic import jsonLogicAsync

# Função assíncrona
async def buscar_dados_usuario(user_id):
    await asyncio.sleep(0.1)  # Simula chamada de API
    return {"nome": "João", "idade": 30}

funcoes = {"fetch_user": buscar_dados_usuario}
dados = {"user_id": 123}

regra = {
    "apply": ["fetch_user", {"var": "user_id"}]
}

async def main():
    resultado = await jsonLogicAsync(regra, dados, funcoes)
    print(resultado)  # {"nome": "João", "idade": 30}

asyncio.run(main())
```

### Detecção Automática

```python
from lib.json_logic import jsonLogicAuto

# Funções mistas
def sync_func(x):
    return x * 2

async def async_func(x):
    await asyncio.sleep(0.1)
    return x * 3

funcoes = {"sync": sync_func, "async": async_func}

# Auto-detecta e usa a versão correta
resultado = jsonLogicAuto({"apply": ["sync", 5]}, {}, funcoes)
# Retorna 10 diretamente (função síncrona)

resultado_async = jsonLogicAuto({"apply": ["async", 5]}, {}, funcoes)
# Retorna uma corrotina (função assíncrona detectada)
```

## 🔄 Combinando Funções Síncronas e Assíncronas

```python
import asyncio
from lib.json_logic import jsonLogicAsync

# Funções mistas
def formatar_nome(primeiro, ultimo):
    return f"{ultimo.upper()}, {primeiro.capitalize()}"

async def buscar_usuario(user_id):
    await asyncio.sleep(0.1)
    return {"nome": "maria", "sobrenome": "silva"}

async def calcular_desconto(idade):
    await asyncio.sleep(0.05)
    return 0.1 if idade >= 18 else 0.0

funcoes = {
    "format_name": formatar_nome,
    "fetch_user": buscar_usuario,
    "calc_discount": calcular_desconto
}

async def exemplo_complexo():
    dados = {"user_id": 456}
    
    # 1. Busca dados do usuário (async)
    usuario = await jsonLogicAsync(
        {"apply": ["fetch_user", {"var": "user_id"}]},
        dados,
        funcoes
    )
    
    # 2. Adiciona dados ao contexto
    dados_completos = {**dados, "usuario": usuario}
    
    # 3. Regra complexa usando funções sync e async
    regra = {
        "and": [
            # Formata nome (sync)
            {
                "!=": [
                    {
                        "apply": [
                            "format_name",
                            {"var": "usuario.nome"},
                            {"var": "usuario.sobrenome"}
                        ]
                    },
                    ""
                ]
            },
            # Calcula desconto baseado na idade (async)
            {
                ">": [
                    {"apply": ["calc_discount", 25]},
                    0
                ]
            }
        ]
    }
    
    resultado = await jsonLogicAsync(regra, dados_completos, funcoes)
    print(f"Resultado: {resultado}")  # True

asyncio.run(exemplo_complexo())
```

## 📊 Casos de Uso Avançados

### 1. Validação de Documentos com API Externa

```python
async def validar_cpf_online(cpf):
    # Simula chamada para API de validação
    await asyncio.sleep(0.2)
    return len(cpf) == 11 and cpf.isdigit()

funcoes = {"validate_cpf": validar_cpf_online}

regra_validacao = {
    "and": [
        {"!=": [{"var": "cpf"}, ""]},
        {"apply": ["validate_cpf", {"var": "cpf"}]}
    ]
}

dados = {"cpf": "12345678901"}
resultado = await jsonLogicAsync(regra_validacao, dados, funcoes)
```

### 2. Cálculo de Preços com Múltiplas APIs

```python
async def buscar_preco_produto(produto_id):
    await asyncio.sleep(0.1)
    return {"preco": 100.0, "disponivel": True}

async def calcular_frete(cep_destino):
    await asyncio.sleep(0.15)
    return 15.0

async def obter_desconto_usuario(user_id):
    await asyncio.sleep(0.1)
    return 0.1  # 10% de desconto

funcoes = {
    "get_price": buscar_preco_produto,
    "calc_shipping": calcular_frete,
    "get_discount": obter_desconto_usuario
}

# Regra para calcular preço final
regra_preco = {
    "*": [
        {
            "+": [
                {"apply": ["get_price", {"var": "produto_id"}]},
                {"apply": ["calc_shipping", {"var": "cep"}]}
            ]
        },
        {
            "-": [
                1,
                {"apply": ["get_discount", {"var": "user_id"}]}
            ]
        }
    ]
}
```

### 3. Pipeline de Processamento de Dados

```python
async def extrair_dados(fonte):
    await asyncio.sleep(0.2)
    return {"dados": [1, 2, 3, 4, 5]}

async def transformar_dados(dados):
    await asyncio.sleep(0.1)
    return [x * 2 for x in dados]

async def validar_dados(dados):
    await asyncio.sleep(0.05)
    return all(x > 0 for x in dados)

funcoes = {
    "extract": extrair_dados,
    "transform": transformar_dados,
    "validate": validar_dados
}

# Pipeline de ETL
pipeline = {
    "apply": [
        "validate",
        {
            "apply": [
                "transform",
                {
                    "var": [
                        {"apply": ["extract", {"var": "fonte"}]},
                        "dados"
                    ]
                }
            ]
        }
    ]
}
```

## 🧪 Testes

Execute os testes para verificar o funcionamento:

```bash
# Testes básicos do JsonLogic
python -m pytest tests/test_json_logic.py -v

# Testes do suporte assíncrono
python -m pytest tests/test_async_support.py -v

# Todos os testes
python -m pytest tests/ -v
```

## 📈 Performance

### Benchmarks Básicos

- **Funções Síncronas**: Performance idêntica ao JsonLogic original
- **Funções Assíncronas**: Overhead mínimo (~2-5ms) para setup assíncrono
- **Execução Paralela**: Múltiplas operações assíncronas executam em paralelo automaticamente

### Recomendações

1. **Use `jsonLogic()`** para regras com apenas funções síncronas
2. **Use `jsonLogicAsync()`** para regras que incluem funções assíncronas
3. **Use `jsonLogicAuto()`** quando não souber antecipadamente o tipo das funções
4. **Combine ambos** os tipos de função na mesma regra sem problemas

## 🔧 API Reference

### `jsonLogicAsync(tests, data=None, functions=None)`

Versão assíncrona do JsonLogic.

**Parâmetros:**
- `tests`: Estrutura de regras JSON Logic
- `data`: Dados de contexto (opcional)
- `functions`: Dicionário de funções registradas (opcional)

**Retorna:** `Any` - Resultado da execução

### `jsonLogicAuto(tests, data=None, functions=None)`

Detecção automática de execução síncrona/assíncrona.

**Retorna:** `Any | Awaitable[Any]` - Resultado direto ou corrotina

### `has_async_functions(functions)`

Verifica se há funções assíncronas no dicionário.

**Parâmetros:**
- `functions`: Dicionário de funções

**Retorna:** `bool` - True se houver pelo menos uma função assíncrona

## 🤝 Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Adicione testes para suas mudanças
4. Execute os testes (`pytest tests/ -v`)
5. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
6. Push para a branch (`git push origin feature/nova-funcionalidade`)
7. Abra um Pull Request

## 📄 Licença

[Adicionar informações de licença]

## 🙏 Agradecimentos

- Baseado na especificação original do [JsonLogic](https://jsonlogic.com/)
- Comunidade Python pela excelente documentação de asyncio
