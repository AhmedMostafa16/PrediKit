import { Menu, Group, Center, Burger, UnstyledButton, Button } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { IconChevronDown, IconCode, IconPlayerPlayFilled } from '@tabler/icons-react';
import { Link } from 'react-router-dom';
import { shallow } from 'zustand/shallow';
import { notifications } from '@mantine/notifications';
import classes from './EditorHeader.module.css';
import agent from '@/api/agent';
import { useStore } from '@/stores/store';
import { observer } from 'mobx-react-lite';

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

function EditorHeader() {
  const [opened, { toggle }] = useDisclosure(false);

  const { workflowStore } = useStore();
  const { currentWorkflowId } = workflowStore;

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
          <IconCode size={28} />
        </UnstyledButton>
        <Group gap={5} visibleFrom="sm">
          {items}
        </Group>
        <Button
          leftSection={<IconPlayerPlayFilled size={16} />}
          variant="filled"
          onClick={() => {
            if (!currentWorkflowId) return;
            agent.Workflows.execute(currentWorkflowId)
              .then((response) => {
                console.log(response.data);
                notifications.show({
                  title: 'Workflow executed',
                  message: 'The workflow has been executed successfully',
                  color: 'green',
                });
              })
              .catch((error) => {
                console.log(`Error while executing workflow:\n${error}`);
                notifications.show({
                  title: 'Workflow execution failed',
                  message: 'The workflow could not be executed',
                  color: 'red',
                });
              });
          }}
        >
          Run
        </Button>

        <Burger opened={opened} onClick={toggle} size="sm" hiddenFrom="sm" />
      </div>
    </header>
  );
}

export default observer(EditorHeader);
