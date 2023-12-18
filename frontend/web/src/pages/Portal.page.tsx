import { Container, Table } from '@mantine/core';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { shallow } from 'zustand/shallow';
import useFlowStore, { FlowState } from '@/stores/FlowStore';
import { CreateWorkflowDto, Workflow } from '@/models/Workflow';
import { PortalHeader } from '@/components/PortalHeader/PortalHeader';

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

export default PortalPage;
