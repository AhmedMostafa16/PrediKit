using System.Reflection;
using MongoDB.Driver;
using MongoDB.Entities;
using Serilog;
using WorkflowService;


var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddSignalR();
builder.Services.AddAutoMapper(AppDomain.CurrentDomain.GetAssemblies());
builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(Assembly.GetExecutingAssembly()));

// Register validators
// builder.Services.AddTransient(typeof(IPipelineBehavior<,>), typeof(RequestValidationBehavior<,>));

// Register the logger
builder.Services.AddSingleton(LoggerConfig.ConfigureLogger());
builder.Host.UseSerilog(LoggerConfig.ConfigureLogger());

// Register Redis as a distributed cache
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("RedisDefaultConnection");
});

builder.Services.AddHttpClient();
// Register MongoDB
var mongoSettings = MongoClientSettings.FromConnectionString(
        builder.Configuration.GetConnectionString("DefaultConnection"));
mongoSettings.MaxConnecting = Environment.ProcessorCount;

await DB.InitAsync("Cluster0", settings: mongoSettings);

var app = builder.Build();

app.UseSerilogRequestLogging();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// app.UseAntiforgery();

app.UseAuthorization();

app.UseCors(x => x
        .AllowAnyMethod()
        .AllowAnyHeader()
        .SetIsOriginAllowed(origin => true) // allow any origin
        .AllowCredentials()); // allow credentials


app.MapControllers();

app.MapHub<WorkflowNotificationHub>("/workflows");

app.Run();
