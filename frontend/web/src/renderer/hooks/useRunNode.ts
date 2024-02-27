import log from "electron-log";
import { useEffect, useMemo, useRef } from "react";
import { useContext } from "use-context-selector";
import { NodeData } from "../../common/common-types";
import { delay, getInputValues } from "../../common/util";
import { AlertBoxContext } from "../contexts/AlertBoxContext";
import { BackendContext } from "../contexts/BackendContext";
import { GlobalContext } from "../contexts/GlobalWorkflowState";
import { useAsyncEffect } from "./useAsyncEffect";

export const useRunNode = ({ inputData, id, schemaId }: NodeData, shouldRun: boolean): void => {
    const { sendToast } = useContext(AlertBoxContext);
    const { animate, unAnimate, getCurrentWorkflowId: getWorkflowId } = useContext(GlobalContext);
    const { schemata, backend } = useContext(BackendContext);

    const schema = schemata.get(schemaId);

    const didEverRun = useRef(false);

    const inputs = useMemo(
        () => getInputValues(schema, (inputId) => inputData[inputId] ?? null),
        [inputData]
    );
    const inputHash = useMemo(() => JSON.stringify(inputs), [inputData]);
    const lastInputHash = useRef<string>();
    useAsyncEffect(
        async (token) => {
            if (inputHash === lastInputHash.current) {
                return;
            }
            // give it some time for other effects to settle in
            await delay(50);
            token.checkCanceled();

            lastInputHash.current = inputHash;

            if (shouldRun) {
                didEverRun.current = true;
                animate([id], false);

                const result = await backend.runIndividual(
                    {
                        schemaId,
                        id,
                        inputs,
                    },
                    getWorkflowId() as string
                );

                if (!result.success) {
                    unAnimate([id]);
                    sendToast({
                        status: "error",
                        title: "Error",
                        description:
                            result.error ||
                            "Preview failed to load, probably unsupported file type.",
                    });
                }
            }
        },
        [shouldRun, inputHash]
    );

    useEffect(() => {
        return () => {
            if (didEverRun.current) {
                backend
                    .clearNodeCacheIndividual(id, getWorkflowId() as string)
                    .catch((error) => log.error(error));
            }
        };
    }, []);
};
