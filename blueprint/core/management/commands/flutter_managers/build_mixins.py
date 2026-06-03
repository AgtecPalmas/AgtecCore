from pathlib import Path

from core.management.commands.utils import Utils


class MixinsClassBuilder:
    def __init__(self, command) -> None:
        self.command = command

    def build(self):
        try:
            self._build_modal_mixin()
            self._build_connection_mixin()
            self._build_message_mixin()
        except Exception as e:
            Utils.show_error(f"Erro ao executar o build de MixinsClassBuilder: {e}")
            return

    def _build_modal_mixin(self):
        _target_file = Path(f"{self.command.ui_dir}/modal_loading_mixin.dart")
        _snippet_file = Path(f"{self.command.snippet_dir}/loading_modal_mixin.txt")
        try:
            if Utils.check_file_is_locked(str(_target_file)):
                return
            _content = Utils.get_snippet(str(_snippet_file))
            with open(_target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_error(
                f"Erro ao executar o _build_modal_mixin de MixinsClassBuilder: {e}"
            )
            return

    def _build_message_mixin(self):
        _target_file = Path(f"{self.command.ui_dir}/message_mixin.dart")
        _snippet_file = Path(f"{self.command.snippet_dir}/message_mixin.txt")
        try:
            if Utils.check_file_is_locked(str(_target_file)):
                return
            _content = Utils.get_snippet(str(_snippet_file))
            with open(_target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_error(
                f"Erro ao executar o _build_message_mixin de MixinsClassBuilder: {e}"
            )
            return

    def _build_connection_mixin(self):
        _target_file = Path(f"{self.command.ui_dir}/connection_mixin.dart")
        _snippet_file = Path(f"{self.command.snippet_dir}/connection_mixin.txt")
        try:
            if Utils.check_file_is_locked(str(_target_file)):
                return
            _content = Utils.get_snippet(str(_snippet_file))
            with open(_target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_error(
                f"Erro ao executar o _build_connection_mixin de MixinsClassBuilder: {e}"
            )
            return
