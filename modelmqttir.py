#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

The Google Assistant Library can be installed with:
    env/bin/pip install google-assistant-library==0.0.2

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import subprocess
import sys

import aiy.assistant.auth_helpers
import aiy.audio
import aiy.voicehat
from google.assistant.library import Assistant
from google.assistant.library.event import EventType

import paho.mqtt.publish as publish
import traceback
import my_config
import time

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

delay = 0.3
turnondelay = 6

def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    aiy.audio.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('My IP address is %s' % ip_address.decode('utf-8'))


def mosquitto(topic, message):
    """Send MQTT commands"""

    try:
        publish.single(topic, payload=message,
                   hostname=my_config.mqtt_host,
                   port=my_config.mqtt_port,
                   auth={'username':my_config.mqtt_username,
                   'password':my_config.mqtt_password})
        logging.info("MQTT Command received: " + topic + " " +
                   message)
    except Exception as e:
            logging.error("MQTT error: " + traceback.format_exc())
            aiy.audio.say("Error sending MQTT command")


def lights_on():
    mosquitto('room/lights', '1')


def lights_off():
    mosquitto('room/lights', '0')
    
def tv_on():
    mosquitto('home/commands/IR_NEC', '404279343')
	
def channel_up():
    mosquitto('home/commands/IR_NEC', '404265063')

def volume_up():
    mosquitto('home/commands/IR_NEC', '404281383')
	
def volume_down():
    mosquitto('home/commands/IR_NEC', '404248743')
	
def input():
    mosquitto('home/commands/IR_NEC', '404269143')
	
def arrow_up():
    mosquitto('home/commands/IR_NEC', '404235993')
	
def arrow_down():
    mosquitto('home/commands/IR_NEC', '404252313')
	
def ok():
    mosquitto('home/commands/IR_NEC', '404231913')
	
def mute():
    mosquitto('home/commands/IR_NEC', '404238543')
	
def one():
    mosquitto('home/commands/IR_NEC', '404226303')
	
def two():
    mosquitto('home/commands/IR_NEC', '404258943')
	
def three():
    mosquitto('home/commands/IR_NEC', '404242623')
	
def four():
    mosquitto('home/commands/IR_NEC', '404275263')
	
def five():
    mosquitto('home/commands/IR_NEC', '404234463')
	
def six():
    mosquitto('home/commands/IR_NEC', '404267103')
	
def seven():
    mosquitto('home/commands/IR_NEC', '404250783')
	
def eight():
    mosquitto('home/commands/IR_NEC', '404283423')
	
def nine():
    mosquitto('home/commands/IR_NEC', '404230383')
	
def zero():
    mosquitto('home/commands/IR_NEC', '404263023')
	
def dot():
    mosquitto('home/commands/IR_NEC', '404279853')
	
	
	
def hdmi1():
    channel_up()
    time.sleep(delay)
    input()
    time.sleep(delay)
    arrow_up()
    time.sleep(delay)
    arrow_up()
    time.sleep(delay)
    arrow_up()
    time.sleep(delay)
    arrow_up()
    time.sleep(delay)
    arrow_up()
    time.sleep(delay)
    ok()
	
def hdmi2():
    channel_up()
    time.sleep(delay)
    input()
    time.sleep(delay)
    arrow_up()
    time.sleep(delay)
    arrow_up()
    time.sleep(delay)
    arrow_up()
    time.sleep(delay)
    arrow_up()
    time.sleep(delay)
    ok()
    
def movie_time():
    lights_off()
    tv_on()
    time.sleep(turnondelay)
    hdmi1()
    
def sleep():
    lights_off()
    tv_on()
	
	
def process_event(assistant, event):
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'power off':
            assistant.stop_conversation()
            power_off_pi()
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'ip address':
            assistant.stop_conversation()
            say_ip()
        elif text == 'lights on':
            assistant.stop_conversation()
            lights_on()
        elif text == 'lights off':
            assistant.stop_conversation()
            lights_off()
        elif text == 'tv on':
            assistant.stop_conversation()
            tv_on()
        elif text == 'tv off':
            assistant.stop_conversation()
            tv_on()
        elif text == 'unmute tv':
            assistant.stop_conversation()
            mute()
        elif text == 'mute tv':
            assistant.stop_conversation()
            mute()
        elif text == 'volume up':
            assistant.stop_conversation()
            volume_up()
        elif text == 'volume down':
            assistant.stop_conversation()
            volume_down()
        elif text == 'channel up':
            assistant.stop_conversation()
            channel_up()
        elif text == 'channel down':
            assistant.stop_conversation()
            channel_down()
        elif text == 'hdmi 1':
            assistant.stop_conversation()
            hdmi1()
        elif text == 'hdmi 2':
            assistant.stop_conversation()
            hdmi2()
        elif text == 'movie time':
            assistant.stop_conversation()
            movie_time()
        elif text == 'sleep':
            assistant.stop_conversation()
            sleep()


    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()
