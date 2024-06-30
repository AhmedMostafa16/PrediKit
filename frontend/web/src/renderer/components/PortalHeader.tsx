import {
    Box,
    Flex,
    HStack,
    Heading,
    IconButton,
    Menu,
    MenuButton,
    MenuItem,
    MenuList,
    Spacer,
    Tag,
    useDisclosure,
} from "@chakra-ui/react";
import { ipcRenderer } from "electron";
import { memo, useState } from "react";
import { BsCodeSlash } from "react-icons/bs";
import { FaUser } from "react-icons/fa";
import { MdLogout } from "react-icons/md";
import { useNavigate } from "react-router-dom";
import { useContext } from "use-context-selector";
import { UserInfo } from "../../common/common-types";
import { UserContext } from "../contexts/UserContext";
import { useAsyncEffect } from "../hooks/useAsyncEffect";
import { CreateWorkflowButton } from "./CreateWorkflowModal";
import { AccountSettingsButton, SettingsButton } from "./SettingsModal";

export const PortalHeader = memo(() => {
    const [appVersion, setAppVersion] = useState("#.#.#");
    const { setUserInfo } = useContext(UserContext);
    const navigate = useNavigate();

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
                    <Menu>
                        <MenuButton
                            aria-label="Account"
                            as={IconButton}
                            icon={<FaUser />}
                            variant="outline"
                        />
                        <MenuList>
                            <AccountSettingsButton />
                            <MenuItem
                                icon={<MdLogout />}
                                onClick={() => {
                                    setUserInfo({} as UserInfo);
                                    navigate("/login");
                                }}
                            >
                                Logout
                            </MenuItem>
                        </MenuList>
                    </Menu>
                </HStack>
            </Flex>
        </Box>
    );
});
