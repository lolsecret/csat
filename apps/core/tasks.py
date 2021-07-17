from celery import Task
from typing import Dict, Optional, Tuple, Type
from requests.exceptions import ConnectionError, HTTPError, Timeout
import requests


class BaseNotifyTask(Task):
    autoretry_for: Tuple[Type[Exception], ...] = (Timeout, HTTPError, ConnectionError)
    retry_kwargs: dict = {"max_retries": 5}
    timeout: tuple = (1, 5)
    default_retry_delay: int = 1
    ignore_result = True
    headers: Optional[Dict[str, str]] = None
    auth: Optional[Tuple[str, str]] = None
    _session = None

    @property
    def session(self):
        if not self._session:
            self.__session = requests.Session()
            self.__session.verify = False
            self.__session.auth = self.auth
            if self.headers:
                self.__session.headers = self.headers  # type:ignore
        return self.__session