from pydantic import BaseModel

from microstack.docker.enums import NetworkDrivers


class Network(BaseModel):
    id_: str
    name: str
    driver: NetworkDrivers
    scope: str  # todo update this with an enum
