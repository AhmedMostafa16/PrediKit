using System.Diagnostics;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Text;
using System.Text.Json;
using AutoMapper;
using MediatR;
using MessagePack;
using MessagePack.Resolvers;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Caching.Distributed;
using Microsoft.IdentityModel.Tokens;
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using MongoDB.Entities;
using NetMQ;
using NetMQ.Sockets;


namespace WorkflowService
{
    [ApiController]
    [Route("api/[controller]")]
    public class WorkflowsController : ControllerBase
    {
        private readonly byte[] PING = [80, 105, 110, 103,]; // Ping
        private readonly byte[] PONG = [80, 111, 110, 103,]; // Pong
        private readonly byte[] OK = [79, 107,]; // Ok
        private readonly IMapper _mapper;
        private readonly IMediator _mediator;
        // private readonly IDistributedCache _distributedCache;
        private readonly HttpClient _httpClient;
        private readonly ILogger<WorkflowsController> _logger;

        public WorkflowsController(IMapper mapper,
                                   IMediator mediator,
                                   //    IDistributedCache distributedCache,
                                   IHttpClientFactory httpClientFactory,
                                   ILogger<WorkflowsController> logger
                                   )
        {
            _mapper = mapper;
            _mediator = mediator;
            // _distributedCache = distributedCache;
            _httpClient = httpClientFactory.CreateClient();
            _logger = logger;
        }

        [HttpGet("{id}/get_columns_names")]
        public async Task<ActionResult<List<string>>> GetColumnsNames(string id)
        {
            try
            {
                var workflow = await DB.Find<Workflow>().OneAsync(id);

                if (workflow is null)
                {
                    return NotFound();
                }


                var inputDataNode = _mapper.Map<ExecutionNode>(workflow.Nodes.Find(n => n.Type == "inputDataNode"));
                if (inputDataNode is null)
                {
                    string _message = "Basic filter node doesn't take any input";
                    _logger.LogError(_message);
                    return BadRequest(_message);
                }

                ExecutionNode executionNode = _mapper.Map<ExecutionNode>(inputDataNode);
                // executionNode.DataFrame = [];


                // Serialize the data to MessagePack format
                var serializedData = MessagePackSerializer.Serialize(executionNode, ContractlessStandardResolver.Options);

                // Create HttpContent with MessagePack data
                ByteArrayContent content = new(serializedData);
                content.Headers.Add("Content-Type", "application/msgpack");

                // Send POST request to the execution API endpoint
                var response = await _httpClient.PostAsync($"http://localhost:5501/execute_node", content);

                if (response.IsSuccessStatusCode)
                {
                    _logger.LogInformation($"Response: {response}");

                    var x = await response.Content.ReadAsByteArrayAsync();

                    ByteArrayContent content2 = new(x);
                    content2.Headers.Add("Content-Type", "application/msgpack");

                    var response2 = await _httpClient.PostAsync($"http://localhost:5501/get_all_columns", content2);

                    if (response2.IsSuccessStatusCode)
                    {
                        _logger.LogInformation($"Response: {response2}");
                        var columns = MessagePackSerializer.Deserialize<List<string>>(await response2.Content.ReadAsByteArrayAsync());

                        return Ok(columns);
                    }
                    else
                    {
                        _logger.LogError($"Response: {response2}");
                        // Handle unsuccessful response
                        return StatusCode((int)response2.StatusCode, "Request failed");
                    }

                }
                else
                {
                    _logger.LogError($"Response: {response}");
                    // Handle unsuccessful response
                    return StatusCode((int)response.StatusCode, "Request failed");
                }

            }
            catch (Exception ex)
            {
                _logger.LogError(ex.Message);
                // Handle exceptions
                return StatusCode(500, $"Internal Server Error: {ex.Message}");
            }
        }



