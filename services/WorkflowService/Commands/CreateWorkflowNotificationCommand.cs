using MediatR;

namespace WorkflowService;

public class UpdateEdgesNotificationCommand : IRequest<Result<Unit>>
{
    public UpdateEdgesNotificationDto UpdateEdgesNotificationDto { get; set; }
}