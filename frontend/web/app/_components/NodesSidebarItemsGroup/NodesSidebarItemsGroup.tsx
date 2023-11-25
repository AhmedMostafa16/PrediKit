import React, { useState } from "react";
import {
  Group,
  Box,
  Collapse,
  ThemeIcon,
  Text,
  UnstyledButton,
  rem,
} from "@mantine/core";
import { IconChevronRight } from "@tabler/icons-react";
import classes from "./NodesSidebarItemsGroup.module.css";
import { Color } from "@/app/_utils/Color";

type ItemsGroupProps = {
  color: Color;
  label: string;
  initiallyOpened?: boolean;
  items?: { label: string; icon: JSX.Element; nodeType: string; data: any }[];
};

export function ItemsGroup({
  color,
  label,
  initiallyOpened,
  items,
}: ItemsGroupProps) {
  const hasItems = Array.isArray(items);
  const [opened, setOpened] = useState(initiallyOpened || false);
  const onDragStart = (
    event: React.DragEvent<HTMLAnchorElement>,
    node: any,
  ): void => {
    event.dataTransfer.setData("application/reactflow", JSON.stringify(node));
    event.dataTransfer.effectAllowed = "move";
    console.log("Started dragging: " + node.label);
  };

  const elements = (hasItems ? items : []).map((item) => (
    <React.Fragment key={item.label}>
      <Group justify="space-between" gap={0}>
        <Text<"a">
          component="a"
          className={classes.item}
          onClick={(event) => event.preventDefault()}
          onDragStart={(event: React.DragEvent<HTMLAnchorElement>) =>
            onDragStart(event, item)
          }
          draggable
        >
          <Box style={{ display: "flex", alignItems: "center" }}>
            <ThemeIcon variant="filled" color={color} size={36}>
              {item.icon}
            </ThemeIcon>
            <Box ml="md">{item.label}</Box>
          </Box>
        </Text>
      </Group>
    </React.Fragment>
  ));

  return (
    <>
      <UnstyledButton
        onClick={() => setOpened((o) => !o)}
        className={classes.control}
      >
        <Group justify="space-between" gap={0}>
          <Box style={{ display: "flex", alignItems: "center" }}>
            <ThemeIcon variant="filled" color={color} size={32}></ThemeIcon>
            <Box ml="md">{label}</Box>
          </Box>
          {hasItems && (
            <IconChevronRight
              className={classes.chevron}
              stroke={1.5}
              style={{
                width: rem(16),
                height: rem(16),
                transform: opened ? "rotate(-90deg)" : "none",
              }}
            />
          )}
        </Group>
      </UnstyledButton>
      {hasItems ? <Collapse in={opened}>{elements}</Collapse> : null}
    </>
  );
}
