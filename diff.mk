all: diff.nod.xml

diff.nod.xml: porto-fixed.net.xml porto-osm-geo.net.xml
	python3 ${SUMO_HOME}/tools/net/netdiff.py porto-osm-geo.net.xml porto-fixed.net.xml diff
