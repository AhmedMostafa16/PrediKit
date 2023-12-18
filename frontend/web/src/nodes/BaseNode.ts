import { Connection, OnConnect } from 'reactflow';
import { FormField } from '@/components/FormBuilder/FormBuilder';
import { Color } from '@/types/Color';

// Used as a base class for the factory nodes
export interface BaseNode {
  readonly type: string;
  readonly label: string;
  readonly inputHandles: HandleProperties[];
  readonly outputHandles: HandleProperties[];
  readonly color: Color;
  readonly icon: JSX.Element;
  readonly formFields: FormField[];
  readonly onClick?: (event: React.MouseEvent) => void;
}

export type HandleProperties = {
  onConnect?: OnConnect;
  isValidConnection?: (connection: Connection) => boolean;
};
