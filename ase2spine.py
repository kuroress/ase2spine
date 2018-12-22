import copy
import json
import os
import subprocess
import sys
import tempfile

import imageio
import numpy as np
from PIL import Image


class SpineImage:
    def __init__(self, image):
        self.image = image

    def basename(self):
        return self.image.name()

    def to_slot(self):
        return {"name": self.basename(),
                "bone": "root",
                "attachment": self.basename()
                }

    def to_skin(self):
        x1, y1, x2, y2 = self.image.bbox()
        xc, yc = (x1 + x2) / 2, (y1 + y2) / 2
        return {
            self.basename(): {
                "x": xc,
                "y": -yc,
                "width": x2 - x1,
                "height": y2 - y1
            }
        }


class SpineSkeleton:
    VERSION = "3.7.76-beta"

    def __init__(self, images, dir_name):
        self._images = images
        self.dir_name = dir_name

    def images(self):
        return [SpineImage(im) for im in self._images]

    def to_json(self):
        images = self.images()
        data = {
            "skeleton": {
                "spine": SpineSkeleton.VERSION
            },
            "bones": [
                {
                    "name": "root"
                }
            ],
            "slots": [
                im.to_slot() for im in images
            ],
            "skins": {
                "default": {
                    im.basename(): im.to_skin() for im in images
                }
            }
        }
        with open(os.path.join(self.dir_name, 'skeleton.json'), 'w') as f:
            json.dump(data, f)

    def to_png(self):
        for im in self._images:
            im.trim().to_png(os.path.join(self.dir_name, im.name()))


class NamedImage:
    def __init__(self, file_name):
        self.data = imageio.imread(file_name)
        self.file_name = file_name

    def name(self):
        return os.path.splitext(os.path.basename(self.file_name))[0]

    def trim(self):
        new = copy.copy(self)
        new.data = np.asarray(Image.fromarray(self.data).crop(self.bbox()))
        return new

    def bbox(self):
        return Image.fromarray(self.data[:, :, 3]).getbbox()

    def to_png(self, file_name):
        Image.fromarray(self.data).save(file_name + '.png')

    def empty(self):
        return not self.data[:, :, 3].any()


class AsepriteFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def layers(self):
        with tempfile.TemporaryDirectory() as dir_name:
            layer_file = os.path.join(dir_name, 'layers.txt')
            subprocess.call(['aseprite', '-b',
                             '--all-layers',
                             '--list-layers', self.file_path,
                             '--data', layer_file],
                            stdout=subprocess.DEVNULL)
            with open(layer_file, 'r') as f:
                def _get_name(layer):
                    return f"{layer.get('group', '')}-{layer['name']}"

                layers = [_get_name(l)
                          for l in json.load(f)['meta']['layers']
                          if 'opacity' in l]
                return list(reversed(layers))

    def images(self, tag):
        with tempfile.TemporaryDirectory() as dir_name:
            subprocess.call([
                'aseprite', '-b',
                '--all-layers',
                '--split-layers', self.file_path,
                '--filename-format',
                os.path.join(dir_name, '{tag}-{group}-{layer}.{extension}'),
                '--save-as', '.png'
            ])
            images = [NamedImage(os.path.join(dir_name, tag + '-' + layer + '.png'))
                      for layer in self.layers()]
            return [im for im in images if not im.empty()]


if __name__ == '__main__':
    src = sys.argv[1]
    tag = sys.argv[2]
    dst = sys.argv[3]

    ase = AsepriteFile(src)
    sk = SpineSkeleton(ase.images(tag), dst)
    sk.to_json()
    sk.to_png()
