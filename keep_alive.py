'''
Copyright 2021 Makiyu-py

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

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