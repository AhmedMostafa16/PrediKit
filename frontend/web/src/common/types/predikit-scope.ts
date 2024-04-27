import { lazy } from "../util";
import { globalScope } from "./global-scope";
import { parseDefinitions } from "./parse";
import { formatTextPattern } from "./predikit-format";
import { BuiltinFunctionDefinition, Scope, ScopeBuilder } from "./scope";
import { SourceDocument } from "./source";
import { StringType, StructType, Type } from "./types";
import { union } from "./union";

const code = `
struct null;

struct Directory { path: string }


struct DatasetFile;
struct Dataset {
    columns: any,
    data: any,
    index: any,
    dtypes: any,
    shape: int(0..),
}


struct MathOperation { operation: string }
struct LogicalOperation { operation: string }
`;

export const getPrediKitScope = lazy((): Scope => {
    const builder = new ScopeBuilder("PrediKit scope", globalScope);

    const definitions = parseDefinitions(new SourceDocument(code, "predikit-internal"));
    for (const d of definitions) {
        builder.add(d);
    }

    builder.add(
        new BuiltinFunctionDefinition(
            "formatPattern",
            formatTextPattern as (..._: Type[]) => Type,
            [StringType.instance],
            union(StringType.instance, new StructType("null"))
        )
    );

    return builder.createScope();
});
