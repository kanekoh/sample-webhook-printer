import time
import sys
import os
import json
import webhook_listener
import datetime
import logging
import logging.handlers

def init_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
    fh_formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')

    sh = logging.StreamHandler()
    sh.setFormatter(fh_formatter)

    logger.addHandler(sh)
    return logger

def alert_from_alertmanager(alerts):
    for alert in alerts:
       logger.debug("%s", json.dumps(alert))
       try:
         annotate = alert['annotations']
         if "description" in annotate:
           logger.info("%s, %s, %s", alert['status'], alert['labels']['alertname'], annotate['description'])
         else:
           logger.info("%s, %s, %s", alert['status'], alert['labels']['alertname'], annotate['message'])
       except:
           print("Oops!", sys.exc_info()[0], "occurred.")
    return

def alert_from_grafana(alert):
    logger.debug("%s", json.dumps(alert))
    try:
        state = alert['state']
        message = alert['message']
        rulename = alert['ruleName']
        title = alert['title']
        for value in alert['evalMatches']:
            if "node" in value['tags']:
                logger.info("%s, %s, %s, %s, %s, %s", state, rulename, title, message, value['tags']['node'], value['value'])
            else:
                logger.info("%s, %s, %s, %s, %s, %s", state, rulename, title, message, value['metric'], value['value'])
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
    return

def process_post_request(request, *args, **kwargs):
    body_raw = request.body.read(int(request.headers['Content-Length'])) if int(request.headers.get('Content-Length',0)) > 0 else '{}'
    body = json.loads(body_raw.decode('utf-8'))
    
    if "alerts" in body:
        alert_from_alertmanager(body['alerts'])
    else:
        alert_from_grafana(body)

    return

logger = init_logger('root')

webhooks = webhook_listener.Listener(handlers={"POST": process_post_request})
webhooks.start()

while True:
    time.sleep(300)

