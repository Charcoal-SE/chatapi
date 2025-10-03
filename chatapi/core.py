from typing import Literal, Callable, Any
from types import SimpleNamespace
from requests import Response
from threading import Thread
from random import randint
from websocket import WebSocketApp
from rich.console import Console
from rich.markdown import Markdown

Host = Literal["stackexchange.com", "meta.stackexchange.com", "stackoverflow.com"]
console = Console()


def send_message(room: int, server: Host, msg: str) -> None:
    print(f"[API] {room}@{server}: ", end="")
    console.print(Markdown(msg))


def new_id() -> int:
    return randint(1000, 100000)


class User:
    def __init__(self) -> None:
        self.name = "cocomac"
        self.id = new_id()


class MessageOwner:
    def __init__(self) -> None:
        self.id: int = -1
        self.name: str = "cocomac"
        # TODO: While everyone shouldn't be a mod, it makes testing easier
        self.is_moderator = True


class Client:
    # **_?
    def get_message(self, msg_id: int) -> "Message":
        # presumably this gets a message by its ID?
        return Message()

    def __init__(self, host: Host = "stackexchange.com") -> None:
        self.host: Host = host
        self._br = SimpleNamespace(user_id=-2)

    def get_room(self, roomid: int) -> "Room":
        return Room(room_id=roomid)

    def get_me(self) -> User:
        return User()

    def get_user(self, _user_id: int) -> User:
        return User()

    def _do_action_despite_throttling(
        self, data: tuple[Literal["send"], int, str]
    ) -> None | Response:
        assert data[0] == "send"
        send_message(data[1], self.host, data[2])

        def fake_json() -> dict[Any, Any]:
            return {}

        res = Response()
        res.json = fake_json  # type: ignore[method-assign,assignment]
        return res


class MessagePosted:
    def __init__(self, text: str) -> None:
        self.message = Message()
        self.message.content = text
        self.message.content_source = text
        self.data: dict = {}  # type: ignore


class MessageEdited:
    def __init__(self) -> None:
        self.message = Message()
        self.data: dict = {}  # type: ignore


class Message:
    def __init__(self) -> None:
        self.id = new_id()
        self.data: dict = {}  # type: ignore
        self.room = Room(141239)
        self.owner: MessageOwner = MessageOwner()
        self.parent: Message = Message()  # TODO: what should this do?
        self.content_source: str = ""
        """`content_source` is the Markdown. That matters for thigns like regular expressions,
        where the content can have characters which would be recognized as Markdown and changed.
        ~ Makyen (https://chat.stackexchange.com/transcript/message/54465303)
        """
        self.content: str = ""
        """`content` is what's displayed in chat and includes having been processed from Markdown
        into HTML. ~ Makyen (https://chat.stackexchange.com/transcript/message/54465303)"""
        self.text_content: str = self.content
        self._client = Client()


class Room:
    def __init__(self, room_id: int) -> None:
        self._client = Client()
        self.last_activity = None
        self.room_id: int = room_id

    def watch_socket(
        self, action: Callable[[MessagePosted | MessageEdited, Client], None]
    ) -> None:
        def msg_handler(_: Any, msg: str) -> None:
            action(MessagePosted(msg), self._client)

        def ws_err_handler(_: Any, ex: Exception) -> None:
            raise ex

        def on_close_handler(*_: Any) -> None:
            raise ConnectionError("Chat websocket closed")

        Thread(
            target=WebSocketApp(
                "ws://127.0.0.1:8080",
                on_message=msg_handler,
                on_error=ws_err_handler,
                on_close=on_close_handler,
            ).run_forever,
            name="ChatSocket",
        ).start()

    def get_current_user_ids(self) -> list[int]:
        """Return a list of user IDs in the room"""
        return [new_id() for _ in range(10)]

    def join(self) -> None:
        pass
