sphfile
=======

.. image:: https://img.shields.io/pypi/v/sphfile.svg
    :target: https://pypi.python.org/pypi/sphfile
    :alt: Latest PyPI version

Numpy-based NIST SPH audio-file reader. This is for use 
with NIST SPH audio-files, the most likely use being 
extracting the TEDLIUM_release2 audio into formats that
standard tools can easily process.

Note that this library doesn't require any external tools
such as `vox` or `gstreamer`. It just loads the data into a
numpy array and then lets you dump it back out to wave 
files.

Usage
-----

.. code:: python

    from sphfile import SPHFile
    sph =SPHFile( 
        'TEDLIUM_release2/test/sph/JamesCameron_2010.sph' 
    )
    # Note that the following loads the whole file into ram
    print( sph.format )
    # write out a wav file with content from 111.29 to 123.57 seconds
    sph.write_wav( 'test.wav', 111.29, 123.57 )

Requirements
------------

* numpy

Licence
-------

    MIT License (c) 2017 Mike C. Fletcher

Authors
-------

`sphfile` was written by `Mike C. Fletcher <mcfletch@vrplumber.com>`_.
