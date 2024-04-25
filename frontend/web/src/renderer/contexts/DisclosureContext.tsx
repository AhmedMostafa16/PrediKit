import { UseDisclosureReturn, useDisclosure } from "@chakra-ui/react";
import { createContext, memo, useContext } from "react";

interface DisclosureContextType {
    disclosure: UseDisclosureReturn;
}

const DisclosureContext = createContext<DisclosureContextType | undefined>(undefined);

export const useDisclosureContext = () => {
    const context = useContext(DisclosureContext);
    if (!context) {
        throw new Error("useDisclosureContext must be used within a DisclosureProvider");
    }
    return context;
};

export const DisclosureProvider = memo(({ children }: React.PropsWithChildren<unknown>) => {
    const disclosure = useDisclosure();

    return (
        <DisclosureContext.Provider value={{ disclosure }}>{children}</DisclosureContext.Provider>
    );
});
