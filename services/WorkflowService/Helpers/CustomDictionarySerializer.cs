using System.Text.Json;
using MongoDB.Bson;
using MongoDB.Bson.Serialization;
using MongoDB.Bson.Serialization.Serializers;

namespace WorkflowService;

public sealed class CustomDictionarySerializer : SerializerBase<Dictionary<string, object>>
{
    static readonly JsonSerializerOptions _options = new() { WriteIndented = false };
    public override Dictionary<string, object> Deserialize(BsonDeserializationContext context, BsonDeserializationArgs args)
    {
        return BsonSerializer.Deserialize<Dictionary<string, object>>(context.Reader);
    }

    public override void Serialize(BsonSerializationContext context, BsonSerializationArgs args, Dictionary<string, object> value)
    {
        string jsonDocument = JsonSerializer.Serialize(value, _options);
        BsonDocument bsonDocument = BsonSerializer.Deserialize<BsonDocument>(jsonDocument);
        BsonSerializer.Serialize(context.Writer, bsonDocument);
    }
}


