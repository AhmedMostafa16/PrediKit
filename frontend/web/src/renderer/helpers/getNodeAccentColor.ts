export const getNodeAccentColor = (category: string | undefined): string => {
    switch (category) {
        case "Dataset":
            return "#C53030";
        case "Visualization":
            return "#EBB40F";
        default:
            return "#718096";
    }
};
