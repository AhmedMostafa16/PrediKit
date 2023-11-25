import { Connection, Node } from "reactflow";
import { Color } from "../_utils/Color";
import { FormField } from "../_components/FormBuilder/FormBuilder";

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
