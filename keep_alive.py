from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I FEEL ALLAAAAA-HAAA-AHHAAAAAAYVE AND THE WORRRRLLLDDDDD I'LL TURN IT INSIDE OUTTTT YEAAHHHH\nI'M FLOATING AROUND IN ECSTASY SOOOO\nDON'T STOP ME NOWWWWW"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()