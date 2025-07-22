import React, { memo, useEffect } from 'react';
import { Handle, Position } from 'reactflow';
import { useFields } from '../contexts/FieldsContext';

const parseInputValue = (valueString) => {
  if (typeof valueString !== 'string') return valueString;
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
  const { availableFields } = useFields();

  // Efeito para definir automaticamente o campo quando criado via addBiro
  useEffect(() => {
    // Se há um valor inicial (fieldName do addBiro) e ainda não foi definido um campo
    if (data.value && !data.field && availableFields.some(field => field.value === data.value)) {
      data.onUpdate(id, { ...data, field: data.value, value: '' });
    }
  }, [data, id, availableFields]);

  const handleChange = (evt) => {
    const { name, value } = evt.target;
    const newData = { ...data, [name]: value };
    if (name === 'field') {
      newData.operator = '';
      newData.value = '';
    }
    if (name === 'value') {
      newData.value = parseInputValue(value);
    }
    data.onUpdate(id, newData);
  };

  return (
    <div className="react-flow-node comparison-node">
      <div className="handle-label left" title="Ponto de entrada para aninhamento">Entrada</div>
      <Handle type="target" position={Position.Left} id="entry" className="handle-target" />
      
      <div className="node-header">Bloco de Comparação</div>
      <div className="node-content">
        <select name="field" value={data.field || ''} onChange={handleChange}>
          <option value="" disabled>Selecione Campo</option>
          {availableFields.map(field => (
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
        <input type="text" name="value" placeholder="Valor" value={data.value ?? ''} onChange={handleChange}/>
      </div>

      <div className="handle-label right" title="Fornece o resultado (verdadeiro/falso) da comparação">Saída</div>
      <Handle type="source" position={Position.Right} id="source" className="handle-source" />
    </div>
  );
});