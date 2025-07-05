import React, { useState } from 'react';
import { useDraggable } from '@dnd-kit/core';

// Componente Draggable (arrastável) reutilizável
function Draggable({ id, data, children }) {
  const { attributes, listeners, setNodeRef } = useDraggable({ id, data });
  return (
    <div ref={setNodeRef} {...listeners} {...attributes} className="toolbox-item">
      {children}
    </div>
  );
}

// Formulário para adicionar um item customizado
function AddItemForm({ onAdd, label, placeholder }) {
    const [value, setValue] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if(value) {
            onAdd(value);
            setValue('');
        }
    }
    return (
        <form onSubmit={handleSubmit} className="add-item-form">
            <input 
                type="text" 
                placeholder={placeholder}
                value={value}
                onChange={(e) => setValue(e.target.value)}
            />
            <button type="submit">{label}</button>
        </form>
    );
}


function Toolbox({ customFields, customValues, onAddField, onAddValue }) {
  return (
    <div className="toolbox">
      <h3>Blocos de Lógica</h3>
      
      <h4>Estrutura</h4>
      <Draggable id="drag-if" data={{ type: 'if' }}>Bloco IF/THEN/ELSE</Draggable>
      <Draggable id="drag-and" data={{ type: 'and' }}>Bloco Lógico (AND)</Draggable>
      {/* ADICIONADO DE VOLTA */}
      <Draggable id="drag-comparison" data={{ type: 'comparison' }}>Bloco de Comparação</Draggable>
      
      <hr />

      {/* SEÇÃO DE CAMPOS DINÂMICOS */}
      <h4>Campos</h4>
      <AddItemForm onAdd={onAddField} label="Adicionar Campo" placeholder="Ex: idade_cliente"/>
      <div className="toolbox-section">
        <Draggable id="drag-field-score" data={{ type: 'field', value: 'pontuacao_credito' }}>Pontuação Crédito</Draggable>
        <Draggable id="drag-field-debt" data={{ type: 'field', value: 'possui_divida_ativa' }}>Possui Dívida Ativa</Draggable>
        {customFields.map(field => (
            <Draggable key={field.id} id={field.id} data={field}>
                {field.value}
            </Draggable>
        ))}
      </div>
      
      <hr />
      
      {/* SEÇÃO DE OPERADORES ATUALIZADA */}
      <h4>Operadores</h4>
      <div className="toolbox-section">
        <Draggable id="drag-op-eq" data={{ type: 'operator', value: '==' }}>== (Igual)</Draggable>
        <Draggable id="drag-op-neq" data={{ type: 'operator', value: '!=' }}>!= (Diferente)</Draggable>
        <Draggable id="drag-op-gt" data={{ type: 'operator', value: '>' }}>&gt; (Maior que)</Draggable>
        <Draggable id="drag-op-lt" data={{ type: 'operator', value: '<' }}>&lt; (Menor que)</Draggable>
        <Draggable id="drag-op-gte" data={{ type: 'operator', value: '>=' }}>&gt;= (Maior ou Igual)</Draggable>
        <Draggable id="drag-op-lte" data={{ type: 'operator', value: '<=' }}>&lt;= (Menor ou Igual)</Draggable>
      </div>

      <hr />

      {/* SEÇÃO DE VALORES DINÂMICOS */}
      <h4>Valores</h4>
      <AddItemForm onAdd={onAddValue} label="Adicionar Valor" placeholder="Ex: 1000, true, 'ATIVO'"/>
      <div className="toolbox-section">
        <Draggable id="drag-val-750" data={{ type: 'static_value', value: 750 }}>Valor: 750</Draggable>
        <Draggable id="drag-val-false" data={{ type: 'static_value', value: false }}>Valor: Falso</Draggable>
        {customValues.map(val => (
            <Draggable key={val.id} id={val.id} data={val}>
                Valor: {String(val.value)}
            </Draggable>
        ))}
      </div>

      <hr />

      <h4>Resultados</h4>
      <Draggable id="drag-res-approved" data={{ type: 'static_value', value: 'APROVADO' }}>Resultado: APROVADO</Draggable>
      <Draggable id="drag-res-rejected" data={{ type: 'static_value', value: 'RECUSADO' }}>Resultado: RECUSADO</Draggable>
      <Draggable id="drag-res-manual" data={{ type: 'static_value', value: 'ANALISE_MANUAL' }}>Resultado: ANÁLISE MANUAL</Draggable>
    </div>
  );
}

export default Toolbox;