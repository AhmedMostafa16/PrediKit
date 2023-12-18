import { IconFileExport, IconFileImport, IconFilter, IconSparkles } from '@tabler/icons-react';
import { Connection } from 'reactflow';
import NodeFactory from '../components/NodeFactory/NodeFactory';
import { InputDataNode } from '../nodes/InputDataNode';
import { ExportFormat, OutputDataNode } from '../nodes/OutputDataNode';
import { DataCleansingNode, OutlierMethod, ReplaceNullWith } from '../nodes/DataCleansingNode';
import { BasicFilterNode } from '../nodes/BasicFilterNode';
import useFlowStore from '@/stores/FlowStore';

export const InputNodeProps: InputDataNode = {
  type: 'inputDataNode',
  data: {
    file: undefined,
    extension: 'csv',
  },
  inputHandles: [],
  outputHandles: [{}],
  label: 'Input Data',
  color: 'teal',
  icon: <IconFileImport />,
  formFields: [
    /*
    {
      type: 'dropzone',
      id: 'file',
      label: 'Upload file',
      maxSize: Number.MAX_VALUE,
      required: true,
      acceptedMIME: [
        'text/ms-excel',
        'application/msexcel',
        'application/vnd.ms-excel',
        'application/vnd.msexcel',
        'application/x-csv',
        'text/comma-separated-values',
        'text/csv',
        'text/x-csv',
        'text/x-comma-separated-values',
        'application/octet-stream',
      ],
    },
    */
    {
      type: 'input',
      label: 'File Path',
      id: 'file',
    },
    {
      type: 'select',
      label: 'Extension',
      id: 'extension',
      allowDeselect: true,
      placeholder: 'Select extension',
      defaultValue: 'csv',
      options: [
        { label: 'CSV', value: 'csv' },
        { label: 'Excel (XLS)', value: 'xls' },
        { label: 'Excel (XLSX)', value: 'xlsx' },
        { label: 'Pickle', value: 'pickle' },
        { label: 'Parquet', value: 'parquet' },
      ],
    },
  ],
};
const InputNodeComponent = NodeFactory(InputNodeProps);

export const OutputNodeProps: OutputDataNode = {
  type: 'outputDataNode',
  data: {
    format: ExportFormat.CSV,
    filename: null,
  },
  inputHandles: [{}],
  outputHandles: [],
  label: 'Output Data',
  color: 'teal',
  icon: <IconFileExport />,
  formFields: [
    {
      type: 'input',
      label: 'Filename',
      id: 'filename',
      placeholder: '',
      defaultValue: null,
    },
    {
      type: 'select',
      label: 'Format',
      id: 'format',
      allowDeselect: true,
      placeholder: 'Select format',
      defaultValue: ExportFormat.CSV,
      options: [
        // { label: 'Original', value: ExportFormat.Original },
        { label: 'CSV', value: ExportFormat.CSV },
        { label: 'Excel (XLS)', value: ExportFormat.XLS },
        { label: 'Excel (XLSX)', value: ExportFormat.XLSX },
        { label: 'Pickle', value: ExportFormat.PICKLE },
        { label: 'Parquet', value: ExportFormat.PARQUET },
      ],
    },
  ],
};
const OutputNodeComponent = NodeFactory(OutputNodeProps);

