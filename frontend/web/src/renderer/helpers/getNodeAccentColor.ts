export const getNodeAccentColor = (category: string | undefined): string => {
    switch (category) {
        case "Dataset":
            return "#C53030";
        default:
            return "#718096";
    }
};
