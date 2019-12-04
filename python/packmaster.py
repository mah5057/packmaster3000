from model import (FOOTWEAR, 
				   SOCKS, 
				   UNDIES, 
				   BOTTOMS, 
				   TOPS, 
				   WARM_LAYERS, 
				   OUTER_LAYERS, 
				   GLOVES, 
				   HATS, 
				   FOOTWEAR_BASE_AMOUNTS, 
				   SOCKS_BASE_AMOUNTS, 
				   UNDIES_BASE_AMOUNTS, 
				   BOTTOMS_BASE_AMOUNTS,
				   TOPS_BASE_AMOUNTS,
				   WARM_LAYERS_BASE_AMOUNTS,
				   OUTER_LAYERS_BASE_AMOUNTS,
				   GLOVES_BASE_AMOUNTS,
				   HATS_BASE_AMOUNTS)

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
	kind = FOOTWEAR[climate]
	amount = FOOTWEAR_BASE_AMOUNTS[duration]
	return "%s x %s" % (kind, amount) if kind else None

def get_socks(duration, climate):
	kind = SOCKS[climate]
	amount = SOCKS_BASE_AMOUNTS[duration]
	return "%s socks x %s" % (kind, amount) if kind else None

def get_undies(duration, climate):
	kind = UNDIES[climate]
	amount = UNDIES_BASE_AMOUNTS[duration]
	return "%s x %s" % (kind, amount) if kind else None

def get_bottoms(duration, climate):
	kind = BOTTOMS[climate]
	amount = BOTTOMS_BASE_AMOUNTS[duration]
	return "%s x %s" % (kind, amount) if kind else None

def get_tops(duration, climate):
	kind = TOPS[climate]
	amount = TOPS_BASE_AMOUNTS[duration]
	return "%s x %s" % (kind, amount) if kind else None

def get_warm_layers(duration, climate):
	kind = WARM_LAYERS[climate]
	amount = WARM_LAYERS_BASE_AMOUNTS[duration]
	return "%s x %s" % (kind, amount) if kind else None

def get_outer_layers(duration, climate):
	kind = OUTER_LAYERS[climate]
	amount = OUTER_LAYERS_BASE_AMOUNTS[duration]
	return "%s x %s" % (kind, amount) if kind else None

def get_gloves(duration, climate):
	kind = GLOVES[climate]
	amount = GLOVES_BASE_AMOUNTS[duration]
	return "%s x %s" % (kind, amount) if kind else None

def get_hats(duration, climate):
	kind = HATS[climate]
	amount = HATS_BASE_AMOUNTS[duration]
	return "%s x %s" % (kind, amount) if kind else None


# TODO: Laundry bag, belt
def main(args):
	duration = int(args[0])
	temp = int(args[1])
	climate = get_climate_key(temp)

	if get_footwear(duration, climate):
		print get_footwear(duration, climate)
	if get_socks(duration, climate):
		print get_socks(duration, climate)
	if get_undies(duration, climate):
		print get_undies(duration, climate)
	if get_bottoms(duration, climate):
		print get_bottoms(duration, climate)
	if get_tops(duration, climate):
		print get_tops(duration, climate)
	if get_warm_layers(duration, climate):
		print get_warm_layers(duration, climate)
	if get_outer_layers(duration, climate):
		print get_outer_layers(duration, climate)
	if get_gloves(duration, climate):
		print get_gloves(duration, climate)
	if get_hats(duration, climate):
		print get_hats(duration, climate)


################################################################
# run main with sys args
################################################################
if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except SystemExit, e:
        if e.code == 0:
            pass
    except:
        traceback.print_exc()
