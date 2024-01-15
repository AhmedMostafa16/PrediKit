import { BaseNode } from './BaseNode';
import { PropertiesBase } from './PropertiesBase';

export interface JoinNode extends BaseNode {
  data: JoinNodeDataModel;
}

interface JoinNodeDataModel extends PropertiesBase {
  joinType: JoinType;
}

export enum JoinType {
  INNER = 'INNER',
  LEFT = 'LEFT',
  RIGHT = 'RIGHT',
  // FULL = 'FULL',
  // CROSS = 'CROSS',
}
