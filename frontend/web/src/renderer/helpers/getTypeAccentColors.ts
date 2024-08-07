import { evaluate } from "../../common/types/evaluate";
import { NamedExpression } from "../../common/types/expression";
import { isDisjointWith } from "../../common/types/intersection";
import { getPredikitScope } from "../../common/types/predikit-scope";
import { NumberType, StringType, Type } from "../../common/types/types";
import { lazy } from "../../common/util";

export const defaultColor = "#718096";

const colorList = lazy(() => {
    const scope = getPredikitScope();
    return [
        { type: evaluate(new NamedExpression("Directory"), scope), color: "#e69138" },
        { type: evaluate(new NamedExpression("Dataset"), scope), color: "#C53030" },
        { type: evaluate(new NamedExpression("Plot"), scope), color: "#EBB40F" },
        { type: evaluate(new NamedExpression("Image"), scope), color: "#6532a8" },
        { type: NumberType.instance, color: "#3182CE" },
        { type: StringType.instance, color: "#10B52C" },
    ];
});

export const getTypeAccentColors = (inputType: Type): string[] => {
    if (inputType.type === "any") {
        return [defaultColor];
    }

    const colors: string[] = [];
    for (const { type, color } of colorList()) {
        if (!isDisjointWith(type, inputType)) {
            colors.push(color);
        }
    }
    return colors.length > 0 ? colors : [defaultColor];
};
