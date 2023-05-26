- porto-boundary-strict.poly
  - Obtained from http://polygons.openstreetmap.fr/index.py?id=3372453
- porto-boundary-strict.osm
  - Strict boundary of municipality of Porto
- porto-boundary.osm
  - Wider version of porto-boundary-strict.osm. Manually drawn from porto-boundary-strict.osm

To get all data from Porto in Overpass API:
```txt
[out:xml][timeout:30];
(
    node(area:3603372453);
    way(area:3603372453);
    relation(area:3603372453);
);
(._;>;);
out meta;
```

To get all roads from Porto in Overpass API:
```txt
[out:xml][timeout:30];
way["highway"](area:3603372453);
(._;>;);
out meta;
```
