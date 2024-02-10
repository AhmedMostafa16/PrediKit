import { Viewport, XYPosition } from 'reactflow';
import { PropertiesBase } from '@/nodes/PropertiesBase';

export interface NodeDto {
  id: string;
  type: string;
  position: XYPosition;
  positionAbsolute: XYPosition;
  data?: PropertiesBase;
}

export interface EdgeDto {
  id: string;
  source: string;
  target: string;
  sourceHandle: string;
  targetHandle: string;
}

export interface CreateWorkflowDto {
  title: string;
  description?: string;
  nodes: NodeDto[];
  edges: EdgeDto[];
  viewPort: Viewport;
  createdOn: string;
  modifiedOn: string;
}

export interface UpdateWorkflowDto {
  id: string;
  title: string;
  description: string;
  nodes: NodeDto[];
  edges: EdgeDto[];
  viewPort: Viewport;
  modifiedOn: string;
}

export interface Workflow {
  id: string;
  title: string;
  description: string;
  nodes: NodeDto[];
  edges: EdgeDto[];
  viewPort: Viewport;
  createdOn: string;
  modifiedOn: string;
}
