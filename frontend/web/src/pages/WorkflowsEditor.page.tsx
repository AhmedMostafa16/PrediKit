import React, { useCallback, useEffect, useRef, useState } from 'react';
import ReactFlow, {
  Connection,
  Background,
  Controls,
  MiniMap,
  Node,
  ReactFlowProvider,
  XYPosition,
  ReactFlowInstance,
  Viewport,
  getOutgoers,
  ControlButton,
  getIncomers,
  ProOptions,
  Edge,
  DefaultEdgeOptions,
  ConnectionMode,
} from 'reactflow';
import { shallow } from 'zustand/shallow';
import { IconDeviceFloppy } from '@tabler/icons-react';
import { v4 as uuidv4 } from 'uuid';
import { FormField } from '@/components/FormBuilder/FormBuilder';
import { NodeSidebar } from '@/components/NodesSidebar/NodesSidebar';
import { PropertiesSidebar } from '@/components/PropertiesSidebar/PropertiesSidebar';
import useFlowStore, { FlowState } from '@/stores/FlowStore';
import { nodeTypesProps, nodeTypes } from '@/types/NodeTypes';
import 'reactflow/dist/style.css';
import EditorHeader from '@/components/EditorHeader/EditorHeader';
import { useSignalRStore } from '@/stores/SignalrStore';
import { useNavigate } from 'react-router-dom';
import { UpdateEdgesNotificationDto } from '@/models/UpdateEdgesNotificationDto';
import { Color } from '@/types/Color';
import { useMantineColorScheme, useMantineTheme } from '@mantine/core';
import signalrService from '@/services/signalrService';

const proOptions: ProOptions = { hideAttribution: true };
const defaultViewport: Viewport = { x: 0, y: 0, zoom: 1.0 };

const selector = (state: FlowState) => ({
  nodes: state.nodes,
  edges: state.edges,
  currentWorkflowId: state.currentWorkflowId,
  selectedNode: state.selectedNode,
  onNodesChange: state.onNodesChange,
  onEdgesChange: state.onEdgesChange,
  onConnect: state.onConnect,
  addNode: state.addNode,
  updateNodeData: state.updateNodeData,
  setNodes: state.setNodes,
  setEdges: state.setEdges,
  setViewport: state.setViewport,
  setSelectedNode: state.setSelectedNode,
  updateWorkflow: state.updateWorkflow,
});

