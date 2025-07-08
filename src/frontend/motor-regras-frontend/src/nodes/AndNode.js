import React from 'react';
import { Handle, Position } from 'reactflow';

const AndNode = () => {
  return (
    <div className="react-flow-node logical-node and-node">
      <div className="handle-label left-a" title="Entrada para a primeira condição">Entrada A</div>
      <div className="handle-label left-b" title="Entrada para a segunda condição">Entrada B</div>
      <Handle type="target" id="a" position={Position.Left} style={{ top: '33%' }} className="handle-target" />
      <Handle type="target" id="b" position={Position.Left} style={{ top: '66%' }} className="handle-target" />
      
      <div className="node-header">E (AND)</div>
      
      <div className="handle-label right" title="Saída com o resultado da lógica AND">Saída</div>
      <Handle type="source" position={Position.Right} className="handle-source" />
    </div>
  );
};

export default AndNode;