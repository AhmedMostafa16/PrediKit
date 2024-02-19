
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Data.Analysis;

namespace WorkflowService;

class CustomDataFrameJsonConverter : JsonConverter<DataFrame>
{
    public override DataFrame? Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        throw new NotImplementedException("Deserialization is not implemented for DataFrame");
    }

    public override void Write(Utf8JsonWriter writer, DataFrame value, JsonSerializerOptions options)
    {
        writer.WriteStartObject();

        // Write columns
        writer.WriteStartArray("columns");
        foreach (DataFrameColumn column in value.Columns)
        {
            writer.WriteStringValue(column.Name);
        }
        writer.WriteEndArray();

        writer.WriteStartArray("data");
        foreach (DataFrameRow row in value.Rows)
        {
            writer.WriteStartObject();
            for (int i = 0; i < value.Columns.Count; i++)
            {
                writer.WritePropertyName(value.Columns[i].Name);
                writer.WriteStringValue(row[i].ToString());
            }
            writer.WriteEndObject();
        }
        writer.WriteEndArray();

        writer.WriteEndObject();
    }
}