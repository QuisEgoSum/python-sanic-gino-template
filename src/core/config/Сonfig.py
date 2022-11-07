from pydantic import Field

from src.core.config.project import root_dir, project_metadata
from src.core.validator import Schema


class Config(Schema, frozen=True):
    class Paths(Schema, frozen=True):
        root: str = root_dir

    class Server(Schema, frozen=True):

        class HttpServer(Schema, frozen=True):
            host: str = Field(min_length=1)
            port: int = Field(ge=1, le=65353)
            workers: int = Field(ge=1, le=124)

        http: HttpServer

    class Database(Schema, frozen=True):
        user: str = Field(min_length=1)
        password: str = Field(min_length=1)
        host: str = Field(min_length=1)
        port: int = Field(ge=1, le=65353)
        name: str = Field(min_length=1)

        @property
        def uri(self):
            return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'

    class Logger(Schema, frozen=True):
        destination: str = root_dir + '/logs'

    class Project(Schema, frozen=True):
        name: str = project_metadata.get('name')
        version: str = project_metadata.get('version')

    debug: bool
    paths: Paths = Paths()
    server: Server
    database: Database
    project: Project = Project()
    logger: Logger = Logger()
