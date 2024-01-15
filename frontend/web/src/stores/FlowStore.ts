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

export type FlowState = {
  nodes: Node[];
  edges: Edge[];
  workflows: Workflow[];
  currentWorkflowId: string;
  currentWorkflow?: Workflow;
  columnNames: string[];
  viewPort: Viewport;

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
  executeWorkflow: () => void;
};

const useFlowStore = create<FlowState>((set, get) => ({
  workflows: [],
  nodes: [],
  edges: [],
  currentWorkflowId: '',
  currentWorkflow: undefined,
  fileType: '',
  columnNames: [],
  viewPort: {
    zoom: 1,
    x: 0,
    y: 0,
  },

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
        currentWorkflow: workflow,
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
    const { nodes, edges, currentWorkflow, viewPort } = get();

    if (!currentWorkflow) return;

    function sortNodesByEdges() {
      const sortedNodes: Node[] = [];
      const visited: { [id: string]: boolean } = {};

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
          const connectedEdges = edges.filter((e) => e.source === nodeId || e.target === nodeId);
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

    function scheduleTasks(): string[] {
      const result: string[] = [];
      const visited: { [key: string]: boolean } = {};

      const visitNode = (nodeId: string) => {
        if (!visited[nodeId]) {
          visited[nodeId] = true;

          const edgesFromNode = edges.filter((edge) => edge.source === nodeId);

          edgesFromNode.forEach((edge) => {
            visitNode(edge.target);
          });

          result.push(nodeId);
        }
      };

      nodes.forEach((node) => {
        visitNode(node.id);
      });
      return result.reverse(); // Reverse the result to get the correct order
    }

    console.log('Scheduled tasks:', scheduleTasks());

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
      viewPort,
      title: currentWorkflow.title,
      description: currentWorkflow.description,
      modifiedOn: new Date().toUTCString(),
    };
    console.log('Updating workflow:', workflow);
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
  // EXPERIMENTAL
  executeWorkflow: async () => {
    const { currentWorkflowId, updateWorkflow } = get();
    // Update workflow
    updateWorkflow(currentWorkflowId);

    // Extract paths from the graph
    function extractPaths(nodes: Node[], edges: Edge[]): Path[] {
      // Filter out start nodes that do not have any outgoing edges
      const startNodes = nodes.filter((node) => !edges.find((edge) => edge.target === node.id));
      const paths: Path[] = [];

      // Recursive function to traverse the graph and create paths
      function traverse(currentPath: Path): void {
        const lastNode = currentPath.nodes[currentPath.nodes.length - 1];
        const outgoingEdges = edges.filter((edge) => edge.source === lastNode.id);

        // If there are no outgoing edges, add the current path to the list of paths
        if (outgoingEdges.length === 0) {
          paths.push(currentPath);
          return;
        }

        // Traverse each outgoing edge and create a new path
        for (const edge of outgoingEdges) {
          const nextNode = nodes.find((node) => node.id === edge.target);
          if (nextNode) {
            const nextPath: Path = {
              nodes: [...currentPath.nodes, nextNode],
              edges: [...currentPath.edges, edge],
            };
            traverse(nextPath);
          }
        }
      }

      // Traverse each start node and create an initial path
      for (const startNode of startNodes) {
        const initialPath: Path = {
          nodes: [startNode],
          edges: [],
        };
        traverse(initialPath);
      }

      return paths;
    }

    // Execute paths
    const { nodes, edges } = get();
    const paths = extractPaths(nodes, edges);
    console.log('Paths:', paths);

    await agent.Workflows.executePaths(currentWorkflowId, paths)
      .then(() => {
        console.log('Workflow executed');
        notifications.show({
          title: 'Workflow executed',
          message: 'Workflow executed successfully',
          color: 'green',
        });
      })
      .catch((error) => {
        console.error('Error executing workflow:', error);
        notifications.show({
          title: 'Error executing workflow',
          message: error.message,
          color: 'red',
          autoClose: false,
        });
      })
      .finally(() => {
        console.log('Workflow execution finished');
      });
  },
}));

export default useFlowStore;
