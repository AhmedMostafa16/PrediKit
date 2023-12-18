using MediatR;
using MongoDB.Entities;

namespace WorkflowService;

public class GetWorkflowQueryHandler : IRequestHandler<GetWorkflowQuery, Result<WorkflowDto>>
{
    public async Task<Result<WorkflowDto>> Handle(GetWorkflowQuery request, CancellationToken cancellationToken)
    {
        Workflow? workflow = null;
        try
        {
            workflow = await DB.Find<Workflow>()
           .OneAsync(request.Id, cancellationToken);
        }
        catch (Exception ex)
        {
#if DEBUG
            return Result<WorkflowDto>.Fail("Failed to find workflow.\n" + ex.ToString());
#else
            return Result<WorkflowDto>.Fail($"Failed to find workflow with Id: {request.Id}.");
#endif
        }

        if (workflow is null)
        {
            return Result<WorkflowDto>.Fail("Workflow not found.");
        }

        var workflowDto = new WorkflowDto
        {
            // Manual mapping
            Title = workflow.Title,
            Description = workflow.Description,
            Nodes = workflow.Nodes,
            Edges = workflow.Edges,
            ViewPort = workflow.ViewPort,
            CreatedOn = workflow.CreatedOn,
            ModifiedOn = workflow.ModifiedOn
        };

        return Result<WorkflowDto>.Ok(workflowDto);
    }
}
