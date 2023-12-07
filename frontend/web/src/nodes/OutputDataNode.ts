import { BaseNode } from './BaseNode';

export interface OutputDataNode extends BaseNode {
  data: OutputDataNodeDataModel;
}

interface OutputDataNodeDataModel {
  format: ExportFormat;
  delimiter?: string;
}

export enum ExportFormat {
  Original = 'Original',
  CSV = 'CSV',
  XLS = 'XLS',
  XLSX = 'XLSX',
  PICKLE = 'PICKLE',
  PARQUET = 'PARQUET',
}
