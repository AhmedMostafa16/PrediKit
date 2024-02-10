using System.Text.Json;
using MediatR;
using Microsoft.Extensions.Caching.Distributed;
using MongoDB.Entities;
using StackExchange.Redis;

namespace WorkflowService;

// Review: I'm not sure if this service is not working as intended.
public sealed class BatchSaveService : IHostedService, IDisposable
{
    private readonly IDistributedCache _distributedCache;
    private readonly IMediator _mediator;
    private readonly Timer _timer;

    public BatchSaveService(IDistributedCache distributedCache, IMediator mediator)
    {
        _distributedCache = distributedCache;
        _mediator = mediator;
        _timer = new Timer(DoWork, null, TimeSpan.Zero, TimeSpan.FromMinutes(3));
    }

    private void DoWork(object state)
    {
        // Retrieve all keys from Redis
        using ConnectionMultiplexer redis = ConnectionMultiplexer.Connect("localhost:6379,allowAdmin=true");
        IDatabase db = redis.GetDatabase();

        var allKeys = redis.GetServer("localhost", 6379).Keys();

        // Fetch values from Redis and save to MongoDB
        List<Workflow> workflows = new(allKeys.Count());
        foreach (var key in allKeys)
        {
            var cachedValue = _distributedCache.GetString(key);
            var cachedWorkflowDto = JsonSerializer.Deserialize<UpdateWorkflowDto>(cachedValue);

            if (cachedWorkflowDto == null)
            {
                continue;
            }

            // var entity = new Workflow
            // {
            //     // Manual mapping
            //     ID = cachedWorkflowDto.Id,
            //     Title = cachedWorkflowDto.Title,
            //     Description = cachedWorkflowDto.Description,
            //     Nodes = cachedWorkflowDto.Nodes,
            //     Edges = cachedWorkflowDto.Edges,
            //     ViewPort = cachedWorkflowDto.ViewPort,
            //     ModifiedOn = cachedWorkflowDto.ModifiedOn,
            //     CreatedOn = cachedWorkflowDto.CreatedOn
            // };

            // workflows.Add(entity);
        }
        _mediator.Send(new BatchSaveWorkflowCommand { Workflows = workflows });
    }

    public Task StartAsync(CancellationToken cancellationToken)
    {
        _timer.Change(TimeSpan.Zero, TimeSpan.FromMinutes(3));
        return Task.CompletedTask;
    }

    public Task StopAsync(CancellationToken cancellationToken)
    {
        _timer.Change(Timeout.Infinite, 0);
        return Task.CompletedTask;
    }

    public void Dispose()
    {
        _timer.Dispose();
    }
}
