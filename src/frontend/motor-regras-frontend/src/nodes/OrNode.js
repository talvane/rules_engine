import React from 'react';
import { Handle, Position } from 'reactflow';

export default () => {
  return (
    <div className="react-flow-node logical-node or-node">
      <div className="handle-label left-a" title="Entrada para a primeira condição">Entrada A</div>
      <div className="handle-label left-b" title="Entrada para a segunda condição">Entrada B</div>
      <Handle type="target" id="a" position={Position.Left} style={{ top: '33%' }} className="handle-target" />
      <Handle type="target" id="b" position={Position.Left} style={{ top: '66%' }} className="handle-target" />
      
      <div className="node-header">OU (OR)</div>
      
      <div className="handle-label right" title="Saída com o resultado da lógica OR">Saída</div>
      <Handle type="source" position={Position.Right} className="handle-source" />
    </div>
  );
};