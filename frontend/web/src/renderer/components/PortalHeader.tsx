import {
    Box,
    Button,
    Flex,
    HStack,
    Heading,
    IconButton,
    Spacer,
    Tag,
    Tooltip,
} from "@chakra-ui/react";
import { ipcRenderer } from "electron";
import { memo, useState } from "react";
import { BsCodeSlash } from "react-icons/bs";
import { useAsyncEffect } from "../hooks/useAsyncEffect";
import { SettingsButton } from "./SettingsModal";
import { CreateWorkflowButton } from "./CreateWorkflowModal";

export const PortalHeader = memo(() => {
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
                <HStack>
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
                <Spacer />
                <HStack>
                    <CreateWorkflowButton />
                    <SettingsButton />
                </HStack>
            </Flex>
        </Box>
    );
});
