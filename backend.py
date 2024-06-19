
from flask import Flask, render_template,request, jsonify
from flask_cors import CORS
import requests
from bot import llm
app=Flask(__name__)
CORS(app)
@app.route('/')
def chat_page() :
    return render_template('lingus3.html')

# API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b-it"
API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b-it"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def converter(text,src,tr) :
   url = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
   headers={
    "userID" :"e28eed36b79a471ebba8df32358bbcdd",
    "ulcaApiKey" : "0082ebf9fe-38bc-447c-8c4d-78442d5e7d7c"
}
   payload={
    "pipelineTasks": [

        {
            "taskType": "translation",
            "config": {
                "language": {
                    "sourceLanguage": src,
                    "targetLanguage": tr
                }
            }
        },

    ],
    "pipelineRequestConfig": {
        "pipelineId" : "64392f96daac500b55c543cd"
    }
}
   resp=requests.post(url,json=payload,headers=headers)
   response_data = resp.json()
   service_id = response_data["pipelineResponseConfig"][0]["config"][0]["serviceId"]

   compute_payload = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": src,
                            "targetLanguage": tr
                        },
                        "serviceId": service_id
                    }
                }
            ],
            "inputData": {
                "input": [
                    {
                        "source": text
                    }
                ],

            }
        }
   callback_url = response_data["pipelineInferenceAPIEndPoint"]["callbackUrl"]
   headers2 = {
            "Content-Type": "application/json",
            response_data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["name"]:
                response_data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["value"]
}
   compute_response = requests.post(callback_url, json=compute_payload, headers=headers2)
   compute_response_data = compute_response.json()
   translated_content = compute_response_data["pipelineResponse"][0]["output"][0]["target"]
   return translated_content

@app.route('/resp',methods = ['POST'])
def process() :
    data = request.get_json()
    text = data['text']
    lang = data['lang']
   # text_converted=converter(text,lang,"en_XX")
    if lang!="en":
      text=converter(text,lang,"en")

    output = llm(text)
    if lang!="en":
      output=converter(output,"en",lang)
   # back_converted=converter(output[0]['generated_text'],"en_XX",lang)
    return jsonify({'result' : output})
    


if __name__=="__main__":
    app.run(debug=True)
