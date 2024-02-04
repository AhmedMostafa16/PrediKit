import { UpdateEdgesNotificationDto } from '@/models/UpdateEdgesNotificationDto';
import useFlowStore from '@/stores/FlowStore';
import * as signalR from '@microsoft/signalr';
import { HubConnectionBuilder, LogLevel } from '@microsoft/signalr';

// const URL = process.env.HUB_ADDRESS ?? 'https://localhost:5000/workflows';
const URL = 'http://localhost:5000/workflows';

class SignalrService {
  private connection?: signalR.HubConnection;
  public events: (
    onNotificationReceived: (notifications: UpdateEdgesNotificationDto) => void
  ) => void;
  static instance: SignalrService;
  constructor() {
    (async () => {
      this.connection = new HubConnectionBuilder()
        .withUrl(URL + '?workflowId=' + useFlowStore.getState().currentWorkflowId, {
          /* options */
        })
        .withAutomaticReconnect()
        .configureLogging(LogLevel.Information)
        .build();

      await this.connection.start().catch((err) => console.error(err));
    })();

    this.events = (onNotificationReceived) => {
      this.connection?.on('UpdateEdgesNotification', (notifications: UpdateEdgesNotificationDto) => {
        // console.debug('Received notifications: ', notifications);
        onNotificationReceived(notifications);
      });
    };
  }

  public static getInstance(): SignalrService {
    if (!SignalrService.instance) SignalrService.instance = new SignalrService();
    return SignalrService.instance;
  }
}

export default SignalrService.getInstance;
