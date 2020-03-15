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
        return "Boots x 1"
    elif luxury == 1:
        return "Boots x 1\nCamp shoes x 1"
    elif luxury == 2:
        base = "Boots x 1\nCamp shoes x 1"
        if climate in ["CHILLY", "MILD", "WARM", "HOT", "VERY_HOT", "MELTING"]:
            base += "\nSandals x 1"
        return base
    elif luxury == 3:
        base = "Boots x 1\nCamp shoes x 1"
        if climate in ["FREEZING", "VERY_COLD", "COLD"]:
            base += "\nBoots x 1"
        if climate in ["CHILLY", "MILD", "WARM", "HOT", "VERY_HOT", "MELTING"]:
            base += "\nSandals x 1"
        return base
    elif luxury == 4:
        base = "Shoes x 1"
        if climate in ["FREEZING", "VERY_COLD", "COLD"]:
            base += "\nBoots x 1"
        if climate in ["CHILLY", "MILD", "WARM", "HOT", "VERY_HOT", "MELTING"]:
            base += "\nSandals x 1"
        return base
    elif luxury == 5:
        base = "Shoes x 1"
        if climate in ["FREEZING", "VERY_COLD", "COLD"]:
            base += "\nBoots x 1"
        if climate in ["CHILLY", "MILD", "WARM", "HOT", "VERY_HOT", "MELTING"]:
            base += "\nSandals x 1"
        return base
    elif luxury == 6:
        base = "Shoes x 1"
        if climate in ["FREEZING", "VERY_COLD", "COLD"]:
            base += "\nBoots x 1"
        if climate in ["CHILLY", "MILD", "WARM", "HOT", "VERY_HOT", "MELTING"]:
            base += "\nSandals x 1"
        return base
    elif luxury == 7:
        base = ""
        if climate in ["FREEZING", "VERY_COLD", "COLD"]:
            base += "Boots x 1\nShoes x 1\nSandals x 1\nDress shoes x 1"
        else:
            base += "Shoes x 1\nSandals x 1\nDress shoes x 1"
        return base
    elif luxury == 8:
        base = ""
        if climate in ["FREEZING", "VERY_COLD", "COLD"]:
            base += "Boots x 1\nShoes x 1\nSandals x 1\nDress shoes x 1"
        else:
            base += "Shoes x 1\nSandals x 1\nDress shoes x 1"
        return base


def get_socks(duration, climate, luxury):
    kind = model.SOCKS[climate]
    amount = duration + 1
    base = "Socks x %s" % amount

    if luxury == 7 or luxury == 8:
        dress_socks_amount = int(math.ceil(duration / 2))
        base += "\nDress socks x %s" % dress_socks_amount
    return base if kind else None


def get_undies(duration, climate, luxury):
    kind = model.UNDIES[climate]
    amount = duration + 1
    return "%s x %s" % (kind, amount) if kind else None


def get_bottoms(duration, climate, luxury):
    if luxury == 0:
        return "%s x 1" % model.BOTTOMS[climate]
    else:
        kind = model.BOTTOMS[climate]
        if duration <= 3:
            amount = 2
        elif duration > 3:
            amount = 3
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
            base += "\nThermal x 1"
    return base


def get_warm_layers(duration, climate, luxury):
    kind = model.WARM_LAYERS[climate]
    if kind:
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
    else:
        return ""


def get_outer_layers(duration, climate, luxury):
    kind = model.OUTER_LAYERS[climate]
    amount = 1
    return "%s x %s" % (kind, amount) if kind else None


def get_gloves(duration, climate, luxury):
    kind = model.GLOVES[climate]
    # amount = model.GLOVES_BASE_AMOUNTS[duration]
    amount = 1
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

    if bonus == "hot":
        temp += 10

    if bonus == "cold":
        temp -= 10

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
        "belt": "Belt x 1",
        "laundry_bag": "Laundry bag x 1"
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
