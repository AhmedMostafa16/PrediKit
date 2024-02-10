using Serilog;
using Serilog.Events;
using Serilog.Formatting.Compact;

namespace WorkflowService;

public class LoggerConfig
{
    public static Serilog.ILogger ConfigureLogger()
    {
#if DEBUG
        return new LoggerConfiguration()
            .MinimumLevel.Information()
            .Enrich.FromLogContext()
            .WriteTo.Console(restrictedToMinimumLevel: LogEventLevel.Information)
            // Add more sinks or configuration here (e.g., file, database, etc.)
            .CreateLogger();
#else
        return new LoggerConfiguration()
            .MinimumLevel.Warning()
            .Enrich.FromLogContext()
            .WriteTo.File(new CompactJsonFormatter(), "WorkflowService.log", rollingInterval: RollingInterval.Day, retainedFileCountLimit: 31, buffered: true, flushToDiskInterval: TimeSpan.FromSeconds(1))
            .WriteTo.Console(restrictedToMinimumLevel: LogEventLevel.Warning, outputTemplate:
        "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj}{NewLine}{Exception}")
            // Add more sinks or configuration here (e.g., file, database, etc.)
            .CreateLogger();
#endif

    }
}
