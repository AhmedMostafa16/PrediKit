import { Box, Center, HStack, Text, VStack } from "@chakra-ui/react";
import log from "electron-log";
import { memo, useEffect, useState } from "react";
import { EdgeTypes, NodeTypes } from "react-flow-renderer";
import { useContext } from "use-context-selector";
import useFetch, { CachePolicies } from "use-http";
import { BackendNodesResponse } from "../common/Backend";
import { Category, NodeType, SchemaId } from "../common/common-types";
import { ipcRenderer } from "../common/safeIpc";
import { SchemaMap } from "../common/SchemaMap";
import { FunctionDefinition } from "../common/types/function";
import { getPredikitScope } from "../common/types/predikit-scope";
import { getLocalStorage, getStorageKeys } from "../common/util";
import { CustomEdge } from "./components/CustomEdge";
import { EditorHeader } from "./components/EditorHeader";
import { IteratorHelperNode } from "./components/node/IteratorHelperNode";
import { IteratorNode } from "./components/node/IteratorNode";
import { Node } from "./components/node/Node";
import { NodeSelector } from "./components/NodeSelectorPanel/NodeSelectorPanel";
import { ReactFlowBox } from "./components/ReactFlowBox";
import { AlertBoxContext, AlertType } from "./contexts/AlertBoxContext";
import { useIpcRendererListener } from "./hooks/useIpcRendererListener";
import { useLastWindowSize } from "./hooks/useLastWindowSize";

export interface NodesInfo {
    schemata: SchemaMap;
    categories: Category[];
    functionDefinitions: Map<SchemaId, FunctionDefinition>;
    categoriesMissingNodes: string[];
}

export const processBackendResponse = ({
    nodes,
    categories,
    categoriesMissingNodes,
}: BackendNodesResponse): NodesInfo => {
    const schemata = new SchemaMap(nodes);

    const functionDefinitions = new Map<SchemaId, FunctionDefinition>();

    const errors: string[] = [];

    for (const schema of nodes) {
        try {
            functionDefinitions.set(
                schema.schemaId,
                FunctionDefinition.fromSchema(schema, getPredikitScope())
            );
        } catch (error) {
            errors.push(String(error));
        }
    }

    if (errors.length) {
        throw new Error(errors.join("\n\n"));
    }

    return { schemata, categories, functionDefinitions, categoriesMissingNodes };
};

const nodeTypes: NodeTypes & Record<NodeType, unknown> = {
    regularNode: Node,
    iterator: IteratorNode,
    iteratorHelper: IteratorHelperNode,
};
const edgeTypes: EdgeTypes = {
    main: CustomEdge,
};

interface MainProps {
    port: number;
    reactFlowWrapper: React.RefObject<HTMLDivElement>;
}

export const Main = memo(({ port, reactFlowWrapper }: MainProps) => {
    const { sendAlert } = useContext(AlertBoxContext);

    const [nodesInfo, setNodesInfo] = useState<NodesInfo | null>(null);

    // const reactFlowWrapper = useRef<HTMLDivElement>(null);

    const [backendReady, setBackendReady] = useState(false);

    const { loading, error, data, response } = useFetch<BackendNodesResponse>(
        `http://localhost:${port}/workflows/nodes`,
        { cachePolicy: CachePolicies.NO_CACHE, retries: 250 },
        [port]
    );

    useEffect(() => {
        if (response.ok && data && !loading && !error && !backendReady) {
            try {
                setNodesInfo(processBackendResponse(data));
            } catch (e) {
                log.error(e);
                sendAlert({
                    type: AlertType.CRIT_ERROR,
                    title: "Unable to process backend nodes",
                    message:
                        "A critical error occurred while processing the node data returned by the backend." +
                        `\n\n${String(e)}`,
                    copyToClipboard: true,
                });
            }
            setBackendReady(true);
            ipcRenderer.send("backend-ready");
        }

        if (error) {
            sendAlert(
                AlertType.CRIT_ERROR,
                null,
                `PrediKit has encountered a critical error: ${error.message}`
            );
            setBackendReady(true);
            ipcRenderer.send("backend-ready");
        }
    }, [response, data, loading, error, backendReady]);

    useLastWindowSize();

    useIpcRendererListener(
        "show-collected-information",
        (_, info) => {
            const localStorage = getLocalStorage();
            const fullInfo = {
                ...info,
                settings: Object.fromEntries(
                    getStorageKeys(localStorage).map((k) => [k, localStorage.getItem(k)])
                ),
            };

            sendAlert({
                type: AlertType.INFO,
                title: "System information",
                message: JSON.stringify(fullInfo, undefined, 2),
                copyToClipboard: true,
            });
        },
        [sendAlert]
    );

    if (error) return null;

    if (!nodesInfo || !data) {
        return (
            <Box
                h="100vh"
                w="100vw"
            >
                <Center
                    h="full"
                    w="full"
                >
                    <VStack>
                        {/* <BsCodeSlash size={256} /> */}
                        <Text>Loading...</Text>
                    </VStack>
                </Center>
            </Box>
        );
    }

    return (
        <VStack
            bg="var(--window-bg)"
            h="100vh"
            overflow="hidden"
            p={2}
            w="100vw"
        >
            <EditorHeader />
            <HStack
                h="calc(100vh - 80px)"
                minH="360px"
                minW="720px"
                w="full"
            >
                <NodeSelector />
                <ReactFlowBox
                    edgeTypes={edgeTypes}
                    nodeTypes={nodeTypes}
                    wrapperRef={reactFlowWrapper}
                />
            </HStack>
        </VStack>
    );
});
