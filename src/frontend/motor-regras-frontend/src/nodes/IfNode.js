import React from 'react';
import { Handle, Position } from 'reactflow';

export default () => (
  <div className="react-flow-node if-node">
    <Handle type="target" id="condition" position={Position.Top} />
    <Handle type="target" id="entry" position={Position.Left} />
    <div className="node-header">SE</div>
    <div className="node-content">
      <div className="handle-label then-label">ENTÃO</div>
      <div className="handle-label else-label">SENÃO</div>
    </div>
    <Handle type="source" id="then" position={Position.Bottom} style={{ left: '25%' }} />
    <Handle type="source" id="else" position={Position.Bottom} style={{ left: '75%' }} />
  </div>
);