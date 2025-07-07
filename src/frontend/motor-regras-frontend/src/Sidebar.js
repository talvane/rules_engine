import React, { useState } from 'react';

function AddFieldForm({ onAdd }) {
    const [name, setName] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if(name.trim()) {
            onAdd(name.trim());
            setName('');
        }
    }
    return (
        <form onSubmit={handleSubmit} className="sidebar-form">
            <input
                type="text"
                placeholder="Nome do novo campo"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <button type="submit">Adicionar</button>
        </form>
    );
}

export default ({ addNode, onAddNewField }) => {
  return (
    <aside className="sidebar">
      <h3>Caixa de Ferramentas</h3>
      <p>Adicione e conecte os nós na área de construção.</p>

      <h4>Adicionar Campo Customizado</h4>
      <AddFieldForm onAdd={onAddNewField} />

      <hr/>

      <h4>Adicionar Bloco de Lógica</h4>
      <button onClick={() => addNode('if')}>Adicionar Bloco IF</button>
      <button onClick={() => addNode('comparison')}>Adicionar Comparação</button>

      <hr/>

      <h4>Adicionar Resultado</h4>
      <button onClick={() => addNode('result', 'APROVADO')}>Resultado: APROVADO</button>
      <button onClick={() => addNode('result', 'RECUSADO')}>Resultado: RECUSADO</button>
      <button onClick={() => addNode('result', 'ANALISE_MANUAL')}>Resultado: ANÁLISE MANUAL</button>
    </aside>
  );
};