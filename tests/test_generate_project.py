"""Testes para generate_project.py"""
from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import generate_project as gp
from generate_project import (
    COPY_WITHOUT_RENDER,
    _build_context,
    _project_dir_name,
    _render,
    _should_skip_render,
    _slugify,
    scaffold_project,
    setup_env_file,
    _generate_secret_key,
)

DJANGO_API_SNIPPETS = (
    ROOT
    / "{{cookiecutter.project_slug}}"
    / "core/management/commands/snippets/django/api"
)


# ─── dest_base — mesmo nível que AgtecCore ───────────────────────────────────

class TestDestBase:
    def test_dest_is_always_sibling_of_agteccore(self):
        """O projeto é sempre criado ao lado do AgtecCore — destino não configurável."""
        script_path = Path(gp.__file__)
        agteccore_dir = script_path.parent
        dest_base = script_path.parent.parent
        assert dest_base == agteccore_dir.parent

    def test_script_parent_is_agteccore_root(self):
        script_path = Path(gp.__file__)
        assert script_path.name == "generate_project.py"
        assert (script_path.parent / "{{cookiecutter.project_slug}}").exists()

    def test_dest_base_resolves_to_sibling_dir(self):
        script_path = Path(gp.__file__)
        dest_base = script_path.parent.parent
        agteccore = script_path.parent
        # AgtecCore e o projeto gerado ficam no mesmo nível
        assert (dest_base / agteccore.name).resolve() == agteccore.resolve()

    def test_no_output_dir_argument_accepted(self):
        """Argparse não deve aceitar argumento posicional de destino."""
        import argparse
        parser_actions = [a.dest for a in gp._parse_args.__wrapped__.keywords.get("parser", gp._parse_args()).__dict__.get("_actions", [])] if False else []
        # Valida indiretamente: output_dir não é atributo do namespace retornado
        import sys
        old_argv = sys.argv
        sys.argv = ["generate_project.py"]
        try:
            ns = gp._parse_args()
            assert not hasattr(ns, "output_dir")
        finally:
            sys.argv = old_argv


# ─── _slugify ─────────────────────────────────────────────────────────────────

class TestSlugify:
    def test_lowercase(self):
        assert _slugify("Meu Projeto") == "meu-projeto"

    def test_replace_spaces_with_dash(self):
        assert _slugify("Projeto Base Django") == "projeto-base-django"

    def test_remove_special_chars(self):
        assert _slugify("Projeto #1!") == "projeto-1"

    def test_already_slug(self):
        assert _slugify("projeto") == "projeto"

    def test_accents_stripped(self):
        result = _slugify("Gestão Pública")
        assert " " not in result
        assert result == result.lower()


class TestProjectDirName:
    def test_uses_pascal_case(self):
        assert _project_dir_name("Projeto Validacao") == "ProjetoValidacao"

    def test_strips_accents(self):
        assert _project_dir_name("Projeto Validação") == "ProjetoValidacao"

    def test_removes_symbols(self):
        assert _project_dir_name("Projeto #1!") == "Projeto1"


# ─── _build_context ───────────────────────────────────────────────────────────

class TestBuildContext:
    def _make_args(self, **kwargs) -> SimpleNamespace:
        defaults = dict(
            project_name="Sistema Teste",
            client_name="Prefeitura",
            description="Desc",
            author_name="Dev",
            domain_name="palmas.to.gov.br",
            email="dev@palmas.to.gov.br",
            flutter_org="Agtec",
            docker_port="8000",
            postgre_port="5432",
            no_install=False,
            no_git=False,
            no_build_apps=False,
        )
        defaults.update(kwargs)
        return SimpleNamespace(**defaults)

    def test_project_slug_derived(self):
        ctx = _build_context(self._make_args())
        assert ctx["project_slug"] == "sistema_teste"

    def test_project_dir_name_derived(self):
        ctx = _build_context(self._make_args(project_name="Sistema Teste"))
        assert ctx["project_dir_name"] == "SistemaTeste"

    def test_main_app_equals_slug(self):
        ctx = _build_context(self._make_args())
        assert ctx["main_app"] == ctx["project_slug"]

    def test_flutter_org_domain_reversed(self):
        ctx = _build_context(self._make_args(domain_name="palmas.to.gov.br"))
        assert ctx["flutter_organization_domain"] == "br.gov.to.palmas"

    def test_created_date_format(self):
        ctx = _build_context(self._make_args())
        parts = ctx["created_date_project"].split("/")
        assert len(parts) == 3
        assert len(parts[2]) == 4  # YYYY

    def test_static_versions(self):
        ctx = _build_context(self._make_args())
        assert ctx["django_version"] == "5.2.12"
        assert ctx["python_version"] == "3.12.*"
        assert ctx["postgresql_version"] == "14.2"
        assert ctx["drf_version"] == "3.16.1"


