import React, { useState, useCallback } from 'react';
import './LocalAIAnalyzer.css';

const LocalAIAnalyzer = ({ nodes, edges, generatedJson, availableFields }) => {
  const [analysis, setAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  // Funções auxiliares básicas
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
    
    return rootNodes.length > 0 ? Math.max(...rootNodes.map(node => dfs(node.id, 0))) : 0;
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

    const warnings = [];
    const suggestions = [];

    // Análise de problemas comuns
    if (orphanNodes.length > 0) {
      warnings.push(`${orphanNodes.length} nó(s) órfão(s) detectado(s). Considere conectá-los ou removê-los.`);
    }

    if (complexity > 10) {
      warnings.push('Complexidade alta detectada. Considere dividir a regra em sub-regras menores.');
    }

    if (depth > 5) {
      warnings.push('Profundidade muito alta. Regras muito aninhadas podem ser difíceis de manter.');
    }

    // Sugestões baseadas nos tipos de nós
    if (nodeTypes.if > 3) {
      suggestions.push('Muitas condições IF detectadas. Considere usar uma tabela de decisão.');
    }

    if (nodeTypes.comparison > 5) {
      suggestions.push('Muitas comparações. Considere agrupar condições relacionadas.');
    }

    if (!nodeTypes.result) {
      warnings.push('Nenhum nó de resultado detectado. Adicione pelo menos um resultado.');
    }

    return {
      totalNodes: nodes.length,
      totalEdges: edges.length,
      nodeTypes,
      complexity,
      depth,
      orphanNodes: orphanNodes.length,
      warnings,
      suggestions,
      hasCircularDependencies: detectCircularDependencies(nodes, edges)
    };
  }, [calculateComplexity, calculateGraphDepth, detectCircularDependencies]);

  const generateLocalAnalysis = useCallback((graphAnalysis) => {
    const analysis = [];
    
    analysis.push('## 📊 Análise Estrutural');
    analysis.push(`- **Nós totais**: ${graphAnalysis.totalNodes}`);
    analysis.push(`- **Conexões**: ${graphAnalysis.totalEdges}`);
    analysis.push(`- **Complexidade**: ${graphAnalysis.complexity.toFixed(1)}`);
    analysis.push(`- **Profundidade**: ${graphAnalysis.depth}`);
    analysis.push('');

    if (graphAnalysis.warnings.length > 0) {
      analysis.push('## ⚠️ Problemas Detectados');
      graphAnalysis.warnings.forEach(warning => {
        analysis.push(`- ${warning}`);
      });
      analysis.push('');
    }

    if (graphAnalysis.suggestions.length > 0) {
      analysis.push('## 💡 Sugestões de Melhoria');
      graphAnalysis.suggestions.forEach(suggestion => {
        analysis.push(`- ${suggestion}`);
      });
      analysis.push('');
    }

    analysis.push('## 📈 Boas Práticas');
    
    if (graphAnalysis.complexity <= 5) {
      analysis.push('✅ Complexidade baixa - fácil de entender');
    } else if (graphAnalysis.complexity <= 10) {
      analysis.push('🔶 Complexidade média - aceitável');
    } else {
      analysis.push('🔴 Complexidade alta - considere refatorar');
    }

    if (graphAnalysis.depth <= 3) {
      analysis.push('✅ Profundidade baixa - boa legibilidade');
    } else if (graphAnalysis.depth <= 5) {
      analysis.push('🔶 Profundidade média - aceitável');
    } else {
      analysis.push('🔴 Profundidade alta - difícil de manter');
    }

    analysis.push('');
    analysis.push('## 🔧 Recomendações de Manutenção');
    analysis.push('- Teste cada caminho do fluxo com dados reais');
    analysis.push('- Documente as regras de negócio em linguagem natural');
    analysis.push('- Considere usar versionamento para mudanças');
    analysis.push('- Mantenha backup das regras antes de modificações');

    return analysis.join('\n');
  }, []);

  const analyzeGraph = useCallback(async () => {
    setIsAnalyzing(true);
    try {
      const graphAnalysis = analyzeGraphStructure(nodes, edges);
      
      const analysisResult = {
        suggestions: generateLocalAnalysis(graphAnalysis),
        model: 'Análise Local',
        endpoint: 'local'
      };
      
      setAnalysis({
        ...analysisResult,
        graphStats: graphAnalysis,
        timestamp: new Date().toLocaleString('pt-BR')
      });
    } catch (error) {
      console.error('Erro na análise:', error);
      setAnalysis({
        error: 'Erro ao analisar o grafo.',
        timestamp: new Date().toLocaleString('pt-BR')
      });
    } finally {
      setIsAnalyzing(false);
    }
  }, [nodes, edges, analyzeGraphStructure, generateLocalAnalysis]);

  return (
    <div className="local-ai-analyzer">
      <div className="local-ai-analyzer-header">
        <button 
          className="local-ai-analyzer-toggle"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          🔍 Análise Inteligente {isExpanded ? '▼' : '▶'}
        </button>
        
        <button 
          className="analyze-button"
          onClick={analyzeGraph}
          disabled={isAnalyzing || nodes.length === 0}
        >
          {isAnalyzing ? 'Analisando...' : 'Analisar'}
        </button>
      </div>

      {isExpanded && (
        <div className="local-ai-analyzer-content">
          {analysis && (
            <div className="analysis-results">
              <div className="analysis-header">
                <h3>Análise do Grafo</h3>
                <span className="analysis-timestamp">{analysis.timestamp}</span>
              </div>
              
              {analysis.error ? (
                <div className="analysis-error">
                  <p>{analysis.error}</p>
                </div>
              ) : (
                <>
                  <div className="graph-stats">
                    <h4>Estatísticas</h4>
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
                    <h4>Análise e Sugestões</h4>
                    <div className="suggestions-content">
                      {analysis.suggestions.split('\n').map((line, index) => (
                        <div key={index} className={line.startsWith('##') ? 'section-header' : 'suggestion-line'}>
                          {line}
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="analysis-info">
                    <small>
                      Analisado por: {analysis.model} | 
                      Endpoint: {analysis.endpoint}
                    </small>
                  </div>
                </>
              )}
            </div>
          )}
          
          {!analysis && !isAnalyzing && (
            <div className="no-analysis">
              <p>Clique em "Analisar" para obter insights sobre sua regra de negócio.</p>
              <p><small>Análise local inteligente - não requer APIs externas.</small></p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default LocalAIAnalyzer;