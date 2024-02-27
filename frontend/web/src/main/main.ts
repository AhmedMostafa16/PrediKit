/* eslint-disable @typescript-eslint/no-floating-promises */
/* eslint-disable @typescript-eslint/no-misused-promises */
import { BrowserWindow, app, dialog, nativeTheme, powerSaveBlocker } from "electron";
import log from "electron-log";
import { readdirSync, rmSync } from "fs";
import { LocalStorage } from "node-localstorage";
import os from "os";
import path from "path";
import { WindowSize } from "../common/common-types";
import { BrowserWindowWithSafeIpc, ipcMain } from "../common/safeIpc";
import { SaveFile, openSaveFile } from "../common/SaveFile";
import { lazy } from "../common/util";
import { getArguments } from "./arguments";
import { MenuData, setMainMenu } from "./menu";
import { useFetch } from "use-http";

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
// eslint-disable-next-line global-require
if (require("electron-squirrel-startup")) {
    app.quit();
}

const hasInstanceLock = app.requestSingleInstanceLock();

if (!hasInstanceLock) {
    app.quit();
}

const localStorageLocation = path.join(app.getPath("userData"), "settings");
ipcMain.handle("get-localstorage-location", () => localStorageLocation);
const localStorage = new LocalStorage(localStorageLocation);

const lastWindowSize = JSON.parse(
    localStorage.getItem("use-last-window-size") || "null"
) as WindowSize | null;
const disableHardwareAcceleration = localStorage.getItem("disable-hw-accel") === "true";
if (disableHardwareAcceleration) {
    app.disableHardwareAcceleration();
}

// log.transports.file.resolvePath = () => path.join(app.getAppPath(), 'logs/main.log');
log.transports.file.resolvePath = (variables) =>
    path.join(variables.electronDefaultDir!, variables.fileName!);
log.transports.file.level = "info";

process.env.ELECTRON_DISABLE_SECURITY_WARNINGS = "true";

const ownsBackend = !getArguments().noBackend;
ipcMain.handle("owns-backend", () => ownsBackend);

const registerEventHandlers = (mainWindow: BrowserWindowWithSafeIpc) => {
    ipcMain.handle("dir-select", (event, dirPath) =>
        dialog.showOpenDialog(mainWindow, {
            defaultPath: dirPath,
            properties: ["openDirectory", "createDirectory", "promptToCreate"],
        })
    );

    ipcMain.handle("file-select", (event, filters, allowMultiple = false, dirPath = undefined) =>
        dialog.showOpenDialog(mainWindow, {
            filters: [...filters, { name: "All Files", extensions: ["*"] }],
            defaultPath: dirPath,
            properties: allowMultiple ? ["openFile", "multiSelections"] : ["openFile"],
        })
    );

    ipcMain.handle("file-save-as-json", async (event, saveData, defaultPath) => {
        try {
            const { canceled, filePath } = await dialog.showSaveDialog(mainWindow, {
                title: "Save PrediKit Workflow File",
                filters: [{ name: "PrediKit Workflow File", extensions: ["pkw"] }],
                defaultPath,
            });
            if (!canceled && filePath) {
                await SaveFile.write(filePath, saveData, app.getVersion());
                return { kind: "Success", path: filePath };
            }
            return { kind: "Canceled" };
        } catch (error) {
            log.error(error);
            throw error;
        }
    });

    ipcMain.handle("file-save-json", async (event, saveData, savePath) => {
        try {
            await SaveFile.write(savePath, saveData, app.getVersion());
        } catch (error) {
            log.error(error);
            throw error;
        }
    });

    ipcMain.handle("quit-application", () => {
        app.exit();
    });

    ipcMain.handle("relaunch-application", async () => {
        app.relaunch();
        app.exit();
    });

    ipcMain.handle("get-app-version", () => app.getVersion());

    let blockerId: number | undefined;
    ipcMain.on("start-sleep-blocker", () => {
        if (blockerId === undefined) {
            blockerId = powerSaveBlocker.start("prevent-app-suspension");
        }
    });
    ipcMain.on("stop-sleep-blocker", () => {
        if (blockerId !== undefined) {
            powerSaveBlocker.stop(blockerId);
            blockerId = undefined;
        }
    });
};

const checkBackendConnection = async () => {
    log.info("Attempting to check for an internet connection...");
    ipcMain.handle("get-internet-state", () => {
        // const res =  useFetch('http://localhost:5001/ping').response.ok;
        return true;
    });
};

