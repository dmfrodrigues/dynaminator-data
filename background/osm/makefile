all: porto.poly.xml

porto.poly.xml: ../../porto.net.xml ../../porto-unbounded.osm osm.typ.xml
	polyconvert \
		--net-file  ../../porto.net.xml \
		--osm-files ../../porto-unbounded.osm \
		--type-file osm.typ.xml \
		--output-file porto.poly.xml

../../porto.net.xml:
	make -C ../.. porto.net.xml
