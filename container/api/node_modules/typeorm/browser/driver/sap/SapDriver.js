import { promisify } from "node:util";
import { ConnectionIsNotSetError } from "../../error/ConnectionIsNotSetError";
import { DriverPackageNotInstalledError } from "../../error/DriverPackageNotInstalledError";
import { TypeORMError } from "../../error/TypeORMError";
import { PlatformTools } from "../../platform/PlatformTools";
import { RdbmsSchemaBuilder } from "../../schema-builder/RdbmsSchemaBuilder";
import { ApplyValueTransformers } from "../../util/ApplyValueTransformers";
import { DateUtils } from "../../util/DateUtils";
import { InstanceChecker } from "../../util/InstanceChecker";
import { OrmUtils } from "../../util/OrmUtils";
import { DriverUtils } from "../DriverUtils";
import { SapQueryRunner } from "./SapQueryRunner";
/**
 * Organizes communication with SAP Hana DBMS.
 *
 * todo: looks like there is no built in support for connection pooling, we need to figure out something
 */
export class SapDriver {
    // -------------------------------------------------------------------------
    // Constructor
    // -------------------------------------------------------------------------
    constructor(connection) {
        /**
         * Indicates if replication is enabled.
         */
        this.isReplicated = false;
        /**
         * Indicates if tree tables are supported by this driver.
         */
        this.treeSupport = true;
        /**
         * Represent transaction support by this driver
         */
        this.transactionSupport = "simple";
        /**
         * Gets list of supported column data types by a driver.
         *
         * @see https://help.sap.com/docs/SAP_HANA_PLATFORM/4fe29514fd584807ac9f2a04f6754767/20a1569875191014b507cf392724b7eb.html
         * @see https://help.sap.com/docs/hana-cloud-database/sap-hana-cloud-sap-hana-database-sql-reference-guide/data-types
         */
        this.supportedDataTypes = [
            "alphanum", // removed in SAP HANA Cloud
            "array",
            "bigint",
            "binary",
            "blob",
            "boolean",
            "char", // not officially supported, in SAP HANA Cloud: alias for "nchar"
            "clob", // in SAP HANA Cloud: alias for "nclob"
            "date",
            "dec", // typeorm alias for "decimal"
            "decimal",
            "double",
            "float", // database alias for "real" / "double"
            "half_vector", // only supported in SAP HANA Cloud, not in SAP HANA 2.0
            "int", // typeorm alias for "integer"
            "integer",
            "nchar", // not officially supported
            "nclob",
            "nvarchar",
            "real_vector", // only supported in SAP HANA Cloud, not in SAP HANA 2.0
            "real",
            "seconddate",
            "shorttext", // removed in SAP HANA Cloud
            "smalldecimal",
            "smallint",
            "st_geometry",
            "st_point",
            "text", // removed in SAP HANA Cloud
            "time",
            "timestamp",
            "tinyint",
            "varbinary",
            "varchar", // in SAP HANA Cloud: alias for "nvarchar"
        ];
        /**
         * Returns type of upsert supported by driver if any
         */
        this.supportedUpsertTypes = ["merge-into"];
        /**
         * Gets list of spatial column data types.
         */
        this.spatialTypes = ["st_geometry", "st_point"];
        /**
         * Gets list of column data types that support length by a driver.
         */
        this.withLengthColumnTypes = [
            "alphanum",
            "binary",
            "half_vector",
            "nvarchar",
            "real_vector",
            "shorttext",
            "varbinary",
            "varchar",
        ];
        /**
         * Gets list of column data types that support precision by a driver.
         */
        this.withPrecisionColumnTypes = ["decimal"];
        /**
         * Gets list of column data types that support scale by a driver.
         */
        this.withScaleColumnTypes = ["decimal", "timestamp"];
        /**
         * Orm has special columns and we need to know what database column types should be for those types.
         * Column types are driver dependant.
         */
        this.mappedDataTypes = {
            createDate: "timestamp",
            createDateDefault: "CURRENT_TIMESTAMP",
            updateDate: "timestamp",
            updateDateDefault: "CURRENT_TIMESTAMP",
            deleteDate: "timestamp",
            deleteDateNullable: true,
            version: "integer",
            treeLevel: "integer",
            migrationId: "integer",
            migrationName: "nvarchar",
            migrationTimestamp: "bigint",
            cacheId: "integer",
            cacheIdentifier: "nvarchar",
            cacheTime: "bigint",
            cacheDuration: "integer",
            cacheQuery: "nvarchar(5000)",
            cacheResult: "nclob",
            metadataType: "nvarchar",
            metadataDatabase: "nvarchar",
            metadataSchema: "nvarchar",
            metadataTable: "nvarchar",
            metadataName: "nvarchar",
            metadataValue: "nvarchar(5000)",
        };
        /**
         * Default values of length, precision and scale depends on column data type.
         * Used in the cases when length/precision/scale is not specified by user.
         */
        this.dataTypeDefaults = {
            binary: { length: 1 },
            char: { length: 1 },
            decimal: { precision: 18, scale: 0 },
            nchar: { length: 1 },
            nvarchar: { length: 255 },
            shorttext: { length: 255 },
            varbinary: { length: 255 },
            varchar: { length: 255 },
        };
        /**
         * Max length allowed by SAP HANA for aliases (identifiers).
         * @see https://help.sap.com/docs/hana-cloud-database/sap-hana-cloud-sap-hana-database-sql-reference-guide/system-limitations
         */
        this.maxAliasLength = 128;
        this.cteCapabilities = {
            enabled: true,
        };
        this.dummyTableName = `SYS.DUMMY`;
        this.connection = connection;
        this.options = connection.options;
        this.loadDependencies();
        this.database = DriverUtils.buildDriverOptions(this.options).database;
        this.schema = DriverUtils.buildDriverOptions(this.options).schema;
    }
    // -------------------------------------------------------------------------
    // Public Implemented Methods
    // -------------------------------------------------------------------------
    /**
     * Performs connection to the database.
     * Based on pooling options, it can either create connection immediately,
     * either create a pool and create connection when needed.
     */
    async connect() {
        // HANA connection info
        const connectionOptions = {
            host: this.options.host,
            port: this.options.port,
            user: this.options.username,
            password: this.options.password,
            database: this.options.database,
            currentSchema: this.options.schema,
            encrypt: this.options.encrypt,
            sslValidateCertificate: this.options.sslValidateCertificate,
            key: this.options.key,
            cert: this.options.cert,
            ca: this.options.ca,
        };
        Object.keys(connectionOptions).forEach((key) => {
            if (connectionOptions[key] === undefined) {
                delete connectionOptions[key];
            }
        });
        Object.assign(connectionOptions, this.options.extra ?? {});
        // pool options
        const poolOptions = {
            maxConnectedOrPooled: this.options.pool?.maxConnectedOrPooled ??
                this.options.pool?.max ??
                this.options.poolSize ??
                10,
            maxPooledIdleTime: this.options.pool?.maxPooledIdleTime ??
                (this.options.pool?.idleTimeout
                    ? this.options.pool.idleTimeout / 1000
                    : 30),
        };
        if (this.options.pool?.pingCheck) {
            poolOptions.pingCheck = this.options.pool.pingCheck;
        }
        if (this.options.pool?.poolCapacity) {
            poolOptions.poolCapacity = this.options.pool.poolCapacity;
        }
        this.poolErrorHandler =
            this.options.pool?.poolErrorHandler ??
                ((error) => {
                    this.connection.logger.log("warn", `SAP HANA pool raised an error: ${error}`);
                });
        // create the pool
        try {
            this.master = this.client.createPool(connectionOptions, poolOptions);
        }
        catch (error) {
            this.poolErrorHandler(error);
            throw error;
        }
        const queryRunner = this.createQueryRunner("master");
        const { version, database } = await queryRunner.getDatabaseAndVersion();
        this.version = version;
        this.database = database;
        if (!this.schema) {
            this.schema = await queryRunner.getCurrentSchema();
        }
        await queryRunner.release();
    }
    /**
     * Makes any action after connection (e.g. create extensions in Postgres driver).
     */
    afterConnect() {
        return Promise.resolve();
    }
    /**
     * Closes connection with the database.
     */
    async disconnect() {
        const pool = this.master;
        if (!pool) {
            throw new ConnectionIsNotSetError("sap");
        }
        this.master = undefined;
        try {
            await promisify(pool.clear).call(pool);
        }
        catch (error) {
            this.poolErrorHandler(error);
            throw error;
        }
    }
    /**
     * Obtains a new database connection to a master server.
     * Used for replication.
     * If replication is not setup then returns default connection's database connection.
     */
    async obtainMasterConnection() {
        const pool = this.master;
        if (!pool) {
            throw new TypeORMError("Driver not Connected");
        }
        try {
            return await promisify(pool.getConnection).call(pool);
        }
        catch (error) {
            this.poolErrorHandler(error);
            throw error;
        }
    }
    /**
     * Obtains a new database connection to a slave server.
     * Used for replication.
     * If replication is not setup then returns master (default) connection's database connection.
     */
    async obtainSlaveConnection() {
        return this.obtainMasterConnection();
    }
    /**
     * Creates a schema builder used to build and sync a schema.
     */
    createSchemaBuilder() {
        return new RdbmsSchemaBuilder(this.connection);
    }
    /**
     * Creates a query runner used to execute database queries.
     */
    createQueryRunner(mode) {
        return new SapQueryRunner(this, mode);
    }
    /**
     * Replaces parameters in the given sql with special escaping character
     * and an array of parameter names to be passed to a query.
     */
    escapeQueryWithParameters(sql, parameters, nativeParameters) {
        const escapedParameters = Object.keys(nativeParameters).map((key) => {
            if (nativeParameters[key] instanceof Date)
                return DateUtils.mixedDateToDatetimeString(nativeParameters[key], true);
            return nativeParameters[key];
        });
        if (!parameters || !Object.keys(parameters).length)
            return [sql, escapedParameters];
        sql = sql.replace(/:(\.\.\.)?([A-Za-z0-9_.]+)/g, (full, isArray, key) => {
            if (!parameters.hasOwnProperty(key)) {
                return full;
            }
            const value = parameters[key];
            if (isArray) {
                return value
                    .map((v) => {
                    escapedParameters.push(v);
                    return this.createParameter(key, escapedParameters.length - 1);
                })
                    .join(", ");
            }
            if (typeof value === "function") {
                return value();
            }
            if (value instanceof Date) {
                return DateUtils.mixedDateToDatetimeString(value, true);
            }
            escapedParameters.push(value);
            return this.createParameter(key, escapedParameters.length - 1);
        }); // todo: make replace only in value statements, otherwise problems
        return [sql, escapedParameters];
    }
    /**
     * Escapes a column name.
     */
    escape(columnName) {
        return `"${columnName}"`;
    }
    /**
     * Build full table name with schema name and table name.
     * E.g. myDB.mySchema.myTable
     */
    buildTableName(tableName, schema) {
        const tablePath = [tableName];
        if (schema) {
            tablePath.unshift(schema);
        }
        return tablePath.join(".");
    }
    /**
     * Parse a target table name or other types and return a normalized table definition.
     */
    parseTableName(target) {
        const driverDatabase = this.database;
        const driverSchema = this.schema;
        if (InstanceChecker.isTable(target) || InstanceChecker.isView(target)) {
            const parsed = this.parseTableName(target.name);
            return {
                database: target.database || parsed.database || driverDatabase,
                schema: target.schema || parsed.schema || driverSchema,
                tableName: parsed.tableName,
            };
        }
        if (InstanceChecker.isTableForeignKey(target)) {
            const parsed = this.parseTableName(target.referencedTableName);
            return {
                database: target.referencedDatabase ||
                    parsed.database ||
                    driverDatabase,
                schema: target.referencedSchema || parsed.schema || driverSchema,
                tableName: parsed.tableName,
            };
        }
        if (InstanceChecker.isEntityMetadata(target)) {
            // EntityMetadata tableName is never a path
            return {
                database: target.database || driverDatabase,
                schema: target.schema || driverSchema,
                tableName: target.tableName,
            };
        }
        const parts = target.split(".");
        return {
            database: driverDatabase,
            schema: (parts.length > 1 ? parts[0] : undefined) || driverSchema,
            tableName: parts.length > 1 ? parts[1] : parts[0],
        };
    }
    /**
     * Prepares given value to a value to be persisted, based on its column type and metadata.
     */
    preparePersistentValue(value, columnMetadata) {
        if (columnMetadata.transformer)
            value = ApplyValueTransformers.transformTo(columnMetadata.transformer, value);
        if (value === null || value === undefined)
            return value;
        if (columnMetadata.type === "date") {
            return DateUtils.mixedDateToDateString(value, {
                utc: columnMetadata.utc,
            });
        }
        else if (columnMetadata.type === "time") {
            return DateUtils.mixedDateToTimeString(value);
        }
        else if (columnMetadata.type === "timestamp" ||
            columnMetadata.type === Date) {
            return DateUtils.mixedDateToDatetimeString(value, true);
        }
        else if (columnMetadata.type === "seconddate") {
            return DateUtils.mixedDateToDatetimeString(value, false);
        }
        else if (columnMetadata.type === "simple-array") {
            return DateUtils.simpleArrayToString(value);
        }
        else if (columnMetadata.type === "simple-json") {
            return DateUtils.simpleJsonToString(value);
        }
        else if (columnMetadata.type === "simple-enum") {
            return DateUtils.simpleEnumToString(value);
        }
        else if (columnMetadata.isArray) {
            return () => `ARRAY(${value.map((it) => `'${it}'`)})`;
        }
        return value;
    }
    /**
     * Prepares given value to a value to be persisted, based on its column type or metadata.
     */
    prepareHydratedValue(value, columnMetadata) {
        if (value === null || value === undefined)
            return columnMetadata.transformer
                ? ApplyValueTransformers.transformFrom(columnMetadata.transformer, value)
                : value;
        if (columnMetadata.type === "timestamp" ||
            columnMetadata.type === "seconddate" ||
            columnMetadata.type === Date) {
            value = DateUtils.normalizeHydratedDate(value);
        }
        else if (columnMetadata.type === "date") {
            value = DateUtils.mixedDateToDateString(value, {
                utc: columnMetadata.utc,
            });
        }
        else if (columnMetadata.type === "time") {
            value = DateUtils.mixedTimeToString(value);
        }
        else if (columnMetadata.type === "simple-array") {
            value = DateUtils.stringToSimpleArray(value);
        }
        else if (columnMetadata.type === "simple-json") {
            value = DateUtils.stringToSimpleJson(value);
        }
        else if (columnMetadata.type === "simple-enum") {
            value = DateUtils.stringToSimpleEnum(value, columnMetadata);
        }
        if (columnMetadata.transformer)
            value = ApplyValueTransformers.transformFrom(columnMetadata.transformer, value);
        return value;
    }
    /**
     * Creates a database type from a given column metadata.
     */
    normalizeType(column) {
        if (column.type === Number || column.type === "int") {
            return "integer";
        }
        else if (column.type === "dec") {
            return "decimal";
        }
        else if (column.type === "float") {
            const length = typeof column.length === "string"
                ? parseInt(column.length)
                : column.length;
            // https://help.sap.com/docs/SAP_HANA_PLATFORM/4fe29514fd584807ac9f2a04f6754767/4ee2f261e9c44003807d08ccc2e249ac.html
            if (length && length < 25) {
                return "real";
            }
            return "double";
        }
        else if (column.type === String) {
            return "nvarchar";
        }
        else if (column.type === Date) {
            return "timestamp";
        }
        else if (column.type === Boolean) {
            return "boolean";
        }
        else if (column.type === Buffer) {
            return "blob";
        }
        else if (column.type === "uuid") {
            return "nvarchar";
        }
        else if (column.type === "simple-array" ||
            column.type === "simple-json") {
            return "nclob";
        }
        else if (column.type === "simple-enum") {
            return "nvarchar";
        }
        else if (column.type === "vector") {
            return "real_vector";
        }
        else if (column.type === "halfvec") {
            return "half_vector";
        }
        if (DriverUtils.isReleaseVersionOrGreater(this, "4.0")) {
            // SAP HANA Cloud deprecated / removed these data types
            if (column.type === "varchar" ||
                column.type === "alphanum" ||
                column.type === "shorttext") {
                return "nvarchar";
            }
            else if (column.type === "text" || column.type === "clob") {
                return "nclob";
            }
            else if (column.type === "char") {
                return "nchar";
            }
        }
        else {
            if (column.type === "real_vector" ||
                column.type === "half_vector") {
                return "varbinary";
            }
        }
        return column.type || "";
    }
    /**
     * Normalizes "default" value of the column.
     */
    normalizeDefault(columnMetadata) {
        const defaultValue = columnMetadata.default;
        if (typeof defaultValue === "number") {
            return `${defaultValue}`;
        }
        if (typeof defaultValue === "boolean") {
            return defaultValue ? "true" : "false";
        }
        if (typeof defaultValue === "function") {
            return defaultValue();
        }
        if (typeof defaultValue === "string") {
            return `'${defaultValue}'`;
        }
        if (defaultValue === null || defaultValue === undefined) {
            return undefined;
        }
        return `${defaultValue}`;
    }
    /**
     * Normalizes "isUnique" value of the column.
     */
    normalizeIsUnique(column) {
        return column.entityMetadata.indices.some((idx) => idx.isUnique &&
            idx.columns.length === 1 &&
            idx.columns[0] === column);
    }
    /**
     * Returns default column lengths, which is required on column creation.
     */
    getColumnLength(column) {
        if (column.length)
            return column.length.toString();
        if (column.generationStrategy === "uuid")
            return "36";
        switch (column.type) {
            case "varchar":
            case "nvarchar":
            case "shorttext":
            case String:
                return "255";
            case "alphanum":
                return "127";
            case "varbinary":
                return "255";
        }
        return "";
    }
    /**
     * Creates column type definition including length, precision and scale
     */
    createFullType(column) {
        let type = column.type;
        // used 'getColumnLength()' method, because SqlServer sets `varchar` and `nvarchar` length to 1 by default.
        if (this.getColumnLength(column)) {
            type += `(${this.getColumnLength(column)})`;
        }
        else if (column.precision !== null &&
            column.precision !== undefined &&
            column.scale !== null &&
            column.scale !== undefined) {
            type += `(${column.precision},${column.scale})`;
        }
        else if (column.precision !== null &&
            column.precision !== undefined) {
            type += `(${column.precision})`;
        }
        if (column.isArray)
            type += " array";
        return type;
    }
    /**
     * Creates generated map of values generated or returned by database after INSERT query.
     */
    createGeneratedMap(metadata, insertResult) {
        const generatedMap = metadata.generatedColumns.reduce((map, generatedColumn) => {
            let value;
            if (generatedColumn.generationStrategy === "increment" &&
                insertResult) {
                value = insertResult;
                // } else if (generatedColumn.generationStrategy === "uuid") {
                //     console.log("getting db value:", generatedColumn.databaseName);
                //     value = generatedColumn.getEntityValue(uuidMap);
            }
            return OrmUtils.mergeDeep(map, generatedColumn.createValueMap(value));
        }, {});
        return Object.keys(generatedMap).length > 0 ? generatedMap : undefined;
    }
    /**
     * Differentiate columns of this table and columns from the given column metadatas columns
     * and returns only changed.
     */
    findChangedColumns(tableColumns, columnMetadatas) {
        return columnMetadatas.filter((columnMetadata) => {
            const tableColumn = tableColumns.find((c) => c.name === columnMetadata.databaseName);
            if (!tableColumn) {
                // we don't need new columns, we only need exist and changed
                return false;
            }
            const normalizedDefault = this.normalizeDefault(columnMetadata);
            return (tableColumn.name !== columnMetadata.databaseName ||
                tableColumn.type !== this.normalizeType(columnMetadata) ||
                (columnMetadata.length &&
                    tableColumn.length !==
                        this.getColumnLength(columnMetadata)) ||
                tableColumn.precision !== columnMetadata.precision ||
                tableColumn.scale !== columnMetadata.scale ||
                tableColumn.comment !==
                    this.escapeComment(columnMetadata.comment) ||
                (!tableColumn.isGenerated &&
                    normalizedDefault !== tableColumn.default) || // we included check for generated here, because generated columns already can have default values
                tableColumn.isPrimary !== columnMetadata.isPrimary ||
                tableColumn.isNullable !== columnMetadata.isNullable ||
                tableColumn.isUnique !==
                    this.normalizeIsUnique(columnMetadata) ||
                (columnMetadata.generationStrategy !== "uuid" &&
                    tableColumn.isGenerated !== columnMetadata.isGenerated));
        });
    }
    /**
     * Returns true if driver supports RETURNING / OUTPUT statement.
     */
    isReturningSqlSupported() {
        return false;
    }
    /**
     * Returns true if driver supports uuid values generation on its own.
     */
    isUUIDGenerationSupported() {
        return false;
    }
    /**
     * Returns true if driver supports fulltext indices.
     */
    isFullTextColumnTypeSupported() {
        return !DriverUtils.isReleaseVersionOrGreater(this, "4.0");
    }
    /**
     * Creates an escaped parameter.
     */
    createParameter(parameterName, index) {
        return "?";
    }
    // -------------------------------------------------------------------------
    // Protected Methods
    // -------------------------------------------------------------------------
    /**
     * If driver dependency is not given explicitly, then try to load it via "require".
     */
    loadDependencies() {
        const client = this.options.driver ?? this.options.hanaClientDriver;
        if (client) {
            this.client = client;
            return;
        }
        try {
            this.client = PlatformTools.load("@sap/hana-client");
            this.streamClient = PlatformTools.load("@sap/hana-client/extension/Stream");
        }
        catch {
            // todo: better error for browser env
            throw new DriverPackageNotInstalledError("SAP Hana", "@sap/hana-client");
        }
    }
    /**
     * Escapes a given comment.
     */
    escapeComment(comment) {
        if (!comment)
            return comment;
        comment = comment.replace(/\u0000/g, ""); // Null bytes aren't allowed in comments
        return comment;
    }
}

//# sourceMappingURL=SapDriver.js.map
