from pathlib import Path

from core.management.commands.utils import Utils


class UserInterfaceBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self._command_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self._snippet_dir = self.command.snippet_dir

        self._widget_snippet = Path(f"{self._snippet_dir}/cubit/ui_widget.txt")
        self._widget_target = Path(f"{self.command.ui_dir}/widget.dart")

        self._font_snippet = Path(f"{self._snippet_dir}/ui_font.txt")
        self._font_target = Path(f"{self.command.ui_dir}/font.dart")

    def build(self):
        """
        build _summary_

        Raises
        ------
        e
            _description_
        """
        try:
            self._parser_widget()
            self._parser_font()
        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o build de UserInterfaceBuilder: {error}"
            )
            raise error

    def _parser_widget(self):
        try:
            if Utils.check_file_is_locked(str(self._widget_target)):
                return
            _content = Utils.get_snippet(str(self._widget_snippet))
            with open(self._widget_target, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o _parser_widget do UserInterfaceBuilder: {error}"
            )
            raise error

    def _parser_font(self):
        try:
            if Utils.check_file_is_locked(str(self._font_target)):
                return
            _content = Utils.get_snippet(str(self._font_snippet))
            with open(self._font_target, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o _parser_font do UserInterfaceBuilder: {error}"
            )
            raise error
