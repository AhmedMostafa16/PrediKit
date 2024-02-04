import {
  Stack,
  Checkbox,
  Select,
  InputWrapper,
  Input,
  MultiSelect,
  ActionIcon,
  NumberInput,
  Slider,
} from '@mantine/core';
import { BaseNode } from './BaseNode';
import { PropertiesBase } from './PropertiesBase';
import { useForm } from '@mantine/form';
import agent from '@/api/agent';
import useFlowStore from '@/stores/FlowStore';
import { notifications } from '@mantine/notifications';
import { IconRefresh } from '@tabler/icons-react';

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

export default function DataCleansingNodePropertiesUI({
  data,
}: {
  data: DataCleansingNodeDataModel;
}) {
  const fetchColumnNames = async () => {
    const response = await agent.Workflows.listColumnNames(
      useFlowStore.getState().currentWorkflowId
    )
      .then((response) => response as string[])
      .catch((error) => {
        console.error(`Error while fetching column names:\n${error}`);
        notifications.show({
          title: 'Error',
          message: `Error while fetching column names in node ${useFlowStore.getState().selectedNode}: ${error}`,
          autoClose: 7000,
          color: 'red',
        });
        return [];
      });
    useFlowStore.setState({ columnNames: response });
  };
  return (
    <Stack>
      <MultiSelect
        label="Select Columns"
        placeholder="Select columns"
        description="Select columns to apply data cleansing operations on"
        data={useFlowStore.getState().columnNames}
        value={data.selectedColumns}
        onChange={(event) => (data.selectedColumns = event)}
        searchable
        clearable
        onClick={async () => {
          await fetchColumnNames();
        }}
        leftSection={
          <ActionIcon
            variant="transparent"
            style={{ display: useFlowStore.getState().columnNames.length ? 'none' : undefined }}
            onClick={async () => {
              await fetchColumnNames();
            }}
            aria-label="Refresh column names"
          >
            <IconRefresh />
          </ActionIcon>
        }
      />
      <Checkbox
        label="Clean Missing Values"
        checked={data.missingClean}
        onChange={(event) => (data.missingClean = event.currentTarget.checked)}
      />
      <Select
        label="Missing Value Strategy"
        placeholder="Select missing value strategy"
        value={data.missingStrategy}
        onChange={(event) => (data.missingStrategy = event as MissingValueStrategy)}
        data={[
          { value: MissingValueStrategy.Mean, label: 'Mean' },
          { value: MissingValueStrategy.Median, label: 'Median' },
          { value: MissingValueStrategy.Mode, label: 'Mode (Most frequent)' },
          { value: MissingValueStrategy.Constant, label: 'Constant' },
          { value: MissingValueStrategy.Omit, label: 'Omit (Drop)' },
        ]}
        hidden={!data.missingClean}
        disabled={!data.missingClean}
      />
      <InputWrapper
        label="Fill Value"
        hidden={!data.missingClean || data.missingStrategy !== MissingValueStrategy.Constant}
      >
        <Input
          value={data.missingFillValue}
          onChange={(event) => (data.missingFillValue = event.currentTarget.value)}
          placeholder="Enter fill value"
        />
      </InputWrapper>
      <Checkbox
        label="Add Missing Indicator"
        checked={data.missingIndicator}
        onChange={(event) => (data.missingIndicator = event.currentTarget.checked)}
        hidden={!data.missingClean}
        disabled={!data.missingClean}
      />
      <Checkbox
        label="Clean Outliers"
        checked={data.outlierClean}
        onChange={(event) => (data.outlierClean = event.currentTarget.checked)}
      />
      <Select
        label="Outlier Detection Method"
        placeholder="Select outlier detection method"
        value={data.outlierMethod}
        onChange={(event) => (data.outlierMethod = event as OutlierDetectionMethod)}
        data={[
          { value: OutlierDetectionMethod.IQR, label: 'IQR' },
          { value: OutlierDetectionMethod.ZScore, label: 'Z-Score' },
        ]}
        hidden={!data.outlierClean}
        disabled={!data.outlierClean}
      />
      <InputWrapper label="Outlier Threshold" hidden={!data.outlierClean}>
        <Slider
          value={data.outlierThreshold}
          onChange={(event) => (data.outlierThreshold = event)}
          min={0.5}
          max={10}
          step={0.1}
          defaultValue={data.outlierMethod === OutlierDetectionMethod.IQR ? 1.5 : 3}
          disabled={!data.outlierClean}
        />
      </InputWrapper>
      <Checkbox
        label="Add Outlier Indicator"
        checked={data.outlierIndicator}
        onChange={(event) => (data.outlierIndicator = event.currentTarget.checked)}
        hidden={!data.outlierClean}
        disabled={!data.outlierClean}
      />
      <Checkbox
        label="String Operations"
        checked={data.strOperations}
        onChange={(event) => (data.strOperations = event.currentTarget.checked)}
      />
      <Select
        label="Case Modifier Method"
        placeholder="Select case modifier method"
        value={data.strCaseModifierMethod}
        onChange={(event) => (data.strCaseModifierMethod = event as CaseModifyingMethod)}
        data={[
          { value: CaseModifyingMethod.LowerCase, label: 'Lower Case' },
          { value: CaseModifyingMethod.UpperCase, label: 'Upper Case' },
          { value: CaseModifyingMethod.TitleCase, label: 'Title Case' },
          { value: CaseModifyingMethod.Capitalize, label: 'Capitalize' },
          { value: CaseModifyingMethod.SwapCase, label: 'Swap Case' },
          { value: CaseModifyingMethod.Casefold, label: 'Casefold' },
        ]}
        hidden={!data.strOperations}
        disabled={!data.strOperations}
      />
      <Checkbox
        label="Trim"
        description="Remove leading and trailing whitespace"
        checked={data.strTrim}
        onChange={(event) => (data.strTrim = event.currentTarget.checked)}
        hidden={!data.strOperations}
        disabled={!data.strOperations}
      />
      <Checkbox
        label="Remove Whitespace"
        description="Remove all whitespace characters"
        checked={data.strRemoveWhitespace}
        onChange={(event) => (data.strRemoveWhitespace = event.currentTarget.checked)}
        hidden={!data.strOperations}
        disabled={!data.strOperations}
      />
      <Checkbox
        label="Remove Numbers"
        description="Remove all numeric characters"
        checked={data.strRemoveNumbers}
        onChange={(event) => (data.strRemoveNumbers = event.currentTarget.checked)}
        hidden={!data.strOperations}
        disabled={!data.strOperations}
      />
      <Checkbox
        label="Remove Letters"
        description="Remove all alphabetic characters"
        checked={data.strRemoveLetters}
        onChange={(event) => (data.strRemoveLetters = event.currentTarget.checked)}
        hidden={!data.strOperations}
        disabled={!data.strOperations}
      />
      <Checkbox
        label="Remove Punctuation"
        description="Remove all punctuation characters"
        checked={data.strRemovePunctuation}
        onChange={(event) => (data.strRemovePunctuation = event.currentTarget.checked)}
        hidden={!data.strOperations}
        disabled={!data.strOperations}
      />
    </Stack>
  );
}
