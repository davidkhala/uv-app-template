import unittest

from testcontainers.core.container import DockerContainer  # noqa: F401
from testcontainers.core.wait_strategies import LogMessageWaitStrategy
from testcontainers.core.image import DockerImage
from pathlib import Path
import requests


class AppContainer(DockerContainer):

    def __init__(self, image: str, PORT: int, **kwargs):
        super().__init__(image, **kwargs)
        self.PORT = PORT
        self.with_exposed_ports(PORT)
        self.waiting_for(LogMessageWaitStrategy("Application startup complete."))

    def with_env_dict(self, envs: dict):
        for k, v in envs.items():
            self.with_env(k, v)

    @property
    def exposed_port(self) -> int:
        return self.get_exposed_port(self.PORT)

    @property
    def base_url(self) -> str:
        return f"http://localhost:{self.exposed_port}"


class ContainerTestCase(unittest.TestCase):

    def setUp(self):
        PORT = 8000
        self.image = DockerImage(
            path=Path(__file__).parent.parent,  # Dockerfile 所在目录
        ).build()

        self.container = AppContainer(self.image.short_id, PORT)
        self.container.with_env("PORT", str(PORT))
        self.container.start()

    def tearDown(self):
        self.container.stop()
        self.image.remove()

    def test_fastapi_health(self):
        resp = requests.get(f"{self.container.base_url}/openapi.json")
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
