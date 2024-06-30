export const getNodeAccentColor = (category: string | undefined): string => {
    switch (category) {
        case "Dataset":
            return "#C53030";
        case "OpenCV":
            return "#6532A8";
        case "Image":
            return "#6532A8";
        case "Image (Dimensions)":
            return "#3182CE";
        case "Image (Adjustments)":
            return "#319795";
        case "Image (Filters)":
            return "#38A169";
        case "Image (Utilities)":
            return "#00A3C4";
        case "Image (Channels)":
            return "#D69E2E";
        case "NumPy":
            return "#2B6CB0";
        case "Visualization":
            return "#EBB40F";
        default:
            return "#718096";
    }
};
