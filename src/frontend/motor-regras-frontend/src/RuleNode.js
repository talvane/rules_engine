import React, { memo } from 'react';
import { useDroppable } from '@dnd-kit/core';

function DroppableSlot({ id, children, className = '' }) {
  const { isOver, setNodeRef } = useDroppable({ id });
  const style = {
    backgroundColor: isOver ? '#cce5ff' : 'transparent',
  };
  return <div ref={setNodeRef} style={style} className={`droppable-slot ${className}`}>{children || 'Solte aqui'}</div>;
}

function RuleNode({ node, ruleId }) {
  if (!node) return <div className="node error-node">Nó Inválido</div>;

  switch (node.type) {
    case 'if':
      return (
        <div className="node if-node">
          <div className="if-condition">
            <strong>SE</strong>
            {node.condition ? <RuleNode node={node.condition} ruleId={ruleId}/> : <DroppableSlot id={`droppable-${ruleId}-${node.id}-condition`} />}
          </div>
          <div className="if-then">
            <strong>ENTÃO</strong>
            {node.then ? <RuleNode node={node.then} ruleId={ruleId}/> : <DroppableSlot id={`droppable-${ruleId}-${node.id}-then`} />}
          </div>
          <div className="if-else">
            <strong>SENÃO</strong>
            {node.else ? <RuleNode node={node.else} ruleId={ruleId}/> : <DroppableSlot id={`droppable-${ruleId}-${node.id}-else`} />}
          </div>
        </div>
      );

    case 'and':
      return (
        <div className="node and-node">
          (
            {node.conditions[0] ? <RuleNode node={node.conditions[0]} ruleId={ruleId}/> : <DroppableSlot id={`droppable-${ruleId}-${node.id}-conditions-0`} />}
            <strong>E</strong>
            {node.conditions[1] ? <RuleNode node={node.conditions[1]} ruleId={ruleId}/> : <DroppableSlot id={`droppable-${ruleId}-${node.id}-conditions-1`} />}
          )
        </div>
      );
    
    case 'comparison':
       return (
        <div className="node comparison-node">
            {node.field ? 
                <div className='static-value-node'>{node.field}</div> : 
                <DroppableSlot id={`droppable-${ruleId}-${node.id}-field`}>Campo</DroppableSlot>
            }
            {node.operator ? 
                <div className='static-value-node operator-node'>{node.operator}</div> : 
                <DroppableSlot id={`droppable-${ruleId}-${node.id}-operator`}>Operador</DroppableSlot>
            }
            {node.value !== null && node.value !== undefined ? 
                <div className='static-value-node'>{String(node.value)}</div> : 
                <DroppableSlot id={`droppable-${ruleId}-${node.id}-value`}>Valor</DroppableSlot>
            }
        </div>
       );

    case 'static_value':
      return <div className="node static-value-node result-node">{String(node.value)}</div>;

    default:
      return <div className="node error-node">Tipo de nó desconhecido</div>;
  }
}

export default memo(RuleNode);