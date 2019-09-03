from flask import Flask, request, jsonify
import json
import requests
import pprint as pp
import sapcai
import os 
import psycopg2

app = Flask(__name__)
port = int(os.environ["PORT"])

#Split List like objects into chunks
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

#Helper function to get messages between Bots and users
def getMessages():
    response = requests.get('https://api.cai.tools.sap/connect/v1/conversations/' + data['nlp']['uuid'],
      headers={'Authorization': '54187a3945f3af9ea86d40ebca0400f2'}
    )
    conv_dictionary = json.loads(response.text)
    conv_list = [str(conv_dictionary['results']['messages'][i]['attachment']['content']) for i in range(len(conv_dictionary['results']['messages']))]
    conv_generator = chunks(conv_list,2)
    return conv_generator

def db_connect_insert():
    conn = psycopg2.connect(dbname="d51dpnoammut78", user="mfeteccnqkvtor", 
            password="8c505e55eb950c9b8a5a8a3fb3118b103fc7dabac9b7eb0737b156c9f695fad5", 
            host='ec2-54-217-235-87.eu-west-1.compute.amazonaws.com')
    cur = conn.cursor()
    
    i = getMessages()
    while True:
        try:
            cur.execute("INSERT INTO messages (user_messages, bot_messages) VALUES (%s, %s)", tuple(next(i)))
        except StopIteration:
            break
            
    conn.commit()
    cur.close()
    conn.close()

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
        db_connect_insert()
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