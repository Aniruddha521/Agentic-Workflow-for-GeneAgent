import requests
import json

def get_disease_for_single_gene(gene_name):
    url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/agentapi/disease/?"
    params = {
        "name": gene_name,
        "retmode": "json",
        "limit": 100
        }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json().get("results",{})
        diseases_data = {
            "gene_name": gene_name,
            "diseases": [
                {
                    "disease_caused": result.get("disease_name"),
                    "Number_of_Evidence": result.get("count")
                }
                for result in results
            ]   
        }

        return [diseases_data]
    else:
        return f"Error: Unable to fetch data"

# Example usage
# gene_name = "BRCA1"  # Replace with the gene name you are interested in
# gene_info = get_gene_complex(gene_name)
# print(gene_info)

get_disease_for_single_gene_doc = {
	"name": "get_disease_for_single_gene",
	"description": "Given a gene name, return information on the related diseases containing the disease id and the corresponding disease name.",
	"parameters": {
		"type": "object",
		"properties": {
			"gene_name": {
				"type": "string",
				"description": "A single gene name to search."
                }
            },
		"required": ["gene_name"],
	},
}


