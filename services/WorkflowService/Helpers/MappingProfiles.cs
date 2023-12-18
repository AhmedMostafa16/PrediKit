using AutoMapper;

namespace WorkflowService;

public class MappingProfiles : Profile
{
    public MappingProfiles()
    {
        CreateMap<WorkflowDto, Workflow>();
        CreateMap<Node, ExecutionNode>();
    }
}