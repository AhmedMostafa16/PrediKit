namespace WorkflowService;

/// <summary>
///     Represents a void type, since <see cref="System.Void" /> is not a valid return type in C#.
/// </summary>
public readonly struct Unit : IEquatable<Unit>, IComparable<Unit>, IComparable
{
    // The only instance of Unit. It's a singleton.
    private static readonly Unit _default = new();
    public static ref readonly Unit Default => ref _default;

    public static Task<Unit> Task { get; } = System.Threading.Tasks.Task.FromResult(Default);

    // Implement IEquatable<Unit> for equality comparisons
    public bool Equals(Unit other) => true;

    public override bool Equals(object obj) => obj is Unit;

    public override int GetHashCode() => 0;

    // Override ToString for meaningful debugging output
    public override string ToString() => "()";

    // Implement equality operators
    public static bool operator ==(Unit left, Unit right) => true;

    public static bool operator !=(Unit left, Unit right) => false;

    public int CompareTo(Unit other) => 0;

    public int CompareTo(object? obj) => obj is Unit ? 0 : 1;
}
