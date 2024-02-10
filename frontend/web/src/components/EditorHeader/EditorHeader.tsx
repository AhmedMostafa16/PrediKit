import {
  Menu,
  Group,
  Center,
  Burger,
  UnstyledButton,
  Button,
  ActionIcon,
  useComputedColorScheme,
  useMantineColorScheme,
  Title,
  Box,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import {
  IconChevronDown,
  IconCode,
  IconEdit,
  IconMoon,
  IconPlayerPlayFilled,
  IconSun,
} from '@tabler/icons-react';
import { Link } from 'react-router-dom';
import { shallow } from 'zustand/shallow';
import classes from './EditorHeader.module.css';
import cx from 'clsx';
import useFlowStore, { FlowState } from '@/stores/FlowStore';
import { useState } from 'react';

const links = [
  {
    id: '#1',
    label: 'File',
    links: [{ id: '', label: 'Save' }],
  },
  {
    id: '#2',
    label: 'View',
    links: [
      { id: '/faq', label: 'FAQ' },
      { id: '/demo', label: 'Book a demo' },
      { id: '/forums', label: 'Forums' },
    ],
  },
];

const selector = (state: FlowState) => ({
  executeWorkflow: state.executeWorkflow,
  isExecuting: state.isExecuting,
  currentWorkflow: state.currentWorkflow,
});

export default function EditorHeader() {
  const [opened, { toggle }] = useDisclosure(false);
  const [executing, setExecuting] = useState<boolean>(false);
  const { setColorScheme } = useMantineColorScheme();
  const computedColorScheme = useComputedColorScheme('light', { getInitialValueInEffect: true });

  const { executeWorkflow, isExecuting, currentWorkflow } = useFlowStore(selector, shallow);

  const items = links.map((link) => {
    const menuItems = link.links?.map((item) => <Menu.Item key={item.id}>{item.label}</Menu.Item>);

    if (menuItems) {
      return (
        <Menu key={link.label} trigger="hover" transitionProps={{ exitDuration: 0 }} withinPortal>
          <Menu.Target>
            <UnstyledButton className={classes.link} onClick={(event) => event.preventDefault()}>
              <Center>
                <span className={classes.linkLabel}>{link.label}</span>
                <IconChevronDown size="0.9rem" stroke={1.5} />
              </Center>
            </UnstyledButton>
          </Menu.Target>
          <Menu.Dropdown>{menuItems}</Menu.Dropdown>
        </Menu>
      );
    }

    return (
      <UnstyledButton
        key={link.label}
        className={classes.link}
        onClick={(event) => event.preventDefault()}
      >
        {link.label}
      </UnstyledButton>
    );
  });

  return (
    <header className={classes.header}>
      <div className={classes.inner}>
        <UnstyledButton component={Link} to="/workflows">
          <Group>
            <IconCode size={30} />
          </Group>
        </UnstyledButton>
        {/* <Group>
          <Box>
            <Title size={'h3'}> {currentWorkflow?.title} </Title>
          </Box>
        </Group> */}
        <Group gap={5} visibleFrom="sm">
          {/* {items} */}
          <Title size={'h4'}>{currentWorkflow?.title}</Title>
        </Group>
        <Group gap={5} visibleFrom="sm">
          <ActionIcon
            onClick={() => setColorScheme(computedColorScheme === 'light' ? 'dark' : 'light')}
            variant="default"
            aria-label="Toggle color scheme"
            size={'lg'}
          >
            <IconSun className={cx(classes.icon, classes.light)} stroke={1.5} />
            <IconMoon className={cx(classes.icon, classes.dark)} stroke={1.5} />
          </ActionIcon>
          <Button
            leftSection={<IconPlayerPlayFilled size={16} />}
            variant="filled"
            onClick={() => {
              executeWorkflow();
            }}
            loading={isExecuting}
            onKeyDown={async (event) => {
              if (event.key === 'Enter' && event.ctrlKey) {
                await executeWorkflow();
              }
            }}
          >
            Run
          </Button>
        </Group>

        <Burger opened={opened} onClick={toggle} size="sm" hiddenFrom="sm" />
      </div>
    </header>
  );
}
