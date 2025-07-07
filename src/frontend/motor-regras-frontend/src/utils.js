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

function formatCondition(condition) {
  if (!condition || typeof condition !== 'object') return 'condição inválida';
  
  const operator = Object.keys(condition)[0];
  if (!operator) return 'condição vazia';

  const args = condition[operator];
  if (!Array.isArray(args) || args.length < 2) return 'argumentos inválidos';

  const field = args[0]?.var;
  const value = typeof args[1] === 'string' ? `"${args[1]}"` : args[1];

  return `<strong>${field || ''} ${operator} ${value !== undefined ? value : ''}</strong>`;
}

// Função principal que gera a lista de passos a partir do JSON
export const generateExplanationSteps = (rule) => {
  const steps = [];
  let stepCounter = 1;

  function recurse(currentRule, level = 0, path = '') {
    // Caso base: Se a regra for um resultado final (uma string)
    if (typeof currentRule === 'string') {
      steps.push({ 
        text: `${path} o resultado final é <strong>"${currentRule}"</strong> e o processo termina.`,
        level 
      });
      return;
    }

    // Caso recursivo: Se for um bloco "if"
    if (currentRule && currentRule.if) {
      const [condition, thenBranch, elseBranch] = currentRule.if;
      
      if (!condition) return; // Não processa "if" sem condição

      const conditionText = formatCondition(condition);
      steps.push({ 
        text: `${stepCounter}. Avalia-se a condição: ${conditionText}?`, 
        level
      });
      stepCounter++;

      // Processa o caminho "ENTÃO"
      if (thenBranch) {
        recurse(thenBranch, level + 1, '↳ Se <strong>SIM</strong>,');
      }
      
      // Processa o caminho "SENÃO"
      if (elseBranch) {
        recurse(elseBranch, level + 1, '↳ Se <strong>NÃO</strong>,');
      }
    }
  }

  recurse(rule);
  return steps;
};