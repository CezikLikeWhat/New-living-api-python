import random
import uuid
from enum import Enum

import flask

app = flask.Flask(__name__)


class TypeOfDevice(Enum):
    raspberry = "Raspberry"
    esp32 = "ESP"
    lightBulb = "Light Bulb"
    distanceSensor = "Distance Sensor"
    ledStrip = "Led Strip"
    radio = "Radio"

    def get_instance_of_type(self, string_type):
        if string_type == "Raspberry":
            return self.raspberry
        elif string_type == "ESP":
            return self.esp32
        elif string_type == "Light Bulb":
            return self.lightBulb
        elif string_type == "Distance Sensor":
            return self.distanceSensor
        elif string_type == "Led Strip":
            return self.ledStrip
        else:
            return self.radio

    def get_actions_by_type(self, typeOfDevice) -> dict:
        if typeOfDevice == self.raspberry:
            return {
                "Enable device": False,
                "Error notification": False,
                "Reset device": False,
                "Enable SSH": False
            }
        elif typeOfDevice == self.esp32:
            return {
                "Enable device": False,
                "Error notification": False,
                "Reset device": False,
                "Enable HTTP Server": False
            }
        elif typeOfDevice == self.lightBulb:
            return {
                "Enable bulb": False,
                "Enable rainbow effect": False
            }
        elif typeOfDevice == self.distanceSensor:
            return {
                "Enable sensor": False,
                "Set at 10cm": False,
                "Set at 50cm": False,
                "Set at 1m": False
            }
        elif typeOfDevice == self.ledStrip:
            return {
                "Enable strip": False,
                "Enable rainbow effect": False,
                "Enable the breathing effect": False,
                "Enable the explosion effect": False
            }
        else:
            return {
                "Enable radio": False,
                "Reset radio": False,
                "Play news station": False,
                "Play music station": False
            }


class Notifications:
    emailNotification = False
    popupNotification = False
    smsNotification = False
    telegramNotification = False
    discordNotification = False

    def __init__(self, email, popup, sms, telegram, discord) -> None:
        self.emailNotification = email
        self.popupNotification = popup
        self.smsNotification = sms
        self.telegramNotification = telegram
        self.discordNotification = discord

    def toJson(self) -> dict:
        return {
            "email": self.emailNotification,
            "popup": self.popupNotification,
            "sms": self.smsNotification,
            "telegram": self.telegramNotification,
            "discord": self.discordNotification
        }


def generate_random_mac():
    return "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255))


accounts = [
    {"name": "admin", "surname": "admin", "email": "admin@wp.pl", "password": "admin"},
    {"name": "Cezary", "surname": "Maćkowski", "email": "cezik@wp.pl", "password": "1234"}
]

temp = TypeOfDevice['raspberry']
devices = [
    {"email": "cezik@wp.pl", "id": "8e6b3f82-70ac-4ed6-a348-437069886429", "name": "Raspberry 2W",
     "mac": generate_random_mac(),
     "type": TypeOfDevice.raspberry.value, "description": "Wiatrak za biurkiem", "image": TypeOfDevice.raspberry.value,
     "actions": temp.get_actions_by_type(TypeOfDevice.raspberry)},
    {"email": "cezik@wp.pl", "id": str(uuid.uuid4()), "name": "ESP32 parter", "mac": generate_random_mac(),
     "type": TypeOfDevice.esp32.value, "description": "Czujnik ruchu za drzwiami", "image": TypeOfDevice.esp32.value,
     "actions": temp.get_actions_by_type(TypeOfDevice.esp32)},
    {"email": "cezik@wp.pl", "id": str(uuid.uuid4()), "name": "Żarówka", "mac": generate_random_mac(),
     "type": TypeOfDevice.lightBulb.value, "description": "Żarówka w kuchni", "image": TypeOfDevice.lightBulb.value,
     "actions": temp.get_actions_by_type(TypeOfDevice.lightBulb)},
    {"email": "cezik@wp.pl", "id": str(uuid.uuid4()), "name": "Pasek led", "mac": generate_random_mac(),
     "type": TypeOfDevice.ledStrip.value, "description": "Pasek led za telewizorem",
     "image": TypeOfDevice.ledStrip.value,
     "actions": temp.get_actions_by_type(TypeOfDevice.ledStrip)},
    {"email": "admin@wp.pl", "id": str(uuid.uuid4()), "name": "RPI medium", "mac": generate_random_mac(),
     "type": TypeOfDevice.raspberry.value, "description": "RPI medium service", "image": TypeOfDevice.raspberry.value,
     "actions": temp.get_actions_by_type(TypeOfDevice.raspberry)},
]

notifications = [
    {"email": "cezik@wp.pl", "notifications": Notifications(True, False, False, True, True).toJson()},
    {"email": "admin@wp.pl", "notifications": Notifications(False, False, False, False, False).toJson()}
]


@app.route("/signin/", methods=['POST'])
def signin():
    decoded_json = flask.request.get_json()
    name = decoded_json["name"]
    surname = decoded_json["surname"]
    email = decoded_json["email"]
    password = decoded_json["password"]

    accounts.append({"name": name, "surname": surname, 'email': email, 'password': password})
    return flask.make_response(
        flask.jsonify(info="Created account"),
        200
    )


@app.route("/login/", methods=['GET'])
def login():
    email = flask.request.args.get("email", default="", type=str)
    password = flask.request.args.get("password", default="", type=str)

    for user in accounts:
        if user['email'] == email and user['password'] == password:
            return flask.make_response(
                flask.jsonify(info="Log in successfully"),
                200
            )

    return flask.make_response(
        flask.jsonify(info="Bad data"),
        400
    )


@app.route("/devices/", methods=['GET'])
def list_of_devices():
    email = flask.request.args.get("email", default="", type=str)
    temp = []
    for element in devices:
        if email == element['email']:
            temp.append(element)
    return flask.make_response(
        flask.jsonify(devices=temp),
        200
    )


@app.route("/device/", methods=['GET'])
def get_device():
    identifier = flask.request.args.get("id", default="", type=str)
    for element in devices:
        if identifier == element['id']:
            return flask.make_response(
                flask.jsonify(element),
                200
            )


@app.route("/countDevices/", methods=['GET'])
def count_devices():
    email = flask.request.args.get("email", default="", type=str)
    temp = []
    temp2 = []
    for element in devices:
        temp2.append({
            "email": element['email'],
            "id": element['id'],
            "name": element['name'],
            "mac": element['mac'],
            "type": element['type'],
            "description": element['description'],
            "image": element['image'],
            "actions": ['actions']
        })

    for element in temp2:
        if email == element['email']:
            element.pop('email')
            temp.append(element)

    return flask.make_response(
        flask.jsonify(number=len(temp)),
        200
    )


@app.route("/mostDevice", methods=['GET'])
def most_device():
    email = flask.request.args.get("email", default="", type=str)

    members = [element.value for element in TypeOfDevice]

    temp = {}
    for element in members:
        if element not in temp:
            temp.update({element: 0})
    for element in devices:
        if email == element['email'] and element['type'] in temp.keys():
            temp[element['type']] += 1
    name_of_type = ""
    max = 0
    for key, value in temp.items():
        if value > max:
            max = value
            name_of_type = key

    return flask.make_response(
        flask.jsonify(type=name_of_type, quantity=max),
        200
    )


@app.route("/newSettings", methods=['POST'])
def update_settings():
    decoded_json = flask.request.get_json()
    email = decoded_json["email"]
    notification = decoded_json["notification"]

    for element in notifications:
        if element['email'] == email:
            element.pop('notifications')
            element['notifications'] = notification

    return flask.make_response(
        flask.jsonify(info="Settings updated"),
        200
    )


@app.route("/updateDevice", methods=['POST'])
def update_device():
    decoded_json = flask.request.get_json()
    email = decoded_json["email"]
    identifier = decoded_json["device"]["id"]
    name_of_device = decoded_json["device"]["name"]
    mac = decoded_json["device"]["mac"]
    typeOfDevice = decoded_json["device"]["type"]
    description = decoded_json["device"]["description"]
    actions = decoded_json["device"]["actions"]

    temp_index = -1
    for element in devices:
        if identifier == element['id']:
            temp_index = devices.index(element)

    devices.pop(temp_index)

    devices.insert(temp_index, {
        "email": email,
        "id": identifier,
        "name": name_of_device,
        "mac": mac,
        "type": typeOfDevice,
        "description": description,
        "image": typeOfDevice,
        "actions": actions
    })

    return flask.make_response(
        flask.jsonify(info="Device updated"),
        200
    )


@app.route("/addDevice", methods=['POST'])
def add_new_device():
    decoded_json = flask.request.get_json()
    email = decoded_json["email"]
    identifier = decoded_json["device"]["id"]
    name_of_device = decoded_json["device"]["name"]
    mac = decoded_json["device"]["mac"]
    typeOfDevice = decoded_json["device"]["type"]
    description = decoded_json["device"]["description"]

    temp_type = TypeOfDevice["raspberry"].get_instance_of_type(typeOfDevice)
    devices.append({
        "email": email,
        "id": identifier,
        "name": name_of_device,
        "mac": mac,
        "type": typeOfDevice,
        "description": description,
        "image": typeOfDevice,
        "actions": temp_type.get_actions_by_type(temp_type),
    })

    return flask.make_response(
        flask.jsonify(info="Device added"),
        200
    )


@app.route("/removeDevice", methods=['POST'])
def remove_device():
    decoded_json = flask.request.get_json()
    identifier = decoded_json["id"]

    [devices.remove(device) for device in devices if device['id'] == identifier]

    return flask.make_response(
        flask.jsonify(info="Device removed"),
        200
    )


@app.route("/notifications/", methods=['GET'])
def list_of_notifications():
    email = flask.request.args.get('email', default="", type=str)
    final_notifications = {"notifications": element['notifications'] for element in notifications if
                           email == element['email']}

    return flask.make_response(
        flask.jsonify(final_notifications),
        200
    )


if __name__ == '__main__':
    app.run()