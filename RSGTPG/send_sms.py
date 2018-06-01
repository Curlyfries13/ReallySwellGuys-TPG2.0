# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import configparser
import os
from twilio.rest import Client

config = configparser.ConfigParser()
config.sections()
config.read('example.ini')

account_sid = config['Twilio'].get('account_sid')
auth_token = config['Twilio'].get('auth_token')

client = Client(account_sid, auth_token)

client.messages.create(
        to=config['PhoneNum'].get('twilio_num'),
        from_=config['PhoneNum'].get('customer_num'),
        body="Hello. Your container will be picked up at [Time] at [Address]."
        )