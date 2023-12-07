import { BaseNode } from './BaseNode';

export interface OutputDataNode extends BaseNode {
  data: OutputDataNodeDataModel;
}

interface OutputDataNodeDataModel {
  format: ExportFormat;
}

export enum ExportFormat {
  Original = 'Original',
  CSV = 'CSV',
  XLS = 'XLS',
  XLSX = 'XLSX',
  PICKLE = 'PICKLE',
  PARQUET = 'PARQUET',
}
