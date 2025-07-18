import { MarkerType } from 'reactflow';

let nodeIdCounter = 0;
const generateNodeId = () => `loaded_node_${nodeIdCounter++}`;

function buildGraphRecursively(rule, position, nodes, edges, sharedData) {
  if (rule === null || typeof rule !== 'object') {
    const id = generateNodeId();
    nodes.push({ id, type: 'result', position, data: { ...sharedData, value: rule } });
    return id;
  }

  const operator = Object.keys(rule)[0];
  const values = rule[operator];
  const currentNodeId = generateNodeId();
  let currentNode;
  const Y_OFFSET = 200;
  const X_SPACING = 300;

  switch(operator) {
      case 'if': currentNode = { id: currentNodeId, type: 'if', position, data: { ...sharedData } }; break;
      case 'and': case 'or': currentNode = { id: currentNodeId, type: operator, position, data: { ...sharedData } }; break;
      case 'var': currentNode = { id: currentNodeId, type: 'var', position, data: { ...sharedData, field: values } }; break;
      default: currentNode = { id: currentNodeId, type: 'comparison', position, data: { ...sharedData, operator, field: values[0]?.var, value: values[1] } }; break;
  }
  nodes.push(currentNode);

  if (operator === 'if') {
      const [condition, thenBranch, elseBranch] = values;
      const conditionNodeId = buildGraphRecursively(condition, { x: position.x, y: position.y - Y_OFFSET }, nodes, edges, sharedData);
      if(conditionNodeId) edges.push({ id: `e-${conditionNodeId}-${currentNodeId}`, source: conditionNodeId, target: currentNodeId, targetHandle: 'condition', markerEnd: { type: MarkerType.ArrowClosed } });

      const thenNodeId = buildGraphRecursively(thenBranch, { x: position.x - X_SPACING, y: position.y + Y_OFFSET }, nodes, edges, sharedData);
      if(thenNodeId) edges.push({ id: `e-${currentNodeId}-then-${thenNodeId}`, source: currentNodeId, sourceHandle: 'then', target: thenNodeId, targetHandle: 'entry', markerEnd: { type: MarkerType.ArrowClosed } });

      const elseNodeId = buildGraphRecursively(elseBranch, { x: position.x + X_SPACING, y: position.y + Y_OFFSET }, nodes, edges, sharedData);
      if(elseNodeId) edges.push({ id: `e-${currentNodeId}-else-${elseNodeId}`, source: currentNodeId, sourceHandle: 'else', target: elseNodeId, targetHandle: 'entry', markerEnd: { type: MarkerType.ArrowClosed } });
  } else if (operator === 'and' || operator === 'or') {
      const [condA, condB] = values;
      const nodeA_Id = buildGraphRecursively(condA, { x: position.x - X_SPACING, y: position.y - 70 }, nodes, edges, sharedData);
      if(nodeA_Id) edges.push({ id: `e-${nodeA_Id}-${currentNodeId}-a`, source: nodeA_Id, target: currentNodeId, targetHandle: 'a', markerEnd: { type: MarkerType.ArrowClosed } });
      
      const nodeB_Id = buildGraphRecursively(condB, { x: position.x - X_SPACING, y: position.y + 70 }, nodes, edges, sharedData);
      if(nodeB_Id) edges.push({ id: `e-${nodeB_Id}-${currentNodeId}-b`, source: nodeB_Id, target: currentNodeId, targetHandle: 'b', markerEnd: { type: MarkerType.ArrowClosed } });
  }
  return currentNodeId;
}

export const jsonToGraph = (jsonRule, sharedData) => {
  if (!jsonRule || typeof jsonRule !== 'object' || Object.keys(jsonRule).length === 0) {
    return { nodes: [], edges: [] };
  }
  nodeIdCounter = 0;
  const nodes = [];
  const edges = [];
  buildGraphRecursively(jsonRule, { x: 600, y: 150 }, nodes, edges, sharedData);
  return { nodes, edges };
};

// Função recursiva que percorre o grafo e constrói o JSON
const buildJsonFromNode = (node, nodes, edges, visited = new Set()) => {
  if (!node) return null;

  // Mecanismo de proteção contra loops infinitos (ciclos no grafo)
  if (visited.has(node.id)) {
    console.error("Ciclo detectado na regra, terminando recursão para o nó:", node.id);
    return { "error": `Ciclo detectado no nó ${node.id}. Verifique as conexões.` };
  }
  visited.add(node.id);

  let result;
  switch (node.type) {
    case 'if': {
      // Encontra as arestas de saída para os ramos THEN e ELSE
      const thenEdge = edges.find(e => e.source === node.id && e.sourceHandle === 'then');
      const elseEdge = edges.find(e => e.source === node.id && e.sourceHandle === 'else');
      // A condição é SOMENTE o que está conectado ao handle 'condition'.
      const conditionEdge = edges.find(e => e.target === node.id && e.targetHandle === 'condition');
      
      const thenNode = thenEdge ? nodes.find(n => n.id === thenEdge.target) : null;
      const elseNode = elseEdge ? nodes.find(n => n.id === elseEdge.target) : null;
      const conditionNode = conditionEdge ? nodes.find(n => n.id === conditionEdge.source) : null;


      // Chama a si mesma recursivamente para cada ramo
      result = {
        "if": [
          buildJsonFromNode(conditionNode, nodes, edges, visited),
          buildJsonFromNode(thenNode, nodes, edges, visited),
          buildJsonFromNode(elseNode, nodes, edges, visited)
        ]
      };
      break;
    }
    case 'and':
    case 'or': {
      // Encontra as duas arestas de entrada
      const edgeA = edges.find(e => e.target === node.id && e.targetHandle === 'a');
      const edgeB = edges.find(e => e.target === node.id && e.targetHandle === 'b');
      const nodeA = edgeA ? nodes.find(n => n.id === edgeA.source) : null;
      const nodeB = edgeB ? nodes.find(n => n.id === edgeB.source) : null;

      result = { 
        [node.type]: [
          buildJsonFromNode(nodeA, nodes, edges, visited),
          buildJsonFromNode(nodeB, nodes, edges, visited)
        ] 
      };
      break;
    }
    case 'comparison': {
      const { field, operator, value } = node.data;
      result = (!field || !operator || value === undefined) ? null : { [operator]: [{ "var": field }, value] };
      break;
    }
    case 'var': {
      const { field: varField } = node.data;
      result = varField ? { "var": varField } : null;
      break;
    }
    case 'result': {
      result = node.data.value;
      break;
    }
    default:
      result = null;
  }

  // Libera o nó do set de 'visitados' ao sair de sua ramificação.
  // Isso permite que o mesmo nó seja parte de caminhos diferentes, mas não de um ciclo.
  visited.delete(node.id);
  return result;
};

