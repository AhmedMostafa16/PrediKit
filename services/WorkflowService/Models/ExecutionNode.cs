using System.Text.Json.Serialization;
using MongoDB.Bson.Serialization.Attributes;
using WorkflowService.Helpers;

namespace WorkflowService;

public class ExecutionNode
{
    public string[] Dependencies { get; set; } = [];
    public string CurrentId { get; set; } = string.Empty;
    public string NodeType { get; set; } = string.Empty;
    [BsonSerializer(typeof(CustomDictionarySerializer))]
    [JsonConverter(typeof(CustomDictionaryJsonConverter))]
    public Dictionary<string, object> Data { get; set; } = new();
}
