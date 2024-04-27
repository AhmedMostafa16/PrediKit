import { Box, Flex, HStack, Heading, IconButton, Spacer, Tag, Tooltip } from "@chakra-ui/react";
import { memo, useState } from "react";
import { BsCodeSlash } from "react-icons/bs";
import { IoPause, IoPlay, IoStop } from "react-icons/io5";
import { Link } from "react-router-dom";
import { useContext } from "use-context-selector";
import { Workflow } from "../../common/common-types";
import { ipcRenderer } from "../../common/safeIpc";
import { ExecutionContext, ExecutionStatus } from "../contexts/ExecutionContext";
import { GlobalContext } from "../contexts/GlobalWorkflowState";
import { useAsyncEffect } from "../hooks/useAsyncEffect";
import { SettingsButton } from "./SettingsModal";

export const EditorHeader = memo(() => {
    const { run, pause, kill, status } = useContext(ExecutionContext);
    const { setCurrentWorkflowId, setCurrentWorkflow } = useContext(GlobalContext);

    const [appVersion, setAppVersion] = useState("#.#.#");
    useAsyncEffect(
        {
            supplier: () => ipcRenderer.invoke("get-app-version"),
            successEffect: setAppVersion,
        },
        []
    );

    return (
        <Box
            bg="var(--header-bg)"
            borderRadius="lg"
            borderWidth="0px"
            h="56px"
            w="100%"
        >
            <Flex
                align="center"
                h="100%"
                p={2}
            >
                <HStack
                    as={Link}
                    to="/"
                    onClick={() => {
                        setCurrentWorkflowId("");
                        setCurrentWorkflow({} as Workflow);
                    }}
                >
                    {/* <LinkIcon /> */}
                    {/* <Image
                        boxSize="36px"
                        draggable={false}
                        src={logo}
                    /> */}
                    <BsCodeSlash size="36px" />
                    <Heading size="md">PrediKit</Heading>
                    <Tag>Alpha</Tag>
                    <Tag>{`v${appVersion}`}</Tag>
                </HStack>
                <Spacer />

                <HStack>
                    <Tooltip
                        closeOnClick
                        closeOnMouseDown
                        borderRadius={8}
                        label={status === ExecutionStatus.PAUSED ? "Resume (F5)" : "Run (F5)"}
                        px={2}
                        py={1}
                    >
                        <IconButton
                            aria-label="Run button"
                            colorScheme="green"
                            disabled={
                                !(
                                    status === ExecutionStatus.READY ||
                                    status === ExecutionStatus.PAUSED
                                )
                            }
                            icon={<IoPlay />}
                            size="md"
                            variant="outline"
                            onClick={() => {
                                // eslint-disable-next-line @typescript-eslint/no-floating-promises
                                run();
                            }}
                        />
                    </Tooltip>
                    <Tooltip
                        closeOnClick
                        closeOnMouseDown
                        borderRadius={8}
                        label="Pause (F6)"
                        px={2}
                        py={1}
                    >
                        <IconButton
                            aria-label="Pause button"
                            colorScheme="yellow"
                            disabled={status !== ExecutionStatus.RUNNING}
                            icon={<IoPause />}
                            size="md"
                            variant="outline"
                            onClick={() => {
                                // eslint-disable-next-line @typescript-eslint/no-floating-promises
                                pause();
                            }}
                        />
                    </Tooltip>
                    <Tooltip
                        closeOnClick
                        closeOnMouseDown
                        borderRadius={8}
                        label="Stop (F7)"
                        px={2}
                        py={1}
                    >
                        <IconButton
                            aria-label="Stop button"
                            colorScheme="red"
                            disabled={
                                !(
                                    status === ExecutionStatus.RUNNING ||
                                    status === ExecutionStatus.PAUSED
                                )
                            }
                            icon={<IoStop />}
                            size="md"
                            variant="outline"
                            onClick={() => {
                                // eslint-disable-next-line @typescript-eslint/no-floating-promises
                                kill();
                            }}
                        />
                    </Tooltip>
                </HStack>
                <Spacer />
                <HStack>
                    <SettingsButton />
                </HStack>
            </Flex>
        </Box>
    );
});