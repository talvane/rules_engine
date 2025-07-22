import React, { useState } from 'react';
import { useFields } from './contexts/FieldsContext'; // Importa o hook para adicionar campos
import AIAnalyzer from './AIAnalyzer';

function AddFieldForm({ addNode }) {
    const { addNewField } = useFields(); // Pega a função do contexto
    const [name, setName] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if(name.trim()) {
            addNewField(name.trim());
            // Adiciona um bloco VAR na tela com o campo criado
            addNode('var', name.trim());
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

function AddBiroForm({ addNode }) {
    const { addNewField } = useFields(); // Pega a função do contexto
    const [name, setName] = useState('');
    const [fieldType, setFieldType] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if(name.trim() && fieldType.trim()) {
            const fieldName = `${name}.${fieldType}`;
            addNewField(fieldName);
            // Adiciona um bloco COMPARISON na tela com o campo criado
            addNode('comparison', fieldName);
            setName('');
            setFieldType('');
        }
    }

    return (
        <form onSubmit={handleSubmit} className="sidebar-form">
            <select value={name} onChange={(e) => setName(e.target.value)}>
                <option value="">Selecione um bureau</option>
                <option value="Serasa">Serasa</option>
                <option value="EmailAge">EmailAge</option>
                <option value="Clearsale">Clearsale</option>
            </select>
            {name && (
                    <select value={fieldType} onChange={(e) => setFieldType(e.target.value)}>
                        <option value="">Selecione o tipo de campo</option>
                        <option value="Nome">Nome</option>
                        <option value="Score">Score</option>
                        <option value="Idade">Idade</option>
                    </select>
            )}
            <button type="submit" disabled={!name || !fieldType}>Adicionar</button>
        </form>
    );
}

function LoadJsonForm({ onLoad }) {
  const [jsonText, setJsonText] = useState('');

  const handleLoad = () => {
    try {
      const parsedJson = JSON.parse(jsonText);
      onLoad(parsedJson);
      setJsonText('');
    } catch (e) {
      alert("JSON inválido! Por favor, verifique a sintaxe.");
      console.error("Erro ao fazer parse do JSON:", e);
    }
  };

  return (
    <div className="sidebar-form-vertical">
      <textarea
        placeholder='Cole o seu JSON de regra aqui...'
        value={jsonText}
        onChange={(e) => setJsonText(e.target.value)}
        rows={6}
      />
      <button onClick={handleLoad}>Carregar Diagrama 🔡</button>
    </div>
  );
}

function LoadIaRule({ onLoadIa }) {
  const [iaText, setIaText] = useState('');

  const handleSubmit = async () => {
    if (iaText.trim()) {
      try {
        const result = await AIAnalyzer.analyzeRule(iaText.trim());
        if (!result || !result.json) {
          throw new Error("Resposta da IA inválida ou sem JSON.");
        }
        
        // Reutiliza a mesma lógica do handleLoad
        onLoadIa(result.json);
        
        setIaText('');
      } catch (error) {
        console.error("Error processing rule with AI:", error);
        alert(`Erro ao processar regra com IA: ${error.message}`);
      }
    }
  };

  return (
    <div className="sidebar-form-vertical">
      <textarea
        placeholder='Descreva a regra que você deseja criar...'
        value={iaText}
        onChange={(e) => setIaText(e.target.value)}
        rows={4}
      />
      <button onClick={handleSubmit}>Gerar Regra 🪄</button>
    </div>
  );
}


const Sidebar = ({ addNode, onLoadJson, onLoadIa }) => {
  return (
    <aside className="sidebar">
      <h3>Caixa de Ferramentas</h3>
      <p>Adicione e conecte os nós na área de construção.</p>
      <h4>Adicionar Campo Customizado</h4>
      <AddFieldForm addNode={addNode} />

      <h4>Adicionar Bureau</h4>
      <AddBiroForm addNode={addNode} />

      <h4>Carregar Regra a Partir de JSON</h4>
      <LoadJsonForm onLoad={onLoadJson} />

      <h4>Criar regra com IA</h4>
      <LoadIaRule onLoadIa={onLoadJson} />

      <h4>Adicionar Bloco de Lógica</h4>
      <button onClick={() => addNode('if')}>Adicionar Bloco IF</button>
      <button onClick={() => addNode('comparison')}>Adicionar Comparação</button>
      <button onClick={() => addNode('and')}>Adicionar Bloco AND</button>
      <button onClick={() => addNode('or')}>Adicionar Bloco OR</button>
      <button onClick={() => addNode('var')}>Adicionar Bloco VAR</button>

      <h4>Adicionar Resultado</h4>
      <button onClick={() => addNode('result', 'APROVADO')}>Resultado: APROVADO</button>
      <button onClick={() => addNode('result', 'RECUSADO')}>Resultado: RECUSADO</button>
      <button onClick={() => addNode('result', 'ANALISE_MANUAL')}>Resultado: ANÁLISE MANUAL</button>
    </aside>
  );
};

export default Sidebar;