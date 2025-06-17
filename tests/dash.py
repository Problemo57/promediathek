import unittest
from pathlib import Path

from lib.baseclass.audio import BaseAudio
from lib.baseclass.subtitle import BaseSubtitle
from lib.baseclass.video import BaseVideo
from lib.download_protocols import Dash, HLS
from lib.pakete.sammelpaket import Sammelpaket


class DashCase(unittest.TestCase):

    def setUp(self):
        sp = Sammelpaket(
            type="movie",
            provider="test",
            id="dextertest",
            titel="dexter test",
            description=""
        )
        dash = Dash(sp)
        dash._manifest_url = "file://" + str((Path(__file__).parent / "dash_manifests/dexter.mpd").absolute())
        dash.init()
        self.download_protocol = dash

    def test_dexter(self):
        self.assertIsInstance(self.download_protocol.video, BaseVideo)
        [self.assertIsInstance(audio, BaseAudio) for audio in self.download_protocol.audios]
        [self.assertIsInstance(subtitle, BaseSubtitle) for subtitle in self.download_protocol.subtitles]

        self.assertTrue(self.download_protocol.video.get_quality().valid)
        [self.assertTrue(audio.get_quality().valid) for audio in self.download_protocol.audios]
        [self.assertTrue(subtitle.get_quality().valid) for subtitle in self.download_protocol.subtitles]

        audio_languages = {audio.language for audio in self.download_protocol.audios}
        self.assertEqual(len(audio_languages), len(self.download_protocol.audios))

        normal_subtitles = [subtitle for subtitle in self.download_protocol.subtitles if not subtitle.forced]
        subtitle_languages = {subtitle.language for subtitle in normal_subtitles}
        self.assertEqual(len(normal_subtitles), len(subtitle_languages))

        forced_subtitles = [subtitle for subtitle in self.download_protocol.subtitles if subtitle.forced]
        forced_subtitle_languages = {subtitle.language for subtitle in forced_subtitles}
        self.assertEqual(len(forced_subtitles), len(forced_subtitle_languages))


class HLSText(DashCase):
    def setUp(self):
        sp = Sammelpaket(
            type="movie",
            provider="test",
            id="dextertest",
            titel="dexter test",
            description=""
        )
        hls = HLS(sp)
        hls._manifest_url = "file://" + str((Path(__file__).parent / "dash_manifests/dexter.m3u8").absolute())
        hls.init()
        self.download_protocol = hls


if __name__ == '__main__':
    unittest.main()
