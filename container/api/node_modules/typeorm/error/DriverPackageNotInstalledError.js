"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DriverPackageNotInstalledError = void 0;
const TypeORMError_1 = require("./TypeORMError");
/**
 * Thrown when required driver's package is not installed.
 */
class DriverPackageNotInstalledError extends TypeORMError_1.TypeORMError {
    constructor(driverName, packageName) {
        super(`${driverName} package has not been found installed. Please run "npm install ${packageName}".`);
    }
}
exports.DriverPackageNotInstalledError = DriverPackageNotInstalledError;

//# sourceMappingURL=DriverPackageNotInstalledError.js.map
