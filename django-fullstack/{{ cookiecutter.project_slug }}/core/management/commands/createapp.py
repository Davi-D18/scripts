import os
import shutil

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Cria um app web com estrutura em pacotes (models, views, forms, ...)"

    missing_args_message = "Você precisa fornecer o nome do app."

    def add_arguments(self, parser):
        parser.add_argument("name", help="Nome do app (ex: catalog)")
        parser.add_argument(
            "resource",
            nargs="?",
            help="Nome do recurso no singular/plural (padrão: o nome do app)",
        )

    def handle(self, **options):
        app_name = options.pop("name").lower().strip()
        resource = (options.pop("resource") or app_name).lower().strip()

        if resource.endswith("s"):
            singular, plural = resource[:-1], resource
        else:
            singular, plural = resource, f"{resource}s"

        app_dir = os.path.join("apps", app_name)
        os.makedirs(app_dir, exist_ok=True)

        try:
            call_command("startapp", app_name, app_dir)
            self._build_scaffold(app_dir, app_name, singular, plural)
        except Exception as exc:  # noqa: BLE001
            shutil.rmtree(app_dir, ignore_errors=True)
            raise CommandError(f"Erro ao criar app: {exc}") from exc

        self.stdout.write(
            self.style.SUCCESS(
                f'App "{app_name}" criado em apps/{app_name}/\n'
                f'Recurso "{singular}" ({plural}) adicionado.'
            )
        )
        self.stdout.write(
            "Registre o app em core/settings/base.py: "
            f'INSTALLED_APPS += ["apps.{app_name}"]'
        )

    def _build_scaffold(self, app_dir, app_name, singular, plural):
        class_name = singular.capitalize()

        # startapp cria arquivos únicos; usamos pacotes por responsabilidade
        for legacy in ("views.py", "models.py", "tests.py"):
            legacy_path = os.path.join(app_dir, legacy)
            if os.path.exists(legacy_path):
                os.remove(legacy_path)

        self._write(os.path.join(app_dir, "admin.py"), self._admin(app_name, class_name))
        self._write(
            os.path.join(app_dir, "urls.py"), self._urls(app_name, class_name, singular)
        )
        self._fix_apps_py(os.path.join(app_dir, "apps.py"), app_name)

        # models/
        models_dir = os.path.join(app_dir, "models")
        os.makedirs(models_dir, exist_ok=True)
        self._write(
            os.path.join(models_dir, f"{plural}.py"),
            self._model(class_name, singular, plural),
        )
        self._write(
            os.path.join(models_dir, "__init__.py"),
            f'from .{plural} import {class_name}\n\n__all__ = ["{class_name}"]\n',
        )

        # forms/
        forms_dir = os.path.join(app_dir, "forms")
        os.makedirs(forms_dir, exist_ok=True)
        self._write(
            os.path.join(forms_dir, f"{singular}.py"), self._form(app_name, class_name)
        )
        self._write(
            os.path.join(forms_dir, "__init__.py"),
            f'from .{singular} import {class_name}Form\n\n'
            f'__all__ = ["{class_name}Form"]\n',
        )

        # views/
        views_dir = os.path.join(app_dir, "views")
        os.makedirs(views_dir, exist_ok=True)
        self._write(
            os.path.join(views_dir, f"{singular}.py"),
            self._views(app_name, class_name, singular, plural),
        )
        self._write(
            os.path.join(views_dir, "__init__.py"),
            f"from .{singular} import (\n"
            f"    {class_name}CreateView,\n"
            f"    {class_name}DeleteView,\n"
            f"    {class_name}ListView,\n"
            f"    {class_name}UpdateView,\n"
            ")\n\n"
            "__all__ = [\n"
            f'    "{class_name}CreateView",\n'
            f'    "{class_name}DeleteView",\n'
            f'    "{class_name}ListView",\n'
            f'    "{class_name}UpdateView",\n'
            "]\n",
        )

        # services/ e selectors/
        for package, doc in (
            ("services", "Regras de negócio"),
            ("selectors", "Consultas de leitura"),
        ):
            package_dir = os.path.join(app_dir, package)
            os.makedirs(package_dir, exist_ok=True)
            self._write(
                os.path.join(package_dir, "__init__.py"),
                f'"""{doc} do app {app_name}."""\n',
            )

        # tests/
        tests_dir = os.path.join(app_dir, "tests")
        os.makedirs(tests_dir, exist_ok=True)
        self._write(os.path.join(tests_dir, "__init__.py"), "")
        self._write(
            os.path.join(tests_dir, f"test_{singular}.py"),
            self._test(app_name, class_name, singular, plural),
        )

        # templates/<app>/
        templates_dir = os.path.join(app_dir, "templates", app_name)
        os.makedirs(templates_dir, exist_ok=True)
        self._write(
            os.path.join(templates_dir, f"{singular}_list.html"),
            self._tpl_list(app_name, class_name, singular, plural),
        )
        self._write(
            os.path.join(templates_dir, f"{singular}_form.html"),
            self._tpl_form(app_name, class_name, singular),
        )
        self._write(
            os.path.join(templates_dir, f"{singular}_confirm_delete.html"),
            self._tpl_delete(app_name, class_name, singular),
        )

        self._write(
            os.path.join(app_dir, "README.md"),
            self._readme(app_name, class_name, singular, plural),
        )

    def _write(self, path, content):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(content)

    def _fix_apps_py(self, path, app_name):
        with open(path) as fh:
            content = fh.read()
        content = content.replace(f"name = '{app_name}'", f"name = 'apps.{app_name}'")
        content = content.replace(f'name = "{app_name}"', f'name = "apps.{app_name}"')
        with open(path, "w") as fh:
            fh.write(content)

    # ---- templates de conteúdo -------------------------------------------------

    def _model(self, class_name, singular, plural):
        return (
            "from django.db import models\n\n\n"
            f"class {class_name}(models.Model):\n"
            "    name = models.CharField(max_length=255)\n"
            "    created_at = models.DateTimeField(auto_now_add=True)\n"
            "    updated_at = models.DateTimeField(auto_now=True)\n\n"
            "    class Meta:\n"
            '        ordering = ["name"]\n'
            f'        verbose_name = "{singular}"\n'
            f'        verbose_name_plural = "{plural}"\n\n'
            "    def __str__(self):\n"
            "        return self.name\n"
        )

    def _form(self, app_name, class_name):
        return (
            "from django import forms\n\n"
            f"from apps.{app_name}.models import {class_name}\n\n\n"
            f"class {class_name}Form(forms.ModelForm):\n"
            "    class Meta:\n"
            f"        model = {class_name}\n"
            '        fields = ["name"]\n\n'
            "    def __init__(self, *args, **kwargs):\n"
            "        super().__init__(*args, **kwargs)\n"
            "        for field in self.fields.values():\n"
            '            field.widget.attrs.setdefault("class", "form-control")\n'
        )

    def _views(self, app_name, class_name, singular, plural):
        return (
            "from django.urls import reverse_lazy\n"
            "from django.views.generic import CreateView, DeleteView, ListView, UpdateView\n\n"
            f"from apps.{app_name}.forms import {class_name}Form\n"
            f"from apps.{app_name}.models import {class_name}\n\n\n"
            f"class {class_name}ListView(ListView):\n"
            f"    model = {class_name}\n"
            f'    template_name = "{app_name}/{singular}_list.html"\n'
            f'    context_object_name = "{plural}"\n\n\n'
            f"class {class_name}CreateView(CreateView):\n"
            f"    model = {class_name}\n"
            f"    form_class = {class_name}Form\n"
            f'    template_name = "{app_name}/{singular}_form.html"\n'
            f'    success_url = reverse_lazy("{app_name}:{singular}_list")\n\n\n'
            f"class {class_name}UpdateView(UpdateView):\n"
            f"    model = {class_name}\n"
            f"    form_class = {class_name}Form\n"
            f'    template_name = "{app_name}/{singular}_form.html"\n'
            f'    success_url = reverse_lazy("{app_name}:{singular}_list")\n\n\n'
            f"class {class_name}DeleteView(DeleteView):\n"
            f"    model = {class_name}\n"
            f'    template_name = "{app_name}/{singular}_confirm_delete.html"\n'
            f'    success_url = reverse_lazy("{app_name}:{singular}_list")\n'
        )

    def _urls(self, app_name, class_name, singular):
        return (
            "from django.urls import path\n\n"
            f"from apps.{app_name} import views\n\n"
            f'app_name = "{app_name}"\n\n'
            "urlpatterns = [\n"
            f'    path("", views.{class_name}ListView.as_view(), name="{singular}_list"),\n'
            f'    path("new/", views.{class_name}CreateView.as_view(), name="{singular}_create"),\n'
            f'    path("<int:pk>/edit/", views.{class_name}UpdateView.as_view(), name="{singular}_update"),\n'
            f'    path("<int:pk>/delete/", views.{class_name}DeleteView.as_view(), name="{singular}_delete"),\n'
            "]\n"
        )

    def _admin(self, app_name, class_name):
        return (
            "from django.contrib import admin\n\n"
            f"from apps.{app_name}.models import {class_name}\n\n"
            f"admin.site.register({class_name})\n"
        )

    def _test(self, app_name, class_name, singular, plural):
        return (
            "import pytest\n"
            "from django.urls import NoReverseMatch, reverse\n\n"
            f"from apps.{app_name}.models import {class_name}\n\n\n"
            "@pytest.mark.django_db\n"
            f"def test_{singular}_str():\n"
            f'    obj = {class_name}.objects.create(name="Example")\n'
            '    assert str(obj) == "Example"\n\n\n'
            "@pytest.mark.django_db\n"
            f"def test_{singular}_list_view(client):\n"
            "    try:\n"
            f'        url = reverse("{app_name}:{singular}_list")\n'
            "    except NoReverseMatch:\n"
            '        pytest.skip("Registre as rotas do app em core/urls.py")\n'
            "    assert client.get(url).status_code == 200\n"
        )

    def _tpl_list(self, app_name, class_name, singular, plural):
        return (
            "{% extends \"base.html\" %}\n\n"
            f"{{% block title %}}{class_name}{{% endblock %}}\n\n"
            "{% block content %}\n"
            "  <section class=\"card\">\n"
            f"    <h1>{class_name}</h1>\n"
            f"    <p><a class=\"btn\" href=\"{{% url '{app_name}:{singular}_create' %}}\">Novo</a></p>\n"
            "    <ul>\n"
            f"      {{% for obj in {plural} %}}\n"
            "        <li>\n"
            "          {{ obj }}\n"
            f"          <a href=\"{{% url '{app_name}:{singular}_update' obj.pk %}}\">editar</a>\n"
            f"          <a href=\"{{% url '{app_name}:{singular}_delete' obj.pk %}}\">excluir</a>\n"
            "        </li>\n"
            "      {% empty %}\n"
            "        <li class=\"muted\">Nenhum registro.</li>\n"
            "      {% endfor %}\n"
            "    </ul>\n"
            "  </section>\n"
            "{% endblock %}\n"
        )

    def _tpl_form(self, app_name, class_name, singular):
        return (
            "{% extends \"base.html\" %}\n\n"
            f"{{% block title %}}{class_name}{{% endblock %}}\n\n"
            "{% block content %}\n"
            "  <section class=\"card\">\n"
            f"    <h1>{class_name}</h1>\n"
            "    <form method=\"post\">\n"
            "      {% csrf_token %}\n"
            "      {{ form.as_p }}\n"
            "      <button class=\"btn\" type=\"submit\">Salvar</button>\n"
            f"      <a href=\"{{% url '{app_name}:{singular}_list' %}}\">Cancelar</a>\n"
            "    </form>\n"
            "  </section>\n"
            "{% endblock %}\n"
        )

    def _tpl_delete(self, app_name, class_name, singular):
        return (
            "{% extends \"base.html\" %}\n\n"
            "{% block title %}Excluir{% endblock %}\n\n"
            "{% block content %}\n"
            "  <section class=\"card\">\n"
            f"    <h1>Excluir {class_name}</h1>\n"
            "    <p>Tem certeza que deseja excluir \"{{ object }}\"?</p>\n"
            "    <form method=\"post\">\n"
            "      {% csrf_token %}\n"
            "      <button class=\"btn\" type=\"submit\">Confirmar</button>\n"
            f"      <a href=\"{{% url '{app_name}:{singular}_list' %}}\">Cancelar</a>\n"
            "    </form>\n"
            "  </section>\n"
            "{% endblock %}\n"
        )

    def _readme(self, app_name, class_name, singular, plural):
        return (
            f"# {app_name.title()} App\n\n"
            "App gerado pelo comando `createapp` (estrutura em pacotes).\n\n"
            "## Estrutura\n\n"
            "```\n"
            f"apps/{app_name}/\n"
            "├── models/            # __PLURAL__ .py, __CLASS__\n"
            "├── views/             # __SINGULAR__.py (List/Create/Update/Delete)\n"
            "├── forms/             # __SINGULAR__.py (ModelForm)\n"
            "├── services/          # regras de negócio (opcional)\n"
            "├── selectors/         # consultas de leitura (opcional)\n"
            "├── tests/             # test___SINGULAR__.py\n"
            "├── templates/__APP__/ # list, form, confirm_delete\n"
            "├── admin.py\n"
            "├── apps.py\n"
            "└── urls.py\n"
            "```\n\n"
            "## Registrar\n\n"
            "Adicione em `core/settings/base.py`:\n\n"
            "```python\n"
            f'INSTALLED_APPS = [..., "apps.{app_name}"]\n'
            "```\n\n"
            "Inclua as rotas em `core/urls.py`:\n\n"
            "```python\n"
            f'path("{app_name}/", include("apps.{app_name}.urls")),\n'
            "```\n"
            .replace("__CLASS__", class_name)
            .replace("__SINGULAR__", singular)
            .replace("__PLURAL__", plural)
            .replace("__APP__", app_name)
        )
