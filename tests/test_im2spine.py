import os
import pytest
from im2spine import AsepriteFile
from numpy.testing import assert_equal
import tempfile
import glob

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def ase_file():
    ase_path = os.path.join(DIR_PATH, 'data', '4x4.ase')
    return AsepriteFile(ase_path)


def test_aseprite_file_layers(ase_file):
    assert ase_file.layers() == ['GGG-bbb', 'GGG-ccc', '-aaa']


def test_aseprite_file_images(ase_file):
    images = ase_file.images()
    assert list(images.keys()) == ['GGG-bbb', 'GGG-ccc', '-aaa']
    assert_equal(images['-aaa'][:, :, 3],
                 [[0, 0, 0, 0],
                  [0, 255, 255, 0],
                  [0, 255, 255, 0],
                  [0, 0, 0, 0]])
    assert_equal(images['GGG-ccc'][:, :, 3],
                 [[0, 0, 0, 0],
                  [255, 255, 0, 0],
                  [255, 255, 0, 0],
                  [0, 0, 0, 0]])
    assert_equal(images['GGG-bbb'][:, :, 3],
                 [[255, 255, 0, 0],
                  [255, 255, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 255, 0]])
