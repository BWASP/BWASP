import { FindManyOptions } from "./FindManyOptions";
import { FindOneOptions } from "./FindOneOptions";
import { SelectQueryBuilder } from "../query-builder/SelectQueryBuilder";
import { EntityMetadata } from "../metadata/EntityMetadata";
import { FindTreeOptions } from "./FindTreeOptions";
import { ObjectLiteral } from "../common/ObjectLiteral";
/**
 * Utilities to work with FindOptions.
 */
export declare class FindOptionsUtils {
    /**
     * Checks if given object is really instance of FindOneOptions interface.
     */
    static isFindOneOptions<Entity = any>(obj: any): obj is FindOneOptions<Entity>;
    /**
     * Checks if given object is really instance of FindManyOptions interface.
     */
    static isFindManyOptions<Entity = any>(obj: any): obj is FindManyOptions<Entity>;
    /**
     * Checks if given object is really instance of FindOptions interface.
     */
    static extractFindManyOptionsAlias(object: any): string | undefined;
    static applyOptionsToTreeQueryBuilder<T extends ObjectLiteral>(qb: SelectQueryBuilder<T>, options?: FindTreeOptions): SelectQueryBuilder<T>;
    /**
     * Adds joins for all relations and sub-relations of the given relations provided in the find options.
     */
    static applyRelationsRecursively(qb: SelectQueryBuilder<any>, allRelations: string[], alias: string, metadata: EntityMetadata, prefix: string): void;
    static joinEagerRelations(qb: SelectQueryBuilder<any>, alias: string, metadata: EntityMetadata): void;
}
