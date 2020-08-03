import time
import json
import webhook_listener


def process_post_request(request, *args, **kwargs):
    body_raw = request.body.read(int(request.headers['Content-Length'])) if int(request.headers.get('Content-Length',0)) > 0 else '{}'
    body = json.loads(body_raw.decode('utf-8'))
    print(body)

    return


webhooks = webhook_listener.Listener(handlers={"POST": process_post_request})
webhooks.start()

while True:
    print("Still alive...")
    time.sleep(300)