import os

from PIL import Image

from models.tilestitchargs import TileStitchArgs


class Map:
    @staticmethod
    def stitch(tiles_dir: str, output_dir: str, args: TileStitchArgs, progress_callback=None):
        tiles_x = ((args.to_x - args.from_x) / args.diff + 1)
        tiles_y = ((args.to_y - args.from_y) / args.diff + 1)

        width = tiles_x * args.tile_width
        height = tiles_y * args.tile_height
        total = tiles_x * tiles_y

        img = Image.new(mode='RGB', size=(int(width), int(height)))
        i = 0
        for x in range(args.from_x, args.to_x + 1, args.diff):
            for y in range(args.from_y, args.to_y + 1, args.diff):
                i += 1
                if progress_callback is not None:
                    progress_callback('Stitching ({} of {})'.format(i, int(total)), i, total)

                img_x = ((x - args.from_x) / args.diff) * args.tile_width
                img_y = ((y - args.from_y) / args.diff) * args.tile_height

                tile = Image.open(os.path.join(tiles_dir, '{}_{}.jpg'.format(x, y)))
                tile_img = tile.copy()
                img.paste(tile_img, (int(img_x), int(height - img_y - args.tile_height)))

        img.save(os.path.join(output_dir, 'map.png'))
