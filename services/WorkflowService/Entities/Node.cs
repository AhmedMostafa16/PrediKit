using System.Text.Json;
using System.Text.Json.Serialization;
using MessagePack;
using MessagePack.Formatters;
using MongoDB.Bson.Serialization.Attributes;
using WorkflowService.Helpers;

namespace WorkflowService;

[MessagePackObject]
public class Node
{
    public required string Id { get; set; }
    public required string Type { get; set; }
    public required Position Position { get; set; }
    public required Position PositionAbsolute { get; set; }
    [BsonSerializer(typeof(CustomDictionarySerializer))]
    [JsonConverter(typeof(CustomDictionaryJsonConverter))]
    public required Dictionary<string, object> Data { get; set; } = [];
}

public struct Position
{
    public double X { get; set; }
    public double Y { get; set; }
}
