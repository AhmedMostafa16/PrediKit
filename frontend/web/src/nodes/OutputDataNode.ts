import { BaseNode } from './BaseNode';
import { PropertiesBase } from './PropertiesBase';

export interface OutputDataNode extends BaseNode {
  data: OutputDataNodeDataModel;
}

interface OutputDataNodeDataModel extends PropertiesBase {
  filename: string | null;
  format: ExportFormat;
}

export enum ExportFormat {
  // Original = 'Original',
  CSV = 'csv',
  XLS = 'xls',
  XLSX = 'xlsx',
  PICKLE = 'pickle',
  PARQUET = 'parquet',
}
