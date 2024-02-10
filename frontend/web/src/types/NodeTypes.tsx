import {
  IconArrowsJoin,
  IconFileExport,
  IconFileImport,
  IconFilter,
  IconSparkles,
} from '@tabler/icons-react';
import { Connection } from 'reactflow';
import NodeFactory from '../components/NodeFactory/NodeFactory';
import { InputDataNode } from '../nodes/InputDataNode';
import { ExportFormat, OutputDataNode } from '../nodes/OutputDataNode';
import {
  DataCleansingNode,
  OutlierDetectionMethod,
  MissingValueStrategy,
} from '../nodes/DataCleansingNode';
import { BasicFilterNode } from '../nodes/BasicFilterNode';
import { JoinNode, JoinType } from '@/nodes/JoinNode';
import useFlowStore from '@/stores/FlowStore';
// import useFlowStore from '@/stores/FlowStore';

export const InputNodeProps: InputDataNode = {
  type: 'inputDataNode',
  data: {
    file: undefined,
    // ToDo - add extension to data when BytesIO is implemented
    // extension: 'csv',
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
    // {
    //   type: 'select',
    //   label: 'Extension',
    //   id: 'extension',
    //   allowDeselect: true,
    //   placeholder: 'Select extension',
    //   defaultValue: 'csv',
    //   options: [
    //     { label: 'CSV', value: 'csv' },
    //     { label: 'Excel (XLS)', value: 'xls' },
    //     { label: 'Excel (XLSX)', value: 'xlsx' },
    //     { label: 'Pickle', value: 'pickle' },
    //     { label: 'Parquet', value: 'parquet' },
    //   ],
    // },
  ],
};
const InputNodeComponent = NodeFactory(InputNodeProps);

export const OutputNodeProps: OutputDataNode = {
  type: 'outputDataNode',
  data: {
    format: ExportFormat.Csv,
    filename: null,
    indexColumn: false,
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
      defaultValue: ExportFormat.Csv,
      options: [
        // { label: 'Original', value: ExportFormat.Original },
        { label: 'CSV', value: ExportFormat.Csv },
        { label: 'Excel (XLS)', value: ExportFormat.Xls },
        { label: 'Excel (XLSX)', value: ExportFormat.Xlsx },
        { label: 'Pickle', value: ExportFormat.Pickle },
        { label: 'Parquet', value: ExportFormat.Parquet },
      ],
    },
    // TODO: hide when format is parquet
    {
      type: 'checkbox',
      label: 'Index Column',
      id: 'indexColumn',
    },
  ],
};
const OutputNodeComponent = NodeFactory(OutputNodeProps);

