build:
    rm -rf ./dist
    poetry build

install:
    pip install -e .

uninstall:
    pip uninstall -y bar-protonmail

publish:
    poetry publish
