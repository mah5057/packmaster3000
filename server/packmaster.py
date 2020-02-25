import data_model.model as model
from flask import Flask, jsonify
from flask import request, jsonify, send_from_directory, Response
import cherrypy
import math
import os

app = Flask(__name__)

def get_climate_key(temp):
    if temp % 10 > 5:
        key = temp + (10 - (temp % 10))
    else:
        key = temp - (temp % 10)
    if key < 20:
        key = 20
    if key > 100:
        key = 100
    return {
        20: "FREEZING",
        30: "VERY_COLD",
        40: "COLD",
        50: "CHILLY",
        60: "MILD",
        70: "WARM",
        80: "HOT",
        90: "VERY_HOT",
        100: "MELTING"
    }[key]


def get_footwear(climate, luxury):
    if luxury == 0:
        return "boots x 1"
    elif luxury == 1:
        return "boots x 1\ncamp shoes x 1"
    elif luxury == 2:
        base = "boots x 1\ncamp shoes x 1"
        if climate in ["CHILLY", "MILD", "WARM", "HOT", "VERY_HOT", "MELTING"]:
            base += "\nsandals x 1"
        return base
    elif luxury == 3:
        base = "boots x 1\ncamp shoes x 1"
        if climate in ["FREEZING", "VERY_COLD", "COLD"]:
            base += "\nboots x 1"
        if climate in ["CHILLY", "MILD", "WARM", "HOT", "VERY_HOT", "MELTING"]:
            base += "\nsandals x 1"
        return base
    elif luxury == 4:
        base = "camp shoes x 1"
        if climate in ["FREEZING", "VERY_COLD", "COLD"]:
            base += "\nboots x 1"
        if climate in ["CHILLY", "MILD", "WARM", "HOT", "VERY_HOT", "MELTING"]:
            base += "\nsandals x 1"
        return base
    elif luxury == 5:
        base = "camp shoes x 1"
        if climate in ["FREEZING", "VERY_COLD", "COLD"]:
            base += "\nboots x 1"
        if climate in ["CHILLY", "MILD", "WARM", "HOT", "VERY_HOT", "MELTING"]:
            base += "\nsandals x 1"
        return base
    elif luxury == 6:
        base = "camp shoes x 1"
        if climate in ["FREEZING", "VERY_COLD", "COLD"]:
            base += "\nboots x 1"
        if climate in ["CHILLY", "MILD", "WARM", "HOT", "VERY_HOT", "MELTING"]:
            base += "\nsandals x 1"
        return base
    elif luxury == 7:
        base = ""
        if climate in ["FREEZING", "VERY_COLD", "COLD"]:
            base += "boots x 1\nshoes x 1\nsandals x 1\ndress shoes x 1"
        else:
            base += "shoes x 1\nsandals x 1\ndress shoes x 1"
        return base
    elif luxury == 8:
        base = ""
        if climate in ["FREEZING", "VERY_COLD", "COLD"]:
            base += "boots x 1\nshoes x 1\nsandals x 1\ndress shoes x 1"
        else:
            base += "shoes x 1\nsandals x 1\ndress shoes x 1"
        return base


def get_socks(duration, climate, luxury):
    kind = model.SOCKS[climate]
    amount = model.SOCKS_BASE_AMOUNTS[duration] + 1
    base = "socks x %s" % (amount)

    if luxury == 7 or luxury == 8:
        dress_socks_amount = duration / 2
        base += "\ndress socks x %s" % dress_socks_amount
    return base if kind else None


def get_undies(duration, climate, luxury):
    kind = model.UNDIES[climate]
    amount = model.UNDIES_BASE_AMOUNTS[duration] + 1
    return "%s x %s" % (kind, amount) if kind else None


