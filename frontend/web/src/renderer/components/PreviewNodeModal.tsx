import {
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Table,
    Tbody,
    Td,
    Th,
    Thead,
    Tr,
} from "@chakra-ui/react";
import React, { memo, useEffect } from "react";
import { useContext } from "use-context-selector";
import { AlertBoxContext, AlertType } from "../contexts/AlertBoxContext";
import { useDisclosureContext } from "../contexts/DisclosureContext";
import { GlobalContext } from "../contexts/GlobalWorkflowState";

interface PreviewNodeModalProps {
    nodeId: string;
}

interface DataSetRecord {
    [key: string]: any;
}

export const PreviewNodeModal = memo(({ nodeId }: PreviewNodeModalProps) => {
    const { disclosure } = useDisclosureContext();
    const initialRef = React.useRef(null);

    const { getOutputData } = useContext(GlobalContext);
    const { sendAlert } = useContext(AlertBoxContext);

    const [dataset, setDataset] = React.useState<DataSetRecord[]>([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const result = await getOutputData(nodeId, 1);
                if (result) {
                    const parsedData = JSON.parse(result) as DataSetRecord[];
                    setDataset(parsedData);
                }
            } catch (error: any) {
                sendAlert({
                    title: "Error fetching preview data",
                    message: `An error occurred while fetching preview data ${error.message}`,
                    type: AlertType.ERROR,
                });
            }
        };
        if (disclosure.isOpen) fetchData();
    }, [disclosure.isOpen]);

    let propertyNames: string[] = [];
    const values: any[] = [];
    if (dataset && dataset.length > 0) {
        propertyNames = Object.keys(dataset[0]);

        for (let i = 0; i < dataset.length; i += 1) {
            values.push(Object.values(dataset[i]));
        }
    }
    return (
        <Modal
            blockScrollOnMount
            closeOnEsc
            isCentered
            closeOnOverlayClick={false}
            initialFocusRef={initialRef}
            isOpen={disclosure.isOpen}
            returnFocusOnClose={false}
            scrollBehavior="inside"
            size="full"
            onClose={disclosure.onClose}
        >
            <ModalOverlay />
            <ModalContent>
                <ModalHeader>Preview Data</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                    {/* <table /> */}
                    <Table>
                        <Thead>
                            <Tr>
                                {/* Assuming the keys are same across all records, taking keys from the first record */}
                                {dataset.length > 0 &&
                                    propertyNames.map((key, index) => <Th key={index}>{key}</Th>)}
                            </Tr>
                        </Thead>
                        <Tbody>
                            {dataset.length > 0 &&
                                values.map((record, index) => (
                                    <Tr key={index}>
                                        {record.map((value: any, index: number) => (
                                            <Td key={index}>{value}</Td>
                                        ))}
                                    </Tr>
                                ))}
                        </Tbody>
                    </Table>
                </ModalBody>

                <ModalFooter />
            </ModalContent>
        </Modal>
    );
});