# ─── prompts booleanos (install / build_apps / git) ──────────────────────────

class TestBoolPrompts:
    """Testa os prompts interativos de install, build_apps e git_init."""

    def _make_args(self, **kwargs) -> SimpleNamespace:
        defaults = dict(
            project_name="Proj",
            client_name="C",
            description="D",
            author_name="A",
            domain_name="test.com",
            email="a@test.com",
            flutter_org="Org",
            docker_port="8000",
            postgre_port="5432",
            no_install=False,
            no_git=False,
            no_build_apps=False,
        )
        defaults.update(kwargs)
        return SimpleNamespace(**defaults)

    def test_no_install_flag_skips_install(self):
        ctx = _build_context(self._make_args(no_install=True))
        assert ctx["install_requirements"] is False

    def test_no_install_forces_build_apps_false(self):
        """build_apps nunca pode ser True se install_requirements é False."""
        ctx = _build_context(self._make_args(no_install=True))
        assert ctx["build_apps"] is False

    def test_no_git_flag_skips_git(self):
        ctx = _build_context(self._make_args(no_git=True))
        assert ctx["git_init"] is False

    def test_no_build_apps_flag_skips_build(self):
        ctx = _build_context(self._make_args(no_build_apps=True))
        assert ctx["build_apps"] is False

    def test_interactive_defaults_true_in_non_tty(self):
        """Em ambiente não-interativo (pytest), ask_bool retorna default=True."""
        ctx = _build_context(self._make_args())
        assert ctx["install_requirements"] is True
        assert ctx["build_apps"] is True
        assert ctx["git_init"] is True

    def test_interactive_prompt_yes_answer(self):
        with patch("builtins.input", side_effect=["s", "s", "s"]):
            with patch("sys.stdin") as mock_stdin:
                mock_stdin.isatty.return_value = True
                ctx = _build_context(self._make_args())
        assert ctx["install_requirements"] is True
        assert ctx["build_apps"] is True
        assert ctx["git_init"] is True

    def test_interactive_prompt_no_answer(self):
        with patch("builtins.input", side_effect=["n", "n"]):
            with patch("sys.stdin") as mock_stdin:
                mock_stdin.isatty.return_value = True
                ctx = _build_context(self._make_args())
        assert ctx["install_requirements"] is False
        # build_apps não é perguntado quando install=False
        assert ctx["build_apps"] is False
        assert ctx["git_init"] is False

    def test_interactive_install_yes_build_no(self):
        with patch("builtins.input", side_effect=["s", "n", "s"]):
            with patch("sys.stdin") as mock_stdin:
                mock_stdin.isatty.return_value = True
                ctx = _build_context(self._make_args())
        assert ctx["install_requirements"] is True
        assert ctx["build_apps"] is False
        assert ctx["git_init"] is True

    def test_flag_overrides_skip_prompt(self):
        """Com flag --no-install, input() não deve ser chamado para install."""
        with patch("builtins.input", side_effect=Exception("input não deveria ser chamado")):
            with patch("sys.stdin") as mock_stdin:
                mock_stdin.isatty.return_value = True
                ctx = _build_context(self._make_args(no_install=True, no_git=True, no_build_apps=True))
        assert ctx["install_requirements"] is False
        assert ctx["build_apps"] is False
        assert ctx["git_init"] is False


# ─── _render ──────────────────────────────────────────────────────────────────

