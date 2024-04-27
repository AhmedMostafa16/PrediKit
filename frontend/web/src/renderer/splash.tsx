import { Center, ChakraProvider, Flex, Text, VStack } from "@chakra-ui/react";
import log from "electron-log";
import { memo, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { BsCodeSlash } from "react-icons/bs";
import { ipcRenderer } from "../common/safeIpc";
import { theme } from "./splashTheme";

const Splash = memo(() => {
    const [status, setStatus] = useState("Loading...");

    // Register event listeners
    useEffect(() => {
        // ipcRenderer.on("coonecting-backend", () => {
        //     setShowProgressBar(false);
        //     setOverallProgressPercentage(0.8);
        //     setStatus("Starting up process...");
        // });

        ipcRenderer.on("splash-finish", () => {
            log.info("Splash screen finished");
            setStatus("Loading main application...");
        });

        ipcRenderer.on("finish-loading", () => {
            log.info("Main application finished loading");
            setStatus("Starting the application...");
        });

        // ipcRenderer.on("progress", (event, percentage) => {
        //     log.info(`Progress: ${percentage}`);
        // });
    }, []);

    return (
        <ChakraProvider theme={theme}>
            <Center
                bg="gray.800"
                borderRadius="xl"
                color="white"
                h="400px"
                w="full"
            >
                <Flex
                    flexDirection="column"
                    w="full"
                >
                    <Center>
                        <BsCodeSlash size={256} />
                    </Center>
                    <VStack
                        bottom={0}
                        position="relative"
                        spacing={2}
                        top={8}
                        w="full"
                    >
                        <Center>
                            <Text
                                color="gray.500"
                                textOverflow="ellipsis"
                            >
                                {status}
                            </Text>
                        </Center>
                    </VStack>
                </Flex>
            </Center>
        </ChakraProvider>
    );
});

const container = document.getElementById("root");
const root = createRoot(container!);
root.render(<Splash />);
