using FluentValidation;

namespace WorkflowService;

public class CreateWorkflowCommandValidator : AbstractValidator<Workflow>
{
    public CreateWorkflowCommandValidator()
    {
        RuleFor(x => x.Title).NotEmpty().WithMessage("Title is required.");
        RuleFor(x => x.ViewPort).NotEmpty().WithMessage("ViewPort is required.");
    }

}
