using AutoMapper;
using MediatR;
using Microsoft.AspNetCore.SignalR;

namespace WorkflowService;

public class UpdateEdgesNotificationCommandHandler : IRequestHandler<UpdateEdgesNotificationCommand, Result<Unit>>
{
    private readonly IMapper _mapper;
    private readonly IHubContext<WorkflowNotificationHub> _hubContext;

    public UpdateEdgesNotificationCommandHandler(IMapper mapper, IHubContext<WorkflowNotificationHub> hubContext)
    {
        _mapper = mapper;
        _hubContext = hubContext;
    }

    // This handler should send a notification to the NotificationService
    // to update the UI with the new workflow state.
    public async Task<Result<Unit>> Handle(UpdateEdgesNotificationCommand request, CancellationToken cancellationToken)
    {
        await _hubContext.Clients.Group(request.UpdateEdgesNotificationDto.WorkflowId)
        .SendAsync("UpdateEdgesNotification", request.UpdateEdgesNotificationDto, cancellationToken);

        return Result<Unit>.Ok(Unit.Default);
    }
}
