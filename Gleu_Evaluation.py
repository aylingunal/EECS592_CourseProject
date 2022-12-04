from nltk.translate.gleu_score import sentence_gleu
import gzip, os, json, ast

def evaluate_gleu(prediction, references):
    prediction = prediction.split()
    for reference in references:
        reference = reference.split()
    references = [reference.split() for reference in references]
    return sentence_gleu(references, prediction)

if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    references = []
    with gzip.open('qa_Grocery_and_Gourmet_Food.json.gz') as f:
        for l in f:
            j = l.decode('utf-8') # Decode to string
            j = ast.literal_eval(l.decode('utf-8')) # Turn to dict object
            question = j['question'] # Get only question property
            
            references.append(question) # Split words into array
    prediction = 'this is a test'
    print(evaluate_gleu(prediction, references))
    