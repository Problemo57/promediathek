from lib.baseclass import BaseAPI, BaseProvider
from lib.pakete.sammelpaket import MovieSammelpaket, EpisodeSammelpaket, Sammelpaket
from lib.download_protocols import Dash
from lib.utils.networking import SafeHTTPResponse


class TemplateApi(BaseAPI):
    # TODO change TEMPLATE to provider name
    name = "TEMPLATE"

    def anon_login(self) -> None:
        # TODO optional if anon auth is required.
        self.login_data.last_anon_login_data = "ANON LOGIN DATA"
        raise NotImplementedError

    def login(self) -> None:
        # TODO implement login function and return True if successful.
        self.login_data.last_login_data = "LOGIN DATA"
        raise NotImplementedError

    def prepare_anon_auth(self, **kwargs) -> dict:
        """
        Prepares the anon request data e.g. Headers, Params, Cookies, etc. with the required anon auth data.
        :param kwargs: Optional request data.
        :return: The prepared request data as dict.
        """
        # TODO optional if anon auth is required.
        raise NotImplementedError

    def request_was_anon_authed(self, response: SafeHTTPResponse | dict) -> bool:
        """
        Determines if the request failed because of authentication.
        :param response: The response to check.
        :return: If True, call self._anon_login()
        """
        # TODO optional if anon auth is required.
        raise NotImplementedError

    def prepare_auth(self, **kwargs) -> dict:
        """
        Prepares the request data e.g. Headers, Params, Cookies, etc. with the required auth data.
        :param kwargs: Optional request data.
        :return: The prepared request data as dict.
        """
        # TODO
        raise NotImplementedError

    def request_was_authed(self, response: SafeHTTPResponse | dict) -> bool:
        """
        Determines if the request failed because of authentication.
        Use with auth_get() and auth_post()
        :param response: The response to check.
        :return: If True, call self._login()
        """
        # TODO
        raise NotImplementedError


class TemplateDownloadProtocol(Dash):
    def __init__(self, api: TemplateApi, sammelpaket: Sammelpaket):
        self.api = api
        super().__init__(sammelpaket=sammelpaket)

    def get_manifest_url(self) -> str:
        # TODO implement Function for getting the Dash/HLS manifest url.
        # TODO Optional set required headers/cookies.
        self.request_headers = {}
        self.request_cookies = {}

        raise NotImplementedError

    def _get_drm_keys(self, challenge: bytes | str) -> bytes:
        # TODO send challenge to provider and return response content
        url = 'https://provider/drm' + self.sammelpaket.id

        response = self.api.auth_post(url, data=challenge)
        return response.content


class TemplateProvider(BaseProvider):
    # TODO
    api = TemplateApi()

    def check_if_subscribed(self) -> bool:
        # TODO
        raise NotImplementedError

    def search(self, search_term: str) -> list[Sammelpaket]:
        # TODO: Optional for Speed
        return super().search(search_term)

    def get_all_movies(self) -> list[MovieSammelpaket]:
        # TODO
        movie_pakets = []

        for movie in []:
            movie_pakets.append(MovieSammelpaket(
                type="movie",
                provider=self.name,
                id=movie['id'],
                titel=movie['title'],
                description=movie['shortSynopsis'],
                movie_thumbnail_vertical=movie['poster_url'],
                movie_thumbnail_horizontal=movie['banner_url']
            ))

        return movie_pakets

    def get_all_episodes(self) -> list[EpisodeSammelpaket]:
        # TODO
        episode_pakets = []

        for series in []:
            for season in []:
                for episode in []:
                    episode_pakets.append(EpisodeSammelpaket(
                        type="episode",
                        provider=self.name,
                        id=episode['id'],
                        titel=episode['title'],
                        description=episode['description'],
                        series_thumbnail_vertical=episode['series_poster_url'],
                        series_thumbnail_horizontal=episode['series_banner_url'],
                        series_title=series['title'],
                        series_id=series['id'],
                        series_description=series['description'],
                        season_number=str(season['season_number']),
                        season_id=season['id'],
                        episode_number=str(episode['episode_number']),
                        episode_thumbnail_vertical=None,
                        episode_thumbnail_horizontal=None
                    ))

        return episode_pakets

    def get_downloader(self, sammelpaket: Sammelpaket) -> TemplateDownloadProtocol:
        return TemplateDownloadProtocol(api=self.api, sammelpaket=sammelpaket)


if __name__ == "__main__":
    pass
