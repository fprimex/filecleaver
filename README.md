# FileCleaver

Cleave (split) files (and streams, etc) into chunks.

## Installing

Should work with Python 2 and 3.

```
pip install filecleaver
```

You may wish to use `easy_install` instead of `pip`, and/or use a virtualenv.

## What is this?

### Grep, awk, split... MapReduce?

The motivation for this module came out of a job interview question that dug
deep in my mind like a splinter. First, I was asked how I would retrieve
certain information from a certain kind of text file format. Easy enough; I am
quite adept at shell scripting. Some grep and awk and it’s no problem.

Next, I was asked what if the file was very large, then what? I gave a one word
response, initially, of “MapReduce”, and added “you know, multiple threads or
processes or whatever.” No problem!

But, there is kind of a problem. Splitting a file on disk to feed into a
MapReduce style of coding could be nearly as challenging and resource consuming
as the problem itself. There isn’t a UNIX utility that will efficiently split a
file for you (and I love shell scripting, which is why I was so interested in
this), at least not on line boundaries that other utilities could then read and
make sense out of. If you look at `split(1)`, you’ll see options for splitting
a file based on a number of lines, but this actually starts at the beginning of
the file, reads that number of lines, and then writes a chunk, and repeats.
You’d be better off doing your processing while that line-by-line read was
happening.

So, what we need is a fast way to take a file off disk, chunk it up, and send
the bits to different processes. The split doesn’t need to be exact, just close
enough that all processes are doing similar amounts of meaningful work.

### Seeking and finding

The fastest way to move through files is to forget about line boundaries and
just move the file pointer any number of bytes forward. If you then just read
to the end of the line that you land in the middle of, you’ve found the nearest
next line ending.

This is nothing special. I am betting that this strategy has been repeated
countless times in every existing programming language that has touched
parallel storage. I am just interested in seeing an actual, working
implementation in Python to finish answering the interview question thoroughly
(even though I got the job already).

This is what filecleaver does. You can decide you want N chunks, or you can ask
for chunks of M bytes. Fileclever then seeks in your file (or stream or
whatever) and hands you back a list of easy to use file-like objects called
FileChunks. There are many utilities that do this kind of work, including
`split(1)`, however the special thing about filecleaver is that you get chunks
back on line boundaries quickly that will be approximately the size requested.

Whether this is actually any faster than just reading the file in one process
through one time depends on your storage hardware probably.

## Examples

Split a file into 10 chunks:

    from __future__ import print_function
    from filecleaver import cleave

    filename = 'words'
    readers = cleave(filename, 10)

    for i, reader in enumerate(readers):
        with reader.open() as src, open('out{:02}'.format(i), 'wb') as dst:
            print('Chunk #{} was {} bytes'.format(i, src.end - src.start))
            dst.write(src.read())

Or you can use `readline`, `readlines`, or use the FileChunk object as an
iterator:

    for i, reader in enumerate(readers):
        with reader.open() as src, open(‘out{:02}’.format(i), ‘wb’) as dst:
            for line in src:
                dst.write(line)

    for i, reader in enumerate(readers):
        with reader.open() as src, open(‘out{:02}’.format(i), ‘wb’) as dst:
            dst.writelines(src.readlines())

Split a file into chunks of size 109088170 bytes or larger (up to next line
ending):

    from __future__ import print_function
    from filecleaver import cleavebytes

    filename = 'words'
    readers = cleavebytes(filename, 109088170)

    for i, reader in enumerate(readers):
        with reader.open() as src, open('out{:02}'.format(i), 'wb') as dst:
            print('Chunk #{} was {} bytes'.format(i, src.end - src.start))
            dst.write(src.read())

Split a file into chunks and then process each chunk with multiprocessing:

    from __future__ import print_function

    import multiprocessing

    from filecleaver import cleavebytes

    def writechunk(i, reader):
        with reader.open() as src, open('out{}'.format(i), 'wb') as dst:
            dst.write(src.read())
            return 'Chunk #{} was {} bytes'.format(i, src.end - src.start)

    def writechunk_cb(result):
        print(result)

    filename = 'words'
    readers = cleavebytes(filename, 109088170)
    tasks = []
    pool = multiprocessing.Pool()

    for i, reader in enumerate(readers):
        tasks.append((i, reader))

    for task in tasks:
        pool.apply_async(writechunk, args=task, callback=writechunk_cb)

    pool.close()
    pool.join()

Using `.read()` is definitely the fastest way to go if you’re just reading
chunks and not processing each line. So, one alternative usage of filecleaver
would be to easily iterate over file chunks that are close to the size that you
want to consume in each iteration. You can, of course, do this with the normal
file API, seek, and read, all by yourself, but maybe you’ll like using this
class to get it done since it makes things easy.

