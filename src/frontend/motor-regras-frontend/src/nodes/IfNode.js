import React from 'react';
import { Handle, Position } from 'reactflow';

export default () => {
  return (
    <div className="react-flow-node if-node">
      <div className="handle-label top" title="Recebe o resultado de uma lógica (Comparação, AND, etc.)">Condição</div>
      <Handle type="target" id="condition" position={Position.Top} className="handle-target" />
      
      <div className="handle-label left" title="Ponto de entrada quando este 'IF' é o resultado de outro bloco">Entrada</div>
      <Handle type="target" id="entry" position={Position.Left} className="handle-target" />

      <div className="node-header">SE</div>
      
      <div className="node-content">
        <div className="handle-label then-label" title="Saída se a condição for VERDADEIRA">ENTÃO</div>
        <div className="handle-label else-label" title="Saída se a condição for FALSA">SENÃO</div>
      </div>

      <Handle type="source" id="then" position={Position.Bottom} style={{ left: '25%' }} className="handle-source" />
      <Handle type="source" id="else" position={Position.Bottom} style={{ left: '75%' }} className="handle-source" />
    </div>
  );
};