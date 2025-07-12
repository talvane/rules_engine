# Exemplo de Uso - Análise por IA no FlowBuilder

## Cenário: Análise de Aprovação de Crédito

Vamos criar uma regra de negócio para aprovação de crédito e ver como a IA analisa e sugere melhorias.

### Passo 1: Criando a Regra

1. **Abra o FlowBuilder**
2. **Adicione os seguintes nós:**
   - 1 nó IF (condição principal)
   - 2 nós Comparison (para idade e renda)
   - 1 nó AND (para combinar condições)
   - 2 nós Result (aprovado/rejeitado)

3. **Configure as conexões:**
   ```
   Comparison(idade >= 18) → AND
   Comparison(renda >= 2000) → AND
   AND → IF (condição)
   IF → Result("Aprovado") (then)
   IF → Result("Rejeitado") (else)
   ```

### Passo 2: Análise Local

1. **Clique em "🔍 Análise Inteligente"**
2. **Clique em "Analisar"**

#### Resultado Esperado:
```
## 📊 Análise Estrutural
- **Nós totais**: 6
- **Conexões**: 5
- **Complexidade**: 5.5
- **Profundidade**: 2

## 📈 Boas Práticas
✅ Complexidade baixa - fácil de entender
✅ Profundidade baixa - boa legibilidade

## 🔧 Recomendações de Manutenção
- Teste cada caminho do fluxo com dados reais
- Documente as regras de negócio em linguagem natural
- Considere usar versionamento para mudanças
- Mantenha backup das regras antes de modificações
```

### Passo 3: Análise com OpenAI (Opcional)

1. **Configure sua chave OpenAI**
2. **Clique em "🤖 Análise por IA"**
3. **Clique em "Analisar Grafo"**

#### Resultado Esperado:
```
## Análise Avançada por IA

### Avaliação da Complexidade
A regra apresenta complexidade baixa (5.5) e está bem estruturada. 
A lógica é clara e fácil de seguir.

### Sugestões de Melhoria
1. Considere adicionar validação de score de crédito
2. Implemente diferentes níveis de aprovação baseados na renda
3. Adicione verificação de histórico de crédito
4. Considere fatores como tempo de emprego

### Otimizações de Performance
- A regra é eficiente com apenas 2 comparações
- Não há redundâncias detectadas
- Estrutura otimizada para avaliação rápida

### Boas Práticas
✅ Uso correto de operadores lógicos
✅ Estrutura clara de condições
⚠️ Considere adicionar mais critérios para decisão mais robusta

### Pontos de Atenção
- Teste com casos extremos (renda exatamente 2000)
- Valide comportamento com dados inválidos
- Considere regulamentações financeiras aplicáveis
```

## Exemplo 2: Regra Complexa com Problemas

### Criando uma Regra Problemática

1. **Adicione muitos nós IF aninhados** (mais de 5 níveis)
2. **Deixe alguns nós desconectados**
3. **Crie múltiplas comparações redundantes**

### Análise Esperada:
```
## ⚠️ Problemas Detectados
- 3 nó(s) órfão(s) detectado(s). Considere conectá-los ou removê-los.
- Complexidade alta detectada. Considere dividir a regra em sub-regras menores.
- Profundidade muito alta. Regras muito aninhadas podem ser difíceis de manter.

## 💡 Sugestões de Melhoria
- Muitas condições IF detectadas. Considere usar uma tabela de decisão.
- Muitas comparações. Considere agrupar condições relacionadas.

## 📈 Boas Práticas
🔴 Complexidade alta - considere refatorar
🔴 Profundidade alta - difícil de manter
```

## Exemplo 3: Regra de Desconto Dinâmico

### Cenário: Sistema de Descontos por Fidelidade

```javascript
// Regra JSON gerada
{
  "if": [
    {"and": [
      {">=": [{"var": "anos_cliente"}, 2]},
      {">=": [{"var": "compras_ano"}, 10]}
    ]},
    {"if": [
      {">=": [{"var": "valor_compra"}, 1000]},
      15,  // 15% desconto
      10   // 10% desconto
    ]},
    {"if": [
      {">=": [{"var": "anos_cliente"}, 1]},
      5,   // 5% desconto
      0    // sem desconto
    ]}
  ]
}
```

### Análise da IA:
```
## Análise da Regra de Desconto

### Estrutura Detectada
- Regra condicional aninhada com 3 níveis
- Utiliza anos de cliente, número de compras e valor
- Implementa desconto progressivo baseado em fidelidade

### Pontos Fortes
✅ Lógica clara de progressão de desconto
✅ Considera múltiplos fatores de fidelidade
✅ Estrutura bem organizada

### Sugestões de Melhoria
1. **Adicionar limites máximos**: Considere um teto para descontos
2. **Validação de entrada**: Verifique se os valores são positivos
3. **Flexibilidade**: Considere tabela de configuração para percentuais
4. **Logging**: Adicione logs para auditoria de descontos aplicados

### Casos de Teste Recomendados
- Cliente novo (0 anos): desconto 0%
- Cliente 1 ano, 5 compras: desconto 5%
- Cliente 2 anos, 15 compras, compra R$ 500: desconto 10%
- Cliente 3 anos, 20 compras, compra R$ 1500: desconto 15%
```

## Boas Práticas para Análise

### 1. Preparação
- ✅ Complete o grafo antes de analisar
- ✅ Gere o JSON da regra
- ✅ Configure valores dos nós corretamente

### 2. Interpretação
- 📊 Observe as métricas de complexidade
- ⚠️ Priorize problemas críticos
- 💡 Considere sugestões de melhoria
- 🔧 Implemente recomendações gradualmente

### 3. Iteração
- 🔄 Analise após cada modificação
- 📈 Compare métricas antes/depois
- 🎯 Busque reduzir complexidade
- 📋 Mantenha histórico de análises

## Integração com Workflow

### Desenvolvimento
1. **Criar regra** → **Análise inicial** → **Ajustes**
2. **Teste** → **Análise pós-teste** → **Refinamentos**
3. **Revisão** → **Análise final** → **Deployment**

### Manutenção
1. **Análise periódica** das regras existentes
2. **Monitoramento** de métricas de complexidade
3. **Refatoração** quando necessário
4. **Documentação** das mudanças

## Conclusão

A análise por IA no FlowBuilder oferece:
- ✅ **Insights valiosos** sobre qualidade do código
- ✅ **Detecção precoce** de problemas
- ✅ **Sugestões práticas** de melhoria
- ✅ **Métricas objetivas** de complexidade
- ✅ **Flexibilidade** (local ou cloud)

Use essas ferramentas para criar regras de negócio mais robustas, maintíveis e eficientes!
