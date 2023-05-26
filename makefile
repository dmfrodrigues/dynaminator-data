all: porto.net.xml porto.taz.xml

OSM2POLY=openstreetmap/svn-archive/osm2poly.pl

porto-boundary-strict.osm: porto-unbounded.osm
	osmfilter porto-unbounded.osm \
		--keep="type=boundary and admin_level=7 and name=Porto" \
		--drop="admin_level=8" \
		> $@.tmp
	osmconvert $@.tmp \
		-b=-8.8,41.0,-8.5,41.3 \
		-o=$@
	rm $@.tmp

porto-boundary.poly: porto-boundary.osm
	cat $< > $<.tmp

	sed -i -e "s/    <tag k='admin_level' v='[[:digit:]]\+' \/>//g" $<.tmp
	sed -i -e "s/    <tag k='border_type' v='.\+' \/>//g" $<.tmp
	sed -i -e "s/    <tag k='boundary' v='.\+' \/>//g" $<.tmp
	sed -i -e "s/    <tag k='source' v='.\+' \/>//g" $<.tmp

	$(OSM2POLY) $<.tmp > $@

	rm $<.tmp

porto-nolinks.osm: porto-unbounded.osm porto-boundary.poly
	osmconvert porto-unbounded.osm \
		-B=porto-boundary.poly \
		--complete-ways \
		--complete-multipolygons \
		--complete-boundaries \
		-o=$@.tmp
		# --complete-routeroads \

	osmconvert $@.tmp \
		-b=-8.70,41.06,-8.54,41.19 \
		--complete-multipolygons \
		--complete-boundaries \
		-o=$@
	
	rm $@.tmp

porto-links.osm: porto-unbounded.osm
	osmfilter $< \
		--keep="highway=motorway highway=motorway_link" \
		> $@.tmp

	osmconvert $@.tmp \
		-b=-8.70,41.06,-8.54,41.19 \
		-o=$@.tmp.tmp

	osmconvert $@.tmp.tmp \
		-b=-8.70,41.08,-8.54,41.19 \
		--complete-ways \
		-o=$@

	rm $@.tmp $@.tmp.tmp

porto.osm: porto-nolinks.osm porto-links.osm
	osmosis --rx porto-nolinks.osm --rx porto-links.osm --merge --wx $@

porto-osm.net.xml: porto.osm osmNetconvert-PT-loc.typ.xml
	netconvert --osm-files $< \
		--junctions.join --tls.guess-signals --tls.join --tls.default-type actuated \
		--remove-edges.by-type highway.unsurfaced,highway.living_street,highway.services \
		--remove-edges.isolated \
		--osm.turn-lanes \
		--osm.lane-access \
		--roundabouts.guess false \
		--osm.elevation true \
		--osm.layer-elevation 8.0 \
		--no-turnarounds.except-deadend \
		--keep-edges.by-vclass passenger \
		--geometry.remove \
		--tls.join-dist 30 \
		--junctions.join-dist 10 \
		--junctions.join-exclude 128617101,128616477 \
		--default.junctions.keep-clear \
		--tls.discard-simple \
		--check-lane-foes.roundabout false \
		--type-files osmNetconvert-PT-loc.typ.xml \
		-o $@

porto.net.xml: porto-osm-geo.net.xml diff.con.xml diff.edg.xml diff.nod.xml diff.tll.xml diff.typ.xml
	netconvert --sumo-net-file $< \
		--roundabouts.guess false \
		-x diff.con.xml \
		-e diff.edg.xml \
		-n diff.nod.xml \
		-i diff.tll.xml \
		-t diff.typ.xml \
		-o $@

%-geo.net.xml: %.net.xml
	./removeOffset.py $< > $@

porto-armis-shape.taz.xml: armis/porto-armis.net.xml armis/porto-armis.taz.xml
	./addShapeToTAZ.py $? > $@

OSM_DATE=$(shell date -u --iso-8601=seconds)

porto-unbounded.osm: | overpass-request.txt
	./overpass-request.py $< ${OSM_DATE} $@
