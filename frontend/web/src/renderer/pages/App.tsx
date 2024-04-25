import {
    Box,
    Center,
    ChakraProvider,
    ColorModeScript,
    Spinner,
    VStack,
    Text,
} from "@chakra-ui/react";
import { LocalStorage } from "node-localstorage";
import { memo, useEffect, useRef, useState } from "react";
import { ipcRenderer } from "../../common/safeIpc";
import { AlertBoxContext, AlertBoxProvider, AlertType } from "../contexts/AlertBoxContext";
import { ContextMenuProvider } from "../contexts/ContextMenuContext";
import { useAsyncEffect } from "../hooks/useAsyncEffect";
import { Main, NodesInfo, processBackendResponse } from "../main";
import { theme } from "../theme";
import { HashRouter, Route, Routes } from "react-router-dom";
import { Portal } from "./Portal";
import log from "electron-log";
import useFetch, { CachePolicies } from "use-http";
import { BackendNodesResponse } from "../../common/Backend";
import { BackendProvider } from "../contexts/BackendContext";
import { GlobalProvider } from "../contexts/GlobalWorkflowState";
import { useContext } from "use-context-selector";
import { ReactFlowProvider } from "react-flow-renderer";
import { HistoryProvider } from "../components/HistoryProvider";
import { ExecutionProvider } from "../contexts/ExecutionContext";
import { SettingsProvider } from "../contexts/SettingsContext";
import { DisclosureProvider } from "../contexts/DisclosureContext";

const LoadingComponent = memo(() => (
    <Box
        h="full"
        w="full"
    >
        <Center
            h="full"
            w="full"
        >
            <Spinner />
        </Center>
    </Box>
));

export const App = memo(() => {
    const [port, setPort] = useState<number>(5001);
    const [storageInitialized, setStorageInitialized] = useState(false);
    const reactFlowWrapper = useRef<HTMLDivElement>(null);
    const { sendAlert } = useContext(AlertBoxContext);

    const [nodesInfo, setNodesInfo] = useState<NodesInfo | null>(null);
    useAsyncEffect(
        {
            supplier: () => ipcRenderer.invoke("get-localstorage-location"),
            successEffect: (location) => {
                (global as Record<string, unknown>).customLocalStorage = new LocalStorage(location);
                setStorageInitialized(true);
            },
        },
        []
    );
    // const reactFlowWrapper = useRef<HTMLDivElement>(null);

    const [backendReady, setBackendReady] = useState(false);

    const { loading, error, data, response } = useFetch<BackendNodesResponse>(
        `http://localhost:${port}/workflows/nodes`,
        { cachePolicy: CachePolicies.NO_CACHE, retries: 25 },
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
                        `A critical error occurred while processing the node data returned by the backend.` +
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

    // useLastWindowSize();

    // useIpcRendererListener(
    //     "show-collected-information",
    //     (_, info) => {
    //         const localStorage = getLocalStorage();
    //         const fullInfo = {
    //             ...info,
    //             settings: Object.fromEntries(
    //                 getStorageKeys(localStorage).map((k) => [k, localStorage.getItem(k)])
    //             ),
    //         };

    //         sendAlert({
    //             type: AlertType.INFO,
    //             title: "System information",
    //             message: JSON.stringify(fullInfo, undefined, 2),
    //             copyToClipboard: true,
    //         });
    //     },
    //     [sendAlert]
    // );

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
        <ChakraProvider theme={theme}>
            <ColorModeScript initialColorMode={theme.config.initialColorMode} />
            <ContextMenuProvider>
                <AlertBoxProvider>
                    <DisclosureProvider>
                        <ReactFlowProvider>
                            <SettingsProvider>
                                <BackendProvider
                                    categories={nodesInfo.categories}
                                    categoriesMissingNodes={nodesInfo.categoriesMissingNodes}
                                    functionDefinitions={nodesInfo.functionDefinitions}
                                    port={port}
                                    schemata={nodesInfo.schemata}
                                >
                                    <GlobalProvider reactFlowWrapper={reactFlowWrapper}>
                                        <ExecutionProvider>
                                            <HistoryProvider>
                                                {!port || !storageInitialized ? (
                                                    <LoadingComponent />
                                                ) : (
                                                    // <MainComponent port={port} />
                                                    <HashRouter>
                                                        <Routes>
                                                            <Route
                                                                path="/workflows/:id"
                                                                element={
                                                                    <Main
                                                                        port={port}
                                                                        reactFlowWrapper={
                                                                            reactFlowWrapper
                                                                        }
                                                                    />
                                                                }
                                                            />
                                                            <Route
                                                                path="/"
                                                                element={<Portal />}
                                                            />
                                                        </Routes>
                                                    </HashRouter>
                                                )}
                                            </HistoryProvider>
                                        </ExecutionProvider>
                                    </GlobalProvider>
                                </BackendProvider>
                            </SettingsProvider>
                        </ReactFlowProvider>
                    </DisclosureProvider>
                </AlertBoxProvider>
            </ContextMenuProvider>
        </ChakraProvider>
    );
});
