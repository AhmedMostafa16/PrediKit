using MediatR;
using MongoDB.Entities;

namespace WorkflowService;

public class BatchSaveWorkflowCommandHandler : IRequestHandler<BatchSaveWorkflowCommand, Result<string>>
{
    private readonly ILogger<BatchSaveWorkflowCommandHandler> _logger;

    public BatchSaveWorkflowCommandHandler(ILogger<BatchSaveWorkflowCommandHandler> logger)
    {
        _logger = logger;
    }
    public async Task<Result<string>> Handle(BatchSaveWorkflowCommand request, CancellationToken cancellationToken)
    {
        try
        {
            var bulkWriteResult = await DB.SaveAsync(request.Workflows, cancellation: cancellationToken);
            _logger.LogInformation($"Successfully saved workflows to MongoDB");
            _logger.LogInformation($"Modified count: {bulkWriteResult.ModifiedCount}");
            _logger.LogInformation($"Acknowledged: {bulkWriteResult.IsAcknowledged}");
            _logger.LogInformation($"Inserted count: {bulkWriteResult.InsertedCount}");
            _logger.LogInformation($"Matched count: {bulkWriteResult.MatchedCount}");

            if (bulkWriteResult.IsAcknowledged && bulkWriteResult.ModifiedCount == request.Workflows.Count)
            {
                return Result<string>.Ok("Successfully saved workflows to MongoDB");
            }
            else
            {
                return Result<string>.Fail("Failed to save workflows to MongoDB");
            }
        }
        catch (Exception ex)
        {
#if DEBUG
            return Result<string>.Fail("Failed to save workflows.\n" + ex.ToString());
#else
            return Result<string>.Fail("Failed to save workflow.");
#endif
        }
    }
}
