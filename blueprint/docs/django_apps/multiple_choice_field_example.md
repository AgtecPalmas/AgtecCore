# Aplicando o forms MultipleChoiceField

1. No arquivo forms da app, criar um método chamado __clean_nomeDoCampo__, nesse método vai ser retornado uma função de join para transformar a lista dos items selecionaods em uma string

### Exemplo do arquivo forms:

```python hl_lines="2 3" 

    class UsuarioForm(BaseForm):

        cursos = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(
            attrs={'class': ''}), choices=CHOICE_CURSOS, required=False)

        def clean_cursos(self):
            return ','.join(self.cleaned_data['cursos'])
```

2. No arquivo models da app, criar um método que vai ser retornado uma função de split, que irá transformar a string salva separada por vírgula em uma lista, essa lista será passada para o forms.
    No __init__ do mesma models, atribuir o valor dessa função ao valor do campo que está sendo usado no forms.

### Exemplo do arquivo models:

```python hl_lines="2 3" 
    
    class Usuario(Base):
        cursos = models.CharField(max_length=300, blank=True, null=True)

        def get_cursos(self):
            return self.cursos.split(',')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.cursos:
                self.cursos = self.get_cursos()
```

# Renderização da lista 

1. No arquivo de listagem, usar o template tag __list_to_string__.