export const DataCleansingNodeProps: DataCleansingNode = {
  data: {
    removeOutliers: false,
    outlierMethod: OutlierMethod.IQR,
    replaceNulls: false,
    replaceNullWith: ReplaceNullWith.Mean,
    fillValue: '',
    modifyCase: null,
    removeWhitespace: false,
    // removeDuplicates: false,
    removePunctuation: false,
    removeNumbers: false,
    removeLetters: false,
    trim: false,
    selectedColumns: [],
  },
  type: 'dataCleansingNode',
  label: 'Data Cleansing',
  inputHandles: [{}],
  outputHandles: [{}],
  color: 'blue',
  icon: <IconSparkles />,
  onClick: async () => {
    console.log('DataCleansingNode onClick');
    if (
      useFlowStore.getState().currentWorkflowId === null ||
      !useFlowStore.getState().nodes.find((value) => value.type === 'inputDataNode')
    )
      return;
    useFlowStore.getState().loadColumnNames();
    DataCleansingNodeProps.formFields[0].options = useFlowStore.getState().columnNames;
  },
  formFields: [
    {
      type: 'multiSelect',
      label: 'Selected columns',
      id: 'selectedColumns',
      options: useFlowStore.getState().columnNames,
      placeholder: 'Select columns',
      searchable: true,
    },
    { type: 'checkbox', label: 'Remove outliers', id: 'removeOutliers' },
    {
      type: 'select',
      label: 'Outlier method',
      id: 'outlierMethod',
      defaultValue: 'iqr',
      options: [
        { label: 'IQR', value: 'iqr' },
        { label: 'Z-score', value: 'z_score' },
      ],
      dependencies: [
        {
          fieldId: 'removeOutliers',
          triggerValue: true,
          optional: false,
        },
      ],
    },
    {
      type: 'checkbox',
      label: 'Replace null',
      id: 'replaceNulls',
    },
    {
      type: 'select',
      label: 'Replace null with',
      id: 'replaceNullWith',
      options: [
        { label: 'Mean', value: 'mean' },
        { label: 'Median', value: 'median' },
        { label: 'Mode (Most frequent)', value: 'mode' },
        { label: 'Constant', value: 'constant' },
        { label: 'Drop', value: 'omit' },
      ],
      dependencies: [
        {
          fieldId: 'replaceNulls',
          triggerValue: true,
          optional: false,
        },
      ],
    },
    {
      type: 'input',
      label: 'Constant value',
      id: 'fillValue',
      dependencies: [
        {
          fieldId: 'replaceNullWith',
          triggerValue: 'constant',
          optional: false,
        },
      ],
    },
    { type: 'checkbox', label: 'Remove whitespace from strings', id: 'removeWhitespace' },
    { type: 'checkbox', label: 'Remove letters from strings', id: 'removeLetters' },
    { type: 'checkbox', label: 'Remove numbers from strings', id: 'removeNumbers' },
    { type: 'checkbox', label: 'Remove punctuation from strings', id: 'removePunctuation' },
    // { type: 'checkbox', label: 'Remove duplicates', id: 'removeDuplicates' },
    {
      type: 'select',
      label: 'Modify case',
      id: 'modifyCase',
      allowDeselect: true,
      placeholder: 'Select case',
      defaultValue: null,
      options: [
        // TODO: modify ModifyCase enum
        { label: 'Lowercase', value: 'lower' },
        { label: 'Uppercase', value: 'upper' },
        { label: 'Title case', value: 'title' },
      ],
    },
    { type: 'checkbox', label: 'Trim', id: 'trim' },
  ],
};
const DataCleansingNodeComponent = NodeFactory(DataCleansingNodeProps);

export const BasicFilterNodeProps: BasicFilterNode = {
  data: {
    column: '',
    operator: undefined,
    value: '',
    caseSensitive: true,
  },
  type: 'basicFilterNode',
  label: 'Basic Filter',
  inputHandles: [
    {
      onConnect: async (connection: Connection) => {
        console.log('onConnect');
        console.log(connection.source);
        console.log(connection.target);
      },
    },
  ],
  outputHandles: [{}],
  color: 'blue',
  icon: <IconFilter />,
  onClick: async () => {
    console.log('BasicFilterNode onClick');
    if (
      useFlowStore.getState().currentWorkflowId === null ||
      !useFlowStore.getState().nodes.find((value) => value.type === 'inputDataNode')
    )
      return;
    useFlowStore.getState().loadColumnNames();
    BasicFilterNodeProps.formFields[0].options = useFlowStore.getState().columnNames;
  },
  formFields: [
    {
      type: 'select',
      label: 'Column name',
      id: 'column',
      allowDeselect: true,
      required: true,
      placeholder: 'Select column',
      searchable: true,
      options: useFlowStore.getState().columnNames,
    },
    {
      type: 'select',
      label: 'Operator',
      id: 'operator',
      required: true,
      allowDeselect: true,
      placeholder: 'Select operator',
      options: [
        { label: '=', value: 'equals' },
        { label: '!=', value: 'notequals' },
        { label: '>', value: 'greater' },
        { label: '<', value: 'less' },
        { label: '>=', value: 'greaterequal' },
        { label: '<=', value: 'lessequal' },
        { label: 'Contains', value: 'contains' },
        { label: 'Does not contain', value: 'doesnotcontain' },
        { label: 'Is null', value: 'isnull' },
        { label: 'Is not null', value: 'isnotnull' },
      ],
    },
    {
      type: 'input',
      label: 'Value',
      id: 'value',
      placeholder: 'Enter value',
    },
    {
      type: 'checkbox',
      label: 'Case sensitive',
      id: 'caseSensitive',
      defaultChecked: true,
      dependencies: [
        { fieldId: 'operator', triggerValue: 'contains', optional: true },
        { fieldId: 'operator', triggerValue: 'does not contain', optional: true },
      ],
    },
  ],
};

const BasicFilterNodeComponent = NodeFactory(BasicFilterNodeProps);

export const nodeTypes = {
  inputDataNode: InputNodeComponent,
  outputDataNode: OutputNodeComponent,
  dataCleansingNode: DataCleansingNodeComponent,
  basicFilterNode: BasicFilterNodeComponent,
};

export const nodeTypesProps = {
  inputDataNode: InputNodeProps,
  outputDataNode: OutputNodeProps,
  dataCleansingNode: DataCleansingNodeProps,
  basicFilterNode: BasicFilterNodeProps,
};
