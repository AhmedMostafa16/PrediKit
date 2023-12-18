import { ScrollArea } from '@mantine/core';
import { ItemsGroup } from '../NodesSidebarItemsGroup/NodesSidebarItemsGroup';
import classes from './NodesSidebar.module.css';
import {
  DataCleansingNodeProps,
  BasicFilterNodeProps,
  InputNodeProps,
  OutputNodeProps,
} from '@/types/NodeTypes';
import { Color } from '@/types/Color';

const sidebarData = [
  {
    label: 'Input/Output',
    initiallyOpened: true,
    items: [
      {
        label: InputNodeProps.label,
        icon: InputNodeProps.icon,
        nodeType: InputNodeProps.type,
        data: InputNodeProps.data,
      },
      {
        label: OutputNodeProps.label,
        icon: OutputNodeProps.icon,
        nodeType: OutputNodeProps.type,
        data: OutputNodeProps.data,
      },
    ],
    color: 'teal' as Color,
  },
  {
    label: 'Data Preparation',
    initiallyOpened: true,
    items: [
      {
        label: DataCleansingNodeProps.label,
        icon: DataCleansingNodeProps.icon,
        nodeType: DataCleansingNodeProps.type,
        data: DataCleansingNodeProps.data,
      },
      {
        label: BasicFilterNodeProps.label,
        icon: BasicFilterNodeProps.icon,
        nodeType: BasicFilterNodeProps.type,
        data: BasicFilterNodeProps.data,
      },
    ],
    color: 'blue' as Color,
  },
];

export function NodeSidebar() {
  const links = sidebarData.map((item) => <ItemsGroup {...item} key={item.label} />);

  return (
    <nav className={classes.navbar}>
      {/* <div className={classes.header}>
        <Group justify="space-between">
          <IconCode style={{ width: rem(120) }} />
          <Code fw={700}>v1.1.1</Code>
        </Group>
      </div> */}

      <ScrollArea className={classes.links}>
        <div className={classes.linksInner}>{links}</div>
      </ScrollArea>

      <div className={classes.footer}></div>
    </nav>
  );
}
