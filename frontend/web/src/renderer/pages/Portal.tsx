import {
    Text,
    Table,
    TableContainer,
    Tbody,
    Td,
    Tfoot,
    Th,
    Thead,
    Tr,
    Box,
    VStack,
} from "@chakra-ui/react";
import { memo, useEffect, useMemo, useState } from "react";
import { getBackend } from "../../common/Backend";
import { BackendContext } from "../contexts/BackendContext";
import { useContext } from "use-context-selector";
import { Workflow } from "../../common/common-types";
import { PortalHeader } from "../components/PortalHeader";
import { GlobalContext } from "../contexts/GlobalWorkflowState";
import log from "electron-log";
import { useNavigate } from "react-router-dom";

export const Portal = memo(() => {
    const { /*  getAllWorkflows, */ setCurrentWorkflowId, setCurrentWorkflow } =
        useContext(GlobalContext);
    const { backend } = useContext(BackendContext);
    const [workflows, setWorkflows] = useState<Workflow[]>([]);
    const navigate = useNavigate();

    const fetchWorkflows = async () => {
        try {
            const result = await backend.getAllWorkflows();
            setWorkflows(result); // Update workflows state
            log.info("Workflows: ", result); // Log the updated result
        } catch (error) {
            console.error("Error fetching workflows:", error);
        }
    };

    useEffect(() => {
        fetchWorkflows();
    }, [backend]); // Update dependency array

    const elements = workflows.map((workflow: Workflow) => {
        return (
            <Tr
                key={workflow.id}
                onClick={() => {
                    setCurrentWorkflowId(workflow.id);
                    setCurrentWorkflow(workflow);
                    navigate(`/workflows/${workflow.id}`);
                }}
            >
                <Td>{workflow.title}</Td>
                <Td>{new Date(workflow.updatedAt).toLocaleString()}</Td>
                <Td>{new Date(workflow.createdAt).toLocaleString()}</Td>
            </Tr>
        );
    });

    console.log("Workflows: ", elements);

    const columns = useMemo(() => {
        return (
            <Tr>
                <Th>Title</Th>
                <Th>Last Updated</Th>
                <Th>Created</Th>
            </Tr>
        );
    }, []);

    return (
        <>
            <VStack
                bg="var(--window-bg)"
                h="100vh"
                overflow="hidden"
                p={2}
                w="100vw"
            >
                <PortalHeader />
                <Box
                    bg="var(--chain-editor-bg)"
                    borderRadius="lg"
                    borderWidth="0px"
                    h="100%"
                    w="100%"
                >
                    <TableContainer m={8}>
                        <Table
                            variant="simple"
                            size={"lg"}
                        >
                            {elements.length === 0 ? (
                                <Tr>
                                    <Td colSpan={3}>No workflows available</Td>
                                </Tr>
                            ) : (
                                <>
                                    <Thead>{columns}</Thead>
                                    <Tbody>{elements}</Tbody>
                                    {/* <Tfoot>{columns}</Tfoot> */}
                                </>
                            )}
                        </Table>
                    </TableContainer>
                </Box>
            </VStack>
        </>
    );
});
