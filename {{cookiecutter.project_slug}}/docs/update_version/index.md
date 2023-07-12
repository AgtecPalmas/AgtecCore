# Versões

## 3.1

### Etapas para atualização para a versão 3.1

 1. No arquivo settings.py (base/settings.py)
 
     1.1. Adicinar a entrada de Auditoria, defina o valor como True caso deseje que o sistema todo seja auditado.

        AUDIT_ENABLED = True
 
     1.2. Adicionar a entrada para o novo estilo de Booleano

        BOOLEAN_FIELD_IS_SWITCH = True
 
     1.3. Adicionar a bloco abaixo para gerenciar quais áreas do cabeçalho do HTML serão renderizados  
        
        """
        Configuração para o Middleware Header_control
        O middleware header_control é responsavel por controlar
        Se o componente header do agtec_core vai ser renderizado ou não
        """
        
        # Middleware Header Control
        HEADER_COMPLETO = True
        HEADER_ACTIONS = True
        HEADER_VERTICAL = True
        BREAD_CRUMBS = True

     1.4. Adicionar o bloco abaixo que configura a app TEMPUS_DOMINUS
    
        TEMPUS_DOMINUS_LOCALIZE = True
        TEMPUS_DOMINUS_INCLUDE_ASSETS = True
        TEMPUS_DOMINUS_DATE_FORMAT = "DD/MM/YYYY"
        TEMPUS_DOMINUS_TIME_FORMAT = "HH:mm"

       1.5. Adicionar o bloco para que algum app não seja renderizado no Menu Principal,
       importante quando algum app entra em conflito com o Core (Ex.: CKEditor)

        IGNORED_APPS = []

       1.6. Altere as MESSAGE_TAGS para o padrão GovBR

        MESSAGE_TAGS = {
              messages.DEBUG: "info",
              messages.INFO: "info",
              messages.SUCCESS: "success",
              messages.WARNING: "warning",
              messages.ERROR: "danger",
        }

       1.7. Adicione o `DEFAULT_AUTO_FIELD`

        DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

 2. No arquivo urls.py (base/urls.py)

     2.1. Adicionar a linha abaixo no bloco urlpatterns

            path("core/", include("configuracao_core.urls", namespace="configuracao_core")),

     2.2. Caso exista a entrada da url da app configuracao, remover.

            path("configuracao/", include("configuracao.urls", namespace="configuracao")),  

     2.3. Alterar o import na linha 16 para o valor abaixo.

            from core.views.base import BaseIndexTemplate

3. No arquivo .env adicione a variável de senha padrões para ser usar em Mocks e na geração do Admin

       SENHA_PADRAO=123456

### Atenção nessa etapa, caso você tenha alterado a app usuário, é necessário analisar código por código.

 4. Atualizar os arquivos da app usuario. 
 
     4.1. Copiar os arquivos da app usuario (AgtecCore) para a app usuario do seu projeto.

     4.2. Foi melhorado o Signal que manipula o relacionamento de Usuario com User

     4.3. Campos como E-mail e CPF devem ser únicos
