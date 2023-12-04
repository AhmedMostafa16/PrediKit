"use client";

import React, { useCallback, useRef, useState } from "react";
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
} from "reactflow";
import "reactflow/dist/style.css";

import { NodeSidebar } from "../_components/NodesSidebar/NodesSidebar";
import { nodeTypes, nodeTypesProps } from "../_nodes/NodeTypes";
import { PropertiesSidebar } from "../_components/PropertiesSidebar/PropertiesSidebar";
import useStore, { RFState } from "../_stores/store";
import { shallow } from "zustand/shallow";
import { FormField } from "../_components/FormBuilder/FormBuilder";

const proOptions = { hideAttribution: true };
const defaultViewport: Viewport = { x: 0, y: 0, zoom: 1.0 };

let id: number = 0;
const getId: (nodeType: string) => string = (nodeType: string): string =>
  `${nodeType}_${id++}`;

const selector = (state: RFState) => ({
  nodes: state.nodes,
  edges: state.edges,
  onNodesChange: state.onNodesChange,
  onEdgesChange: state.onEdgesChange,
  onConnect: state.onConnect,
  addNode: state.addNode,
  updateNodeData: state.updateNodeData,
});

export default function Workflow() {
  const reactFlowWrapper: React.MutableRefObject<any> = useRef();

  const {
    nodes,
    edges,
    onNodesChange,
    onEdgesChange,
    onConnect,
    addNode,
    updateNodeData,
  } = useStore(selector, shallow);

  const [reactFlowInstance, setReactFlowInstance] =
    useState<ReactFlowInstance>();
  const [fields, setFields] = useState<FormField[]>([]);
  const [currentNode, setCurrentNode] = useState<Node | null>(null);
  const [showPropertiesSidebar, setShowPropertiesSidebar] =
    useState<boolean>(false);

  const onDragOver = useCallback((event: any) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();

      const node = JSON.parse(
        event.dataTransfer.getData("application/reactflow"),
      );

      // check if the dropped element is valid
      if (typeof node === "undefined" || !node || !reactFlowInstance) {
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
        position: position,
        data: node.data,
      };

      addNode(newNode);
    },
    [addNode, reactFlowInstance],
  );

  const onNodeClick = useCallback(
    (event: React.MouseEvent, node: Node) => {
      event.preventDefault();

      // check if the dropped element is valid
      if (
        typeof node === "undefined" ||
        !node ||
        !node.type ||
        typeof node.data === "undefined"
      ) {
        return;
      }

      const uielements =
        nodeTypesProps[node.type as keyof typeof nodeTypesProps].formFields;

      setFields(uielements);
      // console.log(node.data);
      setCurrentNode(node);
      setShowPropertiesSidebar(true);
    },
    [setCurrentNode],
  );

  const handleAutoSubmit = (formData: { [key: string]: any }) => {
    updateNodeData(currentNode!.id, formData);
    console.log(nodes);
  };

  const isValidConnection = useCallback(
    (connection: Connection) => {
      const target = nodes.find((node: Node) => node.id === connection.target);
      if (!target) return false;
      const hasCycle = (node: Node, visited = new Set()) => {
        if (visited.has(node.id)) return false;

        visited.add(node.id);

        for (const outgoer of getOutgoers(node, nodes, edges)) {
          if (outgoer.id === connection.source) return true;
          if (hasCycle(outgoer, visited)) return true;
        }
      };

      return !hasCycle(target);
    },
    [nodes, edges],
  );

  return (
    <div className="dndflow">
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

            <MiniMap style={{ background: "var(--mantine-color-default)" }} />
            <Controls />
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
  );
}
