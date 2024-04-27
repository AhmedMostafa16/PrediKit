import { AddIcon } from "@chakra-ui/icons";
import {
    Button,
    FormControl,
    FormLabel,
    HStack,
    Input,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Tooltip,
    useDisclosure,
} from "@chakra-ui/react";
import { ipcRenderer } from "electron";
import React, { memo, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useContext } from "use-context-selector";
import { currentMigration } from "../../common/migrations";
import { BackendContext } from "../contexts/BackendContext";
import { GlobalContext } from "../contexts/GlobalWorkflowState";
import { AlertBoxContext, AlertType } from "../contexts/AlertBoxContext";

interface CreateWorkflowModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const CreateWorkflowModal = memo(({ isOpen, onClose }: CreateWorkflowModalProps) => {
    const [input, setInput] = useState<string>("");

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => setInput(e.target.value);

    const { backend } = useContext(BackendContext);
    const { loadWorkflow, setCurrentWorkflowId } = useContext(GlobalContext);
    const { sendAlert } = useContext(AlertBoxContext);

    const navigate = useNavigate();

    const initialRef = React.useRef(null);
    const finalRef = React.useRef(null);

    return (
        <Modal
            blockScrollOnMount
            isCentered
            finalFocusRef={finalRef}
            initialFocusRef={initialRef}
            isOpen={isOpen}
            returnFocusOnClose={false}
            scrollBehavior="inside"
            size="xl"
            onClose={onClose}
        >
            <ModalOverlay />
            <ModalContent>
                <ModalHeader>Create a New Workflow</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                    <FormControl isRequired>
                        <FormLabel>Workflow Title</FormLabel>
                        <Input
                            min={3}
                            placeholder="New Workflow"
                            ref={initialRef}
                            value={input}
                            onChange={handleInputChange}
                        />
                    </FormControl>
                </ModalBody>

                <ModalFooter>
                    <HStack>
                        <Button
                            onClick={async () => {
                                console.log("Backend", backend.port);
                                if (backend) {
                                    const response = await backend.createWorkflow({
                                        title: input,
                                        nodes: [],
                                        edges: [],
                                        viewport: { x: 0, y: 0, zoom: 1 },
                                        migration: currentMigration,
                                        version: (await ipcRenderer.invoke(
                                            "get-app-version"
                                        )) as string,
                                        createdAt: new Date().getTime(),
                                        updatedAt: new Date().getTime(),
                                    });

                                    console.log("Response: ", response);

                                    if (response.type === "success") {
                                        const workflowId: string = response.message;
                                        console.log("Workflow created", workflowId);

                                        // Sleep for 1 second to allow the backend to update the workflow
                                        await new Promise((resolve) => setTimeout(resolve, 1000));

                                        // eslint-disable-next-line @typescript-eslint/no-floating-promises
                                        loadWorkflow(workflowId).then(() => {
                                            onClose();

                                            setCurrentWorkflowId(workflowId);
                                            navigate(`/workflows/${workflowId}`);
                                        });
                                    } else {
                                        console.error(
                                            "Failed to create workflow",
                                            response.message
                                        );
                                        sendAlert({
                                            title: "Failed to create workflow",
                                            message: response.message,
                                            type: AlertType.ERROR,
                                        });
                                    }
                                }
                            }}
                        >
                            Create
                        </Button>
                        <Button
                            colorScheme="blue"
                            mr={3}
                            variant="outline"
                            onClick={onClose}
                        >
                            Close
                        </Button>
                    </HStack>
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
});

export const CreateWorkflowButton = memo(() => {
    const { isOpen, onOpen, onClose } = useDisclosure();

    return (
        <>
            <Tooltip
                closeOnClick
                closeOnEsc
                closeOnMouseDown
                label="Create a new workflow"
                px={2}
                py={1}
            >
                <Button
                    aria-label="Create a new workflow"
                    leftIcon={<AddIcon />}
                    size="md"
                    onClick={onOpen}
                >
                    Create Workflow
                </Button>
            </Tooltip>
            <CreateWorkflowModal
                isOpen={isOpen}
                onClose={onClose}
            />
        </>
    );
});
