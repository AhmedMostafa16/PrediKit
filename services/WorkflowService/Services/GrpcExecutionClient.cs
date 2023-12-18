using Grpc.Net.Client;

namespace WorkflowService;

public class GrpcExecutionClient
{
    private readonly ILogger<GrpcExecutionClient> _logger;
    private readonly IConfiguration _configuration;

    public GrpcExecutionClient(ILogger<GrpcExecutionClient> logger, IConfiguration configuration)
    {
        _logger = logger;
        _configuration = configuration;
    }

    public GrpcExecutionResponse? ExecuteNode(string id, string type, string properties, string dataframe = "")
    {
        _logger.LogInformation($"Executing node with Id: {id}");
        _logger.LogInformation($"config: {_configuration["GrpcExecutionService"]}");
        var handler = new HttpClientHandler();
        handler.ServerCertificateCustomValidationCallback =
            HttpClientHandler.DangerousAcceptAnyServerCertificateValidator;
                    try
        {
        var channel = GrpcChannel.ForAddress("http://localhost:7777", new GrpcChannelOptions { HttpHandler = handler });
        var client = new GrpcExecutionService.GrpcExecutionServiceClient(channel);
        var request = new ExecuteRequest
        {
            Id = id,
            Type = type,
            Properties = properties,
            DataFrame = dataframe
        };


            var response = client.ExecuteNode(request);
            return response;
        }
        catch (System.Exception ex)
        {
            _logger.LogError($"Failed to execute node with Id: {id}");
            _logger.LogError(ex.ToString());
            return null;
        }
    }

}
