import { ActionIcon, Checkbox, Input, InputWrapper, Loader, Select, Stack } from '@mantine/core';
import { Operator } from '../types/Operator';
import { BaseNode } from './BaseNode';
import { PropertiesBase } from './PropertiesBase';
import agent from '@/api/agent';
import useFlowStore from '@/stores/FlowStore';
import { notifications } from '@mantine/notifications';
import { IconRefresh } from '@tabler/icons-react';

export interface BasicFilterNode extends BaseNode {
  data: BasicFilterNodeDataModel;
}

interface BasicFilterNodeDataModel extends PropertiesBase {
  column: string;
  operator: Operator | undefined;
  value: string;
  caseSensitive: boolean;
}

export default function BasicFilterNodePropertiesUI({ data }: { data: BasicFilterNodeDataModel }) {
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
      <InputWrapper label="Column" required>
        <Select
          placeholder="Select column name"
          value={data.column}
          onChange={(event) => (data.column = event || '')}
          leftSection={
            // show refresh button only if there are no column names
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
          onClick={async () => {
            await fetchColumnNames();
          }}
          data={useFlowStore.getState().columnNames}
          required
        />
      </InputWrapper>
      <Select
        value={data.operator}
        onChange={(event) => (data.operator = event as Operator)}
        label="Comparison Operator"
        placeholder="Select operator"
        clearable
        required
        data={[
          { value: Operator.EQUAL, label: 'Equal' },
          { value: Operator.NOTEQUAL, label: 'Not Equal' },
          { value: Operator.LESS, label: 'Less Than' },
          { value: Operator.LESSEQUAL, label: 'Less Than or Equal' },
          { value: Operator.GREATER, label: 'Greater Than' },
          { value: Operator.GREATEREQUAL, label: 'Greater Than or Equal' },
          { value: Operator.CONTAINS, label: 'Contains' },
          { value: Operator.DOES_NOT_CONTAIN, label: 'Not Contains' },
        ]}
      ></Select>
      <InputWrapper label="Value" required>
        <Input
          type="text"
          placeholder="Enter value"
          value={data.value}
          onChange={(event) => (data.value = event.currentTarget.value)}
          required
        />
      </InputWrapper>
      <Checkbox
        checked={data.caseSensitive}
        onChange={(event) => (data.caseSensitive = event.currentTarget.checked)}
      >
        Case Sensitive
      </Checkbox>
    </Stack>
  );
}
