namespace WorkflowService;

public class ExecutionWorkflow
{
    public required string Id { get; set; }
    public required List<Node> Nodes { get; set; }
    public required List<string[]> Paths { get; set; }
    public required Dictionary<string, string[]> Dependencies { get; set; }
}
