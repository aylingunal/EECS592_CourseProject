
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import gzip, os, json, ast

def evaluate_bleu(prediction, references):
    prediction = prediction.split()
    for reference in references:
        reference = reference.split()
    references = [reference.split() for reference in references]
    chencherry = SmoothingFunction()
    return sentence_bleu(references, prediction, smoothing_function=chencherry.method1)

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
    print(evaluate_bleu(prediction, references))
    