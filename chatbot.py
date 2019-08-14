from flask import Flask, request, jsonify
import json
import requests
import pprint as pp
import sapcai
import os 

app = Flask(__name__)
port = int(os.environ["PORT"])

@app.route('/', methods=['POST'])
def index():
    data = json.loads(request.get_data())
#     conversation_id = data['conversation']['id']
#     response = requests.get('https://api.cai.tools.sap/connect/v1/conversations/' + conversation_id,
#       headers={'Authorization': '54187a3945f3af9ea86d40ebca0400f2'}
#     )

#     print(response.text)
#     pp.pprint(conversation_id)

    
    if data['nlp']['intents'][0]['slug'] == 'no':
        
        return jsonify( 
        status=200, 
        replies=[{ 
          'type': 'text', 
          'content': 'Took a note on that', 
        }], 
        conversation={ 
          'memory': { 'key': 'value' } 
        } 
      ) 
    else:
        
        return jsonify( 
        status=200, 
        replies=[{ 
          'type': 'text', 
          'content': 'Thank you!', 
        }], 
        conversation={ 
          'memory': { 'key': 'value' } 
        } 
      )
        

@app.route('/errors', methods=['POST'])
def errors():
    print(json.loads(request.get_data()))
    return jsonify(status=200)

app.run(port=port,host="0.0.0.0")