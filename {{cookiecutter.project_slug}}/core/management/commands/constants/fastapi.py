IGNORE_FIELDS = [
    "id",
    "deleted",
    "deleted_on",
    "enabled",
    "created_on",
    "updated_on"
]

AUTO_PEP_8_COMMAND = (
    "autopep8 --in-place --aggressive --max-line-length 120 --aggressive"
)

# {
#   django_field: {
#       schema: "fastapi_field",
#       model: "pydantic_field"
# }
FIELDS_TYPES = {
    "SmallAutoField": {
        "schema": "int",
        "model": "Integer"
    },
    "AutoField": {
        "schema": "int",
        "model": "Integer"
    },
    "BLANK_CHOICE_DASH": {
        "schema": "BLANK_CHOICE_DASH",
        "model": "BLANK_CHOICE_DASH"
    },
    "BigAutoField": {
        "schema": "int",
        "model": "Integer"
    },
    "BigIntegerField": {
        "schema": "int",
        "model": "Integer"
    },
    "BinaryField": {
        "schema": "str",
        "model": "String"
    },
    "BooleanField": {
        "schema": "bool",
        "model": "Boolean"
    },
    "CharField": {
        "schema": "str",
        "model": "String"
    },
    "CommaSeparatedIntegerField": {
        "schema": "str",
        "model": "String"
    },
    "DateField": {
        "schema": "datetime.date",
        "model": "Date"
    },
    "DateTimeField": {
        "schema": "datetime.datetime",
        "model": "DateTime"
    },
    "DecimalField": {
        "schema": "float",
        "model": "Float"
    },
    "DurationField": {
        "schema": "int",
        "model": "Integer"
    },
    "EmailField": {
        "schema": "str",
        "model": "String"
    },
    "Empty": {
        "schema": "str",
        "model": "String"
    },
    "FileField": {
        "schema": "str",
        "model": "String"
    },
    "Field": {
        "schema": "str",
        "model": "String"
    },
    "FieldDoesNotExist": {
        "schema": "str",
        "model": "String"
    },
    "FilePathField": {
        "schema": "str",
        "model": "String"
    },
    "FloatField": {
        "schema": "float",
        "model": "Float"
    },
    "GenericIPAddressField": {
        "schema": "str",
        "model": "String"
    },
    "IPAddressField": {
        "schema": "str",
        "model": "String"
    },
    "IntegerField": {
        "schema": "int",
        "model": "Integer"
    },
    "FieldFile": {
        "schema": "str",
        "model": "String"
    },
    "NOT_PROVIDED": {
        "schema": "str",
        "model": "String"
    },
    "NullBooleanField": {
        "schema": "bool",
        "model": "Boolean"
    },
    "ImageField": {
        "schema": "str",
        "model": "String"
    },
    "PositiveIntegerField": {
        "schema": "int",
        "model": "Integer"
    },
    "PositiveSmallIntegerField": {
        "schema": "int",
        "model": "Integer"
    },
    "SlugField": {
        "schema": "str",
        "model": "String"
    },
    "SmallIntegerField": {
        "schema": "int",
        "model": "Integer"
    },
    "TextField": {
        "schema": "str",
        "model": "String"
    },
    "TimeField": {
        "schema": "datetime.time",
        "model": "Time"
    },
    "URLField": {
        "schema": "str",
        "model": "String"
    },
    "UUIDField": {
        "schema": "str",
        "model": "String"
    },
    "ForeignKey": {
        "schema": "str",
        "model": "String"
    },
    "OneToOneField": {
        "schema": "str",
        "model": "String"
    },
}