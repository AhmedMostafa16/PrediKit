import { UseDisclosureReturn, useDisclosure } from "@chakra-ui/react";
import { createContext, memo, useContext, useMemo } from "react";

interface DisclosureContextType {
    disclosure: UseDisclosureReturn;
}

export const DisclosureContext = createContext<DisclosureContextType | undefined>(undefined);

export const useDisclosureContext = () => {
    const context = useContext(DisclosureContext);
    if (!context) {
        throw new Error("useDisclosureContext must be used within a DisclosureProvider");
    }
    return context;
};

export const DisclosureProvider = memo(({ children }: React.PropsWithChildren<unknown>) => {
    const disclosure = useDisclosure();

    const contextValue = useMemo(() => ({ disclosure }), [disclosure]);

    return <DisclosureContext.Provider value={contextValue}>{children}</DisclosureContext.Provider>;
});
