import { ScrollArea } from "@mantine/core";
import { ItemsGroup } from "../NodesSidebarItemsGroup/NodesSidebarItemsGroup";
import classes from "./NodesSidebar.module.css";
import {
  DataCleansingNodeProps,
  FilterNodeProps,
  InputNodeProps,
  OutputNodeProps,
} from "@/app/_nodes/NodeTypes";
import { Color } from "@/app/_utils/Color";

const sidebarData = [
  {
    label: "Input/Output",
    initiallyOpened: true,
    items: [
      {
        label: InputNodeProps.label,
        icon: InputNodeProps.icon,
        nodeType: InputNodeProps.name,
        data: InputNodeProps.data,
      },
      {
        label: OutputNodeProps.label,
        icon: OutputNodeProps.icon,
        nodeType: OutputNodeProps.name,
        data: OutputNodeProps.data,
      },
    ],
    color: "teal" as Color,
  },
  {
    label: "Data Preparation",
    initiallyOpened: true,
    items: [
      {
        label: DataCleansingNodeProps.label,
        icon: DataCleansingNodeProps.icon,
        nodeType: DataCleansingNodeProps.name,
        data: DataCleansingNodeProps.data,
      },
      {
        label: FilterNodeProps.label,
        icon: FilterNodeProps.icon,
        nodeType: FilterNodeProps.name,
        data: FilterNodeProps.data,
      },
    ],
    color: "blue" as Color,
  },
];

export function NodeSidebar() {
  const links = sidebarData.map((item) => (
    <ItemsGroup {...item} key={item.label} />
  ));

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