        [HttpGet]
        public async Task<ActionResult<List<Workflow>>> GetAllWorkflows()
        {
            var workflows = await DB.Find<Workflow>().ManyAsync(_ => true);
            return Ok(workflows);
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Workflow>> GetWorkflowById(string id)
        {
            var result = await _mediator.Send(new GetWorkflowQuery { Id = ObjectId.Parse(id) });

            if (result.IsFailure)
            {
                _logger.LogError(result.Error);

                return NotFound(result.Error);
            }

            _logger.LogInformation($"Found workflow with Id: {id}");


            return Ok(result.Value);
        }

        [HttpPost]
        public async Task<ActionResult<Workflow>> CreateWorkflow([FromBody] WorkflowDto workflowDto)
        {
            var result = await _mediator.Send(new CreateWorkflowCommand { WorkflowDto = workflowDto });

            if (result.IsFailure)
            {
                _logger.LogError(result.Error);

                return BadRequest(result.Error);
            }

            _logger.LogInformation($"Created workflow with Id: {result.Value}");

            return Ok(result.Value);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateWorkflow(UpdateWorkflowDto workflowDto)
        {
            var workflow = await DB.Find<Workflow>().OneAsync(workflowDto.Id);
            _logger.LogInformation($"Updating workflow with Id: {workflowDto.Id}");
            _logger.LogInformation($"Workflow: {workflow}");
            if (workflow is null)
            {
                return NotFound();
            }

            workflow.Title = workflowDto.Title ?? workflow.Title;
            workflow.Description = workflowDto.Description ?? workflow.Description;
            workflow.Nodes = workflowDto.Nodes ?? workflow.Nodes;
            workflow.Edges = workflowDto.Edges ?? workflow.Edges;
            workflow.ViewPort = workflowDto.ViewPort;

            await DB.Update<Workflow>()
                .Match(w => w.ID == workflow.ID)
                .Modify(w => w.Title, workflow.Title)
                .Modify(w => w.Description, workflow.Description)
                .Modify(w => w.Nodes, workflow.Nodes)
                .Modify(w => w.Edges, workflow.Edges)
                .Modify(w => w.ViewPort, workflow.ViewPort)
                .ExecuteAsync();
            return Ok();
        }


        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteWorkflow(Guid id)
        {
            var workflow = await DB.Find<Workflow>().OneAsync(id);

            if (workflow is null)
            {
                return NotFound();
            }

            await workflow.DeleteAsync();

            return Ok();
        }

        public class ExecutionWorkflow
        {
            public required string Id { get; set; }
            public required List<Node> Nodes { get; set; }
            public required List<string[]> Paths { get; set; }
            public required Dictionary<string, string[]> Dependencies { get; set; }
        }

        [MethodImpl(MethodImplOptions.AggressiveOptimization)]
        private bool isServerOnline(INetMQSocket client)
        {
            // Send a ping message for health check
            client.SendFrame(MessagePackSerializer.Serialize(PING, ContractlessStandardResolver.Options));

            // Receive the response from the server
            byte[] response = client.ReceiveFrameBytes();

            // Check if the server responded with "Pong"
            return byteArrayCompare(response, PONG);
        }
#if WINDOWS
        [DllImport("msvcrt.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int memcmp(byte[] b1, byte[] b2, long count);

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        private static bool byteArrayCompare(byte[] b1, byte[] b2)
        {
            // Validate buffers are the same length.
            // This also ensures that the count does not exceed the length of either buffer.  
            return b1.Length == b2.Length && memcmp(b1, b2, b1.Length) == 0;
        }

#else
        [DllImport("libc", CallingConvention = CallingConvention.Cdecl)]
        private static extern int memcmp(byte[] b1, byte[] b2, long count);

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        private static bool byteArrayCompare(byte[] b1, byte[] b2)
        {
            // Validate buffers are the same length.
            // This also ensures that the count does not exceed the length of either buffer.  
            return b1.Length == b2.Length && memcmp(b1, b2, b1.Length) == 0;
        }
#endif
        [HttpPost("execute")]
        public async Task<IActionResult> ExecuteWorkflow([FromBody] ExecutionWorkflow executionWorkflow)
        {
            using (DealerSocket client = new DealerSocket())
            {
                // Connect to the Data Science microservice
                client.Connect("tcp://127.0.0.1:5555");

                // Set the identity of the client
                client.Options.Identity = Encoding.UTF8.GetBytes($"Client-{Guid.NewGuid()}");

                // Check if the server responded with "Pong"
                if (!isServerOnline(client))
                {
                    _logger.LogError("Data science microservice is not reachable");
                    return BadRequest("Connection with the server failed");
                }

                Stopwatch stopwatch = new();
                stopwatch.Start();

                // Send the paths to the Data Science microservice
                foreach (string[] path in executionWorkflow.Paths)
                {
                    foreach (string item in path)
                    {
                        Node node = executionWorkflow.Nodes.First(n => n.Id == item);

                        // Map the node to ExecutionNode
                        ExecutionNode executionNode = new()
                        {
                            CurrentId = node.Id,
                            NodeType = node.Type,
                            Data = node.Data,
                            Dependencies = executionWorkflow.Dependencies.TryGetValue(node.Id, out var value) ? value : Array.Empty<string>(),
                        };

                        // Serialize the data to MessagePack format
                        byte[] serializedNode = MessagePackSerializer.Serialize(executionNode, ContractlessStandardResolver.Options);

                        // Send MessagePack data to the server
                        client.SendFrame(serializedNode);

                        // Receive response from the server
                        byte[] response = client.ReceiveFrameBytes();

                        // Check if the server responded with "Ok"
                        if (!byteArrayCompare(response, OK))
                        {
                            return BadRequest("Execution of a node with id: " + node.Id + " failed. \n" + response);
                        }

                        // Send to the notification service that uses SignalR that the node has been executed to update the edges
                        await _mediator.Send(new UpdateEdgesNotificationCommand { UpdateEdgesNotificationDto = new UpdateEdgesNotificationDto { WorkflowId = executionWorkflow.Id, NodeId = node.Id } });
                    }
                    stopwatch.Stop();
                    Console.WriteLine($"Time elapsed: {stopwatch.ElapsedMilliseconds} ms, {stopwatch.ElapsedTicks} ticks");
                }

            }

            return Ok();
        }

    }
}
