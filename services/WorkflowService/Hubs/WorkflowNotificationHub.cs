using Microsoft.AspNetCore.SignalR;

namespace WorkflowService;

public class WorkflowNotificationHub : Hub
{

    public async Task JoinWorkflowGroup(string workflowId)
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, workflowId);
    }

    public async Task LeaveWorkflowGroup(string workflowId)
    {
        await Groups.RemoveFromGroupAsync(Context.ConnectionId, workflowId);
    }

    public override async Task OnConnectedAsync()
    {
        var httpContext = Context.GetHttpContext();
        var workflowId = httpContext?.Request.Query["workflowId"];
        if (workflowId is not null)
        {
            await Groups.AddToGroupAsync(Context.ConnectionId, workflowId!);
            await base.OnConnectedAsync();
        }
    }

    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        await base.OnDisconnectedAsync(exception);
    }
}
