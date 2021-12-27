build:
    python -m build

install:
    pip install -e .

uninstall:
    pip uninstall -y bar-protonmail

upload:
    python -m twine upload --repository pypi dist/*
