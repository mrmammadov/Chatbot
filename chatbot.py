from flask import Flask, request, jsonify, render_template
import json
import requests
import pprint as pp
import sapcai
import os 
import psycopg2
import logging

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

def update_bad_conv():
    conn = psycopg2.connect(dbname="d51dpnoammut78", user="mfeteccnqkvtor", 
            password="8c505e55eb950c9b8a5a8a3fb3118b103fc7dabac9b7eb0737b156c9f695fad5", 
            host='ec2-54-217-235-87.eu-west-1.compute.amazonaws.com')
    cur = conn.cursor()
    cur.execute("SELECT bad_conv FROM messages LIMIT 1;")
    counter = cur.fetchone()[0]
    counter = counter + 1
    cur.execute("UPDATE messages SET bad_conv = %s", [counter])
    conn.commit()
    cur.close()
    conn.close()

def update_good_conv():
    conn = psycopg2.connect(dbname="d51dpnoammut78", user="mfeteccnqkvtor", 
            password="8c505e55eb950c9b8a5a8a3fb3118b103fc7dabac9b7eb0737b156c9f695fad5", 
            host='ec2-54-217-235-87.eu-west-1.compute.amazonaws.com')
    cur = conn.cursor()
    cur.execute("SELECT good_conv FROM messages LIMIT 1;")
    counter = cur.fetchone()[0]
    counter = counter + 1
    cur.execute("UPDATE messages SET good_conv = %s", [counter])
    conn.commit()
    cur.close()
    conn.close()



# def db_connect_insert():
#     conn = psycopg2.connect(dbname="d51dpnoammut78", user="mfeteccnqkvtor", 
#             password="8c505e55eb950c9b8a5a8a3fb3118b103fc7dabac9b7eb0737b156c9f695fad5", 
#             host='ec2-54-217-235-87.eu-west-1.compute.amazonaws.com')
#     cur = conn.cursor()
    
    # i = getMessages()
    # while True:
    #     try:
    #         cur.execute("INSERT INTO messages (user_messages, bot_messages) VALUES (%s, %s)", tuple(next(i)))
    #     except StopIteration:
    #         break
            
    # conn.commit()
    # cur.close()
    # conn.close()

@app.route('/', methods=['POST'])
def index():
    global data
    # if request.get_data():
    
    # return render_template('home.html', data=data)     
    # try:
    #     data = json.loads(request.get_data())
    # except ValueError:  # includes simplejson.decoder.JSONDecodeError
    #     print('Decoding JSON has failed')

    data = json.loads(request.get_data())
    if data['nlp']['intents'][0]['slug'] == 'no':
        # db_connect_insert()
        update_bad_conv()
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
        update_good_conv()
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