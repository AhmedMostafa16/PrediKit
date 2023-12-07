import { create } from 'zustand';
import {
  Connection,
  Edge,
  EdgeChange,
  Node,
  NodeChange,
  addEdge,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
  applyNodeChanges,
  applyEdgeChanges,
} from 'reactflow';

export type FlowState = {
  nodes: Node[];
  edges: Edge[];
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: OnConnect;
  addNode: (node: Node) => void;
  updateNodeData: (nodeId: string, data: object) => void;
};

const useFlowStore = create<FlowState>((set, get) => ({
  nodes: [
    { id: '1', data: { label: 'Node 1' }, position: { x: 100, y: 100 } },
    { id: '2', data: { label: 'Node 2' }, position: { x: 100, y: 200 } },
  ],
  edges: [{ id: 'e1-2', source: '1', target: '2' }],
  onNodesChange: (changes: NodeChange[]) => {
    set({
      nodes: applyNodeChanges(changes, get().nodes),
    });
  },
  onEdgesChange: (changes: EdgeChange[]) => {
    set({
      edges: applyEdgeChanges(changes, get().edges),
    });
  },
  onConnect: (connection: Connection) => {
    set({
      edges: addEdge(connection, get().edges),
    });
  },
  addNode: (node: Node) => {
    set({
      nodes: [...get().nodes, node],
    });
  },
  updateNodeData: (nodeId: string, data: object) => {
    const nodes = [...get().nodes];
    const nodeIndex = nodes.findIndex((node) => node.id === nodeId);
    if (nodeIndex !== -1) {
      const node = { ...nodes[nodeIndex] };
      node.data = { ...node.data, ...data };
      nodes[nodeIndex] = node;
      set({ nodes });
    }
  },
}));

export default useFlowStore;
