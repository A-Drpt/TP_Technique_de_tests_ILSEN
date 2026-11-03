import pytest

@pytest.fixture
def triangulate():
    """Fixture qui charge la fonction triangulate avec gestion d'erreur."""
    try:
        from triangulator.core import triangulate
        return triangulate
    except ModuleNotFoundError:
        pytest.fail("Module `triangulator.core` absent: implémentation à faire.")