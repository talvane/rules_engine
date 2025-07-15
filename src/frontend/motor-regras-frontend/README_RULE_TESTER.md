# Testador de Regras - Manual de Uso

## Visão Geral

O componente **RuleTester** foi adicionado ao FlowBuilder para permitir que você teste suas regras JSON Logic com dados reais. Ele oferece duas opções de processamento:

1. **Frontend (JavaScript)**: Processamento local no navegador
2. **Backend (Python)**: Processamento usando a biblioteca Python original

## Como Usar

### 1. Criando uma Regra

1. Use o FlowBuilder para criar sua regra arrastando nós da barra lateral
2. Conecte os nós conforme necessário
3. Clique em "Gerar JSON da Regra" para gerar o JSON Logic

### 2. Preparando os Dados de Teste

1. Na seção "Testar Regra", você pode:
   - Digitar manualmente os dados JSON no campo de texto
   - Usar o botão "Gerar Dados de Exemplo" para criar dados baseados nos campos disponíveis

### 3. Escolhendo o Método de Processamento

#### Frontend (JavaScript)
- **Prós**: Rápido, não requer configuração adicional
- **Contras**: Implementação simplificada, pode não suportar todas as operações

#### Backend (Python)
- **Prós**: Implementação completa e robusta do JSON Logic
- **Contras**: Requer servidor Python rodando

### 4. Executando o Teste

1. Configure seus dados de entrada
2. Escolha o método de processamento
3. Clique em "Testar Regra"
4. Veja o resultado na seção "Resultado"

## Configuração do Backend Python

Para usar o processamento Python:

### 1. Instalar Dependências

```bash
cd /Users/talvane/Projetos/gb.tech/motor-decisoes-2/poc-jsonlogic
poetry install
```

### 2. Executar o Servidor

```bash
python src/api_server.py
```

O servidor será iniciado em `http://localhost:5000`

### 3. Endpoints Disponíveis

- `GET /api/health` - Verificar status do servidor
- `POST /api/process-rule` - Processar regra com dados
- `POST /api/validate-rule` - Validar regra

## Exemplos de Uso

### Exemplo 1: Regra Simples de Comparação

**Regra**: Verificar se idade é maior que 18

```json
{
  ">": [
    {"var": "idade"},
    18
  ]
}
```

**Dados de Entrada**:
```json
{
  "idade": 25
}
```

**Resultado**: `true`

### Exemplo 2: Regra Complexa com Condições

**Regra**: Aprovação de empréstimo

```json
{
  "and": [
    {">": [{"var": "score"}, 600]},
    {">": [{"var": "renda"}, 3000]},
    {"!": {"var": "possui_divida"}}
  ]
}
```

**Dados de Entrada**:
```json
{
  "score": 750,
  "renda": 5000,
  "possui_divida": false
}
```

**Resultado**: `true`

### Exemplo 3: Regra com Resultado Condicional

**Regra**: Determinar categoria do cliente

```json
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
```

**Dados de Entrada**:
```json
{
  "score": 720
}
```

**Resultado**: `"Regular"`

## Operações Suportadas

### Frontend (JavaScript)
- Comparações: `==`, `!=`, `>`, `>=`, `<`, `<=`
- Lógicas: `!`, `and`, `or`, `if`/`?:`
- Matemáticas: `+`, `-`, `*`, `/`, `%`
- Dados: `var`, `in`, `cat`

### Backend (Python)
- Todas as operações do frontend
- Operações avançadas: `some`, `every`, `none`, `merge`, `map`, `filter`, `reduce`
- Suporte a funções customizadas com `apply`
- Processamento assíncrono

## Solução de Problemas

### Backend Não Disponível
- Verifique se o servidor Python está rodando
- Confirme que a porta 5000 está disponível
- Verifique se as dependências estão instaladas

### Erro de Parsing JSON
- Verifique a sintaxe do JSON nos dados de entrada
- Use aspas duplas para strings
- Não use vírgulas no final de arrays/objetos

### Regra Não Funciona
- Verifique se a regra foi gerada corretamente
- Confirme que os nomes dos campos nos dados correspondem aos usados na regra
- Teste com dados mais simples primeiro

## Dicas de Uso

1. **Comece Simples**: Teste com regras simples antes de criar lógicas complexas
2. **Use Dados Reais**: Teste com dados que representam cenários reais
3. **Valide Sempre**: Sempre teste sua regra antes de usar em produção
4. **Documente**: Mantenha exemplos de dados de teste para referência futura
