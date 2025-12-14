"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.importOrRequireFile = importOrRequireFile;
const tslib_1 = require("tslib");
const promises_1 = tslib_1.__importDefault(require("fs/promises"));
const path_1 = tslib_1.__importDefault(require("path"));
const url_1 = require("url");
async function importOrRequireFile(filePath) {
    const tryToImport = async () => {
        // `Function` is required to make sure the `import` statement wil stay `import` after
        // transpilation and won't be converted to `require`
        return [
            // eslint-disable-next-line @typescript-eslint/no-implied-eval
            await Function("return filePath => import(filePath)")()(filePath.startsWith("file://")
                ? filePath
                : (0, url_1.pathToFileURL)(filePath).toString()),
            "esm",
        ];
    };
    const tryToRequire = () => {
        return [require(filePath), "commonjs"];
    };
    const extension = filePath.substring(filePath.lastIndexOf(".") + ".".length);
    if (extension === "mjs" || extension === "mts")
        return tryToImport();
    else if (extension === "cjs" || extension === "cts")
        return tryToRequire();
    else if (extension === "js" || extension === "ts") {
        const packageJson = await getNearestPackageJson(filePath);
        if (packageJson != null) {
            const isModule = packageJson?.type === "module";
            if (isModule)
                return tryToImport();
            else
                return tryToRequire();
        }
        else
            return tryToRequire();
    }
    return tryToRequire();
}
const packageJsonCache = new Map();
const MAX_CACHE_SIZE = 1000;
function setPackageJsonCache(paths, packageJson) {
    for (const path of paths) {
        // Simple LRU-like behavior: if we're at capacity, remove oldest entry
        if (packageJsonCache.size >= MAX_CACHE_SIZE &&
            !packageJsonCache.has(path)) {
            const firstKey = packageJsonCache.keys().next().value;
            if (firstKey)
                packageJsonCache.delete(firstKey);
        }
        packageJsonCache.set(path, packageJson);
    }
}
async function getNearestPackageJson(filePath) {
    let currentPath = filePath;
    const paths = [];
    while (currentPath !== path_1.default.dirname(currentPath)) {
        currentPath = path_1.default.dirname(currentPath);
        // Check if we have already cached the package.json for this path
        if (packageJsonCache.has(currentPath)) {
            setPackageJsonCache(paths, packageJsonCache.get(currentPath));
            return packageJsonCache.get(currentPath);
        }
        // Add the current path to the list of paths to cache
        paths.push(currentPath);
        const potentialPackageJson = path_1.default.join(currentPath, "package.json");
        try {
            const stats = await promises_1.default.stat(potentialPackageJson);
            if (!stats.isFile()) {
                continue;
            }
            try {
                const parsedPackage = JSON.parse(await promises_1.default.readFile(potentialPackageJson, "utf8"));
                // Cache the parsed package.json object and return it
                setPackageJsonCache(paths, parsedPackage);
                return parsedPackage;
            }
            catch {
                // If parsing fails, we still cache null to avoid repeated attempts
                setPackageJsonCache(paths, null);
                return null;
            }
        }
        catch {
            continue;
        }
    }
    // the top of the file tree is reached
    setPackageJsonCache(paths, null);
    return null;
}

//# sourceMappingURL=ImportUtils.js.map
