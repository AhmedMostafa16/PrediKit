import { Container, Table } from '@mantine/core';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { Workflow } from '@/models/Workflow';
import PortalHeader from '@/components/PortalHeader/PortalHeader';
import { useStore } from '@/stores/store';

interface WorkflowTable {
  id: string;
  title: string;
  description: string;
  createdOn: string;
  modifiedOn: string;
}

function PortalPage() {
  const { workflowStore } = useStore();
  const { workflows, loadWorkflows, loadWorkflow, setCurrentWorkflowId } = workflowStore;

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
      onClick={() => {
        loadWorkflow(element.id);
        navigate(`/workflows/${element.id}`);
        setCurrentWorkflowId(element.id);
      }}
    >
      <Table.Td>{element.title}</Table.Td>
      <Table.Td>{element.description}</Table.Td>
      <Table.Td>{new Date(element.createdOn).toLocaleString()}</Table.Td>
      <Table.Td>{new Date(element.modifiedOn).toLocaleString()}</Table.Td>
    </Table.Tr>
  ));

  return (
    <>
      <PortalHeader />
      <Container size="md">
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

export default observer(PortalPage);
