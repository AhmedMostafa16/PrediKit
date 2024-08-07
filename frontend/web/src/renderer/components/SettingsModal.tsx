import { SettingsIcon } from "@chakra-ui/icons";
import {
    Button,
    Flex,
    FormControl,
    FormErrorMessage,
    FormHelperText,
    FormLabel,
    HStack,
    Icon,
    IconButton,
    Input,
    InputGroup,
    InputRightElement,
    MenuItem,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    NumberDecrementStepper,
    NumberIncrementStepper,
    NumberInput,
    NumberInputField,
    NumberInputStepper,
    Select,
    Stack,
    StackDivider,
    Switch,
    Tab,
    TabList,
    TabPanel,
    TabPanels,
    Tabs,
    Text,
    Tooltip,
    VStack,
    useDisclosure,
} from "@chakra-ui/react";
import { PropsWithChildren, ReactNode, memo, useState } from "react";
import { FieldValues, useForm } from "react-hook-form";
import { BsFillEyeFill, BsFillEyeSlashFill, BsPaletteFill } from "react-icons/bs";
import { FaTools } from "react-icons/fa";
import { useContext } from "use-context-selector";
import { UpdateUserDto } from "../../common/common-types";
import { ipcRenderer } from "../../common/safeIpc";
import { AlertBoxContext } from "../contexts/AlertBoxContext";
import { BackendContext } from "../contexts/BackendContext";
import { SettingsContext } from "../contexts/SettingsContext";
import { UserContext } from "../contexts/UserContext";

interface SettingsItemProps {
    title: ReactNode;
    description: ReactNode;
}

const SettingsItem = memo(
    ({ title, description, children }: PropsWithChildren<SettingsItemProps>) => {
        return (
            <Flex
                align="center"
                w="full"
            >
                <VStack
                    alignContent="left"
                    alignItems="left"
                    w="full"
                >
                    <Text
                        flex="1"
                        textAlign="left"
                    >
                        {title}
                    </Text>
                    <Text
                        flex="1"
                        fontSize="xs"
                        marginTop={0}
                        textAlign="left"
                    >
                        {description}
                    </Text>
                </VStack>
                <HStack>{children}</HStack>
            </Flex>
        );
    }
);

interface ToggleProps extends SettingsItemProps {
    isDisabled?: boolean;
    value: boolean;
    onToggle: () => void;
}

const Toggle = memo(({ title, description, isDisabled, value, onToggle }: ToggleProps) => {
    return (
        <SettingsItem
            description={description}
            title={title}
        >
            <Switch
                defaultChecked={value}
                isChecked={value}
                isDisabled={isDisabled}
                size="lg"
                onChange={onToggle}
            />
        </SettingsItem>
    );
});

interface DropdownProps extends SettingsItemProps {
    isDisabled?: boolean;
    value: string | number;
    options: { label: string; value: string | number }[];
    onChange: React.ChangeEventHandler<HTMLSelectElement>;
}

const Dropdown = memo(
    ({ title, description, isDisabled, value, options, onChange }: DropdownProps) => {
        return (
            <SettingsItem
                description={description}
                title={title}
            >
                <Select
                    isDisabled={isDisabled}
                    minWidth="350px"
                    value={value}
                    onChange={onChange}
                >
                    {options.map(({ label, value: v }) => (
                        <option
                            key={v}
                            value={v}
                        >
                            {label}
                        </option>
                    ))}
                </Select>
            </SettingsItem>
        );
    }
);

const AppearanceSettings = memo(() => {
    const { useSnapToGrid, useIsDarkMode, useAnimateChain } = useContext(SettingsContext);

    const [isDarkMode, setIsDarkMode] = useIsDarkMode;
    const [animateChain, setAnimateChain] = useAnimateChain;

    const [isSnapToGrid, setIsSnapToGrid, snapToGridAmount, setSnapToGridAmount] = useSnapToGrid;

    return (
        <VStack
            divider={<StackDivider />}
            w="full"
        >
            <Toggle
                description="Use dark mode throughout PrediKit."
                title="Dark theme"
                value={isDarkMode}
                onToggle={() => {
                    setIsDarkMode((prev) => !prev);
                }}
            />

            <Toggle
                description="Enable animations that show the processing state of the chain."
                title="Chain animation"
                value={animateChain}
                onToggle={() => {
                    setAnimateChain((prev) => !prev);
                }}
            />

            <Toggle
                description="Enable node grid snapping."
                title="Snap to grid"
                value={isSnapToGrid}
                onToggle={() => {
                    setIsSnapToGrid((prev) => !prev);
                }}
            />

            <SettingsItem
                description="The amount to snap the grid to."
                title="Snap to grid amount"
            >
                <NumberInput
                    defaultValue={snapToGridAmount || 1}
                    max={45}
                    min={1}
                    value={Number(snapToGridAmount || 1)}
                    onChange={(number: string) => setSnapToGridAmount(Number(number || 1))}
                >
                    <NumberInputField />
                    <NumberInputStepper>
                        <NumberIncrementStepper />
                        <NumberDecrementStepper />
                    </NumberInputStepper>
                </NumberInput>
            </SettingsItem>
        </VStack>
    );
});

