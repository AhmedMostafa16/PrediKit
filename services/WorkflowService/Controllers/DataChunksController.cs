using System.Runtime.CompilerServices;
using System.Text.Json;
using Apache.Arrow.Ipc;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Caching.Distributed;
using MongoDB.Bson;
using Parquet;
using Parquet.Rows;
using StackExchange.Redis;

namespace WorkflowService;

[ApiController]
[Route("api/[controller]")]
public class DataChunksController : ControllerBase
{
    private readonly IDatabase _redis;
    private readonly ILogger<DataChunksController> _logger;
    private readonly JsonSerializerOptions _jsonOptions = new()
    {
        WriteIndented = false
    };

    public DataChunksController(IConnectionMultiplexer muxer, ILogger<DataChunksController> logger)
    {
        _logger = logger;
        _redis = muxer.GetDatabase();
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetChunkWithId(string id, [FromQuery] int chunk)
    {
        // Retrieve the chunk from the cache
        string key = $"{id}_{chunk}";
        Console.WriteLine($"Retrieving chunk {chunk} for a node with ID {id} from the cache.");
        System.Console.WriteLine("{0}", key);
        byte[]? data = await _redis.StringGetAsync(key);

        if (data is null)
        {
            return NotFound();
        }

        _logger.LogDebug("Retrieved chunk {Chunk} for a node with ID {Id} from the cache.", chunk, id);

        // Convert the data into JSON from a byte array of Parquet data
        var json = await ParquetToJson(data);
        // var json = data;

        if (json == null)
        {
            string message = $"The data chunk {chunk} of node {id} could not be converted to JSON.";
            _logger.LogError(message);
            return NotFound(message);
        }

        return Ok(json);
    }

    [NonAction]
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private async Task<string> ParquetToJson(byte[] data)
    {
        // Convert the Parquet data into JSON
        using MemoryStream stream = new(data);

        // Deserialize the Parquet data 
        var dataSet = await stream.ReadParquetAsDataFrameAsync();

        // Convert the Parquet data into JSON
        return JsonSerializer.Serialize(dataSet, _jsonOptions);
    }

    // Get the number of keys that start with the given ID as a prefix
    [HttpGet("count/{id}")]
    public async Task<IActionResult> GetChunkCount(string id)
    {
        try
        {
            // Get the number of keys that start with the given ID as a prefix
            var keys = _redis.Multiplexer.GetServer(_redis.Multiplexer.GetEndPoints().First()).Keys(pattern: $"{id}_*");
            long count = keys.LongCount();

            return Ok(count);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "An error occurred while getting the chunk count for ID: {Id}", id);
            return StatusCode(StatusCodes.Status500InternalServerError);
        }
    }


}