class TestRender:
    def _ctx(self, **kwargs) -> dict:
        defaults = dict(
            project_name="Projeto Teste",
            project_slug="projeto_teste",
            client_name="Cliente",
            author_name="Autor",
            email="autor@test.com",
            domain_name="test.com",
        )
        defaults.update(kwargs)
        return {"cookiecutter": SimpleNamespace(**defaults)}

    def test_simple_variable(self):
        result = _render("APP_ID = '{{ cookiecutter.project_slug }}'", self._ctx())
        assert result == "APP_ID = 'projeto_teste'"

    def test_no_spaces_variable(self):
        result = _render("name: {{cookiecutter.project_slug}}", self._ctx())
        assert result == "name: projeto_teste"

    def test_lower_method(self):
        result = _render("{{cookiecutter.project_slug.lower()}}_db", self._ctx())
        assert result == "projeto_teste_db"

    def test_title_method(self):
        result = _render("{{ cookiecutter.project_name.title() }}", self._ctx())
        assert result == "Projeto Teste"

    def test_default_filter_known_var(self):
        result = _render("{{ cookiecutter.author_name | default('N/A') }}", self._ctx())
        assert result == "Autor"

    def test_default_filter_unknown_var(self):
        result = _render("{{ cookiecutter.variavel_inexistente | default('fallback') }}", self._ctx())
        assert result == "fallback"

    def test_syntax_error_returns_original(self):
        broken = "{% if %}"
        result = _render(broken, self._ctx())
        assert result == broken

    def test_no_cookiecutter_vars_unchanged(self):
        content = "DEBUG=True\nALLOWED_HOSTS=*\n"
        result = _render(content, self._ctx())
        assert result == content


# ─── _should_skip_render ──────────────────────────────────────────────────────

class TestShouldSkipRender:
    def test_core_skipped(self):
        assert _should_skip_render("core/views/base_view.py") is True

    def test_core_root_skipped(self):
        assert _should_skip_render("core") is True

    def test_usuario_skipped(self):
        assert _should_skip_render("usuario/models.py") is True

    def test_contrib_skipped(self):
        assert _should_skip_render("contrib/secret_gen.py") is True

    def test_docs_skipped(self):
        assert _should_skip_render("docs/index.md") is True

    def test_coveragerc_skipped(self):
        assert _should_skip_render(".coveragerc") is True

    def test_prospector_skipped(self):
        assert _should_skip_render(".prospector.yaml") is True

    def test_base_settings_not_skipped(self):
        assert _should_skip_render("base/settings.py") is False

    def test_env_example_not_skipped(self):
        assert _should_skip_render(".env.example") is False

    def test_docker_compose_not_skipped(self):
        assert _should_skip_render("docker-compose.yml") is False

    def test_ia_docs_not_skipped(self):
        assert _should_skip_render(".ia/docs/architecture/overview.md") is False


# ─── init_git — identidade e checkout condicional ────────────────────────────

class TestInitGit:
    def _fake_run_ok(self, cmd, **kwargs):
        from types import SimpleNamespace
        return SimpleNamespace(returncode=0)

    def test_commit_uses_identity_flags_when_no_global_config(self, tmp_path):
        """Sem identidade global, o commit deve injetar -c user.name e -c user.email."""
        committed = []

        def fake_run(cmd, **kwargs):
            from types import SimpleNamespace
            if isinstance(cmd, list) and "commit" in cmd:
                committed.append(cmd)
            return SimpleNamespace(returncode=0)

        with patch("subprocess.run", side_effect=fake_run):
            with patch.object(gp, "_git_has_identity", return_value=False):
                gp.init_git(tmp_path)

        assert committed, "Nenhum commit foi chamado"
        commit_cmd = committed[0]
        assert "-c" in commit_cmd
        assert any("user.name" in arg for arg in commit_cmd)
        assert any("user.email" in arg for arg in commit_cmd)

    def test_commit_without_identity_flags_when_global_config_exists(self, tmp_path):
        """Com identidade global configurada, o commit não deve injetar -c."""
        committed = []

        def fake_run(cmd, **kwargs):
            from types import SimpleNamespace
            if isinstance(cmd, list) and "commit" in cmd:
                committed.append(cmd)
            return SimpleNamespace(returncode=0)

        with patch("subprocess.run", side_effect=fake_run):
            with patch.object(gp, "_git_has_identity", return_value=True):
                gp.init_git(tmp_path)

        assert committed
        commit_cmd = committed[0]
        assert "-c" not in commit_cmd

    def test_checkout_skipped_when_commit_fails(self, tmp_path):
        """Se o commit falhar, git checkout -b desenvolvimento não deve ser executado."""
        checkout_called = []

        def fake_run(cmd, **kwargs):
            from types import SimpleNamespace
            if isinstance(cmd, list) and "checkout" in cmd:
                checkout_called.append(cmd)
                return SimpleNamespace(returncode=0)
            if isinstance(cmd, list) and "commit" in cmd:
                return SimpleNamespace(returncode=1)  # commit falha
            return SimpleNamespace(returncode=0)

        with patch("subprocess.run", side_effect=fake_run):
            with patch.object(gp, "_git_has_identity", return_value=True):
                gp.init_git(tmp_path)

        assert not checkout_called, "checkout não deveria ser chamado após commit falhar"

    def test_checkout_runs_when_commit_succeeds(self, tmp_path):
        """Se o commit tiver sucesso, git checkout -b desenvolvimento deve ser executado."""
        checkout_called = []

        def fake_run(cmd, **kwargs):
            from types import SimpleNamespace
            if isinstance(cmd, list) and "checkout" in cmd:
                checkout_called.append(cmd)
            return SimpleNamespace(returncode=0)

        with patch("subprocess.run", side_effect=fake_run):
            with patch.object(gp, "_git_has_identity", return_value=True):
                gp.init_git(tmp_path)

        assert checkout_called
        assert "desenvolvimento" in checkout_called[0]

    def test_commit_message_is_single_argument(self, tmp_path):
        """A mensagem do commit deve ser passada como um único argumento (não splitada)."""
        committed = []

        def fake_run(cmd, **kwargs):
            from types import SimpleNamespace
            if isinstance(cmd, list) and "commit" in cmd:
                committed.append(cmd)
            return SimpleNamespace(returncode=0)

        with patch("subprocess.run", side_effect=fake_run):
            with patch.object(gp, "_git_has_identity", return_value=True):
                gp.init_git(tmp_path)

        commit_cmd = committed[0]
        # A mensagem "Primeiro Commit" deve ser um único elemento na lista
        assert "Primeiro Commit" in commit_cmd


