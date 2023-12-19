using System.Text;
using System.Text.Json;
using AutoMapper;
using MediatR;
using MessagePack;
using MessagePack.Resolvers;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Caching.Distributed;
using MongoDB.Bson;
using MongoDB.Entities;


namespace WorkflowService
{
    [ApiController]
    [Route("api/[controller]")]
    public class WorkflowsController : ControllerBase
    {
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

        [HttpPost("{id}/execute")]
        public async Task<IActionResult> ExecuteWorkflow(string id)
        {
            try
            {
                var workflow = await DB.Find<Workflow>().OneAsync(id);

                if (workflow is null)
                {
                    return NotFound();
                }
                string dataframe = string.Empty;

                foreach (var node in workflow.Nodes)
                {
                    if (node is null)
                    {
                        string _message = "Workflow has no nodes";
                        _logger.LogError(_message);
                        return BadRequest(_message);
                    }

                    ExecutionNode executionNode = _mapper.Map<ExecutionNode>(node);
                    executionNode.DataFrame = dataframe;

                    // System.Console.WriteLine("Dataframe: " + dataframe);

                    // Serialize the data to MessagePack format
                    var serializedData = MessagePackSerializer.Serialize(executionNode, ContractlessStandardResolver.Options);

                    // Create HttpContent with MessagePack data
                    ByteArrayContent content = new ByteArrayContent(serializedData);
                    content.Headers.Add("Content-Type", "application/msgpack");

                    // Send POST request to the execution API endpoint
                    var response = await _httpClient.PostAsync($"http://localhost:5501/execute_node", content);


                    // Check if the request was successful
                    if (response.IsSuccessStatusCode)
                    {
                        _logger.LogInformation($"Response: {response}");

                        var x = await response.Content.ReadAsByteArrayAsync();

                        // System.Console.WriteLine("Dataframe: " + Encoding.UTF8.GetString(x));

                        dataframe = MessagePackSerializer.Deserialize<string>(x);

                        _logger.LogInformation($"Finished: {node.Id}");
                    }
                    else
                    {
                        _logger.LogError($"Response: {response}");
                        // Handle unsuccessful response
                        return StatusCode((int)response.StatusCode, "Request failed");
                    }

                }
                return Ok();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex.Message);
                // Handle exceptions
                return StatusCode(500, $"Internal Server Error: {ex.Message}");
            }
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
                executionNode.DataFrame = string.Empty;


                // Serialize the data to MessagePack format
                var serializedData = MessagePackSerializer.Serialize(executionNode, ContractlessStandardResolver.Options);

                // Create HttpContent with MessagePack data
                ByteArrayContent content = new ByteArrayContent(serializedData);
                content.Headers.Add("Content-Type", "application/msgpack");

                // Send POST request to the execution API endpoint
                var response = await _httpClient.PostAsync($"http://localhost:5501/execute_node", content);

                if (response.IsSuccessStatusCode)
                {
                    _logger.LogInformation($"Response: {response}");

                    var x = await response.Content.ReadAsByteArrayAsync();

                    ByteArrayContent content2 = new ByteArrayContent(x);
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
        public async Task<ActionResult<Workflow>> CreateWorkflow(WorkflowDto workflowDto)
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
    }
}
