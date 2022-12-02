
from nltk.translate.bleu_score import sentence_bleu
import gzip, os, json, ast

def evaluate_bleu(prediction):
    references = []
    prediction = prediction.split()
    with gzip.open('qa_Grocery_and_Gourmet_Food.json.gz') as f:
        for l in f:
            j = l.decode('utf-8') # Decode to string
            j = ast.literal_eval(l.decode('utf-8')) # Turn to dict object
            question = j['question'] # Get only question property
            
            references.append(question.split(' ')) # Split words into array
            
    #candidate = ['this', 'is', 'a', 'test']

    # Commented are the bleu-1,2,3 evals
    # print('Cumulative 1-gram: %f' % sentence_bleu(references, candidate, weights=(1, 0, 0, 0)))
    # print('Cumulative 2-gram: %f' % sentence_bleu(references, candidate, weights=(0.5, 0.5, 0, 0)))
    # print('Cumulative 3-gram: %f' % sentence_bleu(references, candidate, weights=(0.33, 0.33, 0.33, 0)))

    #print('Cumulative 4-gram: %f' % sentence_bleu(references, candidate, weights=(0.25, 0.25, 0.25, 0.25)))
    return sentence_bleu(references, prediction, weights=(0.25, 0.25, 0.25, 0.25))

if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    prediction = 'this is a test'
    print(evaluate_bleu(prediction))
    