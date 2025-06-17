import unittest
from types import NoneType

from lib.baseclass.api import LoginData
from lib.pakete.bestandspaket import VideoQuality, AudioQuality, SubtitleQuality
from providers import *

import warnings


class ProvidersTest(unittest.TestCase):
    def __init__(self, methodName='runTest', provider: BaseProvider = None):
        super().__init__(methodName=methodName)
        self.provider = provider

    @property
    def all_movies(self):
        return self.provider.get_all_movies()

    @property
    def all_episodes(self):
        return self.provider.get_all_episodes()

    def setUp(self):
        if self.provider is None: self.skipTest("Test Template")
        warnings.filterwarnings('ignore')

    def test_sammelpakete(self):
        self.assertIsInstance(self.all_movies, list)
        self.assertIsInstance(self.all_episodes, list)

        [self.assertTrue(m.valid) for m in self.all_movies]
        [self.assertTrue(e.valid) for e in self.all_episodes]

    def test_check_if_subscribed(self):
        self.assertIsInstance(self.provider.check_if_subscribed(), bool)

    def test_search_id(self):
        try:
            self.assertIsNotNone(self.provider.search_id('NON_VALID_ID'))
        except:
            pass

        self.assertIsInstance(self.provider.search_id(self.all_movies[0].id), (dict, NoneType))

    def test_get_manifest(self):
        if not self.provider.check_if_subscribed(): self.skipTest('Not subscribed.')

        movie = self.provider.get_downloader(self.all_movies[0])
        self.assertIsInstance(movie.manifest_url, str)
        self.assertTrue(movie.manifest_url)

    def test_drm(self):
        if not self.provider.check_if_subscribed(): self.skipTest('Not subscribed.')

        movie = None
        psshs = []
        for i in range(10):
            movie = self.provider.get_downloader(self.all_movies[i])
            movie.init()
            psshs = movie.get_psshs()
            if psshs:
                break

        if not psshs:
            self.skipTest('No psshs found.')

        drm_keys = movie.get_drm_keys()
        self.assertIsInstance(drm_keys, list)
        self.assertTrue(drm_keys)
        [self.assertIsInstance(k, str) for k in drm_keys]
        [self.assertTrue(k) for k in drm_keys]

    def test_stream_quality(self):
        if not self.provider.check_if_subscribed(): self.skipTest('Not subscribed.')

        movie = self.provider.get_downloader(self.all_movies[0])
        movie.init()

        video_quality = movie.get_video_qualities()
        self.assertIsInstance(video_quality, VideoQuality)
        self.assertTrue(video_quality.valid)

        audio_qualities = movie.get_audio_qualities()
        self.assertIsInstance(audio_qualities, list)
        [self.assertIsInstance(a, AudioQuality) for a in audio_qualities]
        [self.assertTrue(a.valid) for a in audio_qualities]

        subtitle_qualities = movie.get_subtitle_qualities()
        self.assertIsInstance(subtitle_qualities, list)
        [self.assertIsInstance(s, SubtitleQuality) for s in subtitle_qualities]
        [self.assertTrue(s.valid) for s in subtitle_qualities]

    def test_prep_request(self):
        test_kwargs = {'params': {'random': 1}, 'cookies': {'random': 2}, 'headers': {'random': 3}}
        no_input_auth = self.provider.api.prepare_auth()
        with_input_auth = self.provider.api.prepare_auth(**test_kwargs)

        no_input_auth['params'] = no_input_auth.get('params', {})
        no_input_auth['cookies'] = no_input_auth.get('cookies', {})
        no_input_auth['headers'] = no_input_auth.get('headers', {})

        no_input_auth['params'].update(test_kwargs['params'])
        no_input_auth['cookies'].update(test_kwargs['cookies'])
        no_input_auth['headers'].update(test_kwargs['headers'])

        self.assertEqual(no_input_auth['params'], with_input_auth['params'])
        self.assertEqual(no_input_auth['cookies'], with_input_auth['cookies'])
        self.assertEqual(no_input_auth['headers'], with_input_auth['headers'])

    def test_login(self):
        new_login_data = LoginData('test')
        self.assertNotEqual(self.provider.api.login_data.email, new_login_data.email)
        self.assertNotEqual(self.provider.api.login_data.password, new_login_data.password)

        self.assertIsNone(self.provider.api.login())
        self.assertTrue(self.provider.api.login_data.last_login_data)

        original_login_data = self.provider.api.login_data
        self.provider.api.login_data = new_login_data
        self.assertRaises(Exception, self.provider.api.login)
        self.provider.api.login_data = original_login_data


class ArdPlusTest(ProvidersTest):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName=methodName, provider=ArdProvider())


class CanalPlusTest(ProvidersTest):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName=methodName, provider=CanalPlusProvider())


class ParamountPlusTest(ProvidersTest):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName=methodName, provider=ParamountPlusProvider())


class AdnTest(ProvidersTest):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName=methodName, provider=AdnProvider())


class NetflixTest(ProvidersTest):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName=methodName, provider=NetflixProvider())


class HanimeTest(ProvidersTest):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName=methodName, provider=HanimeProvider())


if __name__ == '__main__':
    unittest.main()
