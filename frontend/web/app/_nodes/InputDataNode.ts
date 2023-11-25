import { BaseNode } from "./BaseNode";

export interface InputDataNode extends BaseNode {
  data: InputDataNodeDataModel;
}

interface InputDataNodeDataModel {
  file: File | undefined;
}
