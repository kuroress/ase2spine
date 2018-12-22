import os
import pytest
from im2spine import AsepriteFile, SpineSkeleton
from numpy.testing import assert_equal
import tempfile
import json
import imageio

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def ase_file():
    ase_path = os.path.join(DIR_PATH, 'data', '4x4.ase')
    return AsepriteFile(ase_path)


def test_aseprite_file_images(ase_file):
    images = ase_file.images()
    assert [i.name() for i in images] == ['GGG-bbb', 'GGG-ccc', '-aaa']
    assert_equal(images[2].data[:, :, 3],
                 [[0, 0, 0, 0],
                  [0, 255, 255, 0],
                  [0, 255, 255, 0],
                  [0, 0, 0, 0]])
    assert_equal(images[1].data[:, :, 3],
                 [[0, 0, 0, 0],
                  [255, 255, 0, 0],
                  [255, 255, 0, 0],
                  [0, 0, 0, 0]])
    assert_equal(images[0].data[:, :, 3],
                 [[255, 255, 0, 0],
                  [255, 255, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 255, 0]])


def test_aseprite_file_trim(ase_file):
    image = ase_file.images()[0]
    trimmed = image.trim()
    assert image.bbox() == (0, 0, 3, 4)
    assert trimmed.name() == image.name()
    assert_equal(trimmed.data[:, :, 3],
                 image.data[:, :3, 3])


def test_spine_skeleton_to_png(ase_file):
    with tempfile.TemporaryDirectory() as dir_name:
        sk = SpineSkeleton(ase_file.images(), dir_name)
        sk.to_png()

        images = [imageio.imread(os.path.join(dir_name, im.name() + '.png'))
                  for im in ase_file.images()]
        assert images[0].shape == (4, 3, 4)
        assert images[1].shape == (2, 2, 4)
        assert images[2].shape == (2, 2, 4)


def test_spine_skeleton_to_json(ase_file):
    with tempfile.TemporaryDirectory() as dir_name:
        sk = SpineSkeleton(ase_file.images(), dir_name)
        sk.to_json()
        with open(os.path.join(dir_name, 'skeleton.json'), 'r') as f:
            assert json.load(f) == {
                "skeleton": {
                    "spine": SpineSkeleton.VERSION
                },
                "bones": [
                    {
                        "name": "root"
                    }
                ],
                "slots": [
                    {
                        "name": "GGG-bbb",
                        "bone": "root",
                        "attachment": "GGG-bbb"
                    },
                    {
                        "name": "GGG-ccc",
                        "bone": "root",
                        "attachment": "GGG-ccc"
                    },
                    {
                        "name": "-aaa",
                        "bone": "root",
                        "attachment": "-aaa"
                    }
                ],
                "skins": {
                    "default": {
                        "-aaa": {
                            "-aaa": {
                                "x": 2.0,
                                "y": -2.0,
                                "width": 2,
                                "height": 2
                            }
                        },
                        "GGG-ccc": {
                            "GGG-ccc": {
                                "x": 1.0,
                                "y": -2.0,
                                "width": 2,
                                "height": 2
                            }
                        },
                        "GGG-bbb": {
                            "GGG-bbb": {
                                "x": 1.5,
                                "y": -2.0,
                                "width": 3,
                                "height": 4
                            }
                        }
                    }
                }
            }
