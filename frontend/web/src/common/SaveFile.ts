import { createHash } from "crypto";
import log from "electron-log";
import { readFile, writeFile } from "fs/promises";
import { Edge, Node, Viewport } from "react-flow-renderer";
import semver from "semver";
import { EdgeData, FileOpenResult, NodeData, Workflow } from "./common-types";
import { currentMigration, migrate } from "./migrations";

export interface ParsedSaveData extends Workflow {
    tamperedWith: boolean;
}

export interface RawSaveFile {
    version: string;
    content: Workflow;
    checksum?: string;
    migration?: number;
}

const hash = (value: string): string => {
    return createHash("sha512").update(value).digest("hex");
};

export class SaveFile {
    static parse(value: string): ParsedSaveData {
        if (!/^\s*\{/.test(value)) {
            // base64 decode
            // eslint-disable-next-line no-param-reassign
            value = Buffer.from(value, "base64").toString("utf-8");
        }

        const rawData = JSON.parse(value) as RawSaveFile;

        const { version, content, checksum, migration } = rawData;

        let data: Workflow = migrate(version, content, migration) as Workflow;
        const tamperedWith = checksum !== hash(JSON.stringify(content));

        return {
            ...data,
            tamperedWith,
        };
    }

    static async read(path: string): Promise<ParsedSaveData> {
        return SaveFile.parse(await readFile(path, { encoding: "utf-8" }));
    }

    static stringify(content: Workflow, version: string): string {
        const { nodes } = content;
        const sanitizedNodes = nodes.map<Node<NodeData>>((n) => ({
            data: {
                schemaId: n.data.schemaId,
                inputData: n.data.inputData,
                inputSize: n.data.inputSize,
                id: n.data.id,
                iteratorSize: n.data.iteratorSize,
                isDisabled: n.data.isDisabled,
                isLocked: n.data.isLocked,
                parentNode: n.data.parentNode,
            },
            id: n.id,
            position: n.position,
            type: n.type,
            selected: n.selected,
            height: n.height,
            width: n.width,
            zIndex: n.zIndex,
            parentNode: n.parentNode,
        }));
        const sanitizedContent = { ...content, nodes: sanitizedNodes };
        const data: Required<RawSaveFile> = {
            version,
            content: sanitizedContent,
            checksum: hash(JSON.stringify(sanitizedContent)),
            migration: currentMigration,
        };
        return JSON.stringify(data);
    }

    static async write(path: string, saveData: Workflow, version: string): Promise<void> {
        await writeFile(path, SaveFile.stringify(saveData, version), "utf-8");
    }
}

export const openSaveFile = async (path: string): Promise<FileOpenResult<ParsedSaveData>> => {
    try {
        const saveData = await SaveFile.read(path);
        return { kind: "Success", path, saveData };
    } catch (error) {
        log.error(error);
        return { kind: "Error", path, error: String(error) };
    }
};