export default function Workflow() {
  const reactFlowWrapper: React.MutableRefObject<HTMLDivElement | null> = useRef(null);

  const {
    nodes,
    edges,
    currentWorkflowId,
    selectedNode,
    onNodesChange,
    onEdgesChange,
    onConnect,
    addNode,
    updateNodeData,
    setNodes,
    setEdges,
    setViewport,
    setSelectedNode,
    updateWorkflow,
  } = useFlowStore(selector, shallow);

  const navigate = useNavigate();
  const theme = useMantineTheme();
  const { colorScheme } = useMantineColorScheme();

  const [reactFlowInstance, setReactFlowInstance] = useState<ReactFlowInstance>();
  const [fields, setFields] = useState<FormField[]>([]);
  const [currentNode, setCurrentNode] = useState<Node | null>(null);
  const [showPropertiesSidebar, setShowPropertiesSidebar] = useState<boolean>(false);

  const autosave = useCallback(async () => {
    await updateWorkflow(currentWorkflowId);
    console.debug('Autosaving...');
  }, []);


  useEffect(() => {
    if (currentWorkflowId === null) navigate('/workflows');
    const { events } = signalrService();

    events((notification) => {
      const edgeIndex: number = edges.findIndex((edge) => edge.target == notification.nodeId);
      if (edgeIndex != -1) {
        const edge = { ...edges[edgeIndex] };
        edge.animated = false;
        edges[edgeIndex] = edge;
        useFlowStore.setState({ edges });
      }
    });

    // Autosave every 1000ms
    let timeoutId: NodeJS.Timeout | null = null;

    const handleAutosave = () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }

      timeoutId = setTimeout(autosave, 1000);
    };

    handleAutosave();

    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [nodes, edges, autosave, navigate, signalrService]);

  const onDragOver = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();

      const node = JSON.parse(event.dataTransfer.getData('application/reactflow'));

      // check if the dropped element is valid
      if (typeof node === 'undefined' || !node || !reactFlowInstance || !reactFlowWrapper.current) {
        return;
      }
      const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();

      const position: XYPosition = reactFlowInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      const newNode: Node = {
        id: uuidv4(),
        type: node.nodeType,
        position,
        data: node.data,
      };

      addNode(newNode);
    },
    [addNode, reactFlowInstance]
  );

  const onNodeClick = useCallback(
    (event: React.MouseEvent, node: Node) => {
      event.preventDefault();

      // check if the dropped element is valid
      if (typeof node === 'undefined' || !node || !node.type || typeof node.data === 'undefined') {
        return;
      }

      const nodeProps = nodeTypesProps[node.type as keyof typeof nodeTypesProps];

      const uielements = nodeProps.formFields;

      setFields(uielements);
      // console.log(node.data);
      setCurrentNode(node);
      setShowPropertiesSidebar(true);
    },
    [setCurrentNode]
  );

  const handleAutoSubmit = (formData: { [key: string]: unknown }) => {
    updateNodeData(currentNode!.id, formData);
    // console.log(nodes);
  };

  const isValidConnection = useCallback(
    (connection: Connection) => {
      if (connection.source === connection.target) return false;

      const target = nodes.find((node: Node) => node.id === connection.target);
      if (!target) return false;
      const hasCycle = (node: Node, visited = new Set()) => {
        if (visited.has(node.id)) return false;

        visited.add(node.id);

        for (const outgoer of getOutgoers(node, nodes, edges)) {
          if (outgoer.id === connection.source) return true;
          if (hasCycle(outgoer, visited)) return true;
        }

        return false;
      };

      const targetProps = nodeTypesProps[target.type as keyof typeof nodeTypesProps];

      const hasMultipleSources =
        getIncomers(target, nodes, edges).length > targetProps.inputHandles.length - 1;

      return !hasCycle(target) && !hasMultipleSources;
    },
    [nodes, edges]
  );

  const onSave = useCallback(() => {
    if (reactFlowInstance) {
      const flow = JSON.stringify(reactFlowInstance.toObject());
      localStorage.setItem('flow', flow);
      console.debug(flow);
    }
  }, [reactFlowInstance]);

  const onRestore = useCallback(() => {
    const restoreFlow = async () => {
      const json = localStorage.getItem('flow');
      if (!json) return;
      const flow = JSON.parse(json);

      if (flow) {
        const { x = 0, y = 0, zoom = 1 } = flow.viewport;
        setNodes(flow.nodes || []);
        setEdges(flow.edges || []);
        setViewport({ x, y, zoom });
      }
    };

    restoreFlow();
  }, [setNodes, setViewport]);

  const onEdgeUpdate = useCallback(
    (oldEdge: Edge, newConnection: Connection) => {
      const newEdge: Edge = {
        id: oldEdge.id,
        source: newConnection.source ?? '',
        target: newConnection.target ?? '',
        sourceHandle: newConnection.sourceHandle ?? '',
        targetHandle: newConnection.targetHandle ?? '',
      };
      // update the old edge with the new connection
      const newEdges = edges.map((edge) => (edge.id === oldEdge.id ? newEdge : edge));

      setEdges(newEdges);
    },
    [setEdges, edges]
  );

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        width: '100%',
      }}
    >
      <EditorHeader />

      <div className="dndflow" style={{ height: '100vh', width: '100%' }}>
        <ReactFlowProvider>
          <NodeSidebar />

          <div className="reactflow-wrapper" ref={reactFlowWrapper}>
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              nodeTypes={nodeTypes}
              proOptions={proOptions}
              onInit={setReactFlowInstance}
              defaultViewport={defaultViewport}
              onDragOver={onDragOver}
              onDrop={onDrop}
              onNodeClick={onNodeClick}
              onPaneClick={() => setShowPropertiesSidebar(false)}
              onEdgeUpdate={onEdgeUpdate}
              isValidConnection={isValidConnection}
              connectionMode={ConnectionMode.Loose}
              nodesDraggable
              zoomOnDoubleClick
              elementsSelectable
              deleteKeyCode={'Delete'}
            >
              <Background
                gap={32}
                style={{
                  backgroundColor:
                    colorScheme === 'dark' ? theme.colors.dark[7] : theme.colors.gray[0],
                }}
              />

              <MiniMap
                style={{ background: 'var(--mantine-color-default)' }}
                nodeColor={(node) => {
                  switch (node.type) {
                    case 'inputDataNode':
                      return theme.colors.teal[5];
                    case 'outputDataNode':
                      return theme.colors.teal[5];
                    case 'basicFilterNode':
                      return theme.colors.blue[5];
                    case 'dataCleaningNode':
                      return theme.colors.blue[5];
                    case 'joinNode':
                      return theme.colors.violet[5];
                    default:
                      return theme.colors.gray[5];
                  }
                }}
              />
              <Controls>
                {process.env.NODE_ENV === 'development' && (
                  <>
                    <ControlButton
                      onClick={async () => {
                        onSave();
                        await updateWorkflow(currentWorkflowId);
                      }}
                      title="Save"
                    >
                      <IconDeviceFloppy size={12} stroke={1} />
                    </ControlButton>
                    <ControlButton onClick={onRestore} title="Restore">
                      <IconDeviceFloppy size={12} stroke={1} />
                    </ControlButton>
                  </>
                )}
              </Controls>
            </ReactFlow>
          </div>
          {showPropertiesSidebar && (
            <PropertiesSidebar
              fields={fields}
              node={currentNode!}
              onAutoSubmit={handleAutoSubmit}
            />
          )}
        </ReactFlowProvider>
      </div>
    </div>
  );

  /*   return (
    <ReactFlowProvider>
      <AppShell>
        <AppShell.Navbar>
          <NodeSidebar />
        </AppShell.Navbar>
        {showPropertiesSidebar && (
          <AppShell.Aside>
            <PropertiesSidebar
              fields={fields}
              node={currentNode!}
              onAutoSubmit={handleAutoSubmit}
            />
          </AppShell.Aside>
        )}
        <AppShell.Main >
          <div
            className="reactflow-wrapper"
            ref={reactFlowWrapper}
            style={{ height: '100vh', width: '100%'}}
          >
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              nodeTypes={nodeTypes}
              proOptions={proOptions}
              onInit={setReactFlowInstance}
              defaultViewport={defaultViewport}
              onDragOver={onDragOver}
              onDrop={onDrop}
              onNodeClick={onNodeClick}
              onPaneClick={() => setShowPropertiesSidebar(false)}
              isValidConnection={isValidConnection}
              nodesDraggable
              zoomOnDoubleClick
              elementsSelectable
            >
              <Background gap={32} />

              <MiniMap style={{ background: 'var(--mantine-color-default)' }} />
              <Controls>
                <ControlButton onClick={onSave}>
                  <IconDeviceFloppy />
                </ControlButton>
              </Controls>
            </ReactFlow>
          </div>
        </AppShell.Main>

      </AppShell>
    </ReactFlowProvider>
  ); */
}
