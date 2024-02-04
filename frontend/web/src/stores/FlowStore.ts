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
import { notifications } from '@mantine/notifications';
import agent from '@/api/agent';
import { EdgeDto, NodeDto, UpdateWorkflowDto, Workflow } from '@/models/Workflow';
import { Path } from '@/types/Path';
import { IDictionary } from '@/interfaces/IDictionary';

export type FlowState = {
  nodes: Node[];
  edges: Edge[];
  workflows: Workflow[];
  currentWorkflowId: string;
  currentWorkflow?: Workflow;
  selectedNode: Node | null;
  columnNames: string[];
  viewPort: Viewport;
  isExecuting: boolean;

  loadWorkflows: () => Promise<void>;
  loadWorkflow: (id: string) => Promise<void>;
  loadColumnNames: () => void;
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: OnConnect;
  addNode: (node: Node) => void;
  updateNodeData: (nodeId: string, data: object) => void;
  setNodes: (nodes: Node[]) => void;
  setEdges: (edges: Edge[]) => void;
  setViewport: (viewport: Viewport) => void;
  setSelectedNode: (id: Node | null) => void;
  updateWorkflow: (id: string) => Promise<void>;
  setCurrentWorkflowId: (id: string) => void;
  executeWorkflow: () => Promise<void>;
};

const useFlowStore = create<FlowState>((set, get) => ({
  workflows: [],
  nodes: [],
  edges: [],
  currentWorkflowId: '',
  currentWorkflow: undefined,
  selectedNode: null,
  fileType: '',
  columnNames: [],
  viewPort: {
    zoom: 1,
    x: 0,
    y: 0,
  },
  isExecuting: false,

  loadWorkflows: async (): Promise<void> => {
    try {
      const response = await agent.Workflows.list();
      console.debug('Workflows:', response);
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
        currentWorkflow: workflow,
        currentWorkflowId: id,
        viewPort: workflow.viewPort ?? get().viewPort,
      });
    } catch (error) {
      console.error('Error loading workflow:', error);
    }
  },
  loadColumnNames: async () => {
    if (!get().currentWorkflowId) return;

    await agent.Workflows.listColumnNames(get().currentWorkflowId)
      .then((response) => {
        console.debug('Column names:', response);
        set({ columnNames: response });
      })
      .catch((error) => {
        console.error('Error loading column names:', error);
      })
      .finally(() => {
        console.debug('Column names loaded');
      });
  },
  updateWorkflow: async (id: string) => {
    const { nodes, edges, currentWorkflow, viewPort } = get();

    if (!currentWorkflow) return;

    function sortNodesByEdges() {
      const sortedNodes: Node[] = [];
      const visited: { [id: string]: boolean } = {};
      const localEdges: Edge[] = edges.reverse();

      // Depth-first search to traverse the nodes
      function dfs(nodeId: string) {
        // Mark the current node as visited
        visited[nodeId] = true;

        // Find the node with the given nodeId
        const node = nodes.find((n) => n.id === nodeId);

        // If the node is found
        if (node) {
          // Add the node to the sortedNodes array
          sortedNodes.push(node);
          // Find all edges connected to the current node
          const connectedEdges = localEdges.filter(
            (e) => e.source === nodeId || e.target === nodeId
          );
          // Traverse each connected edge
          connectedEdges.forEach((edge) => {
            // Determine the next node in the edge
            const nextNodeId = edge.source === nodeId ? edge.target : edge.source;
            // If the next node has not been visited, recursively call dfs on it
            if (!visited[nextNodeId]) {
              dfs(nextNodeId);
            }
          });
        }
      }

      nodes.forEach((node) => {
        if (!visited[node.id]) {
          dfs(node.id);
        }
      });

      return sortedNodes;
    }

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
        })
      ),
      viewPort,
      title: currentWorkflow.title,
      description: currentWorkflow.description,
      modifiedOn: new Date().toUTCString(),
    };
    console.debug('Updating workflow:', workflow);
    await agent.Workflows.update(workflow).catch((error) => {
      console.error('Error updating workflow:', error);
      notifications.show({
        title: 'Error updating workflow',
        message: error.message,
        color: 'red',
        autoClose: false,
      });
    });
  },
  setCurrentWorkflowId: (id: string) => {
    console.debug('Setting current workflow id:', id);
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
  setSelectedNode: (node: Node | null) => {
    set({ selectedNode: node });
  },
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
  updateNodeData: (nodeId: string, data: any) => {
    const nodes = get().nodes;
    const nodeIndex: number = nodes.findIndex((node) => node.id == nodeId);
    if (nodeIndex !== -1) {
      const node = { ...nodes[nodeIndex] };
      node.data = { ...node.data, ...data };
      nodes[nodeIndex] = node;
      set({ nodes });
    }
  },

  // EXPERIMENTAL
  executeWorkflow: async () => {
    const { currentWorkflowId, updateWorkflow, nodes, edges } = get();
    // Update workflow
    await updateWorkflow(currentWorkflowId);

    set({ isExecuting: true });

    // Extract paths from the graph
    async function extractPaths(): Promise<string[][]> {
      const result: string[][] = [];
      const visited: { [key: string]: boolean } = {};
      const localEdges: Edge[] = edges.reverse();

      // Depth-first search to traverse the nodes
      const visitNode = (nodeId: string) => {
        if (!visited[nodeId]) {
          visited[nodeId] = true;

          // Find all edges connected to the current node
          const edgesFromNode = localEdges.filter((edge) => edge.source === nodeId);

          edgesFromNode.forEach((edge) => {
            visitNode(edge.target);
          });

          result[result.length - 1].push(nodeId);
        }
      };

      nodes.forEach((node) => {
        if (!visited[node.id]) {
          result.push([]);
          visitNode(node.id);
        }
      });

      result.forEach((path) => path.reverse());

      return result;
    }

    const paths = await extractPaths();

    console.debug('Extracted paths: ', paths);

    // Get dependencies for a node
    async function getDependencies(): Promise<IDictionary> {
      const dependencies: IDictionary = {};

      edges.forEach((edge) => {
        const sourceId = edge.source;
        const targetId = edge.target;

        // Check if the target node is already in the dictionary, if not, add it
        if (!dependencies[targetId]) {
          dependencies[targetId] = [];
        }

        // Add the source node as a dependency for the target node
        dependencies[targetId].push(sourceId);
      });

      return dependencies;
    }

    const dependencies = await getDependencies();

    console.debug('Dependencies: ', dependencies);

    // Set all edges to animated
    set({ edges: edges.map((edge) => ({ ...edge, animated: true })) });

    // Execute paths
    await agent.Workflows.execute(currentWorkflowId, paths, nodes, dependencies)
      .then(() => {
        set({ isExecuting: false });

        console.debug('Workflow executed');
        notifications.show({
          title: 'Workflow executed',
          message: 'Workflow executed successfully',
          color: 'green',
          autoClose: 5000,
        });
      })
      .catch((error) => {
        set({ isExecuting: false });

        console.error('Error executing workflow:', error);
        notifications.show({
          title: 'Error executing workflow',
          message: error.message,
          color: 'red',
          autoClose: false,
        });
      })
      .finally(() => {
        console.debug('Workflow execution finished');
      });
  },
}));

export default useFlowStore;
