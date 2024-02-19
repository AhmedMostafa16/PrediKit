namespace WorkflowService;

public class UpdateWorkflowDto
{
    public required string Title { get; set; }
    public required string Description { get; set; }
    public required List<Node> Nodes { get; set; } = [];
    public required List<Edge> Edges { get; set; } = [];
    public ViewPort ViewPort { get; set; }
    public required string ModifiedOn { get; set; }
}
