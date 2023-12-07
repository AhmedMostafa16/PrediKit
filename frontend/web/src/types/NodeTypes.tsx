import { IconFileExport, IconFileImport, IconFilter, IconSparkles } from '@tabler/icons-react';
import NodeFactory from '../components/NodeFactory/NodeFactory';
import { InputDataNode } from '../nodes/InputDataNode';
import { ExportFormat, OutputDataNode } from '../nodes/OutputDataNode';
import { DataCleansingNode } from '../nodes/DataCleansingNode';
import { FilterNode } from '../nodes/FilterNode';

export const InputNodeProps: InputDataNode = {
  name: 'inputDataNode',
  data: {
    file: undefined,
  },
  inputHandles: [],
  outputHandles: [{}],
  label: 'Input Data',
  color: 'teal',
  icon: <IconFileImport />,
  formFields: [
    {
      type: 'dropzone',
      id: 'file',
      label: 'Upload file',
      maxSize: Number.MAX_VALUE,
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
  ],
  id: '',
  position: { x: 0, y: 0 },
};
const InputNodeComponent = NodeFactory(InputNodeProps);

export const OutputNodeProps: OutputDataNode = {
  name: 'outputDataNode',
  data: {
    format: ExportFormat.Original,
  },
  inputHandles: [{}],
  outputHandles: [],
  label: 'Output Data',
  color: 'teal',
  icon: <IconFileExport />,
  formFields: [
    {
      type: 'select',
      label: 'Format',
      id: 'format',
      allowDeselect: true,
      placeholder: 'Select format',
      defaultValue: ExportFormat.Original,
      options: [
        { label: 'Original', value: ExportFormat.Original },
        { label: 'CSV', value: ExportFormat.CSV },
        { label: 'Excel (XLS)', value: ExportFormat.XLS },
        { label: 'Excel (XLSX)', value: ExportFormat.XLSX },
        { label: 'Pickle', value: ExportFormat.PICKLE },
        { label: 'Parquet', value: ExportFormat.PARQUET },
      ],
    },
    {
      type: 'input',
      label: 'CSV Delimiter',
      id: 'delimiter',
      placeholder: ',',
      dependencies: [{ fieldId: 'format', triggerValue: ExportFormat.CSV }],
    },
    {
      type: 'button',
      label: 'Download',
      id: 'download',
      onClick: () => {
        // console.log("You've just clicked on the Download button!");
      },
    },
  ],
  id: '',
  position: { x: 0, y: 0 },
};
const OutputNodeComponent = NodeFactory(OutputNodeProps);

export const DataCleansingNodeProps: DataCleansingNode = {
  data: {
    removeNullData: false,
    removeNullRows: false,
    selectedColumns: [],
    replaceNullBlank: false,
    replaceNullNumbers: false,
    trim: false,
    removeWhitespace: false,
    removeAllWhitespace: false,
    removeLetters: false,
    removeNumbers: false,
    removePunctuation: false,
    modifyCase: null,
    removeOutliers: false,
  },
  name: 'dataCleansingNode',
  label: 'Data Cleansing',
  inputHandles: [{}],
  outputHandles: [{}],
  color: 'blue',
  icon: <IconSparkles />,
  formFields: [
    { type: 'checkbox', label: 'Remove null data', id: 'removeNullData' },
    { type: 'checkbox', label: 'Remove null rows', id: 'removeNullRows' },
    { type: 'checkbox', label: 'Remove outliers', id: 'removeOutliers' },
    {
      type: 'checkbox',
      label: 'Replace null with blank',
      id: 'replaceNullBlank',
    },
    {
      type: 'checkbox',
      label: 'Replace null with numbers',
      id: 'replaceNullNumbers',
    },
    { type: 'checkbox', label: 'Remove whitespace', id: 'removeWhitespace' },
    {
      type: 'checkbox',
      label: 'Remove all whitespace',
      id: 'removeAllWhitespace',
    },
    { type: 'checkbox', label: 'Remove letters', id: 'removeLetters' },
    { type: 'checkbox', label: 'Remove numbers', id: 'removeNumbers' },
    { type: 'checkbox', label: 'Remove punctuation', id: 'removePunctuation' },
    {
      type: 'select',
      label: 'Modify case',
      id: 'modifyCase',
      allowDeselect: true,
      placeholder: 'Select case',
      options: [
        // TODO: modify ModifyCase enum
        { label: 'Lowercase', value: 'lowercase' },
        { label: 'Uppercase', value: 'uppercase' },
        { label: 'Title case', value: 'titlecase' },
      ],
    },
    {
      type: 'multiSelect',
      label: 'Selected columns',
      id: 'selectedColumns',
      options: [], // fill the options from axios response
      placeholder: 'Select columns',
    },
    { type: 'checkbox', label: 'Trim', id: 'trim' },
  ],
  id: '',
  position: { x: 0, y: 0 },
};
const DataCleansingNodeComponent = NodeFactory(DataCleansingNodeProps);

export const FilterNodeProps: FilterNode = {
  data: {
    columnName: '',
    operator: undefined,
    value: '',
  },
  name: 'filterNode',
  label: 'Filter',
  inputHandles: [{}],
  outputHandles: [{}, {}],
  color: 'blue',
  icon: <IconFilter />,
  formFields: [], // TODO: fill the form fields
  id: '',
  position: { x: 0, y: 0 },
};

const FilterNodeComponent = NodeFactory(FilterNodeProps);

export const nodeTypes = {
  inputDataNode: InputNodeComponent,
  outputDataNode: OutputNodeComponent,
  dataCleansingNode: DataCleansingNodeComponent,
  filterNode: FilterNodeComponent,
};

export const nodeTypesProps = {
  inputDataNode: InputNodeProps,
  outputDataNode: OutputNodeProps,
  dataCleansingNode: DataCleansingNodeProps,
  filterNode: FilterNodeProps,
};
