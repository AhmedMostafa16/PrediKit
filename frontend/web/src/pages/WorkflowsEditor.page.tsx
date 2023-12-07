import React, { useCallback, useRef, useState } from 'react';
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
} from 'reactflow';
import { shallow } from 'zustand/shallow';
import { IconDeviceFloppy } from '@tabler/icons-react';
import { FormField } from '@/components/FormBuilder/FormBuilder';
import { NodeSidebar } from '@/components/NodesSidebar/NodesSidebar';
import { PropertiesSidebar } from '@/components/PropertiesSidebar/PropertiesSidebar';
import useFlowStore, { FlowState } from '@/stores/FlowStore';
import { nodeTypesProps, nodeTypes } from '@/types/NodeTypes';
import 'reactflow/dist/style.css';

const proOptions = { hideAttribution: true };
const defaultViewport: Viewport = { x: 0, y: 0, zoom: 1.0 };

let id: number = 0;
const getId: (nodeType: string) => string = (nodeType: string): string => {
  const newId = `${nodeType}_${(id += 1)}`;
  return newId;
};
const selector = (state: FlowState) => ({
  nodes: state.nodes,
  edges: state.edges,
  onNodesChange: state.onNodesChange,
  onEdgesChange: state.onEdgesChange,
  onConnect: state.onConnect,
  addNode: state.addNode,
  updateNodeData: state.updateNodeData,
});

export default function Workflow() {
  const reactFlowWrapper: React.MutableRefObject<HTMLDivElement | null> = useRef(null);

  const { nodes, edges, onNodesChange, onEdgesChange, onConnect, addNode, updateNodeData } =
    useFlowStore(selector, shallow);

  const [reactFlowInstance, setReactFlowInstance] = useState<ReactFlowInstance>();
  const [fields, setFields] = useState<FormField[]>([]);
  const [currentNode, setCurrentNode] = useState<Node | null>(null);
  const [showPropertiesSidebar, setShowPropertiesSidebar] = useState<boolean>(false);

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
        id: getId(node.nodeType),
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

      const uielements = nodeTypesProps[node.type as keyof typeof nodeTypesProps].formFields;

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

      return !hasCycle(target);
    },
    [nodes, edges]
  );

  const onSave = useCallback(() => {
    if (reactFlowInstance) {
      const flow = JSON.stringify(reactFlowInstance.toObject());
      localStorage.setItem('flow', flow);
      // console.log(flow);
    }
  }, [reactFlowInstance]);

  return (
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
            isValidConnection={isValidConnection}
            nodesDraggable
            zoomOnDoubleClick
            elementsSelectable
          >
            <Background gap={32} />

            <MiniMap style={{ background: 'var(--mantine-color-default)' }} />
            <Controls>
              <ControlButton onClick={onSave}>
                <IconDeviceFloppy size={12} stroke={1} />
              </ControlButton>
            </Controls>
          </ReactFlow>
        </div>
        {showPropertiesSidebar && (
          <PropertiesSidebar fields={fields} node={currentNode!} onAutoSubmit={handleAutoSubmit} />
        )}
      </ReactFlowProvider>
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
