"""Stand-alone library that *only* needs numpy to convert sph files to wav files

Uses the standard-library's wave module to write the wav files
"""
import numpy

def parse_sph_header( fh ):
    """Read the file-format header for an sph file
    
    The SPH header-file is exactly 1024 bytes at the head of the file,
    there is a simple textual format which AFAIK is always ASCII, but 
    we allow here for latin1 encoding.  The format has a type declaration
    for each field and we only pay attention to fields for which we 
    have some understanding.
    
    returns dictionary describing the format such as::
    
        {
            'sample_rate':8000, 
            'channel_count':1, 
            'sample_byte_format': '01', # little-endian
            'sample_n_bytes':2, 
            'sample_sig_bits': 16, 
            'sample_coding': 'pcm', 
        }
    """
    file_format = {
        'sample_rate':8000, 
        'channel_count':1, 
        'sample_byte_format': '01', # little-endian
        'sample_n_bytes':2, 
        'sample_sig_bits': 16, 
        'sample_coding': 'pcm', 
    }
    end = b'end_head'
    for line in fh.read(1024).splitlines():
        if line.startswith(end):
            break 
        line = line.decode('latin-1')
        for key in file_format.keys():
            if line.startswith(key):
                _, format, value = line.split(None, 3)
                if format == '-i':
                    value = int(value, 10)
                file_format[key] = value 
    return file_format

class SPHFile( object ):
    """SPH data-file that can is read into RAM on access"""
    def __init__( self, filename ):
        self.filename = filename 
        self._rawbytes = None
    def open( self ):
        with open( self.filename, 'rb' ) as fh:
            self._format = format = parse_sph_header( fh )
            content = fh.read()
            if format['sample_n_bytes'] == 1:
                np_format = numpy.uint8
            elif format['sample_n_bytes'] == 2:
                np_format = numpy.int16
            elif format['sample_n_bytes'] == 4:
                np_format = numpy.int32
            else:
                raise RuntimeError( "Unrecognized byte count: %s", format['sample_n_bytes'] )
            remainder = len(content)%format['sample_n_bytes']
            if remainder:
                content = content[:-remainder]
            self._rawbytes = content
            self._content = numpy.fromstring(content,dtype=np_format)
            if self._format['sample_byte_format'] == '10':
                # deal with big-endian data-files as wav is going to expect little-endian
                self._content = self._content.byteswap()
        
    _format = _content = None
    @property
    def format( self ):
        if self._format is None:
            with open( self.filename, 'rb' ) as fh:
                self._format = parse_sph_header( fh )
        return self._format 
    @property
    def content( self ):
        if self._content is None:
            self.open()
        return self._content 
        
    def seconds_to_offset(self, seconds):
        """Calculate buffer offset in seconds (assumes interleaved channels)"""
        return int(seconds * self.format['sample_rate'] * self.format['channel_count'])
    def time_range(self, start=0, stop=None ):
        if stop is not None:
            return self.content[ self.seconds_to_offset(start):self.seconds_to_offset(stop) ]
        else:
            return self.content[ self.seconds_to_offset(start): ]
    
    def write_wav( self, filename, start=None, stop=None  ):
        """Write our audio buffer to given filename as a wave-file"""
        import wave
        with wave.open(filename,'wb') as fh:
            params = (
                self.format['channel_count'], 
                self.format['sample_n_bytes'], 
                self.format['sample_rate'],
                0, 
                'NONE', 'NONE'
            )
            fh.setparams(params)
            if start is not None or stop is not None:
                data = self.time_range( start, stop )
            else:
                data = self.content
            fh.writeframes( data.tostring() )
        return filename
    
def test():
    sph =SPHFile( '/var/datasets/TEDLIUM_release2/test/sph/JamesCameron_2010.sph' )
    sph.write_wav( 'test.wav', 111.29, 123.57 )
    print("test.wav should say: i had to create these images in my head you know we all did as kids having to read a book and through the author 's description put something on on the screen the movie screen in our heads and so my")

if __name__ == "__main__":
    test()
    