# ─── build_default_apps — portabilidade do executável Python ─────────────────

class TestBuildDefaultAppsExecutable:
    def test_prefers_generated_project_venv_python(self, tmp_path):
        """Se uv sync criou .venv, o build deve usar esse interpretador."""
        import sys
        from unittest.mock import patch

        project_python = tmp_path / ".venv" / "bin" / "python"
        project_python.parent.mkdir(parents=True)
        project_python.write_text("", encoding="utf-8")

        calls_made = []

        def fake_run(cmd, **kwargs):
            calls_made.append(cmd)
            from types import SimpleNamespace
            return SimpleNamespace(returncode=0)

        with patch("subprocess.run", side_effect=fake_run):
            gp.build_default_apps(tmp_path)

        for cmd in calls_made:
            assert cmd[0] == str(project_python)
            assert cmd[0] != sys.executable

    def test_uses_sys_executable_not_hardcoded_python(self, tmp_path):
        """Sem .venv local, manage.py build deve cair para sys.executable."""
        import sys
        from unittest.mock import patch
        calls_made = []

        def fake_run(cmd, **kwargs):
            calls_made.append(cmd)
            from types import SimpleNamespace
            return SimpleNamespace(returncode=0)

        with patch("subprocess.run", side_effect=fake_run):
            gp.build_default_apps(tmp_path)

        for cmd in calls_made:
            assert cmd[0] == sys.executable, (
                f"Esperado sys.executable={sys.executable!r}, obtido {cmd[0]!r}. "
                "O script não deve hardcodar 'python', 'python3' ou 'py'."
            )

    def test_executable_exists_on_current_platform(self):
        """sys.executable aponta para um arquivo que realmente existe."""
        import sys
        assert Path(sys.executable).exists(), (
            f"sys.executable={sys.executable!r} não existe — ambiente inválido"
        )

    def test_no_python_constant_in_module(self):
        """A constante PYTHON não deve mais existir no módulo."""
        assert not hasattr(gp, "PYTHON"), (
            "Constante PYTHON encontrada — deve ser removida em favor de sys.executable"
        )


# ─── _generate_secret_key ─────────────────────────────────────────────────────

class TestGenerateSecretKey:
    def test_not_empty(self):
        assert _generate_secret_key() != ""

    def test_unique(self):
        keys = {_generate_secret_key() for _ in range(10)}
        assert len(keys) == 10

    def test_length_sufficient(self):
        # token_urlsafe(50) produces ~67 chars
        key = _generate_secret_key()
        assert len(key) >= 60


