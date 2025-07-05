// src/utils.js

// Gera um ID único para cada nó
let nextId = 0;
export const generateId = () => `node_${nextId++}`;

// Função recursiva para encontrar e atualizar um nó na árvore de estado
export const findNodeAndReplace = (node, targetId, slot, newContent) => {
  if (node.id === targetId) {
    // Encontrou o nó correto, cria um novo nó com o conteúdo atualizado
    return { ...node, [slot]: newContent };
  }

  // Se não encontrou, continua a busca nos filhos do nó
  for (const key of Object.keys(node)) {
    if (node[key] && typeof node[key] === 'object') {
      if (Array.isArray(node[key])) {
        // Se for um array de nós (como no 'and')
        const newArray = node[key].map(childNode => 
          findNodeAndReplace(childNode, targetId, slot, newContent)
        );
        if (JSON.stringify(newArray) !== JSON.stringify(node[key])) {
          return { ...node, [key]: newArray };
        }
      } else if (node[key].id) {
        // Se for um único nó filho
        const newNode = findNodeAndReplace(node[key], targetId, slot, newContent);
        if (newNode !== node[key]) {
          return { ...node, [key]: newNode };
        }
      }
    }
  }

  return node; // Retorna o nó original se o alvo não for encontrado nesta ramificação
};

// Função recursiva para converter nossa árvore de estado em JSON Logic puro
export const generateJsonLogic = (node) => {
  if (!node) return null;

  switch (node.type) {
    case 'if':
      return {
        "if": [
          generateJsonLogic(node.condition),
          generateJsonLogic(node.then),
          generateJsonLogic(node.else)
        ]
      };
    case 'and':
      return {
        "and": node.conditions.map(generateJsonLogic)
      };
    case 'comparison':
      const { field, operator, value } = node;
      if (!field || !operator || value === null) return null;
      return { [operator]: [{ "var": field }, value] };
    case 'static_value':
      return node.value;
    default:
      return null;
  }
};

// src/utils.js

// ... (as funções generateId, findNodeAndReplace, generateJsonLogic permanecem aqui em cima) ...

// NOVA FUNÇÃO: Encontra um nó e atualiza uma de suas propriedades
export const findNodeAndUpdateProperty = (node, targetId, property, value) => {
  if (!node) return null;

  if (node.id === targetId) {
    // Encontrou o nó, retorna uma nova versão com a propriedade atualizada
    return { ...node, [property]: value };
  }

  // Busca recursiva nos filhos
  for (const key of Object.keys(node)) {
    if (node[key] && typeof node[key] === 'object') {
      if (Array.isArray(node[key])) {
        const newArray = node[key].map(childNode =>
          findNodeAndUpdateProperty(childNode, targetId, property, value)
        );
        if (JSON.stringify(newArray) !== JSON.stringify(node[key])) {
          return { ...node, [key]: newArray };
        }
      } else if (node[key].id) {
        const newNode = findNodeAndUpdateProperty(node[key], targetId, property, value);
        if (newNode !== node[key]) {
          return { ...node, [key]: newNode };
        }
      }
    }
  }

  return node;
};

export const findNodeById = (node, targetId) => {
  if (!node) return null;
  if (node.id === targetId) return node;

  for (const key of Object.keys(node)) {
    if (node[key] && typeof node[key] === 'object') {
      if (Array.isArray(node[key])) {
        for (const childNode of node[key]) {
          const found = findNodeById(childNode, targetId);
          if (found) return found;
        }
      } else if (node[key].id) {
        const found = findNodeById(node[key], targetId);
        if (found) return found;
      }
    }
  }

  return null;
};