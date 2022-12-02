from nltk.translate.meteor_score import meteor_score
import gzip, os, json, ast

# Uncomment if you haven't installed wordnet yet
# import nltk
# nltk.download('omw-1.4')
# nltk.download('wordnet')


def evaluate_meteor(prediction):
    references = []
    prediction = prediction.split()
    with gzip.open('qa_Grocery_and_Gourmet_Food.json.gz') as f:
        for l in f:
            j = l.decode('utf-8') # Decode to string
            j = ast.literal_eval(l.decode('utf-8')) # Turn to dict object
            question = j['question'] # Get only question property
            
            references.append(question.split(' ')) # Split words into array
            

    return meteor_score(references, prediction)

if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    prediction = 'this is a test'
    print(evaluate_meteor(prediction))