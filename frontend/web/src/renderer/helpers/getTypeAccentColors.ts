import { getPrediKitScope } from "../../common/types/predikit-scope";
import { evaluate } from "../../common/types/evaluate";
import { NamedExpression } from "../../common/types/expression";
import { isDisjointWith } from "../../common/types/intersection";
import { NumberType, StringType, Type } from "../../common/types/types";
import { lazy } from "../../common/util";

export const defaultColor = "#718096";

const colorList = lazy(() => {
    const scope = getPrediKitScope();
    return [
        // { type: evaluate(new NamedExpression('Directory'), scope), color: '#805AD5' },
        { type: evaluate(new NamedExpression("Dataset"), scope), color: "#D69E2E" },
        { type: NumberType.instance, color: "#3182CE" },
        { type: StringType.instance, color: "#10b52c" },
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
