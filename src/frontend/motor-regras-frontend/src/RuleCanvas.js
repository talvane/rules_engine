import React from 'react';
import { useDroppable } from '@dnd-kit/core';

// Componente reutilizável para uma área de soltura (encaixe)
function Droppable({ id, children, hasItem }) {
  const { isOver, setNodeRef } = useDroppable({
    id: id,
  });
  
  const style = {
    backgroundColor: isOver ? '#cce5ff' : (hasItem ? '#e9ecef' : '#f8f9fa'),
    border: `2px dashed ${isOver ? '#007bff' : '#ced4da'}`
  };

  return (
    <div ref={setNodeRef} style={style} className="droppable-slot">
      {children}
    </div>
  );
}

// A área de construção principal
function RuleCanvas({ ruleState }) {
  const { condition } = ruleState;

  return (
    <div className="canvas">
      <h2>Área de Construção de Regra</h2>
      <p>Arraste os blocos da esquerda para os encaixes abaixo para construir a condição de aprovação.</p>

      <div className="rule-template">
        <span className="rule-text">SE (</span>
        <Droppable id="condition-field" hasItem={!!condition.field}>
          {condition.field || 'Campo'}
        </Droppable>
        <Droppable id="condition-operator" hasItem={!!condition.operator}>
          {condition.operator || 'Operador'}
        </Droppable>
        <Droppable id="condition-value" hasItem={condition.value !== null}>
          {condition.value !== null ? condition.value : 'Valor'}
        </Droppable>
        <span className="rule-text"> E <strong>não possui dívida</strong> )</span>
        <span className="rule-text rule-then">ENTÃO</span>
        <div className="outcome approved">APROVADO</div>
      </div>
      <div className="rule-else">
        <span className="rule-text">SENÃO</span>
        <div className="outcome">Lógica Padrão (Recusado / Análise Manual)</div>
      </div>
    </div>
  );
}

export default RuleCanvas;
