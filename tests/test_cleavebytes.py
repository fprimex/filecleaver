import os

from filecleaver import cleave, cleavebytes

from cleave_common import compare, remove

class TestCleaveBytes(object):
    def setup(self):
        self.src_filename = os.path.join('tests', 'words')
        self.dst_basenames = []

        size = os.path.getsize(self.src_filename)
        chunks = 8
        self.b = size // chunks

        self.readers = list(cleavebytes(self.src_filename, self.b))
        self.n = len(self.readers)

    def teardown(self):
        try:
            remove(self.dst_basenames, self.n)
        except (OSError, IOError) as e:
            raise e
            #pass

    def test_cleavebytes_iter(self):
        basename = 'cleavebytes_iter'
        self.dst_basenames.append(basename)

        for i, reader in enumerate(self.readers):
            with reader.open() as src, open(basename + '{:02}'.format(i), 'wb') as dst:
                for line in src:
                    dst.write(line)

        assert compare(self.src_filename, basename, self.n)

    def test_cleavebytes_readlines(self):
        basename = 'cleavebytes_readlines'
        self.dst_basenames.append(basename)

        for i, reader in enumerate(self.readers):
            with reader.open() as src, open(basename + '{:02}'.format(i), 'wb') as dst:
                dst.writelines(src.readlines())

        assert compare(self.src_filename, basename, self.n)

    def test_cleavebytes_read(self):
        basename = 'cleavebytes_read'
        self.dst_basenames.append(basename)

        for i, reader in enumerate(self.readers):
            with reader.open() as src, open(basename + '{:02}'.format(i), 'wb') as dst:
                dst.write(src.read())

        assert compare(self.src_filename, basename, self.n)

