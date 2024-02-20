import { BaseNode } from './BaseNode';
import { PropertiesBase } from './PropertiesBase';

export interface OutputDataNode extends BaseNode {
  data: OutputDataNodeDataModel;
}

interface OutputDataNodeDataModel extends PropertiesBase {
  filename: string | null;
  format: ExportFormat;
  indexColumn: boolean;
}

export enum ExportFormat {
  Original = 'original',
  Csv = 'csv',
  Xls = 'xls',
  Xlsx = 'xlsx',
  Pickle = 'pickle',
  Parquet = 'parquet',
}
