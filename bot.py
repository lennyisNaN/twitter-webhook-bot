from flask import Flask, request
import base64
import hashlib
import hmac
import json
import credentials

app = Flask(__name__)

CONSUMER_SECRET = credentials.consumer_key_secret

@app.route('/webhooks/twitter', methods=['GET', 'POST'])
def webhook_challenge():
  if request.method == 'GET':
    crc = request.args['crc_token']
    validation = hmac.new(key=bytes(CONSUMER_SECRET, 'utf-8'), msg=bytes(crc, 'utf-8'),
                          digestmod=hashlib.sha256
                          )
    digested = base64.b64encode(validation.digest())
    response = {
      'response_code': 200,
      'response_token': 'sha256=' + format(str(digested)[2:-1])
    }
    print('responding to CRC call')
    return json.dumps(response)

  if request.method == 'POST': # new webhook event
    response = {
      'response_code': 200
    }
    webhook_response = json.loads(request.data)
    print(webhook_response)
    return json.dumps(response)


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)