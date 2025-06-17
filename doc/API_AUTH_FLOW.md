# BaseApi - Flow
Um die Klasse BaseApi zu implementieren, müssen folgende Methoden implementiert werden:

    def login(self) -> bool:
        # TODO implement login function and return True if successful.
        self.login_data.last_login_data = "LOGIN DATA"
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

Der Ablauf eines Requests ist wie folgt:
1. Rufe prepare_auth() mit allen request infos auf, diese sollen mit den relevanten Authentifizierungsinformationen modifiziert werden und das angepasste dict soll zurückgeben werden.
2. Der Netzwerk request wird durchgeführt.
3. Die Antwort des request wird mit request_was_authed() darauf überprüft ob der request gescheitert ist wegen falscher Authentifizierung, falls ja wird login() aufgerufen und wieder bei 1. angefangen.
