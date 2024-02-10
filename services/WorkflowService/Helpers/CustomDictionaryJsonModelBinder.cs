using System.Text.Json;
using Microsoft.AspNetCore.Mvc.ModelBinding;

namespace WorkflowService.Helpers;

public sealed class CustomDictionaryJsonModelBinder : IModelBinder
{
    private readonly ILogger<CustomDictionaryJsonModelBinder> _logger;

    private static readonly JsonSerializerOptions _defaultJsonSerializerOptions = new JsonSerializerOptions(JsonSerializerDefaults.General)
    {
        Converters = { new CustomDictionaryJsonConverter() }
    };

    public CustomDictionaryJsonModelBinder(ILogger<CustomDictionaryJsonModelBinder> logger)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }


    public async Task BindModelAsync(ModelBindingContext bindingContext)
    {
        ArgumentNullException.ThrowIfNull(bindingContext);

        if (bindingContext.ModelType != typeof(Dictionary<string, object>))
        {
            throw new NotSupportedException($"The '{nameof(CustomDictionaryJsonModelBinder)}' model binder should only be used on Dictionary<string, object>, it will not work on '{bindingContext.ModelType.Name}'");
        }

        try
        {
            Dictionary<string, object>? data = await JsonSerializer.DeserializeAsync<Dictionary<string, object>>(bindingContext.HttpContext.Request.Body, _defaultJsonSerializerOptions);
            bindingContext.Result = ModelBindingResult.Success(data);
        }
        catch (Exception e)
        {
            _logger.LogError(e, "Error when trying to model bind Dictionary<string, object>");
            bindingContext.Result = ModelBindingResult.Failed();
        }
    }
}
