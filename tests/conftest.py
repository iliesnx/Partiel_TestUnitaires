"""
Configuration pytest pour les tests du club de sport.
"""
import pytest

@pytest.fixture
def sample_member():
    """Fixture pour un adhérent de test."""
    return {
        "id": 1,
        "name": "Jean Dupont",
        "balance": 100.0
    }

@pytest.fixture
def sample_court():
    """Fixture pour une salle de test."""
    return {
        "id": "tennis_01",
        "sport": "tennis",
        "capacity": 4,
        "hourly_rate": 25.0,
        "available": True
    }
