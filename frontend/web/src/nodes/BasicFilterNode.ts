import { Operator } from '../types/Operator';
import { BaseNode } from './BaseNode';
import { PropertiesBase } from './PropertiesBase';

export interface BasicFilterNode extends BaseNode {
  data: BasicFilterNodeDataModel;
}

interface BasicFilterNodeDataModel extends PropertiesBase {
  column: string;
  operator: Operator | undefined;
  value: string;
  caseSensitive: boolean;
}
