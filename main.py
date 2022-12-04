from Bleu_Evaluation import *
from Meteor_Evaluation import *
from Gleu_Evaluation import *
from transformers import pipeline, BartTokenizer, BartForConditionalGeneration
import os, sys, math, json

def create_product_file():
    products = []

    # Get questions from QA
    print("Loading questions")
    products = {} 
    with gzip.open('qa_Grocery_and_Gourmet_Food.json.gz') as f:
        for l in f:
            j = l.decode('utf-8') 
            j = ast.literal_eval(l.decode('utf-8')) 
            if j['asin'] not in products.keys():
                products[j['asin']] = {}
                products[j['asin']]['questions'] = []
           
            products[j['asin']]['questions'].append(j['question']) 

    # Get products from meta
    print("Loading products")
    with gzip.open('meta_Grocery_and_Gourmet_Food.json.gz') as f:
        for l in f:
            j = l.decode('utf-8')
            j = ast.literal_eval(l.decode('utf-8'))
            description = ' '.join(j['description'])
            if j['asin'] in products.keys():
                products[j['asin']]['description'] = description

    # Remove if no product description is found
    products = list(products.values()) # Flatten (remove asin key)
    products = [product for product in products if 'description' in product.keys()]
    
    # Serializing json
    json_object = json.dumps(products, indent=4)
    
    # Writing to sample.json
    with open("output/products.json", "w") as outfile:
        outfile.write(json_object)

def generate_questions():
    f = open('output/products.json')
    products = json.load(f)
    output = []
    # Load Model
    # Loads model from /models/fine-tuned-bart folder
    print("Loading model")
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
    model = BartForConditionalGeneration.from_pretrained("./models/fine_tuned_bart", local_files_only=True)
    #generator = pipeline(task="text-generation", model=model, tokenizer=tokenizer)
    #generator(references[0])

    # Generate questions based on description
    print(f"Generating questions {len(products)}")
    
    for (i, product) in enumerate(products):
        print(i)
        description = product['description']
        
        inputs = tokenizer(description, max_length=1024, truncation=True, return_tensors="pt")
        input_ids = model.generate(inputs["input_ids"], max_new_tokens=1024)
        generated_question = tokenizer.batch_decode(input_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        product['generated_question'] = generated_question

    
    # Serializing json
    json_object = json.dumps(products, indent=4)
    
    # Writing to sample.json
    with open("output/generated_questions.json", "w") as outfile:
        outfile.write(json_object)

def evaluate_questions():
    references = []
    with gzip.open('qa_Grocery_and_Gourmet_Food.json.gz') as f:
        for l in f:
            j = l.decode('utf-8') # Decode to string
            j = ast.literal_eval(l.decode('utf-8')) # Turn to dict object
            question = j['question'] # Get only question property
            
            references.append(question) # Split words into array


    f = open('output/generated_questions.json')
    products = json.load(f)
    print("Evaluating generated questions")
    for (i, product) in enumerate(products):
        print(i)
        generated_question = product['generated_question']
        product['gleu_score'] = evaluate_gleu(generated_question, references)
        product['bleu_score'] = evaluate_bleu(generated_question, references)
        product['meteor_score'] = evaluate_meteor(generated_question)

    # Serializing json
    json_object = json.dumps(products, indent=4)
    
    # Writing to sample.json
    with open("output/generated_questions.json", "w") as outfile:
        outfile.write(json_object)

if __name__ == '__main__':
    # create_product_file()
    # generate_questions()
    evaluate_questions()
    # # Output file
    # output_file = "products.json"

    # # Get products from meta
    

    # exit(0)
    # # Load Model
    # # Loads model from /models/fine-tuned-bart folder
    # print("Loading model")
    # tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
    # model = BartForConditionalGeneration.from_pretrained("./models/fine_tuned_bart", local_files_only=True)
    # #generator = pipeline(task="text-generation", model=model, tokenizer=tokenizer)
    # #generator(references[0])

    # # Generate questions based on description
    # output = []
    # print(f"Generating and evaluating questions {len(descriptions)}")
    # num_per_file = 10 # Number of questions to generate per file
    # i = 0

    # # while i < len(descriptions):
    # #     print(i)
        

    # #     description = descriptions[i]
        
    # #     inputs = tokenizer(description, max_length=1024, truncation=True, return_tensors="pt")
    # #     input_ids = model.generate(inputs["input_ids"], max_new_tokens=1024)
    # #     generated_question = tokenizer.batch_decode(input_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        
    # #     gleu_score = evaluate_gleu(generated_question, references)
    # #     bleu_score = evaluate_bleu(generated_question, references)
    # #     meteor_score = evaluate_meteor(generated_question)
    # #     outputObj = {
    # #         "description": description,
    # #         "question": generated_question,
    # #         "gleu_score": gleu_score,
    # #         "bleu_score": bleu_score,
    # #         "meteor_score": meteor_score
    # #     }
    # #     output.append(outputObj)

    # #     if (i+1) % num_per_file == 0:
    # #         # Serializing json
    # #         json_object = json.dumps(output, indent=4)
            
    # #         output_file = f"output/output-{math.floor(i/num_per_file)}.json"

    # #         # Writing to sample.json
    # #         with open(output_file, "w") as outfile:
    # #             outfile.write(json_object)

    # #         output = []

    # #         if i == 20:
    # #             break
        
        
    # #     i+=1

        

    # for description in descriptions:
    #     inputs = tokenizer(description, max_length=1024, truncation=True, return_tensors="pt")
    #     input_ids = model.generate(inputs["input_ids"], max_new_tokens=1024)
    #     generated_question = tokenizer.batch_decode(input_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        
    #     # gleu_score = evaluate_gleu(generated_question, references)
    #     # bleu_score = evaluate_bleu(generated_question, references)
    #     # meteor_score = evaluate_meteor(generated_question)
    #     outputObj = {
    #         "description": description,
    #         "question": generated_question,
    #         # "gleu_score": gleu_score,
    #         # "bleu_score": bleu_score,
    #         # "meteor_score": meteor_score
    #     }
    #     output.append(outputObj)

    #     print(i)
    #     i+=1
        
    # # Serializing json
    # json_object = json.dumps(output, indent=4)
    
    # # Writing to sample.json
    # with open("output/questions.json", "w") as outfile:
    #     outfile.write(json_object)
