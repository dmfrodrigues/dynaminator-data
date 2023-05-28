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

porto-osm.net.xml: porto.osm netconvert.netccfg osmNetconvert-PT-loc.typ.xml
	netconvert --osm-files $< \
		-c netconvert.netccfg \
		-t osmNetconvert-PT-loc.typ.xml \
		-o $@

# netconvert (and netedit) tend to fix geometry without warning beforehand.
# As such, I am calling netconvert many times on the same file to make
# netconvert stabilize on a version.
	netconvert -s $@ -c netconvert.netccfg -o $@
	netconvert -s $@ -c netconvert.netccfg -o $@
# From experience, only two calls are necessary, but I am calling again just to
# be extra sure all needed changes are made by netconvert.
	netconvert -s $@ -c netconvert.netccfg -o $@

porto.net.xml: porto-osm-geo.net.xml netconvert.netccfg diff.con.xml diff.edg.xml diff.nod.xml diff.tll.xml diff.typ.xml
	netconvert --sumo-net-file $< \
		-c netconvert.netccfg \
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

OSM_DATE ?= $(shell date -u --iso-8601=seconds)

porto-unbounded.osm: | overpass-request.txt
	./overpass-request.py $| ${OSM_DATE} $@
