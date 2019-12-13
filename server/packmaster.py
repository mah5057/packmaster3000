import data_model.model as model
from flask import Flask, jsonify
from flask import request, jsonify, send_from_directory, Response
import cherrypy
import os

import traceback
import sys

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


def get_footwear(duration, climate):
    kind = model.FOOTWEAR[climate]
    amount = model.FOOTWEAR_BASE_AMOUNTS[duration]
    return "%s x %s" % (kind, amount) if kind else None


def get_socks(duration, climate):
    kind = model.SOCKS[climate]
    amount = model.SOCKS_BASE_AMOUNTS[duration]
    return "%s socks x %s" % (kind, amount) if kind else None


def get_undies(duration, climate):
    kind = model.UNDIES[climate]
    amount = model.UNDIES_BASE_AMOUNTS[duration]
    return "%s x %s" % (kind, amount) if kind else None


def get_bottoms(duration, climate):
    kind = model.BOTTOMS[climate]
    amount = model.BOTTOMS_BASE_AMOUNTS[duration]
    return "%s x %s" % (kind, amount) if kind else None


def get_tops(duration, climate):
    kind = model.TOPS[climate]
    amount = model.TOPS_BASE_AMOUNTS[duration]
    return "%s x %s" % (kind, amount) if kind else None


def get_warm_layers(duration, climate):
    kind = model.WARM_LAYERS[climate]
    amount = model.WARM_LAYERS_BASE_AMOUNTS[duration]
    return "%s x %s" % (kind, amount) if kind else None


def get_outer_layers(duration, climate):
    kind = model.OUTER_LAYERS[climate]
    amount = model.OUTER_LAYERS_BASE_AMOUNTS[duration]
    return "%s x %s" % (kind, amount) if kind else None


def get_gloves(duration, climate):
    kind = model.GLOVES[climate]
    amount = model.GLOVES_BASE_AMOUNTS[duration]
    return "%s x %s" % (kind, amount) if kind else None


def get_hats(duration, climate):
    kind = model.HATS[climate]
    amount = model.HATS_BASE_AMOUNTS[duration]
    return "%s x %s" % (kind, amount) if kind else None


@app.route('/', methods=['GET'])
def index():
    print("HELLLLLP")
    return send_from_directory(os.path.join('..', 'packmaster3000', 'dist', 'packmaster3000'), 'index.html')


@app.route('/<path:path>', methods=['GET'])
def index_all(path):
    if '.' in path:
        return send_from_directory(os.path.join('..', 'packmaster3000', 'dist', 'packmaster3000'), path, cache_timeout=0)
    else:
        return send_from_directory(os.path.join('..', 'packmaster3000', 'dist', 'packmaster3000'), 'index.html', cache_timeout=0)


# TODO: Laundry bag, belt
@app.route('/api/packlist', methods=['POST'])
def packlist():
    data = request.get_json()
    duration = int(data['duration'])
    temp = int(data['temperature'])
    climate = get_climate_key(temp)

    response = {
        "footwear": get_footwear(duration, climate),
        "socks": get_socks(duration, climate),
        "undies": get_undies(duration, climate),
        "bottoms": get_bottoms(duration, climate),
        "tops": get_tops(duration, climate),
        "warm_layers": get_warm_layers(duration, climate),
        "outer_layers": get_outer_layers(duration, climate),
        "gloves": get_gloves(duration, climate),
        "hats": get_hats(duration, climate)
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

# ################################################################
# # run main with sys args
# ################################################################
# if __name__ == '__main__':
#     try:
#         main(sys.argv[1:])
#     except SystemExit as e:
#         if e.code == 0:
#             pass
#     except:
#         traceback.print_exc()
