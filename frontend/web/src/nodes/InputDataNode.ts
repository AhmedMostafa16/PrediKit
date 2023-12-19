import { BaseNode } from './BaseNode';
import { PropertiesBase } from './PropertiesBase';

export interface InputDataNode extends BaseNode {
  data: InputDataNodeDataModel;
}

interface InputDataNodeDataModel extends PropertiesBase {
  file?: string;
  // ToDo uncomment whenever you decide to switch from passing
  // a file path to a BytesIO Object
  // extension?: string;
}
