import json
import gzip


filename = 'Cooking & Baking_schema.json' 
f = open(filename)
data = json.load(f)

# Loop through product items
for _, product in data.items():
    
    #print(product)
    description_schema = product['description_schema'] # Global Context
    print("Description Schema")
    print(product['description_schema'])
    for q in product["questions"]: # Loop through each question for the product
        local_schema = q['schema']
        missing_schema = [i for i in description_schema if i not in local_schema]
        if description_schema != missing_schema:
            print("Local Schema")
            print(local_schema)
            print("Missing Schema")
            print(missing_schema)
    print("------------------------")