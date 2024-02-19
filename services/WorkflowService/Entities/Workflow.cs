using MessagePack;
using MongoDB.Entities;

namespace WorkflowService;

public class Workflow : Entity
{
    public required string Title { get; set; }
    public required string Description { get; set; }
    public required List<Node> Nodes { get; set; }
    public required List<Edge> Edges { get; set; }
    public required ViewPort ViewPort { get; set; }
    public required string CreatedOn { get; set; }
    public required string ModifiedOn { get; set; }
}

[MessagePackObject]
public struct ViewPort
{
    public double X { get; set; }
    public double Y { get; set; }
    public double Zoom { get; set; }
}