import { memo } from "react";
import { createContext } from "use-context-selector";
import { UserInfo } from "../../common/common-types";
import { useLocalStorage } from "../hooks/useLocalStorage";
import { useMemoObject } from "../hooks/useMemo";

interface UserContextType {
    getUserInfo: () => UserInfo;
    getIsLoggedIn: () => boolean;
    setUserInfo: (userInfo: UserInfo) => void;
}

export const UserContext = createContext<UserContextType>({} as UserContextType);

export const UserProvider = memo(({ children }: React.PropsWithChildren<unknown>) => {
    const [userInfo, setUserInfo] = useLocalStorage<UserInfo>("user-info", {} as UserInfo);

    const getUserInfo = (): UserInfo => {
        return userInfo;
    };

    const getIsLoggedIn = (): boolean => {
        return !!userInfo && !!userInfo.user && !!userInfo.user.id;
    };

    const contextValue = useMemoObject<UserContextType>({
        getUserInfo,
        getIsLoggedIn,
        setUserInfo,
    });

    return <UserContext.Provider value={contextValue}>{children}</UserContext.Provider>;
});
