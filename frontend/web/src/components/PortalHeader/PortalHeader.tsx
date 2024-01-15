import { Container, Group, Burger, Button, Center, Box, Title } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { IconCode } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import { shallow } from 'zustand/shallow';
import classes from './PortalHeader.module.css';
import agent from '@/api/agent';
import useFlowStore, { FlowState } from '@/stores/FlowStore';
import { CreateWorkflowDto } from '@/models/Workflow';

const selector = (state: FlowState) => ({
  workflows: state.workflows,
  loadWorkflows: state.loadWorkflows,
  loadWorkflow: state.loadWorkflow,
  setCurrentWorkflowId: state.setCurrentWorkflowId,
});

export function PortalHeader() {
  const [opened, { toggle }] = useDisclosure(false);
  const navigate = useNavigate();
  const { setCurrentWorkflowId, loadWorkflows } = useFlowStore(selector, shallow);

  return (
    <header className={classes.header}>
      <Container size="md" className={classes.inner}>
        <Group>
          <Center inline>
            <IconCode size={30} />
            <Box ml={5}>
              <Title order={3}>PrediKit</Title>
            </Box>
          </Center>
        </Group>
        <Group gap={5} visibleFrom="xs">
          <Button
            variant="filled"
            onClick={() => {
              const workflow: CreateWorkflowDto = {
                title: 'Untitled Workflow',
                description: '',
                createdOn: new Date().toUTCString(),
                modifiedOn: new Date().toUTCString(),
                nodes: [],
                edges: [],
                viewPort: { x: 0, y: 0, zoom: 1 },
              };
              agent.Workflows.create(workflow)
                .then((response) => {
                  navigate(`/workflows/${response.data.id}`);
                  setCurrentWorkflowId(response.data.id);
                })
                .catch((error) => {
                  console.error(`Error while creating new workflow:\n${error}`);
                });
              loadWorkflows();
            }}
          >
            Create New Workflow
          </Button>
        </Group>

        <Burger opened={opened} onClick={toggle} hiddenFrom="xs" size="sm" />
      </Container>
    </header>
  );
}
