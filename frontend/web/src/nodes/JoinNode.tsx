import { Stack, Select } from '@mantine/core';
import { BaseNode } from './BaseNode';
import { PropertiesBase } from './PropertiesBase';

export interface JoinNode extends BaseNode {
  data: JoinNodeDataModel;
}

interface JoinNodeDataModel extends PropertiesBase {
  joinType: JoinType;
}

export enum JoinType {
  INNER = 'INNER',
  LEFT = 'LEFT',
  RIGHT = 'RIGHT',
  // FULL = 'FULL',
  // CROSS = 'CROSS',
}

export default function JoinNode({ data }: { data: JoinNodeDataModel }) {
  return (
    <Stack>
      <Select
        label="Join Type"
        placeholder="Select join type"
        value={data.joinType}
        data={[
          { value: JoinType.INNER, label: 'Inner' },
          { value: JoinType.LEFT, label: 'Left' },
          { value: JoinType.RIGHT, label: 'Right' },
          // { value: JoinType.FULL, label: 'Full' },
          // { value: JoinType.CROSS, label: 'Cross' },
        ]}
      />
    </Stack>
  );
}