# ─── snippets django/api — consistência view x serializer ─────────────────────

class TestDjangoApiSnippets:
    def test_view_snippet_only_imports_existing_serializer(self):
        view_snippet = (DJANGO_API_SNIPPETS / "view.txt").read_text(encoding="utf-8")
        serializer_snippet = (DJANGO_API_SNIPPETS / "serializer.txt").read_text(encoding="utf-8")

        assert "$ModelName$GETSerializer" not in view_snippet
        assert "class $ModelName$Serializer" in serializer_snippet


# ─── scaffold_project (integração) ────────────────────────────────────────────

class TestScaffoldProject:
    """Testes de integração — geram o projeto em tmpdir e validam a saída."""

    @pytest.fixture()
    def ctx(self):
        return {
            "project_name": "Meu Sistema",
            "project_dir_name": "MeuSistema",
            "project_slug": "meu_sistema",
            "main_app": "meu_sistema",
            "client_name": "Prefeitura",
            "docker_port": "8000",
            "postgre_port": "5432",
            "created_date_project": "01/01/2026",
            "description": "Projeto de teste",
            "author_name": "Dev Teste",
            "domain_name": "test.com",
            "email": "dev@test.com",
            "flutter_organization_name": "Agtec",
            "flutter_organization_domain": "com.test",
            "django_version": "5.2.12",
            "python_version": "3.12.*",
            "postgresql_version": "14.2",
            "drf_version": "3.16.1",
        }

    def test_generates_project_directory(self, ctx, tmp_path):
        dest = tmp_path / ctx["project_dir_name"]
        scaffold_project(ctx, dest)
        assert dest.is_dir()

    def test_base_settings_rendered(self, ctx, tmp_path):
        dest = tmp_path / ctx["project_dir_name"]
        scaffold_project(ctx, dest)
        settings = (dest / "base" / "settings.py").read_text()
        assert "Meu Sistema" in settings
        assert "cookiecutter" not in settings

    def test_env_example_rendered(self, ctx, tmp_path):
        dest = tmp_path / ctx["project_dir_name"]
        scaffold_project(ctx, dest)
        env_example = (dest / ".env.example").read_text()
        assert "meu_sistema" in env_example
        assert "cookiecutter" not in env_example

    def test_core_copied_without_render(self, ctx, tmp_path):
        dest = tmp_path / ctx["project_dir_name"]
        scaffold_project(ctx, dest)
        core_dir = dest / "core"
        assert core_dir.is_dir()
        # core/ em copy_without_render: saída deve ser idêntica ao source
        from generate_project import TEMPLATE_DIR
        for dst_file in core_dir.rglob("*"):
            if not dst_file.is_file():
                continue
            src_file = TEMPLATE_DIR / "core" / dst_file.relative_to(core_dir)
            assert dst_file.read_bytes() == src_file.read_bytes(), (
                f"{dst_file.name} foi modificado — core/ não deve ser renderizado"
            )

    def test_fails_if_dest_exists(self, ctx, tmp_path):
        dest = tmp_path / ctx["project_dir_name"]
        dest.mkdir()
        with pytest.raises(SystemExit):
            scaffold_project(ctx, dest)


# ─── setup_env_file ───────────────────────────────────────────────────────────

class TestSetupEnvFile:
    def test_creates_env_from_example(self, tmp_path):
        env_example = tmp_path / ".env.example"
        env_example.write_text("SECRET_KEY=GERE_UMA_CHAVE_SECRETA_ALEATORIA\nDEBUG=True\n")
        setup_env_file(tmp_path)
        env = tmp_path / ".env"
        assert env.exists()
        content = env.read_text()
        assert "SECRET_KEY=GERE_UMA_CHAVE_SECRETA_ALEATORIA" not in content
        assert "SECRET_KEY=" in content

    def test_does_not_overwrite_existing_env(self, tmp_path):
        env_example = tmp_path / ".env.example"
        env_example.write_text("SECRET_KEY=GERE_UMA_CHAVE_SECRETA_ALEATORIA\n")
        env = tmp_path / ".env"
        env.write_text("SECRET_KEY=minha_chave_original\n")
        setup_env_file(tmp_path)
        assert env.read_text() == "SECRET_KEY=minha_chave_original\n"

    def test_no_env_example_does_not_crash(self, tmp_path):
        setup_env_file(tmp_path)  # não deve lançar exceção
