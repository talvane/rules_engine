import React, { useRef, useState, useCallback } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  MiniMap,
} from 'reactflow';
import 'reactflow/dist/style.css';

import { FieldsProvider } from './contexts/FieldsContext';
import { useFlowBuilder } from './hooks/useFlowBuilder';
import Sidebar from './Sidebar';
import ErrorBoundary from './ErrorBoundary';
import IfNode from './nodes/IfNode';
import ComparisonNode from './nodes/ComparisonNode';
import ResultNode from './nodes/ResultNode';
import VarNode from './nodes/VarNode';
import AndNode from './nodes/AndNode';
import OrNode from './nodes/OrNode';
import JsonOutput from './JsonOutput';
import TrashCan from './TrashCan'; // Importa a lixeira
import Explanation from './Explanation';
import './App.css';

const nodeTypes = {
  if: IfNode, comparison: ComparisonNode, result: ResultNode,
  var: VarNode, and: AndNode, or: OrNode,
};

// Este componente interno agora conterá toda a lógica de fluxo e da lixeira.
const FlowBuilder = () => {
  const {
    nodes, edges, generatedJson,
    onNodesChange, onEdgesChange, onConnect,
    addNode, deleteNode, handleGenerateJson
  } = useFlowBuilder();
  
  // --- LÓGICA DA LIXEIRA REINTRODUZIDA AQUI ---
  const trashCanRef = useRef(null);
  const [isDraggingOverTrash, setIsDraggingOverTrash] = useState(false);

  const onNodeDrag = (event, node) => {
    if (!trashCanRef.current) return;
    const trashCanBounds = trashCanRef.current.getBoundingClientRect();
    // Usa as coordenadas do mouse do evento para precisão
    const { clientX, clientY } = event;

    const isOver = clientX >= trashCanBounds.left && clientX <= trashCanBounds.right &&
                   clientY >= trashCanBounds.top && clientY <= trashCanBounds.bottom;
    
    // Atualiza o estado para dar um feedback visual se o nó está sobre a lixeira
    setIsDraggingOverTrash(isOver);
  };
  
  const onNodeDragStop = (event, node) => {
    // Se o arraste terminou sobre a lixeira, chama a função de deletar
    if (isDraggingOverTrash) {
      deleteNode(node.id);
    }
    // Reseta o estado visual da lixeira
    setIsDraggingOverTrash(false);
  };

  return (
    <div className="app-container">
      {/* O Sidebar não precisa da função de adicionar campo, pois ela é pega do contexto */}
      <Sidebar addNode={addNode} />
      <div className="reactflow-wrapper">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          onNodeDrag={onNodeDrag}         // <-- Evento de arrastar re-adicionado
          onNodeDragStop={onNodeDragStop} // <-- Evento de parar de arrastar re-adicionado
          fitView
        >
          <Background />
          <Controls />
          <MiniMap />
        </ReactFlow>
        <TrashCan ref={trashCanRef} isOver={isDraggingOverTrash} />
      </div>
      <div className="json-output-container">
        <button onClick={handleGenerateJson} className="generate-button">Gerar JSON da Regra</button>
        <JsonOutput generatedJson={generatedJson} />
        <Explanation generatedJson={generatedJson} />
      </div>
    </div>
  );
}

// O componente App principal agora apenas monta os Providers de contexto.
const App = () => {
  return (
    <ErrorBoundary>
      <FieldsProvider>
        <ReactFlowProvider>
          <FlowBuilder />
        </ReactFlowProvider>
      </FieldsProvider>
    </ErrorBoundary>
  );
};

export default App;