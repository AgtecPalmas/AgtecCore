import subprocess
from collections import defaultdict
from django.core.management.base import BaseCommand
from core.management.commands.utils import Utils


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_pytest_tests():
        # Função para obter a lista de todos os testes existentes no projeto usando o pytest
        result = subprocess.run(['pytest', '--collect-only'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        tests_list = output.split('\n')[2:]
        return tests_list

    def obter_modelos_sem_testes(self):
        modelos_sem_testes = defaultdict(list)  # Dicionário para agrupar as models por app
        apps_models = Utils.get_apps()

        # Obter a lista de todos os testes existentes no projeto
        testes_existentes = self.get_pytest_tests()

        for app, models in apps_models.items():
            for model in models:
                model_nome = model
                test_class_nome = f"Test{model_nome}Models"
                test_form_nome = f"Test{model_nome}Forms"
                test_view_nome = f"Test{model_nome}Views"

                # Verificar se o modelo possui teste nas categorias (models, forms, views)
                has_model_test = any(test_class_nome in teste for teste in testes_existentes)
                has_form_test = any(test_form_nome in teste for teste in testes_existentes)
                has_view_test = any(test_view_nome in teste for teste in testes_existentes)

                # Adicionar o modelo à lista de modelos sem testes na categoria correspondente
                if not has_model_test:
                    modelos_sem_testes[app].append(('models', model_nome))
                if not has_form_test:
                    modelos_sem_testes[app].append(('forms', model_nome))
                if not has_view_test:
                    modelos_sem_testes[app].append(('views', model_nome))

        return modelos_sem_testes

    def handle(self, *args, **options) -> None:
        """Executa o comando"""
        modelos_ignorados = ["Audit"]  # Adicione os nomes dos modelos a serem ignorados
        modelos_sem_testes = self.obter_modelos_sem_testes(modelos_ignorados)

        if modelos_sem_testes:
            print("Os seguintes modelos não possuem testes:")
            for app, models in modelos_sem_testes.items():
                print(f"App: {app}")
                if models:
                    categories = defaultdict(list)  # Dicionário para agrupar os modelos por categoria
                    for category, model in models:
                        categories[category].append(model)

                    # Apresentar os modelos sem testes separados por categoria
                    for category, models_list in categories.items():
                        print(f"  {category.capitalize()}:")
                        for model in models_list:
                            print(f"    \u274c {model}")
        else:
            print("\033[92m\u2714", " Todos os modelos possuem testes.")
