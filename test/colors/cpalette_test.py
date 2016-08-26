#!/usr/bin/env python

#stdlib imports
import urllib.request as request
import tempfile
import os.path
import sys
import shutil

#hack the path so that I can debug these functions if I need to
homedir = os.path.dirname(os.path.abspath(__file__)) #where is this script?
impactdir = os.path.abspath(os.path.join(homedir,'..','..'))
sys.path.insert(0,impactdir) #put this at the front of the system path, ignoring any installed impact stuff

#third party imports
import numpy as np

#local imports
from impactutils.colors import cpalette

TEST_FILE = """#This file is a test file for ColorPalette.
#Lines beginning with pound signs are comments.
#Lines beginning with pound signs followed by a "$" are variable definition lines.
#For example, the following line defines a variable called nan_color.
#$nan_color: 0,0,0,0
#$name: test
Z0 R0  G0  B0  Z1  R1  G1  B1
0   0   0   0   1  85  85  85
1  85  85  85   2 170 170 170
2 170 170 170   3 255 255 255 
"""

TEST_DICT = {'red':[(0.0, -0.999, 0.0), 
                    (0.33333333333333331, 0.3333333333333333, 0.3333333333333333), 
                    (0.66666666666666663, 0.6666666666666666, 0.6666666666666666), 
                    (1.0, 1.0, 0.999)],
             'green':[(0.0, -0.999, 0.0), 
                      (0.33333333333333331, 0.3333333333333333, 0.3333333333333333), 
                      (0.66666666666666663, 0.6666666666666666, 0.6666666666666666), 
                      (1.0, 1.0, 0.999)],
             'blue':[(0.0, -0.999, 0.0), 
                     (0.33333333333333331, 0.3333333333333333, 0.3333333333333333), 
                     (0.66666666666666663, 0.6666666666666666, 0.6666666666666666), 
                     (1.0, 1.0, 0.999)]}

def test_simplemap():
    z0 = [0,1,2]
    z1 = [1,2,3]
    rgb0 = [(0,0,0),
            (85,85,85),
            (170,170,170)]
    rgb1 = [(85,85,85),
            (170,170,170),
            (255,255,255)]
    nan_color = (0,0,0,0)
    cp = cpalette.ColorPalette('test',z0,z1,rgb0,rgb1,nan_color=nan_color)
    assert cp.getDataColor(0.5) == (0.16470588235294117, 0.16470588235294117, 0.16470588235294117, 1.0)
    cp.vmin = -1.0
    cp.vmax = 4.0
    assert cp.getDataColor(0.5) == (0.29803921568627451, 0.29803921568627451, 0.29803921568627451, 1.0)
    assert cp._cdict == TEST_DICT

def test_presets():
    palettes = cpalette.ColorPalette.getPresets()
    palettes.sort()
    assert palettes == ['mmi','pop','shaketopo']

    mmi = cpalette.ColorPalette.fromPreset('mmi')
    assert mmi.vmin == 0
    assert mmi.vmax == 10

    pop = cpalette.ColorPalette.fromPreset('pop')
    assert pop.vmin == 0
    assert pop.vmax == 50000
    
    topo = cpalette.ColorPalette.fromPreset('shaketopo')
    assert topo.vmin == -100
    assert topo.vmax == 9200
    
def test_file():
    try:
        tdir = tempfile.mkdtemp()
        tfile = os.path.join(tdir,'test.cpt')
        f = open(tfile,'wt')
        f.write(TEST_FILE)
        f.close()
        cp = cpalette.ColorPalette.fromFile(tfile)
        assert cp._cdict == TEST_DICT
    except:
        pass
    finally:
        if os.path.isdir(tdir):
            shutil.rmtree(tdir)

if __name__ == '__main__':
    test_simplemap()
    test_presets()
    test_file()

    