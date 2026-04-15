"""
Tests avec mock pour les requêtes HTTP externes.
TDD : Tests qui simulent les appels API externes.
"""
import pytest
import requests_mock
from club_sport.external_api import fetch_reservations, fetch_court_info

class TestExternalAPIWithMock:
    """Test avec mock : simulation des appels API externes."""
    
    def test_fetch_reservations_success(self, requests_mock):
        """Objectif : Vérifier la récupération réussie des réservations.
        Type : Test avec mock de réponse HTTP 200.
        """
        # TDD : Simulation d'une réponse API réussie
        mock_response = {
            "reservations": [
                {"id": 1, "member_id": 101, "court_id": "tennis_01", "duration": 2.0},
                {"id": 2, "member_id": 102, "court_id": "badminton_01", "duration": 1.5}
            ],
            "total": 2
        }
        
        requests_mock.get(
            "https://api.club-sport.com/reservations",
            json=mock_response,
            status_code=200
        )
        
        # TDD : Cette fonction n'existe pas encore
        result = fetch_reservations()
        
        assert result["success"] is True
        assert len(result["reservations"]) == 2
        assert result["reservations"][0]["court_id"] == "tennis_01"
    
    def test_fetch_reservations_api_error(self, requests_mock):
        """Objectif : Vérifier la gestion d'erreur API.
        Type : Test avec mock de réponse HTTP 500.
        """
        requests_mock.get(
            "https://api.club-sport.com/reservations",
            status_code=500,
            text="Internal Server Error"
        )
        
        result = fetch_reservations()
        
        assert result["success"] is False
        assert "erreur" in result["error"].lower()
    
    def test_fetch_reservations_network_error(self, requests_mock):
        """Objectif : Vérifier la gestion d'erreur réseau.
        Type : Test avec mock d'exception réseau.
        """
        requests_mock.get(
            "https://api.club-sport.com/reservations",
            exc=requests.exceptions.ConnectionError("Connection failed")
        )
        
        result = fetch_reservations()
        
        assert result["success"] is False
        assert "réseau" in result["error"].lower() or "connexion" in result["error"].lower()
    
    def test_fetch_court_info_success(self, requests_mock):
        """Objectif : Vérifier la récupération des infos de salle.
        Type : Test avec mock de réponse HTTP 200.
        """
        mock_court = {
            "id": "tennis_01",
            "sport": "tennis",
            "capacity": 4,
            "hourly_rate": 25.0,
            "available": True
        }
        
        requests_mock.get(
            "https://api.club-sport.com/courts/tennis_01",
            json=mock_court,
            status_code=200
        )
        
        # TDD : Cette fonction n'existe pas encore
        result = fetch_court_info("tennis_01")
        
        assert result["success"] is True
        assert result["court"]["sport"] == "tennis"
        assert result["court"]["capacity"] == 4
    
    def test_fetch_court_info_not_found(self, requests_mock):
        """Objectif : Vérifier la gestion de salle non trouvée.
        Type : Test avec mock de réponse HTTP 404.
        """
        requests_mock.get(
            "https://api.club-sport.com/courts/unknown_court",
            status_code=404,
            json={"error": "Court not found"}
        )
        
        result = fetch_court_info("unknown_court")
        
        assert result["success"] is False
        assert "trouvée" in result["error"].lower() or "not found" in result["error"].lower()
    
    def test_fetch_reservations_with_auth(self, requests_mock):
        """Objectif : Vérifier l'authentification dans les requêtes.
        Type : Test avec mock de vérification d'en-têtes.
        """
        mock_response = {"reservations": [], "total": 0}
        
        # TDD : Vérification que le bon token est envoyé
        def match_auth_header(request):
            return request.headers.get("Authorization") == "Bearer secret_token_123"
        
        requests_mock.get(
            "https://api.club-sport.com/reservations",
            json=mock_response,
            status_code=200,
            additional_matcher=match_auth_header
        )
        
        result = fetch_reservations(auth_token="secret_token_123")
        
        assert result["success"] is True
    
    @pytest.mark.parametrize("status_code,should_succeed", [
        (200, True),
        (201, True),
        (400, False),
        (401, False),
        (403, False),
        (404, False),
        (500, False),
        (502, False)
    ])
    def test_fetch_reservations_status_codes(self, requests_mock, status_code, should_succeed):
        """Objectif : Vérifier la gestion des différents codes HTTP.
        Type : Test avec mock paramétré.
        """
        if should_succeed:
            requests_mock.get(
                "https://api.club-sport.com/reservations",
                json={"reservations": [], "total": 0},
                status_code=status_code
            )
        else:
            requests_mock.get(
                "https://api.club-sport.com/reservations",
                status_code=status_code
            )
        
        result = fetch_reservations()
        
        assert result["success"] == should_succeed

class TestExternalAPIIntegration:
    """Test d'intégration avec mock : combinaison API + réservation."""
    
    def test_complete_flow_with_external_data(self, requests_mock):
        """Objectif : Vérifier le flux complet avec données externes.
        Type : Test d'intégration avec mock.
        """
        # Mock des données externes
        mock_court = {
            "id": "tennis_01",
            "sport": "tennis",
            "capacity": 4,
            "hourly_rate": 25.0,
            "available": True
        }
        
        mock_reservations = {
            "reservations": [
                {"id": 1, "member_id": 101, "court_id": "tennis_01", "duration": 2.0}
            ],
            "total": 1
        }
        
        requests_mock.get(
            "https://api.club-sport.com/courts/tennis_01",
            json=mock_court,
            status_code=200
        )
        
        requests_mock.get(
            "https://api.club-sport.com/reservations",
            json=mock_reservations,
            status_code=200
        )
        
        # TDD : Test du flux combiné
        court_info = fetch_court_info("tennis_01")
        reservations = fetch_reservations()
        
        assert court_info["success"] is True
        assert reservations["success"] is True
        assert court_info["court"]["sport"] == "tennis"
        assert len(reservations["reservations"]) == 1
