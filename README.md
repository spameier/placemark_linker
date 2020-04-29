# Placemark linker
This `python` script links points contained in a kml file to other areas contained in other kml files.

The points are expected to be simple points with x, y and maybe z coordinates. The other areas have to be multigeometry containing multiple polygons. If you want to add different shapes you need to expand the function `get_geometry_from_xml` in the class [`Placemark`](./placemark_linker/placemark.py).

## Installation

To install, simply run:
```shell
$ pip3 install .
```
Under Windows you have to install `shapely` manually. Download the matching wheel archives from http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely and install it using pip:
```shell
pip install Shapely-1.6.4.post2-cp37-cp37m-win_amd64.whl
```

### Generate executables
You can also generate executables by using `cx_Freeze`:
#### Linux
1. Install dependencies
    1. Install `cx_Freeze`: `pip3 install cx_Freeze`
	2. Install other requirements: `pip3 install -r requirements.txt`
2. Run the script `cxfreeze`
```
$ cxfreeze placemark_linker/placemark_linker.py --target-dir dist/lin
```

#### Windows
1. Install dependencies
    1. Install `shapely` from http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely
	2. Install `cx_Freeze` from https://www.lfd.uci.edu/~gohlke/pythonlibs/#cx_freeze
	3. Install other requirements: `pip install -r requirements.txt`
2. Run the script `cxfreeze`. On my mobile python installation this was in a relative path.
```
python ..\WPy64-3740\python-3.7.4.amd64\Scripts\cxfreeze placemark_linker\placemark_linker.py --target-dir dist\win
```

## Usage
Placemark linker takes the following arguments:
```
usage: placemark_linker.py [-h] -p filename -g name filename [-c CSV_FILENAME]

Map points to geometries in KML files

optional arguments:
  -h, --help            show this help message and exit
  -p filename, --points filename
                        KML file containing the points
  -g name filename, --geometries name filename
                        KML file(s) containing the geometries
  -c CSV_FILENAME, --csv_filename CSV_FILENAME
                        file to write to (defaults to <points>_<datetime>.csv
```

### Example
If you're in a folder next to placemark linker you might have a folder layout like this:
```
├── placemark_linker
│   ├── dist
│   │   ├── lin
│   │   │   └── placemark_linker
│   │   └── win
│   │       └── placemark_linker.exe
│   └── ...
└── res
    ├── Communes aug 2018.kml
    ├── Districts aug 2018.kml
    ├── Fokontany aug 2018.kml
    ├── Regions aug 2018.kml
    └── villages february 2018.kml
```
Then just execute the following:
- Linux
```
../placemark_linker/dist/lin/placemark_linker --points "villages february 2018.kml" --geometries Fokontany "Fokontany aug 2018.kml" --geometries Commune "Communes aug 2018.kml" --geometries District "Districts aug 2018.kml" --geometries Region "Regions aug 2018.kml" --csv_file villages.csv
```
- Windows
```
..\placemark_linker\dist\win\placemark_linker.exe --points "villages february 2018.kml" --geometries Fokontany "Fokontany aug 2018.kml" --geometries Commune "Communes aug 2018.kml" --geometries District "Districts aug 2018.kml" --geometries Region "Regions aug 2018.kml" --csv_file villages.csv
```

## Output
The script will generate a csv file specified by `--csv_filename` or if not provided defaults to the file name of `--points` plus a timestamp.
