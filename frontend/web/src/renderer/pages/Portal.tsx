import { DeleteIcon } from "@chakra-ui/icons";
import {
    AlertDialog,
    AlertDialogBody,
    AlertDialogContent,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogOverlay,
    Box,
    Button,
    IconButton,
    Table,
    TableContainer,
    Tbody,
    Td,
    Th,
    Thead,
    Tr,
    VStack,
    useDisclosure,
} from "@chakra-ui/react";
import log from "electron-log";
import { memo, useEffect, useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useContext } from "use-context-selector";
import { Workflow } from "../../common/common-types";
import { PortalHeader } from "../components/PortalHeader";
import { AlertBoxContext, AlertType } from "../contexts/AlertBoxContext";
import { BackendContext } from "../contexts/BackendContext";
import { GlobalContext } from "../contexts/GlobalWorkflowState";

export const Portal = memo(() => {
    const { setCurrentWorkflowId, setCurrentWorkflow, loadWorkflow } = useContext(GlobalContext);
    const { backend } = useContext(BackendContext);
    const { showAlert, sendToast } = useContext(AlertBoxContext);
    const [workflows, setWorkflows] = useState<Workflow[]>([]);
    const navigate = useNavigate();
    const { isOpen, onOpen, onClose } = useDisclosure();

    const cancelRef = useRef<HTMLDivElement | HTMLButtonElement | null>(null);

    const fetchWorkflows = async () => {
        try {
            const result = await backend.getAllWorkflows();
            setWorkflows(result); // Update workflows state
            log.info("Workflows: ", result); // Log the updated result
        } catch (error) {
            log.error("Error fetching workflows:", error);
        }
    };

    useEffect(() => {
        // Fetch workflows on component mount
        fetchWorkflows();
    }, [backend.getAllWorkflows]);

    useEffect(() => {
        // Fetch workflows every 5 seconds
        const interval = setInterval(fetchWorkflows, 5000);
        return () => clearInterval(interval);
    }, [backend.getAllWorkflows]);

    const load = (workflow: Workflow) => {
        setCurrentWorkflowId(workflow.id);
        setCurrentWorkflow(workflow);
        // eslint-disable-next-line @typescript-eslint/no-floating-promises
        loadWorkflow(workflow.id);
        navigate(`/workflows/${workflow.id}`);
    };

    const elements = workflows.map((workflow: Workflow) => {
        return (
            <Tr key={workflow.id}>
                <Td
                    onClick={() => {
                        load(workflow);
                    }}
                >
                    {workflow.title}
                </Td>
                <Td
                    onClick={() => {
                        load(workflow);
                    }}
                >
                    {new Date(workflow.updatedAt).toLocaleString()}
                </Td>
                <Td
                    onClick={() => {
                        load(workflow);
                    }}
                >
                    {new Date(workflow.createdAt).toLocaleString()}
                </Td>
                <Td>
                    <IconButton
                        aria-label="Delete"
                        icon={<DeleteIcon />}
                        onClick={() => {
                            onOpen();
                        }}
                    />
                    <AlertDialog
                        isCentered
                        isOpen={isOpen}
                        leastDestructiveRef={cancelRef}
                        onClose={onClose}
                    >
                        <AlertDialogOverlay>
                            <AlertDialogContent>
                                <AlertDialogHeader
                                    fontSize="lg"
                                    fontWeight="bold"
                                >
                                    Delete Workflow
                                </AlertDialogHeader>

                                <AlertDialogBody>
                                    Are you sure? You can't undo this action afterwards.
                                </AlertDialogBody>

                                <AlertDialogFooter>
                                    <Button onClick={onClose}>Cancel</Button>
                                    <Button
                                        colorScheme="red"
                                        ml={3}
                                        onClick={() => {
                                            try {
                                                backend
                                                    .deleteWorkflow(workflow.id)
                                                    .then(() => {
                                                        sendToast({
                                                            description:
                                                                "The workflow has been successfully deleted.",
                                                            status: "success",
                                                        });
                                                    })
                                                    .catch((error: any) => {
                                                        log.error(
                                                            "Error deleting workflow:",
                                                            error
                                                        );
                                                        showAlert({
                                                            title: "Error deleting workflow",
                                                            message: error.message,
                                                            type: AlertType.ERROR,
                                                        });
                                                    });
                                                fetchWorkflows().then(() => {});
                                            } catch (error: any) {
                                                log.error("Error deleting workflow:", error);
                                                showAlert({
                                                    title: "Error deleting workflow",
                                                    message: error.message,
                                                    type: AlertType.ERROR,
                                                });
                                            }
                                            onClose();
                                        }}
                                    >
                                        Delete
                                    </Button>
                                </AlertDialogFooter>
                            </AlertDialogContent>
                        </AlertDialogOverlay>
                    </AlertDialog>
                </Td>
            </Tr>
        );
    });

    // console.log("Workflows: ", elements);

    const columns = useMemo(() => {
        return (
            <Tr>
                <Th>Title</Th>
                <Th>Last Updated</Th>
                <Th>Created</Th>
                <Th>Delete</Th>
            </Tr>
        );
    }, []);

    return (
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
                overflow="scroll"
                w="100%"
            >
                <TableContainer m={8}>
                    <Table
                        size="lg"
                        variant="simple"
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
    );
});
