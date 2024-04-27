import { Tag } from "@chakra-ui/react";
import React, { memo } from "react";
import { StructType, Type } from "../../common/types/types";
import { isNumericLiteral } from "../../common/types/util";
import { without } from "../../common/types/without";

const nullType = new StructType("null");

const getTypeText = (type: Type): string[] => {
    if (isNumericLiteral(type)) return [type.toString()];

    const tags: string[] = [];
    if (type.type === "struct") {
        // if (isDataset(type)) {
        //     tags.push(`Dataset`);
        // }
    }
    return tags;
};

export interface TypeTagProps {
    isOptional?: boolean;
}

export const TypeTag = memo(({ children, isOptional }: React.PropsWithChildren<TypeTagProps>) => {
    return (
        <Tag
            bgColor="var(--tag-bg)"
            color="var(--tag-fg)"
            fontSize="x-small"
            fontStyle={isOptional ? "italic" : undefined}
            height="15px"
            lineHeight="auto"
            minHeight="15px"
            minWidth={0}
            ml={1}
            px={1}
            size="sm"
            variant="subtle"
        >
            {children}
        </Tag>
    );
});

export interface TypeTagsProps {
    type: Type;
    isOptional: boolean;
}

export const TypeTags = memo(({ type, isOptional }: TypeTagsProps) => {
    const tags = getTypeText(without(type, nullType));

    return (
        <>
            {tags.map((text) => (
                <TypeTag key={text}>{text}</TypeTag>
            ))}
            {isOptional && <TypeTag isOptional>optional</TypeTag>}
        </>
    );
});
