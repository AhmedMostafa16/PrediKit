/* eslint-disable react/jsx-props-no-spreading */

import {
    Box,
    Button,
    Card,
    CardBody,
    CardHeader,
    Center,
    Container,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Input,
    InputGroup,
    InputRightElement,
    Link,
    Stack,
    Text,
} from "@chakra-ui/react";
import React, { memo } from "react";
import { FieldValues, useForm } from "react-hook-form";
import { BsFillEyeFill, BsFillEyeSlashFill } from "react-icons/bs";
import { Navigate, Link as ReactRouterLink, useNavigate } from "react-router-dom";
import { useContext } from "use-context-selector";
import { RegisterUserDto } from "../../common/common-types";
import { AlertBoxContext } from "../contexts/AlertBoxContext";
import { BackendContext } from "../contexts/BackendContext";
import { UserContext } from "../contexts/UserContext";

export const Register = memo(() => {
    const navigate = useNavigate();
    const { getIsLoggedIn, setUserInfo } = useContext(UserContext);

    const {
        handleSubmit,
        register,
        formState: { errors, isSubmitting },
    } = useForm();
    const { backend } = useContext(BackendContext);
    const { sendToast } = useContext(AlertBoxContext);
    const [show, setShow] = React.useState(false);
    const handleClick = () => setShow(!show);

    const onSubmit = async (values: FieldValues) => {
        console.log(values);
        const user: RegisterUserDto = {
            fullname: values.fullname,
            email: values.email,
            password: values.password,
        };

        const result = await backend.register(user);
        if (result.success) {
            console.log("User registered successfully");
            setUserInfo(result.data);
            navigate("/workflows");
        } else {
            sendToast({
                title: "User registration failed",
                description: result.error,
                status: "error",
            });
        }
    };

    if (getIsLoggedIn()) {
        return <Navigate to="/workflows" />;
    }

    return (
        <Container>
            <Center h="100vh">
                <Stack>
                    <Text
                        align="center"
                        fontSize="5xl"
                        fontWeight={600}
                        mb="2rem"
                    >
                        Welcome to PrediKit
                    </Text>
                    <Card>
                        <CardHeader>
                            <Text
                                align="center"
                                fontSize="3xl"
                            >
                                Register
                            </Text>
                        </CardHeader>
                        <CardBody>
                            <Box>
                                <form onSubmit={handleSubmit(onSubmit)}>
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
                                            isRequired
                                            isInvalid={!!errors.password}
                                        >
                                            <FormLabel htmlFor="password">Password</FormLabel>
                                            <InputGroup size="md">
                                                <Input
                                                    id="password"
                                                    placeholder="Enter password"
                                                    pr="4.5rem"
                                                    type={show ? "text" : "password"}
                                                    {...register("password", {
                                                        required: "This is required",
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
                                                        {show ? (
                                                            <BsFillEyeSlashFill />
                                                        ) : (
                                                            <BsFillEyeFill />
                                                        )}
                                                    </Button>
                                                </InputRightElement>
                                            </InputGroup>
                                            <FormErrorMessage>
                                                {errors.password && String(errors.password.message)}
                                            </FormErrorMessage>
                                        </FormControl>

                                        <Button
                                            isLoading={isSubmitting}
                                            mt={4}
                                            type="submit"
                                        >
                                            Sign Up
                                        </Button>

                                        <Text mt={4}>
                                            Already have an account?{" "}
                                            <Link
                                                as={ReactRouterLink}
                                                color="blue.500"
                                                to="/"
                                            >
                                                Login
                                            </Link>
                                        </Text>
                                    </Stack>
                                </form>
                            </Box>
                        </CardBody>
                    </Card>
                </Stack>
            </Center>
        </Container>
    );
});
