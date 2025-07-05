import React, { useState } from 'react';
import { DndContext } from '@dnd-kit/core';
import Toolbox from './Toolbox';
import RuleNode from './RuleNode';
import JsonOutput from './JsonOutput';
import ErrorBoundary from './ErrorBoundary';
import {
  generateId,
  findNodeAndReplace,
  findNodeAndUpdateProperty,
  generateJsonLogic,
  findNodeById
} from './utils';
import './App.css';

// Função auxiliar para criar uma nova regra 'IF' vazia
const createNewRule = () => ({
  id: generateId(),
  type: 'if',
  condition: null,
  then: null,
  else: null,
});

function App() {
  const [processingRule, setProcessingRule] = useState(createNewRule());
  const [validationRules, setValidationRules] = useState([]);
  const [customFields, setCustomFields] = useState([]);
  const [customValues, setCustomValues] = useState([]);

  const handleAddField = (fieldName) => {
    if (fieldName && !customFields.some(f => f.value === fieldName)) {
      const newField = { id: `custom-field-${fieldName}`, type: 'field', value: fieldName };
      setCustomFields(prev => [...prev, newField]);
    }
  };

  const handleAddValue = (valueString) => {
    if (valueString.trim() === '') return;
    let parsedValue;
    if (!isNaN(parseFloat(valueString)) && isFinite(valueString)) parsedValue = parseFloat(valueString);
    else if (valueString.toLowerCase() === 'true') parsedValue = true;
    else if (valueString.toLowerCase() === 'false') parsedValue = false;
    else if (valueString.toLowerCase() === 'null') parsedValue = null;
    else parsedValue = valueString;

    if (!customValues.some(v => v.value === parsedValue)) {
      const newValue = { id: `custom-value-${String(parsedValue)}`, type: 'static_value', value: parsedValue };
      setCustomValues(prev => [...prev, newValue]);
    }
  };

  const addValidationRule = () => {
    setValidationRules(current => [...current, createNewRule()]);
  };

  const removeValidationRule = (indexToRemove) => {
    setValidationRules(current => current.filter((_, index) => index !== indexToRemove));
  };

  function handleDragEnd(event) {
    const { active, over } = event;
    if (!over || !over.id) return;

    const draggedItem = active.data.current;
    const [_, ruleTypeOrId, targetNodeId, slotName] = over.id.split('-');
    
    // --- LÓGICA DE ATUALIZAÇÃO PARA A REGRA DE PROCESSAMENTO ---
    if (ruleTypeOrId === 'processing') {
      const targetNode = findNodeById(processingRule, targetNodeId);
      if (!targetNode) return;
      // Reutiliza a lógica de atualização passando o setProcessingRule
      updateRule(draggedItem, targetNode, targetNodeId, slotName, setProcessingRule);
    }
    
    // --- LÓGICA DE ATUALIZAÇÃO PARA AS REGRAS DE VALIDAÇÃO ---
    if (ruleTypeOrId.startsWith('validation')) {
      const validationIndex = parseInt(ruleTypeOrId.split('_')[1], 10);
      if (isNaN(validationIndex)) return;

      const ruleToUpdate = validationRules[validationIndex];
      const targetNode = findNodeById(ruleToUpdate, targetNodeId);
      if (!targetNode) return;

      // Cria uma função de atualização específica para este item da lista
      const updateSpecificValidationRule = (updateFn) => {
        const newValidationRules = [...validationRules];
        newValidationRules[validationIndex] = updateFn(ruleToUpdate);
        setValidationRules(newValidationRules);
      };

      updateRule(draggedItem, targetNode, targetNodeId, slotName, updateSpecificValidationRule);
    }
  }

  // Função genérica que contém a lógica de como uma regra deve ser atualizada
  function updateRule(draggedItem, targetNode, targetNodeId, slotName, stateUpdater) {
    const draggedType = draggedItem.type;
    const draggedValue = draggedItem.value;
    const targetType = targetNode.type;

    if (['if', 'and', 'comparison'].includes(draggedType)) {
      let newNode;
      if (draggedType === 'if') newNode = { id: generateId(), type: 'if', condition: null, then: null, else: null };
      if (draggedType === 'and') newNode = { id: generateId(), type: 'and', conditions: [null, null] };
      if (draggedType === 'comparison') newNode = { id: generateId(), type: 'comparison', field: null, operator: null, value: null };
      stateUpdater(current => findNodeAndReplace(current, targetNodeId, slotName, newNode));
    } else if (draggedType === 'static_value' && targetType === 'if' && (slotName === 'then' || slotName === 'else')) {
      const newNode = { id: generateId(), type: 'static_value', value: draggedValue };
      stateUpdater(current => findNodeAndReplace(current, targetNodeId, slotName, newNode));
    } else if (targetType === 'comparison') {
      const isValidPropertyDrop = (draggedType === 'field' && slotName === 'field') || (draggedType === 'operator' && slotName === 'operator') || (draggedType === 'static_value' && slotName === 'value');
      if (isValidPropertyDrop) {
        stateUpdater(current => findNodeAndUpdateProperty(current, targetNodeId, slotName, draggedValue));
      }
    } else if (draggedType === 'field' && targetType !== 'comparison') {
      const newComparisonNode = { id: generateId(), type: 'comparison', field: draggedValue, operator: null, value: null };
      stateUpdater(current => findNodeAndReplace(current, targetNodeId, slotName, newComparisonNode));
    }
  }

  const finalProcessingJson = generateJsonLogic(processingRule);
  const finalValidationJson = validationRules.map(generateJsonLogic);

  return (
    <ErrorBoundary>
      <DndContext onDragEnd={handleDragEnd}>
        <div className="App">
          <header className="App-header">
            <h1>Construtor de Regras Completo</h1>
          </header>
          <main className="dnd-container">
            <Toolbox customFields={customFields} customValues={customValues} onAddField={handleAddField} onAddValue={handleAddValue} />
            <div className="canvas-and-output">
              <div className="canvas">
                <div className="canvas-header">
                  <h2>Regras de Validação</h2>
                  <button onClick={addValidationRule}>+ Adicionar Regra de Validação</button>
                </div>
                {validationRules.map((rule, index) => (
                  <div key={rule.id} className="rule-container">
                    <RuleNode node={rule} ruleId={`validation_${index}`} />
                    <button onClick={() => removeValidationRule(index)} className="remove-btn">Remover</button>
                  </div>
                ))}
              </div>

              <div className="canvas">
                <h2>Regra de Processamento</h2>
                <RuleNode node={processingRule} ruleId="processing" />
              </div>

              <JsonOutput processingRule={finalProcessingJson} validationRules={finalValidationJson} />
            </div>
          </main>
        </div>
      </DndContext>
    </ErrorBoundary>
  );
}

export default App;