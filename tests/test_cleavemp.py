from __future__ import print_function

import os
import multiprocessing

from filecleaver import cleave

from cleave_common import compare, remove

def writechunk(basename, i, reader):
    with reader.open() as src, open(basename + '{:02}'.format(i), 'wb') as dst:
        dst.write(src.read())
        return 'Chunk #{} was {} bytes'.format(i, src.end - src.start)

def writechunk_cb(result):
    print(result)

class TestCleaveMP(object):
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

    def test_cleave_mp(self):
        tasks = []
        pool = multiprocessing.Pool()

        basename = 'cleave_mp'
        self.dst_basenames.append(basename)

        for i, reader in enumerate(self.readers):
            tasks.append((basename, i, reader))

        for task in tasks:
            pool.apply_async(writechunk, args=task, callback=writechunk_cb)

        pool.close()
        pool.join()

        assert compare(self.src_filename, basename, self.n)