const AdvancedSettings = memo(() => {
    const { useDisHwAccel } = useContext(SettingsContext);
    const [isDisHwAccel, setIsDisHwAccel] = useDisHwAccel;

    return (
        <VStack
            divider={<StackDivider />}
            w="full"
        >
            <Toggle
                description="Disable GPU hardware acceleration for rendering PrediKit's UI. Only disable this is you know hardware acceleration is causing you issues."
                title="Disable Hardware Acceleration (requires restart)"
                value={isDisHwAccel}
                onToggle={() => {
                    setIsDisHwAccel((prev) => !prev);
                }}
            />
        </VStack>
    );
});

interface SettingsModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const SettingsModal = memo(({ isOpen, onClose }: SettingsModalProps) => {
    return (
        <Modal
            isCentered
            isOpen={isOpen}
            returnFocusOnClose={false}
            scrollBehavior="inside"
            size="xl"
            onClose={onClose}
        >
            <ModalOverlay />
            <ModalContent
                maxH="500px"
                maxW="750px"
                minH="500px"
                minW="750px"
            >
                <ModalHeader>Settings</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                    <Tabs isFitted>
                        <TabList>
                            <Tab>
                                <HStack cursor="pointer">
                                    <Icon as={BsPaletteFill} />
                                    <Text cursor="pointer">Appearance</Text>
                                </HStack>
                            </Tab>
                            <Tab>
                                <HStack cursor="pointer">
                                    <Icon as={FaTools} />
                                    <Text cursor="pointer">Advanced</Text>
                                </HStack>
                            </Tab>
                        </TabList>
                        <TabPanels>
                            <TabPanel>
                                <AppearanceSettings />
                            </TabPanel>
                            <TabPanel>
                                <AdvancedSettings />
                            </TabPanel>
                        </TabPanels>
                    </Tabs>
                </ModalBody>

                <ModalFooter>
                    <HStack>
                        <Button
                            variant="ghost"
                            // eslint-disable-next-line @typescript-eslint/no-misused-promises
                            onClick={async () => {
                                await ipcRenderer.invoke("relaunch-application");
                            }}
                        >
                            Restart PrediKit
                        </Button>
                        <Button
                            colorScheme="blue"
                            mr={3}
                            onClick={onClose}
                        >
                            Close
                        </Button>
                    </HStack>
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
});

export const SettingsButton = memo(() => {
    const {
        isOpen: isSettingsOpen,
        onOpen: onSettingsOpen,
        onClose: onSettingsClose,
    } = useDisclosure();
    return (
        <>
            <Tooltip
                closeOnClick
                closeOnMouseDown
                borderRadius={8}
                label="Settings"
                px={2}
                py={1}
            >
                <IconButton
                    aria-label="Settings"
                    icon={<SettingsIcon />}
                    size="md"
                    variant="outline"
                    onClick={onSettingsOpen}
                >
                    Settings
                </IconButton>
            </Tooltip>
            <SettingsModal
                isOpen={isSettingsOpen}
                onClose={onSettingsClose}
            />
        </>
    );
});

const AccountSettingsModal = memo(({ isOpen, onClose }: SettingsModalProps) => {
    const { backend } = useContext(BackendContext);
    const { getUserInfo, setUserInfo } = useContext(UserContext);

    const {
        handleSubmit,
        register,
        formState: { errors, isSubmitting },
    } = useForm({
        defaultValues: {
            fullname: getUserInfo().user.fullname,
            email: getUserInfo().user.email,
            password: "",
        },
    });
    const { sendToast } = useContext(AlertBoxContext);
    const [show, setShow] = useState(false);
    const handleClick = () => setShow(!show);

    const onSubmit = async (values: FieldValues) => {
        console.log(values);
        const user: UpdateUserDto = {
            id: getUserInfo().user.id,
            fullname: values.fullname,
            email: values.email,
            password: values.password,
        };

        const result = await backend.updateAccount(user);
        if (result.success) {
            setUserInfo(result.data);
            onClose();
        } else {
            sendToast({
                title: "Account inforamtion update failed",
                description: result.error,
                status: "error",
            });
        }
    };

    return (
        <Modal
            isCentered
            isOpen={isOpen}
            returnFocusOnClose={false}
            scrollBehavior="inside"
            size="xl"
            onClose={onClose}
        >
            <ModalOverlay />
            <form onSubmit={handleSubmit(onSubmit)}>
                <ModalContent>
                    <ModalHeader>Account Settings</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody>
                        <Stack
                            p={0}
                            spacing={4}
                        >
                            <FormControl
                                isRequired
                                isInvalid={!!errors.fullname}
                            >
                                <FormLabel htmlFor="fullname">Full Name</FormLabel>
                                <Input
                                    id="fullname"
                                    placeholder="John Doe"
                                    {...register("fullname", {
                                        required: "This is required",
                                        minLength: {
                                            value: 3,
                                            message: "Minimum length should be 3",
                                        },
                                    })}
                                />
                                <FormErrorMessage>
                                    {errors.fullname && String(errors.fullname.message)}
                                </FormErrorMessage>
                            </FormControl>
                            <FormControl
                                isRequired
                                isInvalid={!!errors.email}
                            >
                                <FormLabel htmlFor="email">Email</FormLabel>
                                <Input
                                    id="email"
                                    placeholder="email@example.com"
                                    {...register("email", {
                                        required: "This is required",
                                        pattern: {
                                            value: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
                                            message: "Invalid email",
                                        },
                                    })}
                                />
                                <FormErrorMessage>
                                    {errors.email && String(errors.email.message)}
                                </FormErrorMessage>
                            </FormControl>

                            <FormControl
                                isInvalid={!!errors.password}
                                isRequired={false}
                            >
                                <FormLabel htmlFor="password">Password</FormLabel>
                                <FormHelperText>
                                    Leave blank if you do not wish to change the password.
                                </FormHelperText>
                                <InputGroup size="md">
                                    <Input
                                        id="password"
                                        placeholder="Enter password"
                                        pr="4.5rem"
                                        type={show ? "text" : "password"}
                                        {...register("password", {
                                            minLength: {
                                                value: 8,
                                                message: "Minimum length should be 8",
                                            },
                                        })}
                                    />
                                    <InputRightElement width="4rem">
                                        <Button
                                            h="1.75rem"
                                            size="sm"
                                            onClick={handleClick}
                                        >
                                            {show ? <BsFillEyeSlashFill /> : <BsFillEyeFill />}
                                        </Button>
                                    </InputRightElement>
                                </InputGroup>
                                <FormErrorMessage>
                                    {errors.password && String(errors.password.message)}
                                </FormErrorMessage>
                            </FormControl>
                        </Stack>
                    </ModalBody>
                    <ModalFooter>
                        <HStack>
                            <Button
                                colorScheme="blue"
                                isLoading={isSubmitting}
                                type="submit"
                                // eslint-disable-next-line @typescript-eslint/no-misused-promises
                                onClick={async () => {}}
                            >
                                Save
                            </Button>
                            <Button
                                mr={3}
                                variant="ghost"
                                onClick={onClose}
                            >
                                Close
                            </Button>
                        </HStack>
                    </ModalFooter>
                </ModalContent>
            </form>
        </Modal>
    );
});

export const AccountSettingsButton = memo(() => {
    const {
        isOpen: isAccountSettingsOpen,
        onOpen: onAccountSettingsOpen,
        onClose: onAccountSettingsClose,
    } = useDisclosure();
    return (
        <>
            <Tooltip
                closeOnClick
                closeOnMouseDown
                borderRadius={8}
                label="Account Settings"
                px={2}
                py={1}
            >
                <MenuItem
                    aria-label="Account"
                    icon={<SettingsIcon />}
                    onClick={onAccountSettingsOpen}
                >
                    Account Settings
                </MenuItem>
            </Tooltip>
            <AccountSettingsModal
                isOpen={isAccountSettingsOpen}
                onClose={onAccountSettingsClose}
            />
        </>
    );
});
