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


def test_aseprite_file_images(ase_file):
    images = ase_file.images()
    assert [i.name() for i in images] == ['GGG-bbb', 'GGG-ccc', '-aaa']
    assert_equal(images[0].data[:, :, 3],
                 [[255, 255, 0, 0],
                  [255, 255, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 255, 0]])
    assert_equal(images[1].data[:, :, 3],
                 [[0, 0, 0, 0],
                  [255, 255, 0, 0],
                  [255, 255, 0, 0],
                  [0, 0, 0, 0]])
    assert_equal(images[2].data[:, :, 3],
                 [[0, 0, 0, 0],
                  [0, 255, 255, 0],
                  [0, 255, 255, 0],
                  [0, 0, 0, 0]])
