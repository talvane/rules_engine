import React, { useState, useCallback, useRef } from 'react';
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

import Sidebar from './Sidebar';
import ErrorBoundary from './ErrorBoundary';
import IfNode from './nodes/IfNode';
import ComparisonNode from './nodes/ComparisonNode';
import ResultNode from './nodes/ResultNode';
import JsonOutput from './JsonOutput';
import TrashCan from './TrashCan';
import { graphToJsonLogic } from './utils';
import './App.css';

let id = 0;
const getId = () => `node_${id++}`;

const nodeTypes = {
  if: IfNode,
  comparison: ComparisonNode,
  result: ResultNode,
};

const App = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [generatedJson, setGeneratedJson] = useState({});
  const [availableFields, setAvailableFields] = useState([
    { value: 'pontuacao_credito', label: 'Pontuação Crédito' },
    { value: 'renda_mensal', label: 'Renda Mensal' },
    { value: 'possui_divida_ativa', label: 'Possui Dívida Ativa' },
  ]);

  const trashCanRef = useRef(null);
  const [isDraggingOverTrash, setIsDraggingOverTrash] = useState(false);

  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  const deleteNode = useCallback((idToDelete) => {
    // Remove o nó com o ID fornecido
    setNodes((nds) => nds.filter((node) => node.id !== idToDelete));
    // Remove todas as arestas conectadas a esse nó
    setEdges((eds) => eds.filter((edge) => edge.source !== idToDelete && edge.target !== idToDelete));
  }, [setNodes, setEdges]);

  // Evento que dispara continuamente enquanto um nó é arrastado
  const onNodeDrag = (event, node) => {
    if (!trashCanRef.current) return;
    const trashCanBounds = trashCanRef.current.getBoundingClientRect();
    const { clientX, clientY } = event;

    // Verifica se o mouse está sobre a lixeira e atualiza o estado
    const isOver = clientX >= trashCanBounds.left &&
                   clientX <= trashCanBounds.right &&
                   clientY >= trashCanBounds.top &&
                   clientY <= trashCanBounds.bottom;
    setIsDraggingOverTrash(isOver);
  };

  // Evento que dispara quando o usuário solta o nó
  const onNodeDragStop = (event, node) => {
    // Se o nó foi solto sobre a lixeira, delete-o
    if (isDraggingOverTrash) {
      deleteNode(node.id);
    }
    // Reseta o estado visual da lixeira
    setIsDraggingOverTrash(false);
  };

  const handleAddNewField = (newFieldName) => {
    if (newFieldName && !availableFields.some(f => f.value === newFieldName)) {
      setAvailableFields(prev => [...prev, { value: newFieldName, label: newFieldName }]);
    }
  };

  const updateNodeData = (nodeId, newData) => {
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === nodeId) {
          // Substitui o objeto data para garantir consistência
          return { ...node, data: newData };
        }
        return node;
      })
    );
  };

  const addNode = (type, value = '') => {
    const newNode = {
      id: getId(),
      type,
      position: { x: 150 + Math.random() * 300, y: 50 + Math.random() * 150 },
      data: {
        value: value,
        onUpdate: updateNodeData,
        availableFields: availableFields, // Passa a lista de campos para o nó
      },
    };
    setNodes((nds) => nds.concat(newNode));
  };

  const handleGenerateJson = () => {
    const jsonResult = graphToJsonLogic(nodes, edges);
    setGeneratedJson(jsonResult);
  };

  return (
    <ErrorBoundary>
      <div className="app-container">
        <ReactFlowProvider>
          <Sidebar addNode={addNode} onAddNewField={handleAddNewField} />
          <div className="reactflow-wrapper">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              nodeTypes={nodeTypes}
              onNodeDrag={onNodeDrag}
              onNodeDragStop={onNodeDragStop}
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
          </div>
        </ReactFlowProvider>
      </div>
    </ErrorBoundary>
  );
};

export default App;