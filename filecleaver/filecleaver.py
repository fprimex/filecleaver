class FileChunkReadError(Exception):
    def __init__(self, filename, error):
        self.filename = filename
        Exception.__init__(self,
            'Unable to access file to read chunk: {}\nError was: {}'.format(
                filename, error))


class FileChunk(object):
    def __init__(self, filename, start, end):
        self.__filename = filename
        self.__fp = None

        self.__start = start
        self.__end = end

        if(start > end):
            raise ValueError('end must be greater than start')

    def __iter__(self):
        while self.__fp.tell() < self.__end:
            yield self.__fp.readline()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return True

    def open(self, fp=None):
        # Whatever is passed in for fp should correspond to what was passed
        # in to cleavebytes, and should support most of the file methods like
        # close, read, readlines, etc.
        # Each Chunk probably needs to get its own unique, 'r' mode fp unless
        # you really know what you're doing and are very, very careful.
        if fp:
            self.__fp = fp
        else:
            try:
                self.__fp = open(self.__filename, 'rb')
            except (OSError, IOError) as e:
                raise FileChunkReadError(filename, e)

        self.__fp.seek(self.__start)
        return self

    def close(self):
        self.__fp.close()

    def getstart(self):
        return self.__start

    def getend(self):
        return self.__end

    def getfilename(self):
        return self.__filename

    start = property(getstart, None, None, 'Start of file chunk in bytes')
    end = property(getend, None, None, 'End of file chunk in bytes')
    filename = property(getfilename, None, None,
            'Name of file containing chunk')

    def seek(self, pos):
        if(pos < self.__start or pos > end):
            raise IOError('Invalid argument')

        self.__fp.seek(pos)

    def readline(self):
        return self.next()

    def readlines(self):
        return list(self.__iter__())

    def read(self):
        return self.__fp.read(self.__end - self.__fp.tell())


def cleavebytes(filename, chunksize, fp=None):
    if chunksize < 1:
        raise ValueError(
            'cannot cleave file into chunks smaller than 1 byte')

    # if a filepointer was provided, use that rather than using 'open'.
    # this gives us the ability to read a stream, zipfile, file from a
    # zipfile, etc, and give back a chunking configuration for that.
    # If this is done, then an fp will also need to be provided to each
    # FileChunk since it will not be able to use 'open' there either.
    if fp:
        close_fp = False
    else:
        fp = open(filename, 'rb')
        close_fp = True

    # seek in the file chunksize bytes, then read a line to get a
    # line ending
    pos = 0
    eof = False
    while not eof:
        prev_pos = pos
        fp.seek(chunksize, 1)

        if not fp.readline():
            fp.seek(0, 2)
            eof = True

        pos = fp.tell()
        yield FileChunk(filename, prev_pos, pos)

    if close_fp:
        fp.close()


def cleave(filename, chunks):
    if chunks < 1:
        raise ValueError('cannot cleave file into less than 1 chunk')

    import os
    size = os.path.getsize(filename)
    chunksize = size // chunks

    return cleavebytes(filename, chunksize)

