import requests
import json

def get_complex_for_gene_set(gene_name):
    # gene_set = gene_set.replace(" ","")
    
    url = "https://www.ncbi.nlm.nih.gov/research/pubtator3-api/agentapi/complex/?"
    params = {
        "name": gene_name,
        "retmode": "json",
        "limit": 10
        }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json().get("results",{})
        complex_data = {
            "gene_name": gene_name,
            "complexes": [
                {
                    "complex_ac": result.get("complex_ac"),
                    "complex_name": result.get("complex_name"),
                    "Number_of_Evidence": result.get("count")
                }
                for result in results
            ]   
        }

        return [complex_data]
    else:
        return f"Error: Unable to fetch data"


get_complex_for_gene_set_doc = {
	"name": "get_complex_for_gene_set",
	"description": "Given a gene set, return information on its all possible complex protocal ids and the corresponding complex names.",
	"parameters": {
		"type": "object",
		"properties": {
			"gene_set": {
				"type": "string",
				"description": "A gene set only delimitted with \",\" to search, for example, \"x,y,z\"."
                }
            },
		"required": ["gene_set"],
	},
}


