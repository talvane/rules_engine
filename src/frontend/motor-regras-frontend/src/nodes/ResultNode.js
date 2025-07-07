import React from 'react';
import { Handle, Position } from 'reactflow';

export default ({ data }) => (
  <div className="react-flow-node result-node">
    <Handle type="target" position={Position.Left} />
    <div className="node-content">
      <strong>Resultado:</strong> {data.value}
    </div>
  </div>
);