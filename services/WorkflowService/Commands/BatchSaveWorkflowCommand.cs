using MediatR;

namespace WorkflowService;

public class BatchSaveWorkflowCommand : IRequest<Result<string>>
{
    public required List<Workflow> Workflows { get; set; }
}
