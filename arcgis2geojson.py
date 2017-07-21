"""
arcgis2geojson is a derivative work of ESRI's arcgis-to-geojson-utils:
https://github.com/Esri/arcgis-to-geojson-utils/
Original code is Copyright 2015 by Esri and was licensed under
the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
Ported to Python in 2016 by Chris Shaw.

arcgis2geojson is made available under the MIT License.
"""

import numbers


def pointsEqual(a, b):
    """
    checks if 2 [x, y] points are equal
    """
    for i in range(0, len(a)):
        if a[i] != b[i]:
            return False
    return True


def closeRing(coordinates):
    """
    checks if the first and last points of a ring are equal and closes the ring
    """
    if not pointsEqual(coordinates[0], coordinates[len(coordinates) - 1]):
        coordinates.append(coordinates[0])
    return coordinates


def ringIsClockwise(ringToTest):
    """
    determine if polygon ring coordinates are clockwise. clockwise signifies
    outer ring, counter-clockwise an inner ring or hole.
    """

    total = 0
    i = 0
    rLength = len(ringToTest)
    pt1 = ringToTest[i]
    pt2 = None
    for i in range(0, rLength - 1):
        pt2 = ringToTest[i + 1]
        total += (pt2[0] - pt1[0]) * (pt2[1] + pt1[1])
        pt1 = pt2

    return (total >= 0)


def vertexIntersectsVertex(a1, a2, b1, b2):
    uaT = (b2[0] - b1[0]) * (a1[1] - b1[1]) - (b2[1] - b1[1]) * (a1[0] - b1[0])
    ubT = (a2[0] - a1[0]) * (a1[1] - b1[1]) - (a2[1] - a1[1]) * (a1[0] - b1[0])
    uB = (b2[1] - b1[1]) * (a2[0] - a1[0]) - (b2[0] - b1[0]) * (a2[1] - a1[1])

    if uB != 0:
        ua = uaT / uB
        ub = ubT / uB

        if ua >= 0 and ua <= 1 and ub >= 0 and ub <= 1:
            return True

    return False


def arrayIntersectsArray(a, b):
    for i in range(0, len(a)-1):
        for j in range(0, len(b)-1):
            if vertexIntersectsVertex(a[i], a[i + 1], b[j], b[j + 1]):
                return True

    return False


def coordinatesContainPoint(coordinates, point):

    contains = False
    l = len(coordinates)
    i = -1
    j = l - 1
    while ((i + 1) < l):
        i = i + 1
        ci = coordinates[i]
        cj = coordinates[j]
        if ((ci[1] <= point[1] and point[1] < cj[1]) or (cj[1] <= point[1] and point[1] < ci[1])) and\
           (point[0] < (cj[0] - ci[0]) * (point[1] - ci[1]) / (cj[1] - ci[1]) + ci[0]):
            contains = not contains
        j = i
    return contains


def coordinatesContainCoordinates(outer, inner):
    intersects = arrayIntersectsArray(outer, inner)
    contains = coordinatesContainPoint(outer, inner[0])
    if not intersects and contains:
        return True
    return False


def convertRingsToGeoJSON(rings):
    """
    do any polygons in this array contain any other polygons in this array?
    used for checking for holes in arcgis rings
    """

    outerRings = []
    holes = []
    x = None  # iterator
    outerRing = None  # current outer ring being evaluated
    hole = None  # current hole being evaluated

    # for each ring
    for r in range(0, len(rings)):
        ring = closeRing(rings[r])
        if len(ring) < 4:
            continue

        # is this ring an outer ring? is it clockwise?
        if ringIsClockwise(ring):
            polygon = [ring]
            outerRings.append(polygon)  # push to outer rings
        else:
            holes.append(ring)  # counterclockwise push to holes

    uncontainedHoles = []

    # while there are holes left...
    while len(holes):
        # pop a hole off out stack
        hole = holes.pop()

        # loop over all outer rings and see if they contain our hole.
        contained = False
        x = len(outerRings) - 1
        while (x >= 0):
            outerRing = outerRings[x][0]
            if coordinatesContainCoordinates(outerRing, hole):
                # the hole is contained push it into our polygon
                outerRings[x].append(hole)
                contained = True
                break
            x = x-1

        # ring is not contained in any outer ring
        # sometimes this happens https://github.com/Esri/esri-leaflet/issues/320
        if not contained:
            uncontainedHoles.append(hole)

    # if we couldn't match any holes using contains we can try intersects...
    while len(uncontainedHoles):
        # pop a hole off out stack
        hole = uncontainedHoles.pop()

        # loop over all outer rings and see if any intersect our hole.
        intersects = False
        x = len(outerRings) - 1
        while (x >= 0):
            outerRing = outerRings[x][0]
            if arrayIntersectsArray(outerRing, hole):
                # the hole is contained push it into our polygon
                outerRings[x].append(hole)
                intersects = True
                break
            x = x-1

        if not intersects:
            outerRings.append([hole[::-1]])

    if len(outerRings) == 1:
        return {
            'type': 'Polygon',
            'coordinates': outerRings[0]
        }
    else:
        return {
            'type': 'MultiPolygon',
            'coordinates': outerRings
        }


def arcgis2geojson(arcgis, idAttribute=None):
    """
    Convert an ArcGIS JSON object to a GeoJSON object
    """

    geojson = {}

    if 'x' in arcgis and isinstance(arcgis['x'], numbers.Number) and\
        'y' in arcgis and isinstance(arcgis['y'], numbers.Number):
        geojson['type'] = 'Point'
        geojson['coordinates'] = [arcgis['x'], arcgis['y']]

    if 'points' in arcgis:
        geojson['type'] = 'MultiPoint'
        geojson['coordinates'] = arcgis['points']

    if 'paths' in arcgis:
        if len(arcgis['paths']) == 1:
            geojson['type'] = 'LineString'
            geojson['coordinates'] = arcgis['paths'][0]
        else:
            geojson['type'] = 'MultiLineString'
            geojson['coordinates'] = arcgis['paths']

    if 'rings' in arcgis:
        geojson = convertRingsToGeoJSON(arcgis['rings'])

    if 'geometry' in arcgis or 'attributes' in arcgis:
        geojson['type'] = 'Feature'
        if 'geometry' in arcgis:
            geojson['geometry'] = arcgis2geojson(arcgis['geometry'])
        else:
            geojson['geometry'] = None

        if 'attributes' in arcgis:
            geojson['properties'] = arcgis['attributes']
            if idAttribute in arcgis['attributes']:
                geojson['id'] = arcgis['attributes'][idAttribute]
            elif 'OBJECTID' in arcgis['attributes']:
                geojson['id'] = arcgis['attributes']['OBJECTID']
            elif 'FID' in arcgis['attributes']:
                geojson['id'] = arcgis['attributes']['FID']
        else:
            geojson['properties'] = None

    if 'geometry' in geojson and not(geojson['geometry']):
        geojson['geometry'] = None

    return geojson
