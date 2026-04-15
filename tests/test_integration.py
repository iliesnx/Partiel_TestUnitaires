import pytest
from club_sport.reservation import make_reservation, check_availability
from club_sport.pricing import calculate_price
from club_sport.balance import check_balance, update_balance

class TestReservationIntegration:
    """Test d'intégration : processus de réservation complet."""
    
    def test_complete_reservation_success(self):
        """Objectif : Vérifier une réservation complète réussie.
        Type : Test d'intégration de flux nominal.
        """
        # TDD : Ce test va échouer car les fonctions n'existent pas encore
        member = {"id": 1, "name": "Jean", "balance": 100.0}
        court = {"id": "tennis_01", "sport": "tennis", "available": True}
        duration = 2.0
        
        result = make_reservation(member, court, duration)
        
        # Vérifications 
        assert result["success"] is True
        assert result["reservation_id"] is not None
        assert result["total_cost"] == 50.0  # 25.0 * 2.0
        assert result["remaining_balance"] == 50.0  # 100.0 - 50.0
    
    def test_complete_reservation_insufficient_balance(self):
        """Objectif : Vérifier l'échec par solde insuffisant.
        Type : Test d'intégration de cas d'erreur.
        """
        member = {"id": 2, "name": "Marie", "balance": 20.0}
        court = {"id": "tennis_01", "sport": "tennis", "available": True}
        duration = 2.0
        
        result = make_reservation(member, court, duration)
        
        assert result["success"] is False
        assert "solde insuffisant" in result["error"].lower()
    
    def test_complete_reservation_court_unavailable(self):
        """Objectif : Vérifier l'échec par salle indisponible.
        Type : Test d'intégration de cas d'erreur.
        """
        member = {"id": 3, "name": "Paul", "balance": 100.0}
        court = {"id": "tennis_01", "sport": "tennis", "available": False}
        duration = 1.0
        
        result = make_reservation(member, court, duration)
        
        assert result["success"] is False
        assert "indisponible" in result["error"].lower()
    
    def test_complete_reservation_invalid_duration(self):
        """Objectif : Vérifier l'échec par durée invalide.
        Type : Test d'intégration de cas d'erreur.
        """
        member = {"id": 4, "name": "Sophie", "balance": 100.0}
        court = {"id": "tennis_01", "sport": "tennis", "available": True}
        duration = -1.0
        
        result = make_reservation(member, court, duration)
        
        assert result["success"] is False
        assert "durée" in result["error"].lower() or "positive" in result["error"].lower()

class TestAvailabilityIntegration:
    """Test d'intégration : vérification de disponibilité des salles."""
    
    def test_check_availability_available(self):
        """Objectif : Vérifier la disponibilité d'une salle.
        Type : Test d'intégration simple.
        """
        court = {"id": "badminton_01", "sport": "badminton", "capacity": 4, "available": True}
        
        # TDD : Cette fonction n'existe pas encore
        result = check_availability(court)
        
        assert result["available"] is True
        assert result["capacity"] == 4
    
    def test_check_availability_unavailable(self):
        """Objectif : Vérifier l'indisponibilité d'une salle.
        Type : Test d'intégration simple.
        """
        court = {"id": "squash_01", "sport": "squash", "capacity": 2, "available": False}
        
        result = check_availability(court)
        
        assert result["available"] is False
        assert result["capacity"] == 2

class TestMultiStepIntegration:
    """Test d'intégration : processus multi-étapes."""
    
    def test_price_calculation_to_balance_update_flow(self):
        """Objectif : Vérifier le flux calcul prix -> vérification solde -> mise à jour.
        Type : Test d'intégration de flux de données.
        """
        member_balance = 100.0
        sport = "tennis"
        duration = 2.0
        
        # Étape 1: Calcul du prix
        cost = calculate_price(sport, duration)
        assert cost == 50.0
        
        # Étape 2: Vérification du solde
        can_reserve = check_balance(member_balance, cost)
        assert can_reserve is True
        
        # Étape 3: Mise à jour du solde
        new_balance = update_balance(member_balance, cost)
        assert new_balance == 50.0
    
    @pytest.mark.parametrize("sport,duration,balance,expected_success", [
        ("tennis", 1.0, 30.0, True),
        ("badminton", 2.0, 35.0, True),
        ("squash", 1.5, 40.0, True),
        ("tennis", 2.0, 40.0, False),  # Solde insuffisant
        ("badminton", 3.0, 50.0, False)  # Solde insuffisant
    ])
    def test_reservation_scenarios_parametrized(self, sport, duration, balance, expected_success):
        """Objectif : Vérifier plusieurs scénarios de réservation.
        Type : Test d'intégration paramétré.
        """
        member = {"id": 1, "name": "Test", "balance": balance}
        court = {"id": f"{sport}_01", "sport": sport, "available": True}
        
        result = make_reservation(member, court, duration)
        
        assert result["success"] == expected_success
        
        if expected_success:
            assert result["total_cost"] == calculate_price(sport, duration)
            assert result["remaining_balance"] == balance - result["total_cost"]
