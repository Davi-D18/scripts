{% if cookiecutter.usar_serializacao == "s" %}
from marshmallow import Schema, fields, validate, EXCLUDE
class NewsSchema(Schema):
    class Meta:
        unknown = EXCLUDE # Ignora campos não declarados

    id = fields.Int(dump_only=True)  # Aparece apenas na resposta

    # Campos de entrada (validação)
    title = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100, error="Título deve ter entre 3 e 100 caracteres")
    )
    content = fields.Str(
        required=True,
        validate=validate.Length(min=10, error="Conteúdo muito curto (mínimo 10 caracteres)")
    )

{% endif %}
