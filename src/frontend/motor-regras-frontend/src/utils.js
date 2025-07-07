// src/utils.js

const buildJsonFromNode = (node, nodes, edges) => {
  if (!node) return null;

  switch (node.type) {
    case 'if':
      const thenEdge = edges.find(e => e.source === node.id && e.sourceHandle === 'then');
      const elseEdge = edges.find(e => e.source === node.id && e.sourceHandle === 'else');
      const conditionEdge = edges.find(e => e.target === node.id && (e.targetHandle === 'condition' || e.targetHandle === null));
      
      const thenNode = thenEdge ? nodes.find(n => n.id === thenEdge.target) : null;
      const elseNode = elseEdge ? nodes.find(n => n.id === elseEdge.target) : null;
      const conditionNode = conditionEdge ? nodes.find(n => n.id === conditionEdge.source) : null;

      return {
        "if": [
          buildJsonFromNode(conditionNode, nodes, edges),
          buildJsonFromNode(thenNode, nodes, edges),
          buildJsonFromNode(elseNode, nodes, edges)
        ]
      };

    case 'comparison':
      const { field, operator, value } = node.data;
      if (!field || !operator || value === undefined) return null;
      return { [operator]: [{ "var": field }, value] };

    case 'result':
      return node.data.value;

    default:
      return null;
  }
};

// --- LÓGICA DE DETECÇÃO DE NÓ RAIZ CORRIGIDA E SIMPLIFICADA ---
export const graphToJsonLogic = (nodes, edges) => {
  // A nova lógica assume que o nó raiz é o nó 'if' que não é resultado de outro 'if'.
  // Esta abordagem é muito mais robusta para grafos aninhados.
  const rootNode = nodes.find(n => 
    n.type === 'if' && 
    !edges.some(e => e.target === n.id && (e.sourceHandle === 'then' || e.sourceHandle === 'else'))
  );

  if (!rootNode) {
    // Se não encontrar um nó raiz claro, tenta pegar o primeiro IF como fallback.
    const fallbackRoot = nodes.find(n => n.type === 'if');
    if (!fallbackRoot) {
      return { error: "Adicione um 'Bloco IF' para iniciar a regra." };
    }
    return buildJsonFromNode(fallbackRoot, nodes, edges);
  }
  
  return buildJsonFromNode(rootNode, nodes, edges);
};