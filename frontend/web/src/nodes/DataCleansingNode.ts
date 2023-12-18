import { BaseNode } from './BaseNode';
import { PropertiesBase } from './PropertiesBase';

export interface DataCleansingNode extends BaseNode {
  data: DataCleansingNodeDataModel;
}

interface DataCleansingNodeDataModel extends PropertiesBase {
  removeOutliers: boolean;
  outlierMethod: OutlierMethod;
  replaceNulls: boolean;
  replaceNullWith: ReplaceNullWith;
  fillValue: string;
  modifyCase: ModifyCase | null;
  removeWhitespace: boolean;
  // removeDuplicates: boolean;
  removePunctuation: boolean;
  removeNumbers: boolean;
  removeLetters: boolean;
  trim: boolean;
  selectedColumns: string[];
}

export enum OutlierMethod {
  IQR = 'iqr',
  ZScore = 'z_score',
}

export enum ReplaceNullWith {
  Mean = 'mean',
  Median = 'median',
  Mode = 'mode',
  Constant = 'constant',
  Omit = 'omit',
}

export enum ModifyCase {
  LowerCase = 'lower',
  UpperCase = 'upper',
  TitleCase = 'title',
}