const doSplashScreenChecks = async (mainWindow: BrowserWindowWithSafeIpc) =>
    new Promise<void>((resolve) => {
        const splash = new BrowserWindow({
            width: 400,
            height: 400,
            frame: false,
            // backgroundColor: '#2D3748',
            center: true,
            minWidth: 400,
            minHeight: 400,
            maxWidth: 400,
            maxHeight: 400,
            resizable: false,
            minimizable: true,
            maximizable: false,
            closable: false,
            alwaysOnTop: true,
            titleBarStyle: "hidden",
            transparent: true,
            roundedCorners: true,
            webPreferences: {
                webSecurity: false,
                nodeIntegration: true,
                contextIsolation: false,
            },
            // icon: `${__dirname}/public/icons/cross_platform/icon`,
            show: false,
        }) as BrowserWindowWithSafeIpc;
        if (!splash.isDestroyed()) {
            try {
                splash.loadURL(SPLASH_SCREEN_WEBPACK_ENTRY);
                log.info("Loading splash window...");
            } catch (error) {
                log.error("Error loading splash window.", error);
            }
        }

        splash.once("ready-to-show", () => {
            splash.show();
            // splash.webContents.openDevTools();
        });

        splash.on("close", () => {
            mainWindow.destroy();
            resolve();
        });

        // Look, I just wanna see the cool animation
        const sleep = (ms: number) =>
            new Promise((r) => {
                setTimeout(r, ms);
            });

        // Send events to splash screen renderer as they happen
        // Added some sleep functions so I can see that this is doing what I want it to
        // TODO: Remove the sleeps (or maybe not, since it feels more like something is happening here)
        splash.webContents.once("dom-ready", async () => {
            log.info("Splash screen is ready.");
            splash.webContents.send("checking-port");
            await checkBackendConnection();
            log.info("Backend connection checked.");
            registerEventHandlers(mainWindow);
            log.info("Event handlers registered.");

            splash.webContents.send("splash-finish");
            log.info("Splash finish sent.");

            resolve();
            log.info("Resolve called.");
        });

        ipcMain.once("backend-ready", async () => {
            log.info("Backend is ready.");
            splash.webContents.send("finish-loading");
            log.info("Finish loading sent.");
            splash.on("close", () => {});
            await sleep(500);
            splash.destroy();
            mainWindow.show();
            // if (lastWindowSize?.maximized) {
            mainWindow.maximize();
            // }
        });
        log.info("Backend ready event handler registered.");
    });

const createWindow = lazy(async () => {
    // Create the browser window.
    const mainWindow = new BrowserWindow({
        width: lastWindowSize?.width ?? 1280,
        height: lastWindowSize?.height ?? 720,
        backgroundColor: "#1A202C",
        minWidth: 720,
        minHeight: 640,
        darkTheme: nativeTheme.shouldUseDarkColors,
        roundedCorners: true,
        webPreferences: {
            webSecurity: false,
            nodeIntegration: true,
            nodeIntegrationInWorker: true,
            contextIsolation: false,
        },
        // icon: `${__dirname}/public/icons/cross_platform/icon`,
        show: false,
    }) as BrowserWindowWithSafeIpc;

    const menuData: MenuData = { openRecentRev: [] };
    setMainMenu({ mainWindow, menuData, enabled: true });
    ipcMain.on("update-open-recent-menu", (_, openRecent) => {
        menuData.openRecentRev = openRecent;
        setMainMenu({ mainWindow, menuData, enabled: true });
    });
    ipcMain.on("disable-menu", () => {
        setMainMenu({ mainWindow, menuData, enabled: false });
    });
    ipcMain.on("enable-menu", () => {
        setMainMenu({ mainWindow, menuData, enabled: true });
    });

    await doSplashScreenChecks(mainWindow);
    log.info("Splash screen checks done.");
    // registerEventHandlers(mainWindow);

    // mainWindow.show();
    // if (lastWindowSize?.maximized) {
    //     mainWindow.maximize();
    // }

    // and load the index.html of the app.
    if (!mainWindow.isDestroyed()) {
        try {
            log.info("Loading main window...");
            await mainWindow.loadURL(MAIN_WINDOW_WEBPACK_ENTRY);
            // await mainWindow.loadURL("http://localhost:3000");
        } catch (error) {
            log.error("Error loading main window.", error);
        }
    }

    // Open the DevTools.
    if (!app.isPackaged && !mainWindow.isDestroyed()) {
        mainWindow.webContents.openDevTools();
    }

    let hasUnsavedChanges = false;
    ipcMain.on("update-has-unsaved-changes", (_, value) => {
        hasUnsavedChanges = value;
    });

    mainWindow.on("close", (event) => {
        if (hasUnsavedChanges) {
            const choice = dialog.showMessageBoxSync(mainWindow, {
                type: "question",
                buttons: ["Yes", "No"],
                defaultId: 1,
                title: "Discard unsaved changes?",
                message:
                    "The current workflow has some unsaved changes. Do you really want to quit without saving?",
            });
            if (choice === 1) event.preventDefault();
        }
    });

    mainWindow.on("maximize", () => {
        mainWindow.webContents.send("window-maximized-change", true);
    });
    mainWindow.on("unmaximize", () => {
        mainWindow.webContents.send("window-maximized-change", false);
    });
    mainWindow.on("blur", () => {
        mainWindow.webContents.send("window-blur");
    });

    // Opening file with PrediKit
    const { file: filepath } = getArguments();
    if (filepath) {
        const result = openSaveFile(filepath);
        ipcMain.handle("get-cli-open", () => result);
    } else {
        ipcMain.handle("get-cli-open", () => undefined);
    }
});

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on("ready", createWindow);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
});

app.on("quit", () => {
    log.info("Cleaning up temp folders...");
    const tempDir = os.tmpdir();
    // find all the folders starting with 'PrediKit-'
    const tempFolders = readdirSync(tempDir, { withFileTypes: true })
        .filter((dir) => dir.isDirectory())
        .map((dir) => dir.name)
        .filter((name) => name.includes("PrediKit-"));
    tempFolders.forEach((folder) => {
        try {
            rmSync(path.join(tempDir, folder), { force: true, recursive: true });
        } catch (error) {
            log.error(`Error removing temp folder. ${String(error)}`);
        }
    });
});

app.on("activate", () => {
    // On OS X it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

process.on("uncaughtException", (err) => {
    const messageBoxOptions = {
        type: "error",
        title: "Error in Main process",
        message: `Something failed: ${String(err)}`,
    };
    dialog.showMessageBoxSync(messageBoxOptions);
    app.exit(1);
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.
