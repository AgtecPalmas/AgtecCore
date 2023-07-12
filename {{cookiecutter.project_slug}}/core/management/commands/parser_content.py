class ParserContent:
    """Classe responsável para realizar o parser dos dados de modelo da classe Django para os
    arquivos tando do projeto Django como do projeto Flutter
    """

    def __init__(self, keys: list, contents: list, snippet: str):
        super().__init__()
        self.snippet = snippet
        self.keys = keys
        self.contents = contents

    def replace(self) -> str:
        """Método responsável por substituir as chaves contidas nos arquivos de snippet pelos
        dados contidos no models

        Returns:
            str: String para ser salva nos arquivos gerados no projeto Django e Flutter.
        """
        try:
            if (
                len(self.keys) == 0
                or len(self.contents) == 0
                or len(self.snippet.strip()) == 0
            ):
                raise Exception(
                    "It is necessary to inform the keys, contents and snippet values, and they cannot be white."
                )
            if len(self.keys) != len(self.contents):
                raise Exception(
                    "Size of keys and contents attributes must be the same."
                )
            for index, key in enumerate(self.keys):
                self.snippet = self.snippet.replace(key, self.contents[index])
            return self.snippet.strip()
        except Exception as error:
            return f"\nError occurred: \n    {error}.\n"
