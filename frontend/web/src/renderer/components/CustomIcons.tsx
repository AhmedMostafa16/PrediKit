import { Icon } from "@chakra-ui/react";
import { memo } from "react";
import { IconType } from "react-icons";
import * as bs from "react-icons/bs";
import * as cg from "react-icons/cg";
import * as im from "react-icons/im";
import * as md from "react-icons/md";

const libraries = { bs, cg, md, im };

export const IconFactory = memo(
    ({
        icon,
        accentColor,
        boxSize = 4,
    }: {
        icon?: string;
        accentColor?: string;
        boxSize?: number;
    }) => {
        const unknownIcon = (
            <Icon
                alignContent="center"
                alignItems="center"
                as={bs.BsQuestionDiamond}
                boxSize={boxSize}
                color="gray.500"
                transition="0.15s ease-in-out"
            />
        );
        if (!icon) {
            return unknownIcon;
        }

        const prefix = icon.slice(0, 2).toLowerCase();
        const library = (libraries as Partial<Record<string, Partial<Record<string, IconType>>>>)[
            prefix
        ];
        if (!library) {
            return unknownIcon;
        }
        const libraryIcon = library[icon];
        return (
            <Icon
                alignContent="center"
                alignItems="center"
                as={libraryIcon}
                boxSize={boxSize}
                color={accentColor}
                transition="0.15s ease-in-out"
            />
        );
    }
);
