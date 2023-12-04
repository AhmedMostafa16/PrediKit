import { Operator } from "../_utils/Operator";
import { BaseNode } from "./BaseNode";

export interface FilterNode extends BaseNode {
  data: FilterNodeDataModel;
}

interface FilterNodeDataModel {
  columnName: string;
  operator: Operator | undefined;
  value: string;
}
