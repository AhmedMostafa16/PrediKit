namespace WorkflowService;

public readonly struct Result<T>
{
    private readonly T _value;
    private readonly bool _isSuccess;
    private readonly string _error;

    private Result(T value)
    {
        _value = value;
        _isSuccess = true;
        _error = null;
    }

    private Result(string error)
    {
        _error = error ?? throw new ArgumentNullException(nameof(error));
        _value = default;
        _isSuccess = false;
    }

    public static Result<T> Ok(T value) => new(value);

    public static Result<T> Fail(string error) => new(error);

    public bool IsSuccess => _isSuccess;

    public bool IsFailure => !_isSuccess;

    public T Value
    {
        get
        {
            if (!_isSuccess)
            {
                throw new InvalidOperationException("Cannot access the value of a failed result.");
            }

            return _value;
        }
    }

    public string Error
    {
        get
        {
            if (_isSuccess)
            {
                throw new InvalidOperationException("Cannot access the error of a successful result.");
            }

            return _error;
        }
    }

    public Result<T> OnSuccess(Action<T> action)
    {
        if (_isSuccess)
        {
            action(_value);
        }

        return this;
    }

    public Result<T> OnFailure(Action<string> action)
    {
        if (!_isSuccess)
        {
            action(_error);
        }

        return this;
    }

    public Exception ToException()
    {
        if (IsFailure)
        {
            return new InvalidOperationException(Error);
        }

        throw new InvalidOperationException("Cannot convert a successful result to an exception.");
    }
}