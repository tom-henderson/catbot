import json
import urllib2
import logging
import os

from urlparse import parse_qs

import boto3

token_parameter = os.environ['token_parameter']
image_url = "http://thecatapi.com/api/images/get?format=xml"
fact_url = "http://catfacts-api.appspot.com/api/facts"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }


try:
    client = boto3.client('ssm')
    response = client.get_parameters(
        Names=[token_parameter],
        WithDecryption=True
    )
    expected_token = response['Parameters'][0]['Value']
except:
    respond(Exception('Failed to fetch token'))


def get_param(params, key, default=None):
    try:
        return params[key][0]
    except KeyError:
        return default


def get_fact():
    req = urllib2.Request(fact_url)
    res = urllib2.urlopen(req)
    cat_fact = json.loads(res.read())

    return {
        "response_type": "in_channel",
        "text": cat_fact['facts'][0],
    }


def get_image():
    req = urllib2.Request(image_url)
    res = urllib2.urlopen(req)
    cat_image_url = res.read().split('<url>')[1].split('</url>')[0]

    return {
        "response_type": "in_channel",
        "text": cat_image_url,
    }


def lambda_handler(event, context):
    params = parse_qs(event['body'])

    token = params['token'][0]
    if token != expected_token:
        logger.error("Request token (%s) does not match expected", token)
        return respond(Exception('Invalid request token'))

    user = get_param(params, 'user_name')
    command = get_param(params, 'command')
    channel = get_param(params, 'channel_name')
    command_text = get_param(params, 'text')

    if command_text == "fact":
        response_object = get_fact()
    else:
        response_object = get_image()

    return respond(
        None,
        json.dumps(response_object)
    )
