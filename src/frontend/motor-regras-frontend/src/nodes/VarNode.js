import React, { memo } from 'react';
import { Handle, Position } from 'reactflow';
import { useFields } from '../contexts/FieldsContext';

export default memo(({ data, id }) => {
  const { availableFields } = useFields();
  const handleChange = (evt) => {
    data.onUpdate(id, { ...data, field: evt.target.value, availableFields });
  };

  return (
    <div className="react-flow-node var-node">
      <div className="handle-label left" title="Ponto de entrada para aninhamento">Entrada</div>
      <Handle type="target" position={Position.Left} className="handle-target" />
      <div className="node-header">Variável (VAR)</div>
      <div className="node-content">
        <select name="field" value={data.field || ''} onChange={handleChange}>
          <option value="" disabled>Selecione um Campo</option>
          {availableFields.map(field => (
            <option key={field.value} value={field.value}>{field.label}</option>
          ))}
        </select>
      </div>
      <div className="handle-label right" title="Saída com o valor da variável">Saída</div>
      <Handle type="source" position={Position.Right} className="handle-source" />
    </div>
  );
});