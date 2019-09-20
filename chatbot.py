from flask import Flask, request, jsonify, render_template
import json
import requests
import pprint as pp
import sapcai
import os 
import logging
from db_connect import DBConnect
import re

app = Flask(__name__)
port = int(os.environ["PORT"])
# port = 5000


#Split List like objects into chunks
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

#Helper function to get messages between Bots and users
def getMessages():
    response = requests.get('https://api.cai.tools.sap/connect/v1/conversations/' + data['conversation']['id'],
      headers={'Authorization': '54187a3945f3af9ea86d40ebca0400f2'}
    )
    # response = requests.get('https://api.cai.tools.sap/connect/v1/conversations/' + 'f727adaa-90fd-455d-b855-c2d656df66f4',
    #   headers={'Authorization': '54187a3945f3af9ea86d40ebca0400f2'}
    # )
    conv_dictionary = json.loads(response.text)
    if conv_dictionary:
        conv_list = [str(conv_dictionary['results']['messages'][i]['attachment']['content']) for i in range(len(conv_dictionary['results']['messages']))]
        conv_generator = chunks(conv_list,2)
        return conv_generator
    else:
        logging.log(logging.WARNING, 'Empty Response Object')

def insert_message_info(state):
    response = requests.get('https://api.cai.tools.sap/connect/v1/conversations/' + data['conversation']['id'],
      headers={'Authorization': '54187a3945f3af9ea86d40ebca0400f2'}
    )
    d = response.json()
    l = ''
    for i in range(len(d['results']['messages'])):
        l = l + ' ' + str(d['results']['messages'][i]['attachment']['content'])

    len_of_message = len(re.split('Thank you!!! | Took a note on that ', l)[-1].split(' '))
    my_con = DBConnect("d51dpnoammut78","mfeteccnqkvtor","8c505e55eb950c9b8a5a8a3fb3118b103fc7dabac9b7eb0737b156c9f695fad5",
                    'ec2-54-217-235-87.eu-west-1.compute.amazonaws.com')

    if state == 'no':
        my_con.db_connection()
        my_con.cur.execute("INSERT INTO messages_info(bad_mess_len) VALUES(%s);", len_of_message)
        my_con.end_connection()    

@app.route('/', methods=['POST'])
def index():
    global data

    my_con = DBConnect("d51dpnoammut78","mfeteccnqkvtor","8c505e55eb950c9b8a5a8a3fb3118b103fc7dabac9b7eb0737b156c9f695fad5",
                    'ec2-54-217-235-87.eu-west-1.compute.amazonaws.com')
    
    data = json.loads(request.get_data())
    if data['nlp']['intents'][0]['slug'] == 'no':
        my_con.update_bad_conv()
        insert_message_info('no')
        return jsonify( 
        status=200, 
        replies=[{ 
          'type': 'text', 
          'content': 'Take a note on that!',
        }], 
        conversation={ 
          'memory': { 'key': 'value' } 
        } 
      ) 
    else:
        my_con.update_good_conv()
        return jsonify( 
        status=200, 
        replies=[{ 
          'type': 'text', 
          'content': 'Thank you!!!', 
        }], 
        conversation={ 
          'memory': { 'key': 'value' } 
        } 
      )

    return 'None'  
        

@app.route('/errors', methods=['POST'])
def errors():
    print(json.loads(request.get_data()))
    return jsonify(status=200)

app.run(port=port,host="0.0.0.0")

# if __name__ == "__main__":
#     app.run(debug=True)