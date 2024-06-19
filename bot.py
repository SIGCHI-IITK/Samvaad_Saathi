import requests

from summary import summ
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
Summary_url="https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}

def query(payload,url):
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
def llm(current_query) :
    # Reading from a text file
   with open('input.txt', 'r') as file:
     data = file.read()
   if len(data)==0:
      context=current_query
   else : 
    context =current_query + " (Answer in Context of "+ data +")"
    print("context: " + context)
# Second query with context included in the input
   output = query({
    "inputs": context
},API_URL)
   
   response = output[0]['generated_text'][len(context):]
   print("answer : "+response)
   summary=summ(response)
   
   with open("input.txt", 'w') as file:
    file.write(summary)
   return response  

