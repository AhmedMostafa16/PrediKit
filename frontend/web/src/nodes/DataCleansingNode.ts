import { BaseNode } from './BaseNode';

export interface DataCleansingNode extends BaseNode {
  data: DataCleansingNodeDataModel;
}

interface DataCleansingNodeDataModel {
  removeNullData: boolean;
  removeNullRows: boolean;
  selectedColumns: string[];
  replaceNullBlank: boolean;
  replaceNullNumbers: boolean;
  trim: boolean;
  removeWhitespace: boolean;
  removeAllWhitespace: boolean;
  removeLetters: boolean;
  removeNumbers: boolean;
  removePunctuation: boolean;
  modifyCase: ModifyCase | null;
}

enum ModifyCase {
  LowerCase,
  UpperCase,
  TitleCase,
}
