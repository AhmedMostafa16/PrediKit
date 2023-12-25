import { createContext, useContext } from "react";
import WorkflowStore from "./WorkflowStore";

interface Store {
	workflowStore: WorkflowStore;

}

export const store: Store = {
	workflowStore: new WorkflowStore(),
};

export const StoreContext = createContext(store);

export function useStore() {
	return useContext(StoreContext);
}