def get_bottoms(duration, climate, luxury):
    if luxury == 0:
        "%s x 1" % climate
    kind = model.BOTTOMS[climate]
    amount = model.BOTTOMS_BASE_AMOUNTS[duration]
    amount = amount * model.BOTTOMS_MULTIPLIERS[luxury]
    amount = math.ceil(amount)
    return "%s x %s" % (kind, amount) if kind else None


def get_tops(duration, climate, luxury):
    kind = model.TOPS[climate]
    amount = model.TOPS_BASE_AMOUNTS[duration]
    if luxury == 0:
        return "%s x 1" % kind
    else:
        amount = amount * model.TOPS_MULTIPLIERS[luxury]
        amount = math.ceil(amount)
        base = "%s x %s" % (kind, amount) if kind else None
    if luxury < 4:
        if climate in ["FREEZING", "VERY_COLD", "COLD", "CHILLY"]:
            base += "\nthermal x 1"
    return base


def get_warm_layers(duration, climate, luxury):
    kind = model.WARM_LAYERS[climate]
    amount = model.WARM_LAYERS_BASE_AMOUNTS[duration]
    if luxury == 0:
        return "%s x 1" % kind
    amount = amount * model.WARM_LAYERS_MULTIPLIERS[luxury]
    amount = math.ceil(amount)
    if luxury == 1 or luxury == 2:
        amount = amount * model.WARM_LAYERS_MULTIPLIERS[luxury]
        amount /= 2
        amount = math.ceil(amount)
    return "%s x %s" % (kind, amount) if kind else None


def get_outer_layers(duration, climate, luxury):
    kind = model.OUTER_LAYERS[climate]
    amount = model.OUTER_LAYERS_BASE_AMOUNTS[duration]
    amount = amount * model.OUTER_LAYERS_MULTIPLIERS[luxury]
    return "%s x %s" % (kind, amount) if kind else None


def get_gloves(duration, climate, luxury):
    kind = model.GLOVES[climate]
    amount = model.GLOVES_BASE_AMOUNTS[duration]
    if luxury < 4:
        return "%s x 1" % kind
    return "%s x %s" % (kind, amount) if kind else None


def get_hats(duration, climate, luxury):
    kind = model.HATS[climate]
    amount = model.HATS_BASE_AMOUNTS[duration]
    if luxury < 4:
        return "%s x 1" % kind
    return "%s x %s" % (kind, amount) if kind else None


@app.route('/', methods=['GET'])
def index():
    return send_from_directory(os.path.join('..', 'packmaster3000', 'dist', 'packmaster3000'), 'index.html')


@app.route('/<path:path>', methods=['GET'])
def index_all(path):
    if '.' in path:
        return send_from_directory(os.path.join('..', 'packmaster3000', 'dist', 'packmaster3000'), path, cache_timeout=0)
    else:
        return send_from_directory(os.path.join('..', 'packmaster3000', 'dist', 'packmaster3000'), 'index.html', cache_timeout=0)


@app.route('/api/packlist', methods=['POST'])
def packlist():
    data = request.get_json()
    duration = int(data['duration'])
    temp = int(data['temperature'])
    luxury = float(data['luxury'])
    bonus = data['bonus']
    climate = get_climate_key(temp)

    response = {
        "footwear": get_footwear(climate, luxury),
        "socks": get_socks(duration, climate, luxury),
        "undies": get_undies(duration, climate, luxury),
        "bottoms": get_bottoms(duration, climate, luxury),
        "tops": get_tops(duration, climate, luxury),
        "warm_layers": get_warm_layers(duration, climate, luxury),
        "outer_layers": get_outer_layers(duration, climate, luxury),
        "gloves": get_gloves(duration, climate, luxury),
        "hats": get_hats(duration, climate, luxury),
        "laundry_bag": "laundry bag x 1",
        "belt": "belt x 1"
    }

    return jsonify(response)

def main():
    cherrypy.tree.graft(app.wsgi_app, '/')
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 5000,
                            'engine.autoreload.on': False,
                            })

    cherrypy.engine.start()


if __name__ == '__main__':
    main()
