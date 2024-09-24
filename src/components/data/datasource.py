import abc


class DataSource:
    """
    DataSource class that defines the guidelines on how to provide data.

    -> Data must be in strings, preferable there is some adjusted logic where we have "chunks" of strings that we can easily manage
        for the AI models themselves.
        For pdfs this means page per page, for legal texts this would be defined as article by article?

    When the content property is called, users should be able to simply get a list of str[]
    """

    def __init__(self, filetype: str, file: bytes):
        self.filetype = filetype
        self.file = file

    def __byte_pdf_logic(self) -> list[str]:
        pass

    @property
    def content(self) -> list[str]:
        match self.filetype.lower():  # ideally we use enums here!
            case "byte_pdf":
                return self.__byte_pdf_logic()
            case _:
                raise ValueError("unsupported filetype")
