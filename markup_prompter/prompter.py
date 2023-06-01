"""Dictionary module"""

import dataclasses
import glob
from typing import Iterable, TypedDict

import marko


@dataclasses.dataclass(frozen=True)
class ChatMessage:
    """OpenAI ChatCompletion message."""

    content: str
    title: str | None
    role: str | None


class ChatGPTMessage(TypedDict):
    """Schema of ChatGPT messages."""

    role: str
    content: str


def to_chatgpt(program: Iterable[ChatMessage]) -> list[ChatGPTMessage]:
    """Convert the message to the ChatGPT input format.

    Returns:
        The dict of contents.
    """

    def convert(message: ChatMessage) -> ChatGPTMessage:
        role = message.role if message.role is not None else "user"
        content = (
            f"[{message.title}]\n{message.content}\n[/{message.title}]\n"
            if message.title is not None
            else message.content + "\n"
        )
        return {"role": role, "content": content}

    return [convert(m) for m in program]


class Dictionary:
    """Dictionary."""

    _messages: dict[str, str]

    def __init__(self, messages: dict[str, str]) -> None:
        """Initializer.

        Args:
            messages: dict of message name and contents.
        """
        self._messages = messages

    def __call__(
        self, path: str, title: str | None = None, role: str | None = None
    ) -> ChatMessage:
        """Generates a chat message.

        Args:
            path: Path to the message stored in the dictionary.
            title: Title of the message, or None to ignore the title tag.
            role: Role of the message, or None to use the default.

        Returns:
            A chat message.
        """
        return ChatMessage(content=self._messages[path], title=title, role=role)

    @staticmethod
    def parse_document(path: str) -> dict[str, str]:
        """Parses the session document file.

        Args:
            path: Path to the file.

        Returns:
            dict of containing messages: {title: content}
        """
        with open(path) as fp:
            doc = marko.parser.Parser().parse(fp.read())

        if not isinstance(doc, marko.block.Document):
            raise ValueError("Markdown parser didn't return a single document.")

        # Extract all title/content pairs formed as follows:
        #
        # # {title}
        # (anything else)
        # ```
        # {content}
        # ```
        # (anything else)

        result: dict[str, str] = {}
        current_title: str = ""

        for elm in doc.children:
            if isinstance(elm, marko.block.Heading) and elm.level == 1:
                current_title = elm.children[0].children.strip()
            elif isinstance(elm, marko.block.FencedCode):
                result[current_title] = elm.children[0].children.strip()

        return result

    @staticmethod
    def load(prefix: str) -> "Dictionary":
        """Loads messages from a directory.

        Args:
            prefix: Directory prefix to search.
        """
        if not prefix.endswith("/"):
            prefix += "/"

        extension = ".md"

        # {path: message}
        messages: dict[str, str] = {}

        for filename in glob.iglob(prefix + "**"):
            if not filename.startswith(prefix):
                # prefix may contain some wildcards.
                raise ValueError("prefix doesn't support wildcards.")
            if not filename.endswith(extension):
                continue

            shortname = filename[len(prefix) : -len(extension)]
            file_messages = Dictionary.parse_document(filename)
            messages.update(
                {
                    f"{shortname}:{title}": content
                    for title, content in file_messages.items()
                }
            )

        return Dictionary(messages)
