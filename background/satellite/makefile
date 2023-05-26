TILE_GET = ${SUMO_HOME}/tools/tileGet.py

all: porto.jpeg

porto.jpeg: tiles
	python3 stitch.py

tiles: ../../porto.net.xml
	mkdir -p $@
	python3 ${TILE_GET} \
		--net=../../porto.net.xml \
		--bbox="-8.691,41.138,-8.552,41.186" \
		-d tiles \
		-p porto \
		-s porto-decals-tiles.xml \
		-t 8000 \
		-f 1

../../porto.net.xml:
	make -C ../.. porto.net.xml
