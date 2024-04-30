import {
    Button,
    Center,
    Flex,
    Icon,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Spacer,
    useDisclosure,
} from "@chakra-ui/react";
import { Data, Layout } from "plotly.js";
import { memo, useEffect, useState } from "react";
import { BsEyeFill } from "react-icons/bs";
import Plot, { PlotParams } from "react-plotly.js";
import { useContextSelector } from "use-context-selector";
import { GlobalVolatileContext } from "../../contexts/GlobalWorkflowState";
import { OutputProps } from "./props";

export const PlotOutput = memo(({ label, id, outputId, useOutputData }: OutputProps) => {
    const type = useContextSelector(GlobalVolatileContext, (c) =>
        c.typeState.functions.get(id)?.outputs.get(outputId)
    );

    const [value] = useOutputData<string>(outputId);
    const [plotParams, setPlotParams] = useState<PlotParams | undefined>(undefined);

    useEffect(() => {
        setPlotParams(JSON.parse(value ?? "{}\n") as PlotParams);
    }, [id, outputId, value]);

    const { isOpen, onOpen, onClose } = useDisclosure();

    return (
        <Flex
            h="full"
            minH="2rem"
            verticalAlign="middle"
            w="full"
        >
            <Spacer />

            <Center
                cursor="pointer"
                h="2rem"
                verticalAlign="middle"
            >
                <Button
                    _hover={{
                        backgroundColor: "var(--node-image-preview-button-bg-hover)",
                    }}
                    bgColor="var(--node-image-preview-button-bg)"
                    borderRadius="md"
                    cursor="pointer"
                    disabled={!plotParams}
                    h="1.75rem"
                    leftIcon={
                        <Icon
                            as={BsEyeFill}
                            color="var(--node-image-preview-button-fg)"
                        />
                    }
                    maxH="1.75rem"
                    minH="1.75rem"
                    minW="1.75rem"
                    transition="0.15s ease-in-out"
                    onClick={onOpen}
                    isDisabled={!plotParams}
                >
                    Show Plot
                </Button>
            </Center>
            <Spacer />
            <Modal
                isOpen={isOpen}
                size="full"
                onClose={onClose}
            >
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>{label}</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody>
                        <Plot
                            useResizeHandler
                            data={plotParams?.data ?? ([] as Data[])}
                            layout={plotParams?.layout ?? ({} as Layout)}
                            style={{ width: "100%", height: "100%" }}
                        />
                    </ModalBody>

                    <ModalFooter>
                        <Button
                            colorScheme="blue"
                            mr={3}
                            onClick={onClose}
                        >
                            Close
                        </Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </Flex>
    );
});
