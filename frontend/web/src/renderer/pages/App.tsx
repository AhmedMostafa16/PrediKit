import { Box, Center, ChakraProvider, ColorModeScript, Spinner, VStack } from "@chakra-ui/react";
import log from "electron-log";
import { memo, useEffect, useRef, useState } from "react";
import { ReactFlowProvider } from "react-flow-renderer";
import { HashRouter, Route, RouteObject, Routes, createHashRouter } from "react-router-dom";
import { useContext } from "use-context-selector";
import useFetch, { CachePolicies } from "use-http";
import { BackendNodesResponse } from "../../common/Backend";
import { ipcRenderer } from "../../common/safeIpc";
import { HistoryProvider } from "../components/HistoryProvider";
import RequireAuth from "../components/RequireAuth";
import { AlertBoxContext, AlertBoxProvider, AlertType } from "../contexts/AlertBoxContext";
import { BackendProvider } from "../contexts/BackendContext";
import { ContextMenuProvider } from "../contexts/ContextMenuContext";
import { DisclosureProvider } from "../contexts/DisclosureContext";
import { ExecutionProvider } from "../contexts/ExecutionContext";
import { GlobalProvider } from "../contexts/GlobalWorkflowState";
import { SettingsProvider } from "../contexts/SettingsContext";
import { UserProvider } from "../contexts/UserContext";
import { useAsyncEffect } from "../hooks/useAsyncEffect";
import { theme } from "../theme";
import { Login } from "./Login";
import { Main, NodesInfo, processBackendResponse } from "./Main";
import { Portal } from "./Portal";
import { Register } from "./Register";

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
            successEffect: () => {
                const { localStorage } = window;
                localStorage.getItem("user-info");
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

    if (!nodesInfo || !data || !storageInitialized) {
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
                        <Spinner />
                    </VStack>
                </Center>
            </Box>
        );
    }

    const routes: RouteObject[] = [
        {
            path: "/",
            element: <Login />,
            children: [
                // {
                //     element: <RequireAuth />,
                //     children: [
                { path: "workflows", element: <Portal /> },

                // ],
                // },
                { path: "register", element: <Register /> },
            ],
        },
    ];

    const router = createHashRouter(routes);

    return (
        <ChakraProvider theme={theme}>
            <ColorModeScript initialColorMode={theme.config.initialColorMode} />
            <UserProvider>
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
                                                                    element={<Login />}
                                                                    path="/login"
                                                                />
                                                                <Route
                                                                    element={<Register />}
                                                                    path="/register"
                                                                />
                                                                <Route
                                                                    element={<RequireAuth />}
                                                                    path="/"
                                                                >
                                                                    <Route
                                                                        element={<Portal />}
                                                                        path="workflows"
                                                                    />
                                                                    <Route
                                                                        element={
                                                                            <Main
                                                                                port={port}
                                                                                reactFlowWrapper={
                                                                                    reactFlowWrapper
                                                                                }
                                                                            />
                                                                        }
                                                                        path="workflows/:id"
                                                                    />
                                                                </Route>
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
            </UserProvider>
        </ChakraProvider>
    );
});
