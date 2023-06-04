TILE_GET = ${SUMO_HOME}/tools/tileGet.py

all: porto.jpeg

porto.jpeg: tiles
	python3 stitch.py

tiles:
	mkdir -p $@
	python3 ${TILE_GET} \
		--bbox="-8.691,41.138,-8.552,41.186" \
		-d tiles \
		-p porto \
		-s porto-decals-tiles.xml \
		-t 8000 \
		-f 1 \
		-j 8
