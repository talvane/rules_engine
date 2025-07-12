# Análise por IA Generativa - FlowBuilder

## Visão Geral

O FlowBuilder agora inclui duas opções de análise por IA generativa para fornecer insights e sugestões sobre as regras de negócio criadas:

1. **AIAnalyzer** - Integração com OpenAI GPT
2. **LocalAIAnalyzer** - Análise local inteligente (sem APIs externas)

## Funcionalidades

### 🤖 AIAnalyzer (OpenAI)
- **Análise avançada** usando GPT-3.5-turbo
- **Sugestões contextualizadas** baseadas no grafo e lógica JSON
- **Detecção de problemas** complexos
- **Recomendações de otimização** de performance
- **Análise de boas práticas** de desenvolvimento

#### Configuração
1. Obtenha uma chave da API OpenAI em [platform.openai.com](https://platform.openai.com)
2. Clique no botão ⚙️ no componente AIAnalyzer
3. Insira sua chave da API
4. Clique em "Salvar" (a chave é armazenada localmente)

### 🔍 LocalAIAnalyzer (Análise Local)
- **Análise baseada em regras** sem necessidade de APIs externas
- **Detecção de problemas comuns** como nós órfãos, complexidade alta
- **Métricas de qualidade** do código
- **Sugestões de melhoria** baseadas em padrões conhecidos
- **Recomendações de manutenção**

#### Vantagens
- ✅ Funciona offline
- ✅ Não requer chaves de API
- ✅ Análise instantânea
- ✅ Privacidade total dos dados

## Como Usar

### Criando um Grafo
1. Use a barra lateral para adicionar nós ao grafo
2. Conecte os nós para formar a lógica da regra
3. Configure os valores dos nós conforme necessário

### Analisando com IA
1. **AIAnalyzer**:
   - Configure sua chave OpenAI (primeira vez apenas)
   - Clique em "🤖 Análise por IA"
   - Clique em "Analisar Grafo"
   - Aguarde a análise (alguns segundos)

2. **LocalAIAnalyzer**:
   - Clique em "🔍 Análise Inteligente"
   - Clique em "Analisar"
   - Receba insights instantâneos

### Interpretando os Resultados

#### Métricas Exibidas
- **Nós**: Número total de nós no grafo
- **Conexões**: Número de conexões/edges
- **Complexidade**: Medida da complexidade da regra (0-20+)
- **Profundidade**: Nível máximo de aninhamento

#### Categorias de Análise
- **📊 Análise Estrutural**: Estatísticas básicas do grafo
- **⚠️ Problemas Detectados**: Questões que precisam de atenção
- **💡 Sugestões de Melhoria**: Recomendações para otimizar
- **📈 Boas Práticas**: Avaliação de qualidade do código
- **🔧 Recomendações de Manutenção**: Dicas para manter o código

#### Interpretação da Complexidade
- **0-5**: ✅ Baixa - Fácil de entender e manter
- **6-10**: 🔶 Média - Aceitável, mas monitore
- **11+**: 🔴 Alta - Considere dividir em sub-regras

## Exemplos de Problemas Detectados

### Problemas Comuns
- **Nós órfãos**: Nós não conectados que podem ser removidos
- **Complexidade alta**: Regras muito complexas que dificultam manutenção
- **Profundidade excessiva**: Aninhamento muito profundo
- **Muitas condições IF**: Pode ser simplificado com tabelas de decisão
- **Ausência de resultados**: Regras sem nós de resultado

### Sugestões Típicas
- Dividir regras complexas em sub-regras menores
- Agrupar condições relacionadas
- Usar tabelas de decisão para múltiplas condições
- Adicionar documentação em linguagem natural
- Implementar testes para cada caminho

## Integração com APIs Externas

### OpenAI (AIAnalyzer)
- Modelo padrão: `gpt-3.5-turbo`
- Tokens máximos: 1000
- Temperatura: 0.7
- Custo: ~$0.002 por análise

### Ollama (LocalAIAnalyzer - Futuro)
O LocalAIAnalyzer pode ser estendido para suportar modelos locais como:
- Llama 2
- CodeLlama
- Mistral
- Outros modelos via Ollama

## Privacidade e Segurança

### AIAnalyzer
- Dados são enviados para OpenAI
- Chave da API armazenada localmente
- Considere políticas de privacidade da empresa

### LocalAIAnalyzer
- Análise 100% local
- Nenhum dado enviado externamente
- Ideal para ambientes corporativos sensíveis

## Personalização

### Adicionando Novas Regras de Análise
Para adicionar novas regras ao LocalAIAnalyzer:

```javascript
// Em LocalAIAnalyzer.js
const analyzeGraphStructure = (nodes, edges) => {
  // ... código existente ...
  
  // Nova regra personalizada
  if (nodeTypes.custom_condition) {
    suggestions.push('Detectada condição personalizada - considere documentar');
  }
  
  return analysisResult;
};
```

### Customizando Prompts da OpenAI
```javascript
// Em AIAnalyzer.js
const createAnalysisPrompt = (graphAnalysis, jsonAnalysis, fields) => {
  return `
    Contexto adicional: Esta é uma regra para [seu domínio específico]
    
    ${/* prompt existente */}
    
    Considere também:
    - Regulamentações específicas do setor
    - Padrões da empresa
    - Arquitetura existente
  `;
};
```

## Troubleshooting

### Problemas Comuns

1. **Erro de API Key (OpenAI)**
   - Verifique se a chave está correta
   - Confirme se há créditos na conta
   - Teste a chave em uma ferramenta externa

2. **Análise não carrega**
   - Verifique conexão com internet (OpenAI)
   - Tente novamente em alguns segundos
   - Use o LocalAIAnalyzer como alternativa

3. **Resultados imprecisos**
   - Certifique-se de que o grafo está completo
   - Gere o JSON da regra antes de analisar
   - Configure corretamente os valores dos nós

### Logs de Debug
Abra o console do navegador (F12) para ver logs detalhados:
```javascript
// Console logs disponíveis
console.log('Análise iniciada');
console.log('Estrutura do grafo:', graphAnalysis);
console.log('Resposta da IA:', aiResponse);
```

## Roadmap Futuro

### Funcionalidades Planejadas
- [ ] Suporte a múltiplos modelos de IA
- [ ] Análise de performance em tempo real
- [ ] Integração com sistemas de versionamento
- [ ] Exportação de relatórios de análise
- [ ] Histórico de análises
- [ ] Comparação entre versões de regras
- [ ] Sugestões de refatoração automática
- [ ] Integração com ferramentas de CI/CD

### Melhorias Técnicas
- [ ] Cache de análises
- [ ] Análise incremental
- [ ] Suporte a grafos grandes
- [ ] Análise paralela
- [ ] Integração com IDEs

## Contribuindo

Para contribuir com melhorias:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente suas mudanças
4. Adicione testes se necessário
5. Faça commit das mudanças
6. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