// Função principal que inicia a tradução
export const graphToJsonLogic = (nodes, edges) => {
  // A lógica de encontrar o nó raiz: é um 'if' que não é resultado de um 'then' ou 'else' de outro 'if'.
  // Esta é uma heurística robusta para encontrar o início da cadeia de decisão principal.
  const rootNode = nodes.find(n => 
    n.type === 'if' && 
    !edges.some(e => e.target === n.id && (e.sourceHandle === 'then' || e.sourceHandle === 'else'))
  );

  if (!rootNode) {
    // Se a heurística falhar, pega o primeiro 'if' como fallback.
    const fallbackRoot = nodes.find(n => n.type === 'if');
    if (!fallbackRoot) {
      return { "error": "Adicione um 'Bloco IF' para iniciar a regra." };
    }
    return buildJsonFromNode(fallbackRoot, nodes, edges, new Set());
  }
  
  return buildJsonFromNode(rootNode, nodes, edges, new Set());
};

function formatCondition(condition) {
  if (!condition || typeof condition !== 'object') return '<em>condição incompleta</em>';

  const operator = Object.keys(condition)[0];
  if (!operator) return '<em>condição vazia</em>';

  // Caso 1: Operadores lógicos (AND/OR)
  if (operator === 'and' || operator === 'or') {
    const subConditions = condition[operator];
    if (!Array.isArray(subConditions)) return '<em>bloco lógico malformado</em>';

    // Formata cada sub-condição recursivamente e as une com o operador
    const formattedSubs = subConditions
      .map(sub => formatCondition(sub))
      .join(` <strong>${operator.toUpperCase()}</strong> `);
    
    return `(${formattedSubs})`;
  }

  // Caso 2: Operador VAR
  if (operator === 'var') {
    return `<strong>${condition[operator]}</strong> é verdadeiro`;
  }

  // Caso 3: Operadores de Comparação (==, <, >=, etc.)
  const args = condition[operator];
  if (!Array.isArray(args) || args.length < 1) return '<em>argumentos inválidos</em>';
  
  // O primeiro argumento é sempre a variável
  const field = args[0]?.var;
  
  // O segundo argumento é o valor a ser comparado
  let value = args[1];
  if (typeof value === 'string') {
    value = `"${value}"`;
  } else if (value === null) {
    value = 'nulo';
  } else if (value === undefined) {
    // Se o valor for undefined, a condição está incompleta
    return `<strong>${field || 'campo'} ${operator} ...</strong>`;
  }

  return `<strong>${field || ''} ${operator} ${value}</strong>`;
}

export const generateExplanationSteps = (rule) => {
  const steps = [];
  let stepCounter = 1;

  function recurse(currentRule, level = 0, path = '') {
    if (typeof currentRule === 'string') {
      steps.push({ 
        text: `${path} o resultado final é <strong>"${currentRule}"</strong> e o processo termina.`,
        level 
      });
      return;
    }
    if (currentRule === null || currentRule === undefined) {
        steps.push({
            text: `${path} nenhum passo é definido e o processo termina.`,
            level
        });
        return;
    }
    if (currentRule && currentRule.if) {
      if (!Array.isArray(currentRule.if)) {
        steps.push({ text: 'Erro: Bloco "if" malformado.', level });
        return;
      }
      
      const [condition, thenBranch, elseBranch] = currentRule.if;
      
      if (!condition) {
          steps.push({ text: "Um bloco 'SE' não possui uma condição conectada.", level });
          return;
      }

      const conditionText = formatCondition(condition);
      steps.push({ 
        text: `${stepCounter}. Avalia-se a condição: ${conditionText}?`, 
        level
      });
      stepCounter++;
      if (thenBranch !== undefined) recurse(thenBranch, level + 1, '↳ Se <strong>SIM</strong>,');
      if (elseBranch !== undefined) recurse(elseBranch, level + 1, '↳ Se <strong>NÃO</strong>,');
    }
  }

  recurse(rule);
  return steps;
};