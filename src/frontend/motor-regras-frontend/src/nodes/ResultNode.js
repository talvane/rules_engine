import React from 'react';
import { Handle, Position } from 'reactflow';

const ResultNode = ({ data }) => (
  <div className="react-flow-node result-node">
    <div className="handle-label left" title="Recebe o fluxo de uma regra">Entrada</div>
    <Handle type="target" position={Position.Left} className="handle-target" />
    <div className="node-content">
      <strong>Resultado:</strong> {data.value}
    </div>
  </div>
);

export default ResultNode;