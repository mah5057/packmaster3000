import model
import traceback
import sys


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


# TODO: Laundry bag, belt
def main(args):
    duration = int(args[0])
    temp = int(args[1])
    climate = get_climate_key(temp)

    if get_footwear(duration, climate):
        print(get_footwear(duration, climate))
    if get_socks(duration, climate):
        print(get_socks(duration, climate))
    if get_undies(duration, climate):
        print(get_undies(duration, climate))
    if get_bottoms(duration, climate):
        print(get_bottoms(duration, climate))
    if get_tops(duration, climate):
        print(get_tops(duration, climate))
    if get_warm_layers(duration, climate):
        print(get_warm_layers(duration, climate))
    if get_outer_layers(duration, climate):
        print(get_outer_layers(duration, climate))
    if get_gloves(duration, climate):
        print(get_gloves(duration, climate))
    if get_hats(duration, climate):
        print(get_hats(duration, climate))


################################################################
# run main with sys args
################################################################
if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except SystemExit as e:
        if e.code == 0:
            pass
    except:
        traceback.print_exc()
