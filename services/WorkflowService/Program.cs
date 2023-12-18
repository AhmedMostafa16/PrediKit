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
builder.Services.AddAutoMapper(AppDomain.CurrentDomain.GetAssemblies());
builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(Assembly.GetExecutingAssembly()));

// Register validators
// builder.Services.AddTransient(typeof(IPipelineBehavior<,>), typeof(RequestValidationBehavior<,>));

// Register the logger
builder.Services.AddSingleton(LoggerConfig.ConfigureLogger());
builder.Host.UseSerilog(LoggerConfig.ConfigureLogger());

// Register Redis as a distributed cache
// builder.Services.AddStackExchangeRedisCache(options =>
// {
//     options.Configuration = "localhost:6379";
//     options.InstanceName = "WorkflowService";
// });

// builder.Services.AddScoped<GrpcExecutionClient>();
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

app.UseAuthorization();

app.UseCors(builder => builder
    .AllowAnyOrigin()
    .AllowAnyMethod()
    .AllowAnyHeader());


app.MapControllers();

app.Run();
