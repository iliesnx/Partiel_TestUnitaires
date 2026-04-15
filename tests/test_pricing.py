"""
Tests unitaires pour le calcul des prix de réservation.
TDD : On écrit les tests avant le code.
"""
import pytest
from club_sport.pricing import calculate_price

# TDD 1: Écriture des tests qui vont échouer dans tout les cas

class TestCalculatePrice:
    """Test unitaire : vérification du calcul du prix des réservations."""
    
    def test_calculate_price_basic_tennis(self):
        """Objectif : Vérifier le prix pour 1h de tennis.
        Type : Test unitaire simple.
        """
        # Ce test va échouer car la fonction n'existe pas encore
        price = calculate_price("tennis", 1.0)
        assert price == 25.0
    
    def test_calculate_price_basic_badminton(self):
        """Objectif : Vérifier le prix pour 1h de badminton.
        Type : Test unitaire simple.
        """
        price = calculate_price("badminton", 1.0)
        assert price == 20.0
    
    def test_calculate_price_basic_squash(self):
        """Objectif : Vérifier le prix pour 1h de squash.
        Type : Test unitaire simple.
        """
        price = calculate_price("squash", 1.0)
        assert price == 30.0
    
    def test_calculate_price_multiple_hours(self):
        """Objectif : Vérifier le calcul pour plusieurs heures.
        Type : Test unitaire avec paramètres multiples.
        """
        price = calculate_price("tennis", 2.5)
        assert price == 62.5  # 25.0 * 2.5
    
    def test_calculate_price_invalid_sport(self):
        """Objectif : Vérifier gestion des sports invalides.
        Type : Test unitaire d'exception.
        """
        with pytest.raises(ValueError, match="Sport non supporté"):
            calculate_price("football", 1.0)
    
    def test_calculate_price_negative_hours(self):
        """Objectif : Vérifier gestion des heures négatives.
        Type : Test unitaire d'exception.
        """
        with pytest.raises(ValueError, match="La durée doit être positive"):
            calculate_price("tennis", -1.0)
    
    @pytest.mark.parametrize("sport,expected_rate", [
        ("tennis", 25.0),
        ("badminton", 20.0),
        ("squash", 30.0)
    ])
    def test_calculate_price_parametrized(self, sport, expected_rate):
        """Objectif : Vérifier les taux horaires avec paramétrage.
        Type : Test unitaire paramétré.
        """
        price = calculate_price(sport, 1.0)
        assert price == expected_rate
