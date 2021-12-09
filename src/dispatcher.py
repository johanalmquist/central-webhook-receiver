import pika
from pydantic import BaseModel


class Info(BaseModel):
    id: str
    nid: int
    alert_type: str
    setting_id: str
    device_id: str
    text: str
    severity: str
    timestamp: str
    details: dict


class Dispatch(object):
    _dishpatchTo: dict

    def __init__(self, info: Info):
        self.data = info
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        self.channel = self.connection.channel()
        self._dishpatch(info.alert_type)

    def _dishpatch(self, alerttType: str):
        if alerttType == "New AP detected":
            self._newAP(self.data.device_id)
        if alerttType == "AP disconnected":
            self._disconnectedAP(self.data)

    def _newAP(self, device_id: str):
        self.channel.queue_declare(queue="new-ap")
        self.channel.basic_publish(exchange="", routing_key="new-ap", body=device_id)
        self.connection.close()
        return None

    def _disconnectedAP(self, info: Info):
        message = {
            "message": f"{info.text} at {info.details['time']} level {info.severity}"
        }
        url = "http://notification:8001/slack/"
        headers = {"Content-Type": "application/json"}
        import json

        import requests

        requests.post(url=url, data=json.dumps(message), headers=headers)
        return None
