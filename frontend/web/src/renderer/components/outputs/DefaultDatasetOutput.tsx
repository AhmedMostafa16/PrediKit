/* eslint-disable @typescript-eslint/no-explicit-any */
import { Center, Flex, Spacer, Text } from "@chakra-ui/react";
import { memo, useEffect } from "react";
import { useReactFlow } from "react-flow-renderer";
import { useContext, useContextSelector } from "use-context-selector";
import { EdgeData, InputId, NodeData, SchemaId } from "../../../common/common-types";
import { NamedExpression, NamedExpressionField } from "../../../common/types/expression";
import { AnyType } from "../../../common/types/types";
import { createUniqueId, stringifySourceHandle, stringifyTargetHandle } from "../../../common/util";
import { GlobalContext, GlobalVolatileContext } from "../../contexts/GlobalWorkflowState";
import { TypeTags } from "../TypeTag";
import { OutputProps } from "./props";

const VIEW_SCHEMA_ID = "predikit:dataset:view" as SchemaId;

interface DatasetBroadcastData {
    columns: any[];
    data: any;
    index: any[];
    dtype: any[];
    shape: any[];
}

export const DefaultDatasetOutput = memo(({ label, id, outputId, useOutputData }: OutputProps) => {
    const type = useContextSelector(GlobalVolatileContext, (c) =>
        c.typeState.functions.get(id)?.outputs.get(outputId)
    );

    const createNode = useContextSelector(GlobalVolatileContext, (c) => c.createNode);
    const createConnection = useContextSelector(GlobalVolatileContext, (c) => c.createConnection);

    const { setManualOutputType } = useContext(GlobalContext);

    const inputHash = useContextSelector(GlobalVolatileContext, (c) => c.inputHashes.get(id));
    const [value, valueInputHash] = useOutputData<DatasetBroadcastData>(outputId);
    useEffect(() => {
        if (value && valueInputHash === inputHash) {
            setManualOutputType(
                id,
                outputId,
                new NamedExpression("Dataset", [
                    new NamedExpressionField("columns", AnyType.instance),
                    new NamedExpressionField("data", AnyType.instance),
                    new NamedExpressionField("index", AnyType.instance),
                    new NamedExpressionField("dtype", AnyType.instance),
                    new NamedExpressionField("shape", AnyType.instance),
                ])
            );
        } else {
            setManualOutputType(id, outputId, undefined);
        }
    }, [id, outputId, value]);

    const { getNodes } = useReactFlow<NodeData, EdgeData>();

    return (
        <Flex
            h="full"
            minH="2rem"
            verticalAlign="middle"
            w="full"
        >
            <Center
                cursor="pointer"
                h="2rem"
                w="2rem"
                onClick={() => {
                    const byId = new Map(getNodes().map((n) => [n.id, n]));

                    const containingNode = byId.get(id);
                    if (containingNode) {
                        const nodeId = createUniqueId();
                        // TODO: This is a bit of hardcoding, but it works
                        createNode(
                            {
                                id: nodeId,
                                position: {
                                    x: containingNode.position.x + (containingNode.width ?? 0) + 75,
                                    y: containingNode.position.y,
                                },
                                data: {
                                    schemaId: VIEW_SCHEMA_ID,
                                },
                                nodeType: "regularNode",
                            },
                            containingNode.parentNode
                        );
                        createConnection({
                            source: id,
                            sourceHandle: stringifySourceHandle(id, outputId),
                            target: nodeId,
                            targetHandle: stringifyTargetHandle(nodeId, 0 as InputId),
                        });
                    }
                }}
            >
                {/* <Center
                    _hover={{
                        backgroundColor: 'var(--node-image-preview-button-bg-hover)',
                    }}
                    bgColor="var(--node-image-preview-button-bg)"
                    borderRadius="md"
                    cursor="pointer"
                    h="1.75rem"
                    maxH="1.75rem"
                    maxW="1.75rem"
                    minH="1.75rem"
                    minW="1.75rem"
                    overflow="hidden"
                    transition="0.15s ease-in-out"
                    w="1.75rem"
                >
                    <Icon
                        as={BsEyeFill}
                        color="var(--node-image-preview-button-fg)"
                    />
                </Center> */}
            </Center>
            <Spacer />
            {type && (
                <Center
                    h="2rem"
                    verticalAlign="middle"
                >
                    <TypeTags
                        isOptional={false}
                        type={type}
                    />
                </Center>
            )}
            <Text
                h="full"
                lineHeight="2rem"
                marginInlineEnd="0.5rem"
                ml={1}
                textAlign="right"
            >
                {label}
            </Text>
        </Flex>
    );
});
