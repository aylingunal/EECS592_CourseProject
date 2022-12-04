from Bleu_Evaluation import *
from Meteor_Evaluation import *
from Gleu_Evaluation import *
from transformers import pipeline, BartTokenizer, BartForConditionalGeneration, BartConfig, AutoModelForSequenceClassification, AutoTokenizer
import os, sys

if __name__ == '__main__':

    # Output file
    output_file = "output.json"
    count_output = 50 # Number

    # Get descriptions from meta
    print("Loading description")
    descriptions = []   # Description for question generation
    with gzip.open('meta_Grocery_and_Gourmet_Food.json.gz') as f:
        for l in f:
            j = l.decode('utf-8') # Decode to string
            j = ast.literal_eval(l.decode('utf-8')) # Turn to dict object
            #print(j['description'])
            description = ' '.join(j['description'])
            descriptions.append(description) # Split words into array

    # Get questions from QA
    print("Loading questions")
    references = []     # Reference for evaluation
    with gzip.open('qa_Grocery_and_Gourmet_Food.json.gz') as f:
        for l in f:
            j = l.decode('utf-8') # Decode to string
            j = ast.literal_eval(l.decode('utf-8')) # Turn to dict object
            references.append(j['question'])

    # Load Model
    # Loads model from /models/fine-tuned-bart folder
    print("Loading model")
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
    model = BartForConditionalGeneration.from_pretrained("./models/fine_tuned_bart", local_files_only=True)
    #generator = pipeline(task="text-generation", model=model, tokenizer=tokenizer)
    #generator(references[0])

    # Generate questions based on description
    output = []
    print(f"Generating and evaluating questions ${len(descriptions[:50])}")
    i = 0
    for description in descriptions[:count_output]:
        inputs = tokenizer(description, max_length=1024, truncation=True, return_tensors="pt")
        input_ids = model.generate(inputs["input_ids"], max_new_tokens=1024)
        generated_question = tokenizer.batch_decode(input_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        
        gleu_score = evaluate_gleu(generated_question, references)
        bleu_score = evaluate_bleu(generated_question, references)
        meteor_score = evaluate_meteor(generated_question)
        outputObj = {
            "description": description,
            "question": generated_question,
            "gleu_score": gleu_score,
            "bleu_score": bleu_score,
            "meteor_score": meteor_score
        }
        output.append(outputObj)

        print(i)
        i+=1
        
    # Serializing json
    json_object = json.dumps(output, indent=4)
    
    # Writing to sample.json
    with open(output_file, "w") as outfile:
        outfile.write(json_object)
