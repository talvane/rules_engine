import { useState, useCallback } from 'react';
import {
  generateId,
  findNodeAndReplace,
  findNodeAndUpdateProperty,
  findNodeById
} from './utils';

export const useRuleBuilder = (initialState) => {
  const [rule, setRule] = useState(initialState);

  const handleDrop = useCallback((draggedItem, targetNodeId, slotName) => {
    const targetNode = findNodeById(rule, targetNodeId);
    if (!targetNode) return;

    const draggedType = draggedItem.type;
    const draggedValue = draggedItem.value;
    const targetType = targetNode.type;

    // Lógica contextual para manipular a ação de soltar
    if (['if', 'and', 'comparison'].includes(draggedType)) {
      // Caso 1: Arrastando um bloco de estrutura (substitui o encaixe)
      let newNode;
      if (draggedType === 'if') newNode = { id: generateId(), type: 'if', condition: null, then: null, else: null };
      if (draggedType === 'and') newNode = { id: generateId(), type: 'and', conditions: [null, null] };
      if (draggedType === 'comparison') newNode = { id: generateId(), type: 'comparison', field: null, operator: null, value: null };
      setRule(current => findNodeAndReplace(current, targetNodeId, slotName, newNode));
      
    } else if (draggedType === 'static_value') {
      // Caso 2: Arrastando um valor/resultado
      if (targetType === 'if' && (slotName === 'then' || slotName === 'else')) {
        const newNode = { id: generateId(), type: 'static_value', value: draggedValue };
        setRule(current => findNodeAndReplace(current, targetNodeId, slotName, newNode));
      } else if (targetType === 'comparison' && slotName === 'value') {
        setRule(current => findNodeAndUpdateProperty(current, targetNodeId, 'value', draggedValue));
      }

    } else if (draggedType === 'field') {
      // Caso 3: Arrastando um campo
      if (targetType === 'comparison' && slotName === 'field') {
        setRule(current => findNodeAndUpdateProperty(current, targetNodeId, 'field', draggedValue));
      } else if (targetType !== 'comparison') {
        const newComparison = { id: generateId(), type: 'comparison', field: draggedValue, operator: null, value: null };
        setRule(current => findNodeAndReplace(current, targetNodeId, slotName, newComparison));
      }
      
    } else if (draggedType === 'operator') {
      // Caso 4: Arrastando um operador
      if (targetType === 'comparison' && slotName === 'operator') {
        setRule(current => findNodeAndUpdateProperty(current, targetNodeId, 'operator', draggedValue));
      }
    }
  }, [rule]);

  return { rule, setRule, handleDrop };
};