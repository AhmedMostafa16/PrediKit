import log from "electron-log";
import { extname } from "path";
import { XYPosition } from "react-flow-renderer";
import { SchemaId } from "../../common/common-types";
import { ipcRenderer } from "../../common/safeIpc";
import { openSaveFile } from "../../common/SaveFile";
import { SchemaMap } from "../../common/SchemaMap";
import { NodeProto } from "./reactFlowUtil";

export interface PrediKitDragData {
    schemaId: SchemaId;
    offsetX?: number;
    offsetY?: number;
}

export const enum TransferTypes {
    PrediKitSchema = "application/predikit/schema",
}

export interface DataTransferProcessorOptions {
    createNode: (proto: NodeProto) => void;
    getNodePosition: (offsetX?: number, offsetY?: number) => XYPosition;
    schemata: SchemaMap;
}

export const getSingleFileWithExtension = (
    dataTransfer: DataTransfer,
    allowedExtensions: readonly string[]
): string | undefined => {
    if (dataTransfer.files.length === 1) {
        const [file] = dataTransfer.files;
        const extension = extname(file.path).toLowerCase();
        if (allowedExtensions.includes(extension)) {
            return file.path;
        }
    }
    return undefined;
};

/**
 * Returns `false` if the data could not be processed by this processor.
 *
 * Returns `true` if the data has been successfully transferred.
 */
export type DataTransferProcessor = (
    dataTransfer: DataTransfer,
    options: DataTransferProcessorOptions
) => boolean;

const predikitSchemaProcessor: DataTransferProcessor = (
    dataTransfer,
    { getNodePosition, createNode, schemata }
) => {
    if (!dataTransfer.getData(TransferTypes.PrediKitSchema)) return false;

    const { schemaId, offsetX, offsetY } = JSON.parse(
        dataTransfer.getData(TransferTypes.PrediKitSchema)
    ) as PrediKitDragData;

    const nodeSchema = schemata.get(schemaId);

    createNode({
        position: getNodePosition(offsetX, offsetY),
        data: { schemaId },
        nodeType: nodeSchema.nodeType,
    });
    return true;
};

const openPrediKitFileProcessor: DataTransferProcessor = (dataTransfer) => {
    if (dataTransfer.files.length === 1) {
        const [file] = dataTransfer.files;
        if (/\.pkw/i.test(file.path)) {
            // found a .pkw file

            openSaveFile(file.path)
                .then((result) => {
                    // TODO: 1 is hard-coded. Find a better way
                    ipcRenderer.sendTo(1, "file-open", result);
                })
                .catch((reason) => log.error(reason));

            return true;
        }
    }
    return false;
};

export const dataTransferProcessors: readonly DataTransferProcessor[] = [
    predikitSchemaProcessor,
    openPrediKitFileProcessor,
];
