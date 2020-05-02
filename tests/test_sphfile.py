import unittest, pytest, os, glob
from sphfile import sphfile
import io

HERE = os.path.dirname(os.path.abspath(__file__))
CAMERON_SAMPLE = os.path.join(HERE, 'JamesCameron_2010.sph')


class TestSPHFile(unittest.TestCase):

    pytest.mark.skipif(
        not os.path.exists(CAMERON_SAMPLE),
        reason='Missing James Cameron Sample from TEDLium',
    )
    def test_extract(self):
        sph = sphfile.SPHFile(CAMERON_SAMPLE)
        target = CAMERON_SAMPLE[:-4]+'-extract.wav'
        sph.write_wav(target, 111.29, 123.57)
        print(
            "%s should say:\ni had to create these images in my head you know we all did as kids having to read a book and through the author 's description put something on on the screen the movie screen in our heads and so my"%(
                target,
            )
        )
        assert os.stat(target).st_size == 393004

    def test_format(self):
        for filename in glob.glob(os.path.join(HERE, '*.sph'),):
            sph = sphfile.SPHFile(filename)
            assert sph.format
            for key in [
                'sample_rate',
                'channel_count',
                'sample_byte_format',  # little-endian
                'sample_n_bytes',
                'sample_sig_bits',
                'sample_coding',
            ]:
                assert key in sph.format, sph.format
    
    def test_parse_bad_names(self):
        """Test header parsing ignores invalid type names"""
        for header,expected in [
            (
                '''NIST_1A
   1024
sample_count -i 16892238
sample_n_bytes -i 2
channel_count -i 1
_this_and_that -s4 that
this__and -i 3
this__ -i 3
sample_byte_format -s2 10
sample_rate -i 16000
sample_coding -s3 pcm
end_head
''',
                {
                    'sample_count':16892238,
                    'sample_n_bytes':2,
                    'sample_sig_bits': 16,
                    'channel_count': 1,
                    'sample_byte_format': '10',
                    'sample_rate': 16000,
                    'sample_coding': 'pcm',
                }
            )
        ]:
            format = sphfile.parse_sph_header(io.BytesIO(header.encode('ascii')))
            assert format == expected, (header,format)
