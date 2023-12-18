import { BaseNode } from './BaseNode';
import { PropertiesBase } from './PropertiesBase';

export interface InputDataNode extends BaseNode {
  data: InputDataNodeDataModel;
}

interface InputDataNodeDataModel extends PropertiesBase {
  file?: string;
  extension?: string;
}
