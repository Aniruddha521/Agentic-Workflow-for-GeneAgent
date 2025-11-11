import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

def nunique(seq: list):
    unique_seq = set()
    for i in seq:
        unique_seq.add(i)
    return unique_seq

def find_difference(query1: str, query2: str):
    stop = set(stopwords.words('english'))
    pattern = r"[`~!@#$%^&*()_ +={}\[\]:;\"'\/\?\.,><\\|]"
    query1 = list(re.split(pattern, query1))
    query2 = list(re.split(pattern, query2))
    filtered = lambda query: [w for w in query if w.lower() not in stop]
    unique_query1 = nunique(filtered(query1))
    unique_query2 = nunique(filtered(query2))
    
    missing_part = []
    extra_part = []

    for missed in unique_query1:
        if missed not in unique_query2:
            missing_part.append(missed)
        
    for extra in unique_query2:
        if extra not in unique_query1:
            extra_part.append(extra)
    
    query = missing_part + extra_part
    uncommom_part = " ".join(query)

    return uncommom_part
