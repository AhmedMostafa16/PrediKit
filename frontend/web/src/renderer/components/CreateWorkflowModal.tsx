import { AddIcon } from "@chakra-ui/icons";
import {
    Button,
    HStack,
    Icon,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Tooltip,
    Text,
    useDisclosure,
    FormControl,
    FormLabel,
    Input,
} from "@chakra-ui/react";
import { app, ipcRenderer } from "electron";
import React, { memo } from "react";
import { useContext } from "use-context-selector";
import { BackendContext } from "../contexts/BackendContext";
import { WorkflowDto } from "../../common/common-types";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { currentMigration } from "../../common/migrations";
import { AlertBoxContext, AlertType } from "../contexts/AlertBoxContext";
import { GlobalContext } from "../contexts/GlobalWorkflowState";

interface CreateWorkflowModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const CreateWorkflowModal = memo(({ isOpen, onClose }: CreateWorkflowModalProps) => {
    const [input, setInput] = useState<string>("");

    const handleInputChange = (e: any) => setInput(e.target.value);

    const { backend } = useContext(BackendContext);
    const { sendAlert } = useContext(AlertBoxContext);
    const { loadWorkflow } = useContext(GlobalContext);

    const navigate = useNavigate();

    const initialRef = React.useRef(null);
    const finalRef = React.useRef(null);

    return (
        <Modal
            isCentered
            isOpen={isOpen}
            returnFocusOnClose={false}
            scrollBehavior="inside"
            size="xl"
            onClose={onClose}
            blockScrollOnMount={true}
            initialFocusRef={initialRef}
            finalFocusRef={finalRef}
        >
            <ModalOverlay />
            <ModalContent>
                <ModalHeader>Create a New Workflow</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                    <FormControl isRequired>
                        <FormLabel>Workflow Title</FormLabel>
                        <Input
                            ref={initialRef}
                            placeholder="New Workflow"
                            min={3}
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
                                        migration: currentMigration ?? 0,
                                        version: ipcRenderer.invoke("get-app-version"),
                                        createdAt: new Date().getTime(),
                                        updatedAt: new Date().getTime(),
                                    } as WorkflowDto);

                                    console.log("Response", response);

                                    if (response.success) {
                                        console.log("Workflow created", response.data);
                                        loadWorkflow(response.data);
                                        navigate(`/workflow/${response.data}`);
                                        onClose();
                                    }
                                }
                            }}
                        >
                            Create
                        </Button>
                        <Button
                            colorScheme="blue"
                            mr={3}
                            onClick={onClose}
                            variant={"outline"}
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
