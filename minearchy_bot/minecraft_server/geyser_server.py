from __future__ import annotations

__all__ = ("GeyserServer",)

from dataclasses import dataclass
from typing import TYPE_CHECKING

from mcstatus import JavaServer

if TYPE_CHECKING:
    from mcstatus.pinger import PingResponse


@dataclass
class ServerInfo:
    ip: str
    port: int


class GeyserServer:
    def __init__(
        self,
        *,
        java_ip: str,
        java_port: int = 25565,
        bedrock_ip: str,
        bedrock_port: int = 19132,
    ) -> None:
        self.__server = JavaServer.lookup(java_ip, java_port)
        self.java = ServerInfo(java_ip, java_port)
        self.bedrock = ServerInfo(bedrock_ip, bedrock_port)

    async def status(self) -> PingResponse:
        return await self.__server.async_status()
