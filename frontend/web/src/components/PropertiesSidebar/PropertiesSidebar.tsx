import { Text, Group, ScrollArea, Code } from '@mantine/core';
import { Node } from 'reactflow';
import classes from './PropertiesSidebar.module.css';
import FormBuilder, { FormField } from '@/components/FormBuilder/FormBuilder';
import { nodeTypesProps } from '@/types/NodeTypes';

interface Props {
  fields: FormField[];
  node: Node;
  onAutoSubmit: (formData: { [key: string]: any }) => void;
}

export function PropertiesSidebar({ fields, node, onAutoSubmit }: Props) {
  return (
    <nav className={classes.navbar}>
      <div className={classes.header}>
        <Group justify="space-between">
          <Text size="xl" fw={700}>
            {nodeTypesProps[node.type as keyof typeof nodeTypesProps].label} Properties
          </Text>
          <Code fw={700}>{node.id}</Code>
        </Group>
      </div>

      <ScrollArea className={classes.links}>
        <div className={classes.linksInner}>
          <FormBuilder formFields={fields} data={node.data} onAutoSubmit={onAutoSubmit} />
        </div>
      </ScrollArea>

      <div className={classes.footer}></div>
    </nav>
  );
}
