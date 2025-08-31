from langgraph.constants import Send
from gene_agent.states import (
    GeneAgentSingleGeneState,
    GeneAgentMultiGenesState,
    GeneAgentOverallState
)
from gene_agent.tools import (
    get_complex_for_gene_set,
    get_enrichment_for_gene_set,
    get_interactions_for_gene_set,
    get_pathway_for_gene_set,
    get_disease_for_single_gene,
    get_domain_for_single_gene,
    get_gene_summary_for_single_gene
)


def tool_calling_condition(state : GeneAgentOverallState):

    multi_gene_set_tools = [
        # get_enrichment_for_gene_set,
        # get_interactions_for_gene_set,
        get_pathway_for_gene_set,
    ]

    single_gene_tools = [
        get_disease_for_single_gene,
        get_domain_for_single_gene,
        get_complex_for_gene_set,
        # get_gene_summary_for_single_gene 
    ]
    
    single_gene_group = [
            Send(
                "single_gene_data_fetching", 
                GeneAgentSingleGeneState(
                    claims=state.claims,
                    process_names=state.original_process_names,
                    analytical_narrative=state.original_analytical_narrative,
                    attached_tool=tool,
                    gene=gene
                )
            )
            for tool in single_gene_tools
            for gene in state.genes
        ]
 
    multiple_genes_group = [
            Send(
                "gene_set_data_fetching", GeneAgentMultiGenesState(
                    claims=state.claims,
                    process_names=state.original_process_names,
                    analytical_narrative=state.original_analytical_narrative,
                    attached_tool = tool,
                    genes=state.genes
                )
            )
            for tool in multi_gene_set_tools
        ]
    
    return single_gene_group + multiple_genes_group