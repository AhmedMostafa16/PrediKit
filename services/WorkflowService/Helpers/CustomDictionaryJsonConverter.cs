using System.Runtime.CompilerServices;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace WorkflowService.Helpers;

public class CustomDictionaryJsonConverter : JsonConverter<Dictionary<string, object?>>
{
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public override bool CanConvert(Type typeToConvert)
    {
        return typeToConvert == typeof(Dictionary<string, object>)
               || typeToConvert == typeof(Dictionary<string, object?>);
    }

    public override Dictionary<string, object?> Read(
        ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        if (reader.TokenType != JsonTokenType.StartObject)
        {
            throw new JsonException($"JsonTokenType was of type {reader.TokenType}, only objects are supported");
        }

        var dictionary = new Dictionary<string, object?>();
        while (reader.Read())
        {
            if (reader.TokenType == JsonTokenType.EndObject)
            {
                return dictionary;
            }

            if (reader.TokenType != JsonTokenType.PropertyName)
            {
                throw new JsonException("JsonTokenType was not PropertyName");
            }

            var propertyName = reader.GetString();

            if (string.IsNullOrWhiteSpace(propertyName))
            {
                throw new JsonException("Failed to get property name");
            }

            // Get the next token and skip over it
            reader.Read();

            // Extract the value for the property
            dictionary.Add(propertyName, ExtractValue(ref reader, options));
        }

        return dictionary;
    }

    // public override void Write(
    //     Utf8JsonWriter writer, Dictionary<string, object?> value, JsonSerializerOptions options)
    // {
    //     // We don't need any custom serialization logic for writing the json.
    //     // Ideally, this method should not be called at all. It's only called if you
    //     // supply JsonSerializerOptions that contains this JsonConverter in it's Converters list.
    //     // Don't do that, you will lose performance because of the cast needed below.
    //     // Cast to avoid infinite loop: https://github.com/dotnet/docs/issues/19268
    //     JsonSerializer.Serialize(writer, value as IDictionary<string, object?>, options);
    // }

    public override void Write(Utf8JsonWriter writer, Dictionary<string, object?> value, JsonSerializerOptions options)
    {
        writer.WriteStartObject();

        foreach (string key in value.Keys) // TODO: Improve performance
        {
            HandleValue(writer, key, value[key]!);
        }

        writer.WriteEndObject();
    }
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private static void HandleValue(Utf8JsonWriter writer, string? key, object objectValue)
    {
        if (key is not null)
        {
            writer.WritePropertyName(key);
        }

        switch (objectValue)
        {
            case string stringValue:
                writer.WriteStringValue(stringValue);
                break;
            case DateTime dateTime:
                writer.WriteStringValue(dateTime);
                break;
            case long longValue:
                writer.WriteNumberValue(longValue);
                break;
            case int intValue:
                writer.WriteNumberValue(intValue);
                break;
            case float floatValue:
                writer.WriteNumberValue(floatValue);
                break;
            case double doubleValue:
                writer.WriteNumberValue(doubleValue);
                break;
            case decimal decimalValue:
                writer.WriteNumberValue(decimalValue);
                break;
            case bool boolValue:
                writer.WriteBooleanValue(boolValue);
                break;
            case Dictionary<string, object> dict:
                writer.WriteStartObject();
                foreach (var item in dict)
                {
                    HandleValue(writer, item.Key, item.Value);
                }
                writer.WriteEndObject();
                break;
            case object[] array:
                writer.WriteStartArray();
                foreach (var item in array)
                {
                    HandleValue(writer, item);
                }
                writer.WriteEndArray();
                break;
            default:
                writer.WriteNullValue();
                break;
        }
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private static void HandleValue(Utf8JsonWriter writer, object value)
    {
        HandleValue(writer, null, value);
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private object? ExtractValue(ref Utf8JsonReader reader, JsonSerializerOptions options)
    {
        switch (reader.TokenType)
        {
            case JsonTokenType.String:
                if (reader.TryGetDateTime(out var date))
                    return date;
                return reader.GetString();
            case JsonTokenType.False:
                return false;
            case JsonTokenType.True:
                return true;
            case JsonTokenType.Null:
                return null;
            case JsonTokenType.Number:
                if (reader.TryGetInt64(out var result))
                    return result;
                if (reader.TryGetDecimal(out var decimalResult))
                    return decimalResult;
                return reader.GetDouble();

            case JsonTokenType.StartObject:
                return Read(ref reader, null!, options);
            case JsonTokenType.StartArray:
                var list = new List<object?>();
                while (reader.Read() && reader.TokenType != JsonTokenType.EndArray)
                {
                    list.Add(ExtractValue(ref reader, options));
                }
                return list;

            default:
                throw new JsonException($"'{reader.TokenType}' is not supported");
        }
    }
}
