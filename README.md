# bisangkot
Open public-transportation database

* Map-view : https://altilunium.github.io/bisangkot 
* Tabular-view : https://routes.tracestrack.com/id/bus/all/


### How to contribute
Make route relation on OpenStreetMap.

Bus : 
```
type:route
route:bus
```

Angkot : 
```
type:route
route:share_taxi
```

### Process The Data
* Run `/scripts/a.html` to download the relation data from Overpass API
  *  The bounding box (line 32) is currently set to Java island. You can just change it to somewhere else. 
* Copy the relation data from previous step to text editor, save it as xml file.
* Open `/scripts/allrel.py`, configure `line 8` to that xml file. Run it, save the output as .js file.
* Open `index.html`, configure `line 11` to that .js file
