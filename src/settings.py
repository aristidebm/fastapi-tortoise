import yaml
from dotenv import load_dotenv
from pydantic import ValidationError
from src.config import Settings, path_constructor, path_matcher
from src.exceptions import ImproperlyConfigured

yaml.add_implicit_resolver("!path", path_matcher)
yaml.add_constructor("!path", path_constructor)

# I don't why I need to do the stuff of pydantic by myself
# Otherwise it won't work (https://github.com/pydantic/pydantic/issues/1368).
load_dotenv()


try:
    settings = Settings()
except ValidationError as exp:
    raise ImproperlyConfigured from exp


# https://peps.python.org/pep-0562/
def __getattr__(name: str):
    try:
        return globals()[name]
    except KeyError:
        return getattr(settings, name)


def __dir__():
    return dir(settings)
