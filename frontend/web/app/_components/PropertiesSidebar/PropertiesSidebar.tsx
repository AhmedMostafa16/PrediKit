import { Text, Group, ScrollArea, rem, Code } from "@mantine/core";
import classes from "./PropertiesSidebar.module.css";
import FormBuilder, {
  FormField,
} from "@/app/_components/FormBuilder/FormBuilder";
import { IconCode } from "@tabler/icons-react";
import { Node } from "reactflow";
import { nodeTypesProps } from "@/app/_nodes/NodeTypes";

interface Props {
  fields: FormField[];
  node: Node;
  onAutoSubmit: (formData: { [key: string]: any }) => void;
}

export function PropertiesSidebar({ fields, node, onAutoSubmit }: Props) {
  return (
    <nav className={classes.navbar}>
      <div className={classes.header}>
        <Group justify={"space-between"}>
          {/* <IconCode style={{ width: rem(120) }} />
          <Code fw={700}>v1.1.1</Code> */}
          <Text size="xl" fw={700}>
            {nodeTypesProps[node.type as keyof typeof nodeTypesProps].label}{" "}
            Properties
          </Text>
          <Code fw={700}>{node.id}</Code>
        </Group>
      </div>

      <ScrollArea className={classes.links}>
        <div className={classes.linksInner}>
          <FormBuilder
            formFields={fields}
            data={node.data}
            onAutoSubmit={onAutoSubmit}
          />
        </div>
      </ScrollArea>

      <div className={classes.footer}></div>
    </nav>
  );
}
