namespace WorkflowService;

public class WorkflowDto
{
    public required string Title { get; set; }
    public string Description { get; set; } = string.Empty;
    public required List<Node> Nodes { get; set; }
    public required List<Edge> Edges { get; set; }
    public ViewPort ViewPort { get; set; }
    public required string CreatedOn { get; set; }
    public required string ModifiedOn { get; set; }
}