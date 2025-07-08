import { useState, useCallback } from 'react';
import { addEdge, useNodesState, useEdgesState } from 'reactflow';
import { graphToJsonLogic } from '../utils';

let id = 0;
const getId = () => `node_${id++}`;

export const useFlowBuilder = (availableFields) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [generatedJson, setGeneratedJson] = useState({});

  const onConnect = useCallback((params) => {
    const sourceNode = nodes.find(n => n.id === params.source);
    const targetNode = nodes.find(n => n.id === params.target);

    // Validação de Conexão
    if (sourceNode?.type === 'result') return;
    if (targetNode?.type === 'if' && params.targetHandle === 'condition' && sourceNode?.type === 'result') return;

    setEdges((eds) => addEdge(params, eds));
  }, [setEdges, nodes]);

  const updateNodeData = useCallback((nodeId, newData) => {
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === nodeId) {
          return { ...node, data: newData };
        }
        return node;
      })
    );
  }, [setNodes]);

  const addNode = (type, value = '') => {
    const newNode = {
      id: getId(),
      type,
      position: { x: 250, y: 50 + (nodes.length % 10) * 50 },
      data: {
        value: value,
        onUpdate: updateNodeData,
        availableFields: availableFields, // Usa os campos recebidos
      },
    };
    setNodes((nds) => nds.concat(newNode));
  };

  const deleteNode = useCallback((idToDelete) => {
    setNodes((nds) => nds.filter((node) => node.id !== idToDelete));
    setEdges((eds) => eds.filter((edge) => edge.source !== idToDelete && edge.target !== idToDelete));
  }, [setNodes, setEdges]);
  
  const handleGenerateJson = () => {
    const jsonResult = graphToJsonLogic(nodes, edges);
    setGeneratedJson(jsonResult);
  };

  const setFlow = useCallback(({ nodes, edges }) => {
    setNodes(nodes);
    setEdges(edges);
  }, [setNodes, setEdges]);

  return {
    nodes, edges, generatedJson,
    onNodesChange, onEdgesChange, onConnect,
    addNode, deleteNode, handleGenerateJson,
    setFlow, updateNodeData
  };
};