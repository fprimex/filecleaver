from __future__ import print_function

import os.path

from filecleaver import cleave, cleavebytes

from cleave_common import compare, remove

class TestCleave(object):
    def setup(self):
        self.src_filename = os.path.join('tests', 'words')
        self.dst_basenames = []
        self.n = 10
        self.readers = cleave(self.src_filename, self.n)

    def teardown(self):
        try:
            remove(self.dst_basenames, self.n)
        except (OSError, IOError) as e:
            raise e
            #pass

    def test_cleave_iter(self):
        basename = 'cleave_iter'
        self.dst_basenames.append(basename)

        for i, reader in enumerate(self.readers):
            with reader.open() as src, open(basename + '{:02}'.format(i), 'wb') as dst:
                for line in src:
                    dst.write(line)

        assert compare(self.src_filename, basename, self.n)

    def test_cleave_readlines(self):
        basename = 'cleave_readlines'
        self.dst_basenames.append(basename)

        for i, reader in enumerate(self.readers):
            with reader.open() as src, open(basename + '{:02}'.format(i), 'wb') as dst:
                dst.writelines(src.readlines())

        assert compare(self.src_filename, basename, self.n)

    def test_cleave_read(self):
        basename = 'cleave_read'
        self.dst_basenames.append(basename)

        for i, reader in enumerate(self.readers):
            with reader.open() as src, open(basename + '{:02}'.format(i), 'wb') as dst:
                print('Chunk #{} was {} bytes'.format(i, src.end - src.start))
                dst.write(src.read())

        assert compare(self.src_filename, basename, self.n)

