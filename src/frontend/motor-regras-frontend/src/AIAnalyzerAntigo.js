import React, { useState, useCallback } from 'react';
import './AIAnalyzer.css';

const AIAnalyzer = ({ nodes, edges, generatedJson, availableFields }) => {
  const [analysis, setAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [showApiKeyInput, setShowApiKeyInput] = useState(false);

  // Funções auxiliares para análise
  const calculateComplexity = useCallback((nodes, edges) => {
    const ifNodes = nodes.filter(n => n.type === 'if').length;
    const logicalNodes = nodes.filter(n => n.type === 'and' || n.type === 'or').length;
    const comparisonNodes = nodes.filter(n => n.type === 'comparison').length;
    
    return ifNodes * 2 + logicalNodes * 1.5 + comparisonNodes * 1;
  }, []);

  const calculateGraphDepth = useCallback((nodes, edges) => {
    const visited = new Set();
    const depths = new Map();
    
    const dfs = (nodeId, depth) => {
      if (visited.has(nodeId)) return depths.get(nodeId) || 0;
      
      visited.add(nodeId);
      depths.set(nodeId, depth);
      
      const outgoingEdges = edges.filter(e => e.source === nodeId);
      let maxChildDepth = depth;
      
      outgoingEdges.forEach(edge => {
        const childDepth = dfs(edge.target, depth + 1);
        maxChildDepth = Math.max(maxChildDepth, childDepth);
      });
      
      return maxChildDepth;
    };
    
    const rootNodes = nodes.filter(node => 
      !edges.some(edge => edge.target === node.id)
    );
    
    return Math.max(...rootNodes.map(node => dfs(node.id, 0)));
  }, []);

  const detectCircularDependencies = useCallback((nodes, edges) => {
    const visited = new Set();
    const recursionStack = new Set();
    
    const hasCycle = (nodeId) => {
      if (recursionStack.has(nodeId)) return true;
      if (visited.has(nodeId)) return false;
      
      visited.add(nodeId);
      recursionStack.add(nodeId);
      
      const outgoingEdges = edges.filter(e => e.source === nodeId);
      for (const edge of outgoingEdges) {
        if (hasCycle(edge.target)) return true;
      }
      
      recursionStack.delete(nodeId);
      return false;
    };
    
    return nodes.some(node => hasCycle(node.id));
  }, []);

  const extractOperators = useCallback((json) => {
    const operators = new Set();
    
    const traverse = (obj) => {
      if (typeof obj === 'object' && obj !== null) {
        Object.keys(obj).forEach(key => {
          operators.add(key);
          if (Array.isArray(obj[key])) {
            obj[key].forEach(traverse);
          } else if (typeof obj[key] === 'object') {
            traverse(obj[key]);
          }
        });
      }
    };
    
    traverse(json);
    return Array.from(operators);
  }, []);

  const extractVariables = useCallback((json) => {
    const variables = new Set();
    
    const traverse = (obj) => {
      if (typeof obj === 'object' && obj !== null) {
        if (obj.var) {
          variables.add(obj.var);
        }
        Object.values(obj).forEach(value => {
          if (typeof value === 'object' || Array.isArray(value)) {
            traverse(value);
          }
        });
      }
    };
    
    traverse(json);
    return Array.from(variables);
  }, []);

  const extractConstants = useCallback((json) => {
    const constants = new Set();
    
    const traverse = (obj) => {
      if (typeof obj === 'object' && obj !== null) {
        Object.values(obj).forEach(value => {
          if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
            constants.add(value);
          } else if (Array.isArray(value)) {
            value.forEach(traverse);
          } else if (typeof value === 'object') {
            traverse(value);
          }
        });
      }
    };
    
    traverse(json);
    return Array.from(constants);
  }, []);

  const analyzeGraphStructure = useCallback((nodes, edges) => {
    const nodeTypes = nodes.reduce((acc, node) => {
      acc[node.type] = (acc[node.type] || 0) + 1;
      return acc;
    }, {});

    const complexity = calculateComplexity(nodes, edges);
    const depth = calculateGraphDepth(nodes, edges);
    const orphanNodes = nodes.filter(node => 
      !edges.some(edge => edge.source === node.id || edge.target === node.id)
    );

    return {
      totalNodes: nodes.length,
      totalEdges: edges.length,
      nodeTypes,
      complexity,
      depth,
      orphanNodes: orphanNodes.length,
      hasCircularDependencies: detectCircularDependencies(nodes, edges)
    };
  }, [calculateComplexity, calculateGraphDepth, detectCircularDependencies]);

  const analyzeJsonLogic = useCallback((json) => {
    if (!json || Object.keys(json).length === 0) {
      return { isEmpty: true };
    }

    const operators = extractOperators(json);
    const variables = extractVariables(json);
    const constants = extractConstants(json);

    return {
      isEmpty: false,
      operators,
      variables,
      constants,
      jsonSize: JSON.stringify(json).length
    };
  }, [extractOperators, extractVariables, extractConstants]);

  const createAnalysisPrompt = useCallback((graphAnalysis, jsonAnalysis, fields) => {
    console.log('JSON que ele tá analisando:', jsonAnalysis)
    console.log('Fields da IA:', fields)
    return `
Analise esta regra de negócio criada em um editor visual de fluxo:

ESTRUTURA DO GRAFO:
- Total de nós: ${graphAnalysis.totalNodes}
- Total de conexões: ${graphAnalysis.totalEdges}
- Tipos de nós: ${JSON.stringify(graphAnalysis.nodeTypes)}
- Complexidade: ${graphAnalysis.complexity}
- Profundidade: ${graphAnalysis.depth}
- Nós órfãos: ${graphAnalysis.orphanNodes}
- Dependências circulares: ${graphAnalysis.hasCircularDependencies}

LÓGICA JSON:
${jsonAnalysis.isEmpty ? 'Nenhuma lógica gerada ainda' : JSON.stringify(jsonAnalysis)}

CAMPOS DISPONÍVEIS:
${fields.map(f => `- ${f.value}: ${f.label}`).join('\n')}

Por favor, forneça uma análise detalhada em português brasileiro incluindo:
1. Avaliação da complexidade e legibilidade
2. Possíveis problemas ou inconsistências
3. Sugestões de melhoria
4. Otimizações de performance
5. Boas práticas não seguidas
6. Pontos de atenção para manutenção

Seja específico e prático nas suas recomendações.
`;
  }, []);

  const callAIAPI = useCallback(async (prompt, apiKey) => {
    const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-goog-api-key': apiKey
      },
      body: JSON.stringify({
        contents: [
          {
            parts: [
              {
                text: `Você é um especialista em análise de regras de negócio e otimização de fluxos. Forneça análises detalhadas e sugestões práticas.\n\n${prompt}`
              }
            ]
          }
        ]
      })
    });

    if (!response.ok) {
      throw new Error(`Erro da API: ${response.status}`);
    }

    const data = await response.json();
    return {
      suggestions: data.candidates?.[0]?.content?.parts?.[0]?.text || "Sem resposta da API",
      model: "gemini-2.0-flash",
      usage: null // Gemini API não fornece dados de uso de tokens como o OpenAI
    };
  }, []);

  const analyzeGraph = useCallback(async () => {
    if (!apiKey) {
      setShowApiKeyInput(true);
      return;
    }

    setIsAnalyzing(true);
    try {
      const graphAnalysis = analyzeGraphStructure(nodes, edges);
      const jsonAnalysis = analyzeJsonLogic(generatedJson);
      
      const analysisPrompt = createAnalysisPrompt(graphAnalysis, jsonAnalysis, availableFields);
      
      const aiResponse = await callAIAPI(analysisPrompt, apiKey);
      
      setAnalysis({
        ...aiResponse,
        graphStats: graphAnalysis,
        timestamp: new Date().toLocaleString('pt-BR')
      });
    } catch (error) {
      console.error('Erro na análise:', error);
      setAnalysis({
        error: 'Erro ao analisar o grafo. Verifique sua chave da API.',
        timestamp: new Date().toLocaleString('pt-BR')
      });
    } finally {
      setIsAnalyzing(false);
    }
  }, [nodes, edges, generatedJson, availableFields, apiKey, analyzeGraphStructure, analyzeJsonLogic, createAnalysisPrompt, callAIAPI]);

  const handleSaveApiKey = () => {
    localStorage.setItem('gemini-api-key', apiKey);
    setShowApiKeyInput(false);
  };

  const handleLoadApiKey = () => {
    const savedKey = localStorage.getItem('gemini-api-key');
    if (savedKey) {
      setApiKey(savedKey);
    }
  };

  React.useEffect(() => {
    handleLoadApiKey();
  }, []);

  return (
    <div className="ai-analyzer">
      <div className="ai-analyzer-header">
        <button 
          className="ai-analyzer-toggle"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          🤖 Análise por IA {isExpanded ? '▼' : '▶'}
        </button>

        {!showApiKeyInput && (
          <button 
            className="analyze-button"
            onClick={analyzeGraph}
            disabled={isAnalyzing || nodes.length === 0}
          >
            
            {isAnalyzing ? 'Analisando...' : 'Analisar Grafo'}
          </button>
        )}
        
        <button 
          className="config-button"
          onClick={() => setShowApiKeyInput(!showApiKeyInput)}
        >
          ⚙️
        </button>
      </div>

       {showApiKeyInput && (
        <div className="api-key-input">
          <input
            type="password"
            placeholder="Chave da API Gemini"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />
          <button onClick={handleSaveApiKey}>Salvar</button>
          <button onClick={() => setShowApiKeyInput(false)}>Cancelar</button>
        </div>
      )}

      {isExpanded && (
        <div className="ai-analyzer-content">
          {analysis && (
            <div className="analysis-results">
              <div className="analysis-header">
                <h3>Análise Gerada</h3>
                <span className="analysis-timestamp">{analysis.timestamp}</span>
              </div>
              
              {analysis.error ? (
                <div className="analysis-error">
                  <p>{analysis.error}</p>
                </div>
              ) : (
                <>
                  <div className="graph-stats">
                    <h4>Estatísticas do Grafo</h4>
                    <div className="stats-grid">
                      <div className="stat">
                        <span className="stat-label">Nós:</span>
                        <span className="stat-value">{analysis.graphStats.totalNodes}</span>
                      </div>
                      <div className="stat">
                        <span className="stat-label">Conexões:</span>
                        <span className="stat-value">{analysis.graphStats.totalEdges}</span>
                      </div>
                      <div className="stat">
                        <span className="stat-label">Complexidade:</span>
                        <span className="stat-value">{analysis.graphStats.complexity.toFixed(1)}</span>
                      </div>
                      <div className="stat">
                        <span className="stat-label">Profundidade:</span>
                        <span className="stat-value">{analysis.graphStats.depth}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="ai-suggestions">
                    <h4>Sugestões da IA</h4>
                    <div className="suggestions-content">
                      {analysis.suggestions.split('\n').map((line, index) => (
                        <p key={index}>{line}</p>
                      ))}
                    </div>
                  </div>
                  
                  {analysis.usage && (
                    <div className="usage-info">
                      <small>
                        Tokens utilizados: {analysis.usage.total_tokens} | 
                        Modelo: {analysis.model}
                      </small>
                    </div>
                  )}
                </>
              )}
            </div>
          )}
          
          {!analysis && !isAnalyzing && (
            <div className="no-analysis">
              <p>Clique em "Analisar Grafo" para obter dicas da IA sobre sua regra de negócio.</p>
              <p><small>Você precisará fornecer uma chave da API Gemini.</small></p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AIAnalyzer;