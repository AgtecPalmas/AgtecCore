"""
Build para gerenciar a cópia do core do projeto Flutter Web

Aqui será feita a copia pura, sem necessidade de mapear as classes
do projeto Django

"""
from pathlib import Path

from base.settings import FLUTTER_APPS_WEB
from core.management.commands.utils import Utils


class AppsWebInjectMenuItensBuilder:
    def __init__(self, command, flutter_project) -> None:
        self.command = command
        self.flutter_project = flutter_project
        self.flutter_web_dir = self.command.flutter_dir

    def build(self):
        from core.management.commands.flutter import AppModel
        """
        build _summary_
        """
        try:
            _list_menu_itens = ""
            # Executando o looping pelas apps do flutter
            for app in FLUTTER_APPS_WEB:
                # Pegando a app
                _app = AppModel(self.flutter_project, app)
                # Percorrendo os models de cada app
                for model in _app.models:
                    if len(model) < 2:
                        continue
                    _title = model[1]
                    _path = model[2]
                    _go_path = f"{{context.go('/{model[2]}');}}"
                    _comando = f"AppMenuItem(title: '{_title}', icon: 'enabled.png', onTap: () {_go_path}, isSelected: widget.currentPath == '{_path}'),"
                    # Adicionando os routers no projeto
                    _list_menu_itens += _comando
            # Adicionando os routers no projeto
            _routers_file = Path(f"{self.flutter_web_dir}/lib/core/widgets/app.menu.dart")
            _routers_content = Utils.get_snippet(_routers_file)
            _routers_content = _routers_content.replace("$AppsMenuItem$", _list_menu_itens)
            with open(_routers_file, "w") as arquivo:
                arquivo.write(_routers_content)
        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o build de AppsWebRouterInjectRootRouteBuilder: {error}"
            )
            return
