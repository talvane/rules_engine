import React, { useState } from 'react';
import { useFields } from './contexts/FieldsContext'; // Importa o hook para adicionar campos

function AddFieldForm() {
    const { addNewField } = useFields(); // Pega a função do contexto
    const [name, setName] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if(name.trim()) {
            addNewField(name.trim());
            setName('');
        }
    }
    return (
        <form onSubmit={handleSubmit} className="sidebar-form">
            <input type="text" placeholder="Nome do novo campo" value={name} onChange={(e) => setName(e.target.value)} />
            <button type="submit">Adicionar</button>
        </form>
    );
}

export default ({ addNode }) => {
  return (
    <aside className="sidebar">
      <h3>Caixa de Ferramentas</h3>
      <p>Adicione e conecte os nós na área de construção.</p>
      <h4>Adicionar Campo Customizado</h4>
      <AddFieldForm />
      <hr/>
      <h4>Adicionar Bloco de Lógica</h4>
      <button onClick={() => addNode('if')}>Adicionar Bloco IF</button>
      <button onClick={() => addNode('comparison')}>Adicionar Comparação</button>
      <button onClick={() => addNode('and')}>Adicionar Bloco AND</button>
      <button onClick={() => addNode('or')}>Adicionar Bloco OR</button>
      <button onClick={() => addNode('var')}>Adicionar Bloco VAR</button>
      <hr/>
      <h4>Adicionar Resultado</h4>
      <button onClick={() => addNode('result', 'APROVADO')}>Resultado: APROVADO</button>
      <button onClick={() => addNode('result', 'RECUSADO')}>Resultado: RECUSADO</button>
      <button onClick={() => addNode('result', 'ANALISE_MANUAL')}>Resultado: ANÁLISE MANUAL</button>
    </aside>
  );
};