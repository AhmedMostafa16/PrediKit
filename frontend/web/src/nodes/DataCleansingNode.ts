import { BaseNode } from './BaseNode';
import { PropertiesBase } from './PropertiesBase';

export interface DataCleansingNode extends BaseNode {
  data: DataCleansingNodeDataModel;
}

interface DataCleansingNodeDataModel extends PropertiesBase {
  missingClean: boolean;
  missingStrategy: MissingValueStrategy;
  missingFillValue: string;
  missingIndicator: boolean;
  outlierClean: boolean;
  outlierMethod: OutlierDetectionMethod;
  outlierThreshold: number;
  outlierIndicator: boolean;
  strOperations: boolean;
  strCaseModifierMethod: CaseModifyingMethod | null;
  strTrim: boolean;
  strRemoveWhitespace: boolean;
  strRemoveNumbers: boolean;
  strRemoveLetters: boolean;
  strRemovePunctuation: boolean;
  selectedColumns: string[];
}

export enum MissingValueStrategy {
  Mean = 'mean',
  Median = 'median',
  Mode = 'mode',
  Constant = 'constant',
  Omit = 'omit',
}

export enum OutlierDetectionMethod {
  IQR = 'iqr',
  ZScore = 'z_score',
}

export enum CaseModifyingMethod {
  LowerCase = 'lower',
  UpperCase = 'upper',
  TitleCase = 'title',
  Capitalize = 'capitalize',
  SwapCase = 'swapcase',
  Casefold = 'casefold',
}
