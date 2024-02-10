import { Checkbox, Input, InputWrapper, Select, Stack } from '@mantine/core';
import { BaseNode } from './BaseNode';
import { PropertiesBase } from './PropertiesBase';
import { useState } from 'react';

export interface OutputDataNode extends BaseNode {
  data: OutputDataNodeDataModel;
}

interface OutputDataNodeDataModel extends PropertiesBase {
  filename: string | null;
  format: ExportFormat;
  indexColumn: boolean;
}

export enum ExportFormat {
  // Original = 'original',
  Csv = 'csv',
  Xls = 'xls',
  Xlsx = 'xlsx',
  Pickle = 'pickle',
  Parquet = 'parquet',
}

export default function OutputDataNodePropertiesUI({ data }: { data: OutputDataNodeDataModel}) {
  const [value, setValue] = useState<string>('');

  return (
    <Stack>
      <InputWrapper label="Filename" required>
        <Input
          type="text"
          placeholder="Enter filename"
          value={data.filename || ''}
          onChange={(event) => (data.filename = event.currentTarget.value)}
          mt="md"
        />
      </InputWrapper>
      <Select
        label="File Format"
        placeholder="Select format"
        value={data.format || ''}
        onChange={(event) => (data.format = event as ExportFormat)}
        clearable
        defaultValue={ExportFormat.Csv}
        data={[
          { value: ExportFormat.Csv, label: 'CSV' },
          { value: ExportFormat.Xls, label: 'XLS' },
          { value: ExportFormat.Xlsx, label: 'XLSX' },
          { value: ExportFormat.Pickle, label: 'Pickle' },
          { value: ExportFormat.Parquet, label: 'Parquet' },
        ]}
      ></Select>
      <Checkbox
        checked={data.indexColumn}
        onChange={(event) => (data.indexColumn = event.currentTarget.checked)}
      >
        Include Index Column
      </Checkbox>
    </Stack>
  );
}
