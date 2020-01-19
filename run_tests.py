#!/usr/bin/env python

import io
import json
import sys
import unittest
from copy import deepcopy
from unittest.mock import patch

from arcgis2geojson import arcgis2geojson, main


"""
arcgis2geojson is a derivative work of ESRI's arcgis-to-geojson-utils:
https://github.com/Esri/arcgis-to-geojson-utils/
Original code is Copyright 2015 by Esri and was licensed under
the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
Ported to Python in 2016 by Chris Shaw.

arcgis2geojson is made available under the MIT License.
"""


class ArcGisToGeoJsonTests(unittest.TestCase):

    def test_convert_arcgis_point_to_geojson_point(self):
        input = {
            'x': -66.796875,
            'y': 20.0390625,
            'spatialReference': {
                'wkid': 4326
            }
        }
        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [-66.796875, 20.0390625])
        self.assertEqual(output['type'], 'Point')

    def test_convert_string_json_to_string_json(self):
        input = json.dumps({
            'x': -66.796875,
            'y': 20.0390625,
            'spatialReference': {
                'wkid': 4326
            }
        })
        output = arcgis2geojson(input)
        self.assertIsInstance(output, str)
        output = json.loads(output)
        self.assertEqual(output['coordinates'], [-66.796875, 20.0390625])
        self.assertEqual(output['type'], 'Point')

    def test_convert_arcgis_point_with_z_value_to_geojson_point(self):
        input = {
            'x': -66.796875,
            'y': 20.0390625,
            'z': 1,
            'spatialReference': {
                'wkid': 4326
            }
        }
        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [-66.796875, 20.0390625, 1])
        self.assertEqual(output['type'], 'Point')

    def test_convert_arcgis_null_island_to_geojson_point(self):
        input = {
            'x': 0,
            'y': 0,
            'spatialReference': {
                'wkid': 4326
            }
        }
        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [0, 0])
        self.assertEqual(output['type'], 'Point')

    def test_invalid_geometry(self):
        input = {
            'geometry': {
                'x': 'NaN',
                'y': 'NaN'
            },
            'attributes': {
                'foo': 'bar'
            }
        }
        output = arcgis2geojson(input)
        self.assertIsNone(output['geometry'])

    def test_convert_arcgis_polyline_to_geojson_linestring(self):
        input = {
            'paths': [
                [
                    [6.6796875, 47.8125],
                    [-65.390625, 52.3828125],
                    [-52.3828125, 42.5390625]
                ]
            ],
            'spatialReference': {
                'wkid': 4326
            }
        }
        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [
            [6.6796875, 47.8125],
            [-65.390625, 52.3828125],
            [-52.3828125, 42.5390625]
        ])
        self.assertEqual(output['type'], 'LineString')

    def test_convert_arcgis_polyline_with_z_values_to_geojson_linestring(self):
        input = {
            'paths': [
                [
                    [6.6796875, 47.8125, 1],
                    [-65.390625, 52.3828125, 1],
                    [-52.3828125, 42.5390625, 1]
                ]
            ],
            'spatialReference': {
                'wkid': 4326
            }
        }
        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [
            [6.6796875, 47.8125, 1],
            [-65.390625, 52.3828125, 1],
            [-52.3828125, 42.5390625, 1]
        ])
        self.assertEqual(output['type'], 'LineString')

    def test_convert_arcgis_polygon_to_geojson_polygon(self):
        input = {
            'rings': [
                [
                    [41.8359375, 71.015625],
                    [56.953125, 33.75],
                    [21.796875, 36.5625],
                    [41.8359375, 71.015625]
                ]
            ],
            'spatialReference': {
                'wkid': 4326
            }
        }
        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [
            [
                [41.8359375, 71.015625],
                [21.796875, 36.5625],
                [56.953125, 33.75],
                [41.8359375, 71.015625]
            ]
        ])
        self.assertEqual(output['type'], 'Polygon')

    def test_convert_arcgis_polygon_with_z_values_to_geojson_polygon(self):
        input = {
            'rings': [
                [
                    [41.8359375, 71.015625, 1],
                    [56.953125, 33.75, 1],
                    [21.796875, 36.5625, 1],
                    [41.8359375, 71.015625, 1]
                ]
            ],
            'spatialReference': {
                'wkid': 4326
            }
        }
        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [
            [
                [41.8359375, 71.015625, 1],
                [21.796875, 36.5625, 1],
                [56.953125, 33.75, 1],
                [41.8359375, 71.015625, 1]
            ]
        ])
        self.assertEqual(output['type'], 'Polygon')

    def test_close_rings_in_convert_arcgis_polygon_to_geojson_polygon(self):
        input = {
            'rings': [
                [
                    [41.8359375, 71.015625],
                    [56.953125, 33.75],
                    [21.796875, 36.5625]
                ]
            ],
            'spatialReference': {
                'wkid': 4326
            }
        }
        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [
            [
                [41.8359375, 71.015625],
                [21.796875, 36.5625],
                [56.953125, 33.75],
                [41.8359375, 71.015625]
            ]
        ])
        self.assertEqual(output['type'], 'Polygon')

    def test_parse_arcgis_multipoint_to_geojson_multipoint(self):
        input = {
            'points': [
                [
                    [41.8359375, 71.015625],
                    [56.953125, 33.75],
                    [21.796875, 36.5625]
                ]
            ],
            'spatialReference': {
                'wkid': 4326
            }
        }
        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [
            [
                [41.8359375, 71.015625],
                [56.953125, 33.75],
                [21.796875, 36.5625],
            ]
        ])
        self.assertEqual(output['type'], 'MultiPoint')

    def test_parse_arcgis_polyline_to_geojson_multilinestring(self):
        input = {
            'paths': [
                [
                    [41.8359375, 71.015625],
                    [56.953125, 33.75]
                ],
                [
                    [21.796875, 36.5625],
                    [41.8359375, 71.015625]
                ]
            ],
            'spatialReference': {
                'wkid': 4326
            }
        }
        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [
            [
                [41.8359375, 71.015625],
                [56.953125, 33.75]
            ],
            [
                [21.796875, 36.5625],
                [41.8359375, 71.015625]
            ]
        ])
        self.assertEqual(output['type'], 'MultiLineString')

    def test_parse_arcgis_polygon_to_geojson_multipolygon(self):
        input = {
            'rings': [
                [
                    [-122.63, 45.52],
                    [-122.57, 45.53],
                    [-122.52, 45.50],
                    [-122.49, 45.48],
                    [-122.64, 45.49],
                    [-122.63, 45.52],
                    [-122.63, 45.52]
                ],
                [
                    [-83, 35],
                    [-74, 35],
                    [-74, 41],
                    [-83, 41],
                    [-83, 35]
                ]
            ],
            'spatialReference': {
                'wkid': 4326
            }
        }

        expected = [
            [
                [
                    [-122.63, 45.52],
                    [-122.63, 45.52],
                    [-122.64, 45.49],
                    [-122.49, 45.48],
                    [-122.52, 45.5],
                    [-122.57, 45.53],
                    [-122.63, 45.52]
                ]
            ],
            [
                [
                    [-83, 35],
                    [-74, 35],
                    [-74, 41],
                    [-83, 41],
                    [-83, 35]
                ]
            ]
        ]

        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], expected)
        self.assertEqual(output['type'], 'MultiPolygon')

    def test_strip_invalid_rings_in_convert_arcgis_polygon_to_geojson_polygon(self):
        input = {
            'rings': [
                [
                    [-122.63, 45.52],
                    [-122.57, 45.53],
                    [-122.52, 45.50],
                    [-122.49, 45.48],
                    [-122.64, 45.49],
                    [-122.63, 45.52],
                    [-122.63, 45.52]
                ],
                [
                    [-83, 35],
                    [-74, 35],
                    [-83, 35]
                ]
            ],
            'spatialReference': {
                'wkid': 4326
            }
        }

        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [
            [
                [-122.63, 45.52],
                [-122.63, 45.52],
                [-122.64, 45.49],
                [-122.49, 45.48],
                [-122.52, 45.5],
                [-122.57, 45.53],
                [-122.63, 45.52]
            ]
        ])
        self.assertEqual(output['type'], 'Polygon')

    def test_close_rings_in_convert_arcgis_polygon_to_geojson_multipolygon(self):
        input = {
            'rings': [
                [
                    [-122.63, 45.52],
                    [-122.57, 45.53],
                    [-122.52, 45.50],
                    [-122.49, 45.48],
                    [-122.64, 45.49]
                ],
                [
                    [-83, 35],
                    [-74, 35],
                    [-74, 41],
                    [-83, 41]
                ]
            ],
            'spatialReference': {
                'wkid': 4326
            }
        }

        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [
            [
                [
                    [-122.63, 45.52],
                    [-122.64, 45.49],
                    [-122.49, 45.48],
                    [-122.52, 45.5],
                    [-122.57, 45.53],
                    [-122.63, 45.52]
                ]
            ],
            [
                [
                    [-83, 35],
                    [-74, 35],
                    [-74, 41],
                    [-83, 41],
                    [-83, 35]
                ]
            ]
        ])
        self.assertEqual(output['type'], 'MultiPolygon')

    def test_parse_arcgis_multipolygon_with_holes_to_geojson_multipolygon(self):
        input = {
            'type': 'Polygon',
            'rings': [
                [
                    [-100.74462180954974, 39.95017165502381],
                    [-94.50439384003792, 39.91647453608879],
                    [-94.41650267263967, 34.89313438177965],
                    [-100.78856739324887, 34.85708140996771],
                    [-100.74462180954974, 39.95017165502381]
                ],
                [
                    [-99.68993678392353, 39.341088433448896],
                    [-99.68993678392353, 38.24507658785885],
                    [-98.67919734199646, 37.86444431771113],
                    [-98.06395917020868, 38.210554846669694],
                    [-98.06395917020868, 39.341088433448896],
                    [-99.68993678392353, 39.341088433448896]
                ],
                [
                    [-96.83349180978595, 37.23732027507514],
                    [-97.31689323047635, 35.967330282988534],
                    [-96.5698183075912, 35.57512048069255],
                    [-95.42724211456674, 36.357601429255965],
                    [-96.83349180978595, 37.23732027507514]
                ],
                [
                    [-101.4916967324349, 38.24507658785885],
                    [-101.44775114873578, 36.073960493943744],
                    [-103.95263145328033, 36.03843312329154],
                    [-103.68895795108557, 38.03770050767439],
                    [-101.4916967324349, 38.24507658785885]
                ]
            ],
            'spatialReference': {
                'wkid': 4326
            }
        }

        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [
            [
                [
                    [-100.74462180954974, 39.95017165502381],
                    [-100.78856739324887, 34.85708140996771],
                    [-94.41650267263967, 34.89313438177965],
                    [-94.50439384003792, 39.91647453608879],
                    [-100.74462180954974, 39.95017165502381]
                ],
                [
                    [-96.83349180978595, 37.23732027507514],
                    [-95.42724211456674, 36.357601429255965],
                    [-96.5698183075912, 35.57512048069255],
                    [-97.31689323047635, 35.967330282988534],
                    [-96.83349180978595, 37.23732027507514]
                ],
                [
                    [-99.68993678392353, 39.341088433448896],
                    [-98.06395917020868, 39.341088433448896],
                    [-98.06395917020868, 38.210554846669694],
                    [-98.67919734199646, 37.86444431771113],
                    [-99.68993678392353, 38.24507658785885],
                    [-99.68993678392353, 39.341088433448896]
                ]
            ],
            [
                [
                    [-101.4916967324349, 38.24507658785885],
                    [-103.68895795108557, 38.03770050767439],
                    [-103.95263145328033, 36.03843312329154],
                    [-101.44775114873578, 36.073960493943744],
                    [-101.4916967324349, 38.24507658785885]
                ]
            ]
        ])
        self.assertEqual(output['type'], 'MultiPolygon')

    def test_parse_holes_outside_outer_rings_in_arcgis_polygon_with_holes_to_geojson_polygon(self):
        input = {
            'rings': [
                [
                    [-122.45, 45.63], [-122.45, 45.68], [-122.39, 45.68],
                    [-122.39, 45.63], [-122.45, 45.63]
                ],
                [
                    [-122.46, 45.64], [-122.4, 45.64], [-122.4, 45.66],
                    [-122.46, 45.66], [-122.46, 45.64]
                ]
            ],
            'spatialReference': {
                'wkid': 4326
            }
        }

        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [
            [
                [-122.45, 45.63], [-122.39, 45.63], [-122.39, 45.68],
                [-122.45, 45.68], [-122.45, 45.63]
            ],
            [
                [-122.46, 45.64], [-122.46, 45.66], [-122.4, 45.66],
                [-122.4, 45.64], [-122.46, 45.64]
            ]
        ])
        self.assertEqual(output['type'], 'Polygon')

    def test_parse_arcgis_feature_to_geojson_feature(self):
        input = {
            'geometry': {
                'rings': [
                    [
                        [41.8359375, 71.015625],
                        [56.953125, 33.75],
                        [21.796875, 36.5625],
                        [41.8359375, 71.015625]
                    ]
                ],
                'spatialReference': {
                    'wkid': 4326
                }
            },
            'attributes': {
                'foo': 'bar'
            }
        }

        output = arcgis2geojson(input)
        self.assertEqual(output['geometry']['coordinates'], [
            [
                [41.8359375, 71.015625],
                [21.796875, 36.5625],
                [56.953125, 33.75],
                [41.8359375, 71.015625]
            ]
        ])
        self.assertEqual(output['geometry']['type'], 'Polygon')

    def test_convert_arcgis_feature_array_to_geojson_featurecollection(self):
        input = {
            "displayFieldName": "prop0",
            "fieldAliases": {"prop0": "prop0"},
            "geometryType": "esriGeometryPolygon",
            "fields": [
                {
                    "length": 20,
                    "name": "prop0",
                    "type": "esriFieldTypeString",
                    "alias": "prop0"
                },
                {
                    "name": "OBJECTID",
                    "type": "esriFieldTypeOID",
                    "alias": "OBJECTID"
                },
                {
                    "name": "FID",
                    "type": "esriFieldTypeDouble",
                    "alias": "FID"
                }
            ],
            "spatialReference": {"wkid": 4326},
            "features": [
                {
                    "geometry": {
                        "x": 102,
                        "y": 0.5
                    },
                    "attributes": {
                        "prop0": "value0",
                        "FID": 0,
                        "OBJECTID": 0
                    }
                },
                {
                    "geometry": {
                        "paths": [
                            [
                                [102, 0],
                                [103, 1],
                                [104, 0],
                                [105, 1]
                            ]
                        ]
                    },
                    "attributes": {
                        "prop0": None,
                        "FID": 1,
                        "OBJECTID": None
                    }
                },
                {
                    "geometry": {
                        "rings": [
                            [
                                [100, 0],
                                [100, 1],
                                [101, 1],
                                [101, 0],
                                [100, 0]
                            ]
                        ]
                    },
                    "attributes": {
                        "prop0": None,
                        "FID": 30.25,
                        "OBJECTID": 2
                    }
                }
            ]
        }

        output = arcgis2geojson(input, 'prop0')
        self.assertEqual(output, {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "prop0": "value0",
                        "OBJECTID": 0,
                        "FID": 0
                    },
                    "id": "value0",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            102.0,
                            0.5
                        ]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "prop0": None,
                        "OBJECTID": None,
                        "FID": 1
                    },
                    "id": 1,
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [102.0, 0.0],
                            [103.0, 1.0],
                            [104.0, 0.0],
                            [105.0, 1.0]
                        ]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "prop0": None,
                        "OBJECTID": 2,
                        "FID": 30.25
                    },
                    "id": 2,
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [100.0, 0.0],
                                [101.0, 0.0],
                                [101.0, 1.0],
                                [100.0, 1.0],
                                [100.0, 0.0]
                            ]
                        ]
                    }
                }
            ]
        })

    def test_parse_arcgis_feature_with_objectid(self):
        input = {
            'geometry': {
                'rings': [
                    [
                        [41.8359375, 71.015625],
                        [56.953125, 33.75],
                        [21.796875, 36.5625],
                        [41.8359375, 71.015625]
                    ]
                ],
                'spatialReference': {
                    'wkid': 4326
                }
            },
            'attributes': {
                'OBJECTID': 123
            }
        }

        output = arcgis2geojson(input)
        self.assertEqual(output['id'], 123)

    def test_parse_arcgis_feature_with_fid(self):
        input = {
            'geometry': {
                'rings': [
                    [
                        [41.8359375, 71.015625],
                        [56.953125, 33.75],
                        [21.796875, 36.5625],
                        [41.8359375, 71.015625]
                    ]
                ],
                'spatialReference': {
                    'wkid': 4326
                }
            },
            'attributes': {
                'FID': 123
            }
        }

        output = arcgis2geojson(input)
        self.assertEqual(output['id'], 123)

    def test_parse_arcgis_feature_with_custom_id(self):
        input = {
            'geometry': {
                'rings': [
                    [
                        [41.8359375, 71.015625],
                        [56.953125, 33.75],
                        [21.796875, 36.5625],
                        [41.8359375, 71.015625]
                    ]
                ],
                'spatialReference': {
                    'wkid': 4326
                }
            },
            'attributes': {
                'FooID': 123
            }
        }

        output = arcgis2geojson(input, 'FooID')
        self.assertEqual(output['id'], 123)

    def test_parse_arcgis_feature_with_empty_attributes(self):
        input = {
            'geometry': {
                'rings': [
                    [
                        [41.8359375, 71.015625],
                        [56.953125, 33.75],
                        [21.796875, 36.5625],
                        [41.8359375, 71.015625]
                    ]
                ],
                'spatialReference': {
                    'wkid': 4326
                }
            },
            'attributes': {}
        }

        output = arcgis2geojson(input)
        self.assertEqual(output['geometry']['coordinates'], [
            [
                [41.8359375, 71.015625],
                [21.796875, 36.5625],
                [56.953125, 33.75],
                [41.8359375, 71.015625]
            ]
        ])
        self.assertEqual(output['geometry']['type'], 'Polygon')
        self.assertEqual(output['properties'], {})

    def test_parse_arcgis_feature_with_no_attributes(self):
        input = {
            'geometry': {
                'rings': [
                    [
                        [41.8359375, 71.015625],
                        [56.953125, 33.75],
                        [21.796875, 36.5625],
                        [41.8359375, 71.015625]
                    ]
                ],
                'spatialReference': {
                    'wkid': 4326
                }
            }
        }

        output = arcgis2geojson(input)
        self.assertEqual(output['geometry']['coordinates'], [
            [
                [41.8359375, 71.015625],
                [21.796875, 36.5625],
                [56.953125, 33.75],
                [41.8359375, 71.015625]
            ]
        ])
        self.assertEqual(output['geometry']['type'], 'Polygon')
        self.assertEqual(output['properties'], None)

    def test_parse_arcgis_feature_with_no_geometry(self):
        input = {
            'attributes': {
                'foo': 'bar'
            }
        }

        output = arcgis2geojson(input)
        self.assertEqual(output['geometry'], None)
        self.assertEqual(output['properties']['foo'], 'bar')

    def test_custom_id_field(self):
        input = {
            'x': -66.796875,
            'y': 20.0390625,
            'spatialReference': {
                'wkid': 4326
            },
            'attributes': {
                'OBJECTID': 123,
                'some_field': 456,
            }
        }

        output = arcgis2geojson(input, 'some_field')
        self.assertEqual(456, output['id'])

    def test_id_must_be_string_or_number(self):
        input = {
            'x': -66.796875,
            'y': 20.0390625,
            'spatialReference': {
                'wkid': 4326
            },
            'attributes': {
                'OBJECTID': 123,
                'some_field': {
                    'not a number': 'or a string'
                }
            }
        }

        output = arcgis2geojson(input, 'some_field')

        # 'some_field' isn't a number or string - fall back to OBJECTID
        self.assertEqual(123, output['id'])

    def test_null_id_not_allowed(self):
        input = {
            'x': -66.796875,
            'y': 20.0390625,
            'spatialReference': {
                'wkid': 4326
            },
            # no 'OBJECTID' or 'FID' in 'attributes'
            'attributes': {
                'foo': 'bar'
            }
        }

        output = arcgis2geojson(input)
        self.assertTrue('id' not in output)

    @patch('arcgis2geojson.logging')
    def test_warning_if_crs_not_4326(self, mock_logging):
        input = {
            'x': 392917.31,
            'y': 298521.34,
            'spatialReference': {
                'wkid': 27700
            }
        }

        output = arcgis2geojson(input)

        mock_logging.warning.assert_called_with(
            "Object converted in non-standard crs - {'wkid': 27700}")
        self.assertTrue('crs' not in output)
        self.assertEqual(output['coordinates'], [392917.31, 298521.34])


    def test_do_not_modify_original_arcgis_geometry(self):
        input = {
            'geometry': {
                'rings': [
                    [
                        [41.8359375, 71.015625],
                        [56.953125, 33.75],
                        [21.796875, 36.5625],
                        [41.8359375, 71.015625]
                    ]
                ],
                'spatialReference': {
                    'wkid': 4326
                }
            },
            'attributes': {
                'foo': 'bar'
            }
        }

        expected = deepcopy(input)
        output = arcgis2geojson(input)

        self.assertEqual(input, expected)

    def test_convert_arcgis_extent_to_geojson_polygon(self):
        input = {
            'xmax': -35.5078125,
            'ymax': 41.244772343082076,
            'xmin': -13.7109375,
            'ymin': 54.36775852406841,
            'spatialReference': {
                'wkid': 4326
            }
        }
        output = arcgis2geojson(input)
        self.assertEqual(output['coordinates'], [
            [
                [-35.5078125, 41.244772343082076],
                [-13.7109375, 41.244772343082076],
                [-13.7109375, 54.36775852406841],
                [-35.5078125, 54.36775852406841],
                [-35.5078125, 41.244772343082076]
            ]
        ])

    def test_cli(self):
        stdout = sys.stdout
        sys.stdout = io.StringIO()

        input = u'{ "x": -66.796875, "y": 20.0390625, "spatialReference": { "wkid": 4326 } }'
        stdin = sys.stdin
        sys.stdin = io.StringIO(input)

        main()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, arcgis2geojson(input))

        sys.stdout = stdout
        sys.stdin = stdin

if __name__ == '__main__':
    unittest.main()
