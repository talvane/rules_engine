import React, { memo } from 'react';
import { Handle, Position } from 'reactflow';

const parseInputValue = (valueString) => {
  if (typeof valueString !== 'string') return valueString;
  
  // Substitui a vírgula por ponto para o parse de números
  const trimmed = valueString.trim().replace(',', '.');
  if (trimmed === '') return undefined;

  const num = Number(trimmed);
  if (!isNaN(num) && trimmed !== '') return num;

  if (valueString.toLowerCase() === 'true') return true;
  if (valueString.toLowerCase() === 'false') return false;
  if (valueString.toLowerCase() === 'null') return null;
  
  return valueString;
};

export default memo(({ data, id }) => {

  const handleChange = (evt) => {
    const { name, value } = evt.target;
    
    const newData = { ...data, [name]: value };

    // Limpa os campos dependentes ao trocar o campo principal
    if (name === 'field') {
      newData.operator = '';
      newData.value = '';
    }

    // Processa o valor se ele foi alterado
    if (name === 'value') {
      newData.value = parseInputValue(value);
    }
    
    data.onUpdate(id, newData);
  };

  return (
    <div className="react-flow-node comparison-node">
      <Handle type="target" position={Position.Left} />
      <div className="node-header">Bloco de Comparação</div>
      <div className="node-content">
        <select name="field" value={data.field || ''} onChange={handleChange}>
          <option value="" disabled>Selecione Campo</option>
          {data.availableFields && data.availableFields.map(field => (
            <option key={field.value} value={field.value}>{field.label}</option>
          ))}
        </select>
        
        <select name="operator" value={data.operator || ''} onChange={handleChange}>
            <option value="" disabled>Operador</option>
            <option value="==">== (Igual)</option>
            <option value="!=">!= (Diferente)</option>
            <option value=">">&gt; (Maior)</option>
            <option value="<">&lt; (Menor)</option>
            <option value=">=">&gt;= (Maior ou Igual)</option>
            <option value="<=">&lt;= (Menor ou Igual)</option>
        </select>
        <input 
          type="text" 
          name="value"
          placeholder="Valor"
          value={data.value ?? ''}
          onChange={handleChange}
        />
      </div>
      <Handle type="source" position={Position.Right} id="source" />
    </div>
  );
});