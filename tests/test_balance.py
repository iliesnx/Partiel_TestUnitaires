import pytest
from club_sport.balance import check_balance, update_balance

class TestCheckBalance:
    """Test unitaire : vérification de la validité du solde."""
    
    def test_check_balance_sufficient(self):
        """Objectif : Vérifier qu'un solde suffisant autorise la réservation.
        Type : Test unitaire de cas nominal.
        """
        # TDD : Ce test va échouer car la fonction n'existe pas encore
        result = check_balance(100.0, 50.0)
        assert result is True
    
    def test_check_balance_insufficient(self):
        """Objectif : Vérifier qu'un solde insuffisant bloque la réservation.
        Type : Test unitaire de cas limite.
        """
        result = check_balance(30.0, 50.0)
        assert result is False
    
    def test_check_balance_exact_amount(self):
        """Objectif : Vérifier le cas limite du solde exact.
        Type : Test unitaire de cas limite.
        """
        result = check_balance(50.0, 50.0)
        assert result is True
    
    def test_check_balance_negative_balance(self):
        """Objectif : Vérifier gestion du solde négatif.
        Type : Test unitaire d'exception.
        """
        with pytest.raises(ValueError, match="Le solde ne peut être négatif"):
            check_balance(-10.0, 25.0)
    
    def test_check_balance_negative_cost(self):
        """Objectif : Vérifier gestion du coût négatif.
        Type : Test unitaire d'exception.
        """
        with pytest.raises(ValueError, match="Le coût ne peut être négatif"):
            check_balance(100.0, -25.0)

class TestUpdateBalance:
    """Test unitaire : mise à jour du solde après réservation."""
    
    def test_update_balance_deduct_cost(self):
        """Objectif : Vérifier la déduction du coût du solde.
        Type : Test unitaire de cas nominal.
        """
        # TDD : Ce test va échouer car la fonction n'existe pas encore
        new_balance = update_balance(100.0, 25.0)
        assert new_balance == 75.0
    
    def test_update_balance_full_balance(self):
        """Objectif : Vérifier la déduction complète du solde.
        Type : Test unitaire de cas limite.
        """
        new_balance = update_balance(50.0, 50.0)
        assert new_balance == 0.0
    
    def test_update_balance_insufficient_funds(self):
        """Objectif : Vérifier la gestion de fonds insuffisants.
        Type : Test unitaire d'exception.
        """
        with pytest.raises(ValueError, match="Fonds insuffisants"):
            update_balance(30.0, 50.0)
    
    def test_update_balance_negative_amount(self):
        """Objectif : Vérifier gestion du montant négatif.
        Type : Test unitaire d'exception.
        """
        with pytest.raises(ValueError, match="Le montant ne peut être négatif"):
            update_balance(100.0, -10.0)
    
    def test_update_balance_zero_cost(self):
        """Objectif : Vérifier le cas du coût nul.
        Type : Test unitaire de cas limite.
        """
        new_balance = update_balance(100.0, 0.0)
        assert new_balance == 100.0

@pytest.mark.parametrize("balance,cost,expected", [
    (100.0, 25.0, True),
    (50.0, 50.0, True),
    (30.0, 50.0, False),
    (0.0, 0.0, True)
])
def test_check_balance_parametrized(balance, cost, expected):
    """Objectif : Vérifier les cas de solde avec paramétrage.
    Type : Test unitaire paramétré.
    """
    result = check_balance(balance, cost)
    assert result == expected
