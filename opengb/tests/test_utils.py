"""
Opengb utils unit tests.
"""
import os
import tempfile
import shutil
import builtins
from mock import patch, mock_open

from opengb.tests import OpengbTestCase
from opengb import utils

GCODE = """
    M107
    M190 S115 ; set bed temperature
    M104 S205 ; set temperature
    G28 ; home all axes
    G1 Z5 F5000 ; lift nozzle

    M109 S205 ; wait for temperature to be reached
    G21 ; set units to millimeters
    G90 ; use absolute coordinates
    M82 ; use absolute distances for extrusion
    G92 E0
    G1 Z0.500 F7800.000
    G1 E-2.00000 F2400.00000
    G92 E0
    G1 X75.666 Y76.670 F7800.000
    G1 E2.00000 F2400.00000
    G1 X77.428 Y75.130 E2.14774 F1800.000
    G1 X79.603 Y74.269 E2.29548
    G1 X81.016 Y74.123 E2.38516
    G1 X118.984 Y74.123 E4.78272
    G1 X121.290 Y74.520 E4.93046
"""


class TestFileUtils(OpengbTestCase):

    def setUp(self):
        self.gcode = GCODE

    def test_gcode_file_loaded(self):
        """Gcode file with given id is loaded from the filesystem."""
        gcode_dir = tempfile.mkdtemp()
        id = 123
        with open(os.path.join(gcode_dir, str(id)), 'wb') as p:
            p.write(self.gcode.encode())
        with patch.object(utils.options.mockable(), 'gcode_dir',
                          gcode_dir):
            gcode = utils.load_gcode_file(id)
        self.assertEqual(gcode, self.gcode)
        shutil.rmtree(gcode_dir)

    def test_missing_gcode_file_throws_IOError(self):
        """Loading a missing gcode file throws an IOError"""
        gcode_dir = tempfile.mkdtemp()
        with patch.object(utils.options.mockable(), 'gcode_dir',
                          gcode_dir):
            with self.assertRaises(IOError):
                utils.load_gcode_file(id)
        shutil.rmtree(gcode_dir)

    def test_failed_gcode_file_throws_IOError(self):
        """Failure while loading a gcode file throws an IOError"""
        mopen = mock_open()
        mopen.side_effect = IOError
        with patch('builtins.open', mopen):
            with self.assertRaises(IOError):
                utils.load_gcode_file(123)
