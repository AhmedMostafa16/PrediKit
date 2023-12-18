using AutoMapper;
using MediatR;
using MongoDB.Entities;

namespace WorkflowService;

public class CreateWorkflowCommandHandler : IRequestHandler<CreateWorkflowCommand, Result<string>>
{
    private readonly IMapper _mapper;

    public CreateWorkflowCommandHandler(IMapper mapper)
    {
        _mapper = mapper;
    }

    public async Task<Result<string>> Handle(CreateWorkflowCommand request, CancellationToken cancellationToken)
    {
        var workflow = _mapper.Map<Workflow>(request.WorkflowDto);

        try
        {
            await DB.SaveAsync(workflow, cancellation: cancellationToken);
        }
        catch (Exception ex)
        {
#if DEBUG
            return Result<string>.Fail("Failed to create workflow.\n" + ex.ToString());
#else
            return Result<string>.Fail("Failed to create workflow.");
#endif
        }

        return Result<string>.Ok(workflow.ID);
    }
}
