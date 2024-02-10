using MediatR;

namespace WorkflowService;

public class CreateWorkflowCommand : IRequest<Result<string>>
{
    public required WorkflowDto WorkflowDto { get; set; }
}