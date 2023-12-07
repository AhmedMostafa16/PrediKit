import { Connection, Node } from 'reactflow';
import { FormField } from '@/components/FormBuilder/FormBuilder';
import { Color } from '@/types/Color';

export interface BaseNode extends Node {
  readonly name: string;
  readonly label: string;
  readonly inputHandles: HandleProperties[];
  readonly outputHandles: HandleProperties[];
  readonly color: Color;
  readonly icon: JSX.Element;
  readonly formFields: FormField[];
}

export type HandleProperties = {
  onConnect?: (connection: Connection) => void;
  isValidConnection?: (connection: Connection) => boolean;
};
