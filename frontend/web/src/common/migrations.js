/* eslint-disable no-param-reassign */
/* eslint-disable import/prefer-default-export */
import log from "electron-log";
import semver from "semver";

const versionToMigration = (version) => {
    const versions = {};

    // eslint-disable-next-line no-restricted-syntax
    for (const [ver, migration] of Object.entries(versions)) {
        if (semver.lt(version, ver)) {
            return migration;
        }
    }
    return 0;
};

const migrations = [];

export const currentMigration = migrations.length;

export const migrate = (version, data, migration) => {
    version ||= "0.0.0";
    migration ??= versionToMigration(version);

    try {
        return migrations.slice(migration).reduce((current, fn) => fn(current), data);
    } catch (error) {
        log.error(error);
        throw error;
    }
};
