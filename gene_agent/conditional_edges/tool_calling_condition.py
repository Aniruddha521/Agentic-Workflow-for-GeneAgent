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
    get_pubmed_articles,
    get_disease_for_single_gene,
    get_domain_for_single_gene,
    get_gene_summary_for_single_gene
)


def tool_calling_condition(state : GeneAgentOverallState):

    multi_gene_set_tools = [
        get_complex_for_gene_set,
        get_enrichment_for_gene_set,
        get_interactions_for_gene_set,
        get_pathway_for_gene_set,
        get_pubmed_articles
    ]

    single_gene_tools = [
        get_disease_for_single_gene,
        get_domain_for_single_gene,
        get_gene_summary_for_single_gene 
    ]
    
    single_gene_group = [
            Send(
                "single_gene_subgraph_block", 
                GeneAgentSingleGeneState(
                    claims=state.claims,
                    subgraph_process_names=state.original_process_names,
                    curated_context=state.curated_context,
                    attached_tool = tool,
                    gene=gene
                )
            )
            for gene, tool in zip(state.genes, single_gene_tools)
        ]
    
    multiple_genes_group = [
            Send(
                "single_gene_subgraph_block", GeneAgentMultiGenesState(
                    claims=state.claims,
                    subgraph_process_names=state.original_process_names,
                    curated_context=state.curated_context,
                    attached_tool = tool,
                    gene=state.genes
                )
            )
            for tool in multi_gene_set_tools
        ]
    
    return single_gene_group + multiple_genes_group