import { CloseIcon, CopyIcon, DeleteIcon, LockIcon, UnlockIcon } from "@chakra-ui/icons";
import { MenuItem, MenuList } from "@chakra-ui/react";
import { BsEyeFill, BsLayerForward } from "react-icons/bs";
import { MdPlayArrow, MdPlayDisabled } from "react-icons/md";
import { useContext } from "use-context-selector";
import { NodeData } from "../../common/common-types";
import { GlobalContext } from "../contexts/GlobalWorkflowState";
import { UseContextMenu, useContextMenu } from "./useContextMenu";
import { UseDisabled } from "./useDisabled";
import { useDisclosureContext } from "../contexts/DisclosureContext";

export interface UseNodeMenuOptions {
    canLock?: boolean;
}

export const useNodeMenu = (
    data: NodeData,
    useDisabled: UseDisabled,
    { canLock = true }: UseNodeMenuOptions = {}
): UseContextMenu => {
    const { id, isLocked = false, parentNode } = data;

    const { removeNodeById, clearNode, duplicateNode, toggleNodeLock, releaseNodeFromParent } =
        useContext(GlobalContext);
    const { isDirectlyDisabled, canDisable, toggleDirectlyDisabled } = useDisabled;

    const { disclosure } = useDisclosureContext();

    return useContextMenu(() => (
        <>
            <MenuList className="nodrag">
                <MenuItem
                    icon={<BsEyeFill />}
                    onClick={() => {
                        disclosure.onOpen();
                    }}
                >
                    Preview
                </MenuItem>

                <MenuItem
                    icon={<CopyIcon />}
                    onClick={() => {
                        duplicateNode(id);
                    }}
                >
                    Duplicate
                </MenuItem>
                <MenuItem
                    icon={<CloseIcon />}
                    onClick={() => {
                        clearNode(id);
                    }}
                >
                    Clear
                </MenuItem>
                {canDisable && (
                    <MenuItem
                        icon={isDirectlyDisabled ? <MdPlayArrow /> : <MdPlayDisabled />}
                        onClick={toggleDirectlyDisabled}
                    >
                        {isDirectlyDisabled ? "Enable" : "Disable"}
                    </MenuItem>
                )}

                {canLock && (
                    <MenuItem
                        icon={isLocked ? <UnlockIcon /> : <LockIcon />}
                        onClick={() => {
                            toggleNodeLock(id);
                        }}
                    >
                        {isLocked ? "Unlock" : "Lock"}
                    </MenuItem>
                )}
                <MenuItem
                    icon={<DeleteIcon />}
                    onClick={() => {
                        removeNodeById(id);
                    }}
                >
                    Delete
                </MenuItem>
                {parentNode && (
                    <MenuItem
                        icon={<BsLayerForward />}
                        onClick={() => {
                            releaseNodeFromParent(id);
                        }}
                    >
                        Release
                    </MenuItem>
                )}
            </MenuList>
        </>
    ));
};
