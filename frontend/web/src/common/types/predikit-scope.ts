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

struct Plot {
    data: any,
    layout: any,
}

struct AudioFile;
struct Audio;

struct ImageFile;
struct Image {
    width: uint,
    height: uint,
    channels: int(1..),
}

struct IteratorAuto;

// various inputs
struct AdaptiveMethod;
struct AdaptiveThresholdType;
struct BlendMode;
struct CaptionPosition;
struct ColorMode { inputChannels: 1 | 3 | 4, outputChannels: 1 | 3 | 4 }
struct Colorspace;
struct FillMethod;
struct FlipAxis;
struct GammaOption;
struct ImageExtension;
struct InterpolationMode;
struct MathOperation { operation: string }
struct OverflowMethod;
struct ReciprocalScalingFactor;
struct RotateInterpolationMode;
struct ThresholdType;
struct TileMode;
struct VideoType;

enum Orientation { Horizontal, Vertical }
enum SideSelection { Width, Height, Shorter, Longer }
enum ResizeCondition { Both, Upscale, Downscale }
enum RotateSizeChange { Crop, Expand }
enum FillColor { Auto, Black, Transparent }
enum BorderType { ReflectMirror, Wrap, Replicate, Black, Transparent }


def FillColor::getOutputChannels(fill: FillColor, channels: uint) {
    match fill {
        FillColor::Transparent => 4,
        _ => channels
    }
}
def BorderType::getOutputChannels(type: BorderType, channels: uint) {
    match type {
        BorderType::Transparent => 4,
        _ => channels
    }
}
`;

export const getPredikitScope = lazy((): Scope => {
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
