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
  Viewport,
} from 'reactflow';
import agent from '@/api/agent';
import { EdgeDto, NodeDto, UpdateWorkflowDto, Workflow } from '@/models/Workflow';

export type FlowState = {
  nodes: Node[];
  edges: Edge[];
  viewPort: Viewport;
  title: string;
  description: string;
  workflows: Workflow[];
  currentWorkflowId: string;
  columnNames: string[];

  loadWorkflows: () => void;
  loadWorkflow: (id: string) => void;
  loadColumnNames: () => void;
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: OnConnect;
  addNode: (node: Node) => void;
  updateNodeData: (nodeId: string, data: object) => void;
  setNodes: (nodes: Node[]) => void;
  setEdges: (edges: Edge[]) => void;
  setViewport: (viewport: Viewport) => void;
  updateWorkflow: (id: string) => void;
  setCurrentWorkflowId: (id: string) => void;
};

const useFlowStore = create<FlowState>((set, get) => ({
  workflows: [],
  nodes: [],
  edges: [],
  viewPort: {
    x: 0,
    y: 0,
    zoom: 1,
  },
  title: '',
  description: '',
  currentWorkflowId: '',
  fileType: '',
  columnNames: [],

  loadWorkflows: async () => {
    try {
      const response = await agent.Workflows.list();
      console.log('Workflows:', response);
      set({ workflows: response });
      // set((state) => ({ ...state, workflows: response }))
    } catch (error) {
      console.error('Error loading workflows:', error);
    }
  },
  loadWorkflow: async (id: string) => {
    try {
      const workflow = await agent.Workflows.details(id);
      set({
        nodes: workflow.nodes,
        edges: workflow.edges,
        viewPort: workflow.viewport,
        title: workflow.title,
        description: workflow.description,
      });
    } catch (error) {
      console.error('Error loading workflow:', error);
    }
  },
  loadColumnNames: async () => {
    if (!get().currentWorkflowId) return;

    await agent.Workflows.listColumnNames(get().currentWorkflowId)
      .then((response) => {
        console.log('Column names:', response);
        set({ columnNames: response });
      })
      .catch((error) => {
        console.error('Error loading column names:', error);
      })
      .finally(() => {
        console.log('Column names loaded');
      });
  },
  updateWorkflow: async (id: string) => {
    const { nodes } = get();
    const { edges } = get();

    const sortNodesByEdges = () => {
      const sortedNodes: Node[] = [];
      const visited: { [id: string]: boolean } = {};

      const dfs = (nodeId: string) => {
        visited[nodeId] = true;
        const node = nodes.find((n) => n.id === nodeId);
        if (node) {
          sortedNodes.push(node);
          const connectedEdges = edges.filter((e) => e.source === nodeId || e.target === nodeId);
          connectedEdges.forEach((edge) => {
            const nextNodeId = edge.source === nodeId ? edge.target : edge.source;
            if (!visited[nextNodeId]) {
              dfs(nextNodeId);
            }
          });
        }
      };

      nodes.forEach((node) => {
        if (!visited[node.id]) {
          dfs(node.id);
        }
      });

      return sortedNodes;
    };

    const workflow: UpdateWorkflowDto = {
      id,
      nodes: sortNodesByEdges().map(
        (node): NodeDto => ({
          id: node.id,
          type: node.type!,
          position: node.position,
          positionAbsolute: node.positionAbsolute ?? { x: 0, y: 0 },
          data: node.data,
        })
      ),
      edges: edges.map(
        (edge): EdgeDto => ({
          id: edge.id,
          source: edge.source,
          target: edge.target,
          sourceHandle: edge.sourceHandle!,
          targetHandle: edge.targetHandle!,
          animated: edge.animated ?? false,
        })
      ),
      viewPort: get().viewPort,
      title: get().title,
      description: get().description,
      modifiedOn: new Date().toUTCString(),
    };
    console.log('Updating workflow:', workflow);
    try {
      await agent.Workflows.update(workflow);
    } catch (error) {
      console.error('Error updating workflow:', error);
    }
  },
  setCurrentWorkflowId: (id: string) => {
    console.log('Setting current workflow id:', id);
    set({ currentWorkflowId: id });
  },
  setNodes: (nodes: Node[]) => {
    set({ nodes });
  },
  setEdges: (edges: Edge[]) => {
    set({ edges });
  },
  setViewport: (viewPort: Viewport) => {
    set({ viewPort });
  },
  onNodesChange: (changes: NodeChange[]) => {
    set({
      nodes: applyNodeChanges(changes, get().nodes),
    });
    // get().updateWorkflow(get().currentWorkflowId);
  },
  onEdgesChange: (changes: EdgeChange[]) => {
    set({
      edges: applyEdgeChanges(changes, get().edges),
    });
    // get().updateWorkflow(get().currentWorkflowId);
  },
  onConnect: (connection: Connection) => {
    set({
      edges: addEdge(connection, get().edges),
    });
    // get().updateWorkflow(get().currentWorkflowId);
  },
  addNode: (node: Node) => {
    set({
      nodes: [...get().nodes, node],
    });
    // get().updateWorkflow(get().currentWorkflowId);
  },
  updateNodeData: (nodeId: string, data: object) => {
    const nodes = [...get().nodes];
    const nodeIndex = nodes.findIndex((node) => node.id === nodeId);
    if (nodeIndex !== -1) {
      const node = { ...nodes[nodeIndex] };
      node.data = { ...node.data, ...data };
      nodes[nodeIndex] = node;
      set({ nodes });
      // get().updateWorkflow(get().currentWorkflowId);
    }
  },
}));

export default useFlowStore;
