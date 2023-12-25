import agent from '@/api/agent';
import { EdgeDto, NodeDto, UpdateWorkflowDto, Workflow } from '@/models/Workflow';
import { Path } from '@/types/Path';
import { notifications } from '@mantine/notifications';
import { makeAutoObservable, runInAction } from 'mobx';
import {
  Node,
  Edge,
  Viewport,
  NodeChange,
  applyEdgeChanges,
  applyNodeChanges,
  EdgeChange,
  Connection,
  addEdge,
} from 'reactflow';

export default class WorkflowStore {
  nodes: Node[] = [];
  edges: Edge[] = [];
  workflows: Workflow[] = [];
  currentWorkflowId?: string;
  currentWorkflow?: Workflow;
  columnNames: string[] = [];
  viewPort: Viewport = {
    zoom: 1,
    x: 0,
    y: 0,
  };

  constructor() {
    makeAutoObservable(this);
  }

  loadWorkflows = async () => {
    try {
      const workflows = await agent.Workflows.list();
      runInAction(() => {
        this.workflows = workflows;
      });
    } catch (error) {
      console.log(error);
    }
  };

  loadWorkflow = async (id: string) => {
    try {
      const workflow = await agent.Workflows.details(id);
      runInAction(() => {
        this.nodes = workflow.nodes;
        this.edges = workflow.edges;
        this.currentWorkflow = workflow;
      });
    } catch (error) {
      console.log(error);
    }
  };

  loadColumnNames = async () => {
    if (!this.currentWorkflowId) return;

    await agent.Workflows.listColumnNames(this.currentWorkflowId)
      .then((response) => {
        runInAction(() => {
          this.columnNames = [];
          this.columnNames = response;
        });
      })
      .catch((error) => {
        runInAction(() => {
          this.columnNames = [];
        });
        console.error('Error loading column names:', error);
      })
      .finally(() => {
        console.log('Column names loaded');
      });
  };

  updateWorkflow = async (id: string) => {
    const { nodes, edges, currentWorkflow, viewPort } = this;

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
  };

  setViewPort = (viewPort: Viewport) => {
    this.viewPort = viewPort;
  };

  setCurrentWorkflowId = (id: string) => {
    console.log('Setting current workflow id:', id);
    runInAction(() => {
      this.currentWorkflowId = id;
    });
  };

  setNodes = (nodes: Node[]) => {
    runInAction(() => {
      this.nodes = nodes;
    });
  };

  setEdges = (edges: Edge[]) => {
    runInAction(() => {
      this.edges = edges;
    });
  };

  onNodesChange = (changes: NodeChange[]) => {
    runInAction(() => {
      this.nodes = applyNodeChanges(changes, this.nodes);
    });
  };

  onEdgesChange = (changes: EdgeChange[]) => {
    runInAction(() => {
      this.edges = applyEdgeChanges(changes, this.edges);
    });
  };

  onConnect = (connection: Connection) => {
    runInAction(() => {
      this.edges = addEdge(connection, this.edges);
    });
  };

  addNode = (node: Node) => {
    runInAction(() => {
      this.nodes.push(node);
    });
  };

  updateNodeData = (nodeId: string, data: object) => {
    const nodeIndex = this.nodes.findIndex((node) => node.id === nodeId);
    if (nodeIndex !== -1) {
      const updatedNode = {
        ...this.nodes[nodeIndex],
        data: { ...this.nodes[nodeIndex].data, ...data },
      };
      runInAction(() => {
        this.nodes[nodeIndex] = updatedNode;
      });
    }
  };

  // EXPERIMENTAL
  exportWorkflow = async (id: string) => {
    const { currentWorkflowId, updateWorkflow } = this;
    // Update workflow
    if (!currentWorkflowId) return;
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
    const { nodes, edges } = this;
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
  };
}
