AUTOFLAKE = "autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place --exclude __init__.py"

AUTOPEP8 = "autopep8 --aggressive --max-line-length 88 --aggressive"

ISORT = "isort --float-to-top"

BLACK = "black"

DJLINT = "djlint --reformat --format-css --format-js"
