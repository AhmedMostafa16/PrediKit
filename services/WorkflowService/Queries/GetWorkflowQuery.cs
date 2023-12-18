using MediatR;
using MongoDB.Bson;

namespace WorkflowService;

public class GetWorkflowQuery : IRequest<Result<WorkflowDto>>
{
    public required ObjectId Id { get; set; }
}
