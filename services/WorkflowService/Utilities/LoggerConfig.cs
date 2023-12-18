using Serilog;
using Serilog.Events;

namespace WorkflowService;

public class LoggerConfig
{
    public static Serilog.ILogger ConfigureLogger()
    {
        return new LoggerConfiguration()
            .MinimumLevel.Information()
            .Enrich.FromLogContext()
            .WriteTo.Console()
            // Add more sinks or configuration here (e.g., file, database, etc.)
            .CreateLogger();

    }
}