export const DataCleansingNodeProps: DataCleansingNode = {
  data: {
    missingClean: false,
    missingStrategy: MissingValueStrategy.Mode,
    missingFillValue: '',
    missingIndicator: false,
    outlierClean: false,
    outlierMethod: OutlierDetectionMethod.ZScore,
    outlierThreshold: 3,
    outlierIndicator: false,
    strOperations: false,
    strCaseModifierMethod: null,
    strTrim: false,
    strRemoveWhitespace: false,
    strRemoveNumbers: false,
    strRemoveLetters: false,
    strRemovePunctuation: false,
    selectedColumns: [],
  },
  type: 'dataCleansingNode',
  label: 'Data Cleansing',
  inputHandles: [{}],
  outputHandles: [{}],
  color: 'blue',
  icon: <IconSparkles />,
  onClick: async () => {
    console.debug('DataCleansingNode onClick');
    const { currentWorkflowId, nodes, columnNames, loadColumnNames } = useFlowStore();
    if (currentWorkflowId === null || !nodes.find((value) => value.type === 'inputDataNode'))
      return;
    loadColumnNames();
    DataCleansingNodeProps.formFields[0].options = columnNames;
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
    /* Missing Values Processing */
    {
      type: 'checkbox',
      label: 'Clean Missing',
      id: 'missingClean',
    },
    {
      type: 'select',
      label: 'Missing Strategy',
      id: 'missingStrategy',
      options: [
        { label: 'Mean', value: 'mean' },
        { label: 'Median', value: 'median' },
        { label: 'Most frequent', value: 'mode' },
        { label: 'Constant', value: 'constant' },
        { label: 'Drop', value: 'drop' },
      ],
      dependencies: [
        {
          fieldId: 'missingClean',
          triggerValue: true,
          optional: false,
        },
      ],
    },
    {
      type: 'input',
      label: 'Missing Fill Value',
      id: 'missingFillValue',
      dependencies: [
        {
          fieldId: 'missingStrategy',
          triggerValue: 'constant',
          optional: false,
        },
      ],
    },
    {
      type: 'checkbox',
      label: 'Add Missing Indicator',
      id: 'missingIndicator',
      dependencies: [
        {
          fieldId: 'missingClean',
          triggerValue: true,
          optional: false,
        },
      ],
    },
    /* Outlier Processing */
    { type: 'checkbox', label: 'Remove Outliers', id: 'outlierClean' },
    {
      type: 'select',
      label: 'Outlier Detection Method',
      id: 'outlierMethod',
      defaultValue: 'iqr',
      options: [
        { label: 'IQR', value: 'iqr' },
        { label: 'Z-score', value: 'z_score' },
      ],
      dependencies: [
        {
          fieldId: 'outlierClean',
          triggerValue: true,
          optional: false,
        },
      ],
    },
    {
      type: 'checkbox',
      label: 'Add Outliers Indicator',
      id: 'outlierIndicator',
      dependencies: [
        {
          fieldId: 'outlierClean',
          triggerValue: true,
          optional: false,
        },
      ],
    },
    // {
    //   type: 'slider',
    //   label: 'Outlier Threshold',
    //   id: 'outlierThreshold',
    //   defaultValue: 3,
    //   min: 0.5,
    //   max: 10,
    //   step: 0.2,
    //   dependencies: [
    //     {
    //       fieldId: 'outlierClean',
    //       triggerValue: true,
    //       optional: false,
    //     },
    //   ],
    // },

    /* String Operations Processing */
    { type: 'checkbox', label: 'Operate on Strings', id: 'strOperations' },
    {
      type: 'select',
      label: 'Modify Case',
      id: 'strCaseModifierMethod',
      allowDeselect: true,
      placeholder: 'Select case',
      defaultValue: null,
      options: [
        { label: 'Lowercase', value: 'lower' },
        { label: 'Uppercase', value: 'upper' },
        { label: 'Title Case', value: 'title' },
        { label: 'Capitalize', value: 'capitalize' },
        { label: 'Swap Case', value: 'swapcase' },
        { label: 'Case Fold', value: 'casefold' },
      ],
      dependencies: [
        {
          fieldId: 'strOperations',
          triggerValue: true,
          optional: false,
        },
      ],
    },
    {
      type: 'checkbox',
      label: 'Trim',
      id: 'strTrim',

      dependencies: [
        {
          fieldId: 'strOperations',
          triggerValue: true,
          optional: false,
        },
      ],
    },
    {
      type: 'checkbox',
      label: 'Remove Whitespace from Strings',
      id: 'strRemoveWhitespace',
      dependencies: [
        {
          fieldId: 'strOperations',
          triggerValue: true,
          optional: false,
        },
      ],
    },
    {
      type: 'checkbox',
      label: 'Remove Letters from Strings',
      id: 'strRemoveLetters',
      dependencies: [
        {
          fieldId: 'strOperations',
          triggerValue: true,
          optional: false,
        },
      ],
    },
    {
      type: 'checkbox',
      label: 'Remove Numbers from Strings',
      id: 'strRemoveNumbers',
      dependencies: [
        {
          fieldId: 'strOperations',
          triggerValue: true,
          optional: false,
        },
      ],
    },
    {
      type: 'checkbox',
      label: 'Remove Punctuation from Strings',
      id: 'strRemovePunctuation',
      dependencies: [
        {
          fieldId: 'strOperations',
          triggerValue: true,
          optional: false,
        },
      ],
    },
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
        console.debug('onConnect');
        console.debug(connection.source);
        console.debug(connection.target);
      },
    },
  ],
  outputHandles: [{}],
  color: 'blue',
  icon: <IconFilter />,
  onClick: async () => {
    // console.debug('BasicFilterNode onClick');
    // const { currentWorkflowId, nodes, columnNames, loadColumnNames } = useFlowStore();
    // if (currentWorkflowId === null || !nodes.find((value) => value.type === 'inputDataNode'))
    //   return;
    // loadColumnNames();
    // BasicFilterNodeProps.formFields[0].options = columnNames;
  },
  formFields: [
    {
      // type: 'select',
      type: 'input',
      label: 'Column Name',
      id: 'column',
      allowDeselect: true,
      required: true,
      placeholder: 'Select column',
      searchable: true,
      /* options: () => {
        const { currentWorkflowId, nodes, columnNames, loadColumnNames } = useFlowStore();
        if (currentWorkflowId === null || !nodes.find((value) => value.type === 'inputDataNode'))
          return [];

        // TODO: fix hook is called at top level (not conditionally)
        loadColumnNames();

        if (!columnNames) return [];
        return columnNames;
      }, */
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
        { label: '=', value: 'equal' },
        { label: '!=', value: 'notequal' },
        { label: '>', value: 'greater' },
        { label: '<', value: 'less' },
        { label: '>=', value: 'greaterequal' },
        { label: '<=', value: 'lessequal' },
        { label: 'Contains', value: 'contains' },
        { label: 'Does not contain', value: 'doesnotcontain' },
        { label: 'Is null', value: 'null' },
        { label: 'Is not null', value: 'notnull' },
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

export const JoinNodeProps: JoinNode = {
  data: {
    joinType: JoinType.INNER,
  },
  type: 'joinNode',
  label: 'Join',
  inputHandles: [{}, {}],
  outputHandles: [{}],
  color: 'violet',
  icon: <IconArrowsJoin />,
  formFields: [
    {
      type: 'select',
      label: 'Join Type',
      id: 'joinType',
      options: [
        { label: 'Inner', value: JoinType.INNER },
        { label: 'Left', value: JoinType.LEFT },
        { label: 'Right', value: JoinType.RIGHT },
      ],
    },
  ],
};

const JoinNodeComponent = NodeFactory(JoinNodeProps);

export const nodeTypes = {
  inputDataNode: InputNodeComponent,
  outputDataNode: OutputNodeComponent,
  dataCleansingNode: DataCleansingNodeComponent,
  basicFilterNode: BasicFilterNodeComponent,
  joinNode: JoinNodeComponent,
};

export const nodeTypesProps = {
  inputDataNode: InputNodeProps,
  outputDataNode: OutputNodeProps,
  dataCleansingNode: DataCleansingNodeProps,
  basicFilterNode: BasicFilterNodeProps,
  joinNode: JoinNodeProps,
};
