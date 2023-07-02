import math


class GridRef:
    letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    chunks_per_region = 156250.0

    @staticmethod
    def mc_to_grid_ref(region_x: float, region_z: float) -> str:
        chunk_x = region_x * 32
        chunk_z = region_z * 32

        if chunk_x >= 0:
            letter_x_i = int(math.floor(chunk_x / GridRef.chunks_per_region))
            if letter_x_i > 11:
                raise ValueError('X coordinate out of range')
            letter_x = str(GridRef.letters[letter_x_i])
        else:
            letter_x_i = 11 - int(math.floor(chunk_x / GridRef.chunks_per_region))
            if letter_x_i > 23:
                raise ValueError('X coordinate out of range')
            letter_x = str(GridRef.letters[letter_x_i])

        if chunk_z >= 0:
            letter_z_i = int(math.floor(chunk_z / GridRef.chunks_per_region))
            if letter_z_i > 11:
                raise ValueError('Z coordinate out of range')
            letter_z = str(GridRef.letters[letter_z_i])
        else:
            letter_z_i = 11 - int(math.floor(chunk_z / GridRef.chunks_per_region))
            if letter_z_i > 23:
                raise ValueError('Z coordinates out of range')
            letter_z = str(GridRef.letters[letter_z_i])

        start_coord_x = letter_x_i * GridRef.chunks_per_region
        if letter_x_i > 11:
            start_coord_x = (letter_x_i - 12) * GridRef.chunks_per_region

        start_coord_z = letter_z_i * GridRef.chunks_per_region
        if letter_z_i > 11:
            start_coord_z = (letter_z_i - 12) * GridRef.chunks_per_region

        new_region_x = math.floor(chunk_x / 32)
        if new_region_x < 0:
            new_region_x += 1

        new_region_z = math.floor(chunk_z / 32)
        if new_region_z < 0:
            new_region_z += 1

        new_coord_x = abs(new_region_x) - math.floor(float(start_coord_x / 32)) + 1111
        new_coord_z = abs(new_region_z) - math.floor(float(start_coord_z / 32)) + 1111

        return '{}{} {} {}'.format(letter_x, letter_z, new_coord_x, new_coord_z)

    @staticmethod
    def grid_ref_to_mc(grid_ref: str):
        grid_ref = grid_ref.replace(' ', '')
        if len(grid_ref) != 10:
            raise ValueError('Grid reference is of invalid length')

        if not grid_ref[0].isalpha() or not grid_ref[1].isalpha():
            raise ValueError('First two characters must be letters')

        try:
            x = int(grid_ref[2:6])
        except ValueError:
            raise ValueError('First part must be a number')

        try:
            z = int(grid_ref[6:10])
        except ValueError:
            raise ValueError('Second part must be a number')

        letter_x_i = GridRef.letters.index(grid_ref[0])
        letter_z_i = GridRef.letters.index(grid_ref[1])

        start_coord_x = letter_x_i * GridRef.chunks_per_region
        if letter_x_i > 11:
            start_coord_x = (letter_x_i - 12) * GridRef.chunks_per_region

        start_coord_z = letter_z_i * GridRef.chunks_per_region
        if letter_z_i > 11:
            start_coord_z = (letter_z_i - 12) * GridRef.chunks_per_region

        region_x = int(math.floor(float(start_coord_x / 32.0))) + (x - 1111)
        region_z = int(math.floor(float(start_coord_z / 32.0))) + (z - 1111)

        if letter_x_i > 11:
            region_x = -region_x - 1

        if letter_z_i > 11:
            region_z = -region_z - 1

        return region_x, region_z
