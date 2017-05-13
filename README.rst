sphfile
=======

.. image:: https://img.shields.io/pypi/v/sphfile.svg
    :target: https://pypi.python.org/pypi/sphfile
    :alt: Latest PyPI version

Numpy-based NIST SPH audio-file reader

Usage
-----

.. code::python

    from sphfile import SPHFile
    sph =SPHFile( '/var/datasets/TEDLIUM_release2/test/sph/JamesCameron_2010.sph' )
    print( sph.format )
    # write out a wav file with content from 111.29 to 123.57 seconds
    sph.write_wav( 'test.wav', 111.29, 123.57 )

Requirements
------------

* numpy

Licence
-------

    MIT

Authors
-------

`sphfile` was written by `Mike C. Fletcher <mcfletch@vrplumber.com>`_.
