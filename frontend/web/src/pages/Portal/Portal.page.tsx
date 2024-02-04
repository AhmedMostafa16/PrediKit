import {
  Box,
  Burger,
  Button,
  Center,
  Container,
  Group,
  Modal,
  Stack,
  Table,
  TextInput,
  Textarea,
  Text,
  Title,
} from '@mantine/core';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { shallow } from 'zustand/shallow';
import useFlowStore, { FlowState } from '@/stores/FlowStore';
import { CreateWorkflowDto, Workflow } from '@/models/Workflow';
import agent from '@/api/agent';
import { IconCode } from '@tabler/icons-react';
import { useDisclosure } from '@mantine/hooks';
import classes from './Portal.module.css';
import { modals } from '@mantine/modals';
import { isNotEmpty, useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { formatRelative } from 'date-fns';

interface WorkflowTable {
  id: string;
  title: string;
  description: string;
  createdOn: string;
  modifiedOn: string;
}

const selector = (state: FlowState) => ({
  workflows: state.workflows,
  loadWorkflows: state.loadWorkflows,
  loadWorkflow: state.loadWorkflow,
  setCurrentWorkflowId: state.setCurrentWorkflowId,
});

function PortalPage() {
  const { workflows, loadWorkflows, loadWorkflow, setCurrentWorkflowId } = useFlowStore(
    selector,
    shallow
  );

  const [opened, { toggle }] = useDisclosure(false);
  const [openedModal, { open, close }] = useDisclosure(false);

  const workflowCreationForm = useForm({
    initialValues: {
      title: '',
      description: '',
    },
    validate: {
      title: isNotEmpty('Title must not be empty'),
    },
  });

  useEffect(() => {
    loadWorkflows();
  }, []);

  const elements: WorkflowTable[] = workflows
    ? workflows.map(
        (workflow: Workflow): WorkflowTable => ({
          id: workflow.id,
          title: workflow.title,
          description: workflow.description,
          createdOn: workflow.createdOn,
          modifiedOn: workflow.modifiedOn,
        })
      )
    : [];

  const navigate = useNavigate();

  const rows = elements.map((element) => (
    <Table.Tr
      key={element.id}
      onClick={async () => {
        await loadWorkflow(element.id);
        setCurrentWorkflowId(element.id);
        navigate(`/workflows/${element.id}`);
      }}
    >
      <Table.Td>{element.title}</Table.Td>
      <Table.Td>{element.description}</Table.Td>
      <Table.Td>{formatRelative(element.createdOn, new Date().getDate())}</Table.Td>
      <Table.Td>{formatRelative(element.modifiedOn, new Date().getDate())}</Table.Td>
    </Table.Tr>
  ));

  return (
    <>
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
            <Button variant="filled" onClick={open}>
              Create New Workflow
            </Button>
          </Group>

          <Burger opened={opened} onClick={toggle} hiddenFrom="xs" size="sm" />
        </Container>
      </header>

      <Container size="md">
        <Modal title={'Create New Workflow'} opened={openedModal} onClose={close} centered>
          <form
            onSubmit={workflowCreationForm.onSubmit(
              async (values: { title: string; description: string }) => {
                const workflow: CreateWorkflowDto = {
                  ...values,
                  createdOn: new Date().toUTCString(),
                  modifiedOn: new Date().toUTCString(),
                  nodes: [],
                  edges: [],
                  viewPort: { x: 0, y: 0, zoom: 1 },
                };

                console.log('workflow', workflow);

                await agent.Workflows.create(workflow)
                  .then((response) => {
                    notifications.show({
                      title: 'Workflow Created',
                      message: `Workflow "${workflow.title}" created successfully`,
                      autoClose: 5000,
                    });

                    setCurrentWorkflowId(response);
                    navigate(`/workflows/${response}`);
                  })
                  .catch((error) => {
                    notifications.show({
                      title: 'Workflow Creation Failed',
                      message: `Workflow creation failed: ${error}`,
                      autoClose: 7000,
                      color: 'red',
                    });
                    console.error(`Error while creating new workflow:\n${error}`);
                  })
                  .finally(() => {
                    // close();
                  });
              }
            )}
          >
            <Stack>
              <TextInput
                label="Title"
                placeholder="Workflow Title"
                required
                data-autofocus
                {...workflowCreationForm.getInputProps('title')}
              />
              <Textarea
                label="Description"
                placeholder="Workflow description"
                resize="vertical"
                {...workflowCreationForm.getInputProps('description')}
              />

              <Group justify="flex-end" grow mt={'md'}>
                <Button
                  type="submit"
                  onSubmit={() => {
                    console.log('submitting');
                  }}
                >
                  Create
                </Button>
              </Group>
            </Stack>
          </form>
        </Modal>
        <Table>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Title</Table.Th>
              <Table.Th>Description</Table.Th>
              <Table.Th>Created On</Table.Th>
              <Table.Th>ModifiedOn</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>{rows}</Table.Tbody>
        </Table>
      </Container>
    </>
  );
}

export default PortalPage;
