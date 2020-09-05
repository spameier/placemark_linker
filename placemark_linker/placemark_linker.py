#!/usr/bin/env python3
"""This script links points in a KML file to other bigger areas and creates a csv file"""
import csv
import os
from argparse import ArgumentParser
from datetime import datetime
from threading import Thread

try:
    # this only works when the program has been installed
    from placemark_linker.placemark import Placemark
except ModuleNotFoundError:
    from placemark import Placemark


def main():
    """main function"""

    def _get_thread(placemark, key, other_placemarks):
        """return a thread that links placemark by key to the matching one in other_placemarks"""

        def _link_placemark(placemark, key, other_placemarks):
            """link placemark by key to the matching one in other_placemarks"""
            placemark.links[key] = None
            for other_placemark in other_placemarks:
                if placemark.is_inside(other_placemark):
                    placemark.links[key] = other_placemark
                    break

        thread = Thread(target=_link_placemark, args=(placemark, key, other_placemarks))
        thread.start()
        return thread

    def _get_name(placemark):
        """extract name from placemark"""
        if placemark is not None:
            return placemark.name
        return ""

    def _get_names(links):
        """extract names from a list of placemarks"""
        return [_get_name(l) for l in links.values()]

    parser = ArgumentParser(description="Map points to geometries in KML files")
    parser.add_argument(
        "-p",
        "--points",
        help="KML file containing the points",
        metavar="filename",
        required=True,
    )
    parser.add_argument(
        "-g",
        "--geometries",
        help="KML file(s) containing the geometries",
        metavar=("name", "filename"),
        action="append",
        nargs=2,
        required=True,
    )
    parser.add_argument(
        "-c",
        "--csv_filename",
        help="file to write to (defaults to <points>_<datetime>.csv",
    )

    args = parser.parse_args()

    if args.csv_filename:
        csv_filename = args.csv_filename
    else:
        csv_filename = args.points.replace(".kml", "_{}.csv").format(
            datetime.now().strftime("%Y%m%d-%H%M%S")
        )
    points = Placemark.from_kml(args.points)
    geometries = {}
    for arg in args.geometries:
        geometries[arg[0]] = Placemark.from_kml(arg[1])

    # link points to other areas
    # this is probably not optimal
    for point in points:
        threads = []
        for name in geometries:
            threads.append(_get_thread(point, name, geometries[name]))
        for thread in threads:
            thread.join()
        msg = "{0} / {1}: {2}".format(points.index(point) + 1, len(points), point.name)
        buffer = " " * (os.get_terminal_size().columns - len(msg))
        print(msg + buffer, end="\r")
    print()

    with open(csv_filename, "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Point"] + list(geometries.keys()))
        for point in points:
            writer.writerow([point.name] + _get_names(point.links))


if __name__ == "__main__":
    main()
