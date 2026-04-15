"""
Module pour les appels API externes.
TDD Phase 2 : Implémentation pour faire passer les tests avec mock.
"""
import requests
from typing import Dict, Any, Optional

def fetch_reservations(auth_token: Optional[str] = None) -> Dict[str, Any]:
    """
    Récupère les réservations depuis l'API externe.
    
    Args:
        auth_token: Token d'authentification optionnel
        
    Returns:
        Dictionnaire avec le résultat de la requête
    """
    try:
        url = "https://api.club-sport.com/reservations"
        headers = {}
        
        # TDD : Gestion de l'authentification
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        
        response = requests.get(url, headers=headers, timeout=10)
        
        # TDD : Gestion des différents codes de statut
        if response.status_code in [200, 201]:
            return {
                "success": True,
                "reservations": response.json().get("reservations", []),
                "total": response.json().get("total", 0)
            }
        else:
            return {
                "success": False,
                "error": f"Erreur HTTP {response.status_code}",
                "status_code": response.status_code
            }
            
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Erreur de connexion réseau"
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Délai d'attente dépassé"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Erreur de requête: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}"
        }

def fetch_court_info(court_id: str) -> Dict[str, Any]:
    """
    Récupère les informations d'une salle depuis l'API externe.
    
    Args:
        court_id: Identifiant de la salle
        
    Returns:
        Dictionnaire avec le résultat de la requête
    """
    try:
        url = f"https://api.club-sport.com/courts/{court_id}"
        
        response = requests.get(url, timeout=10)
        
        # TDD : Gestion des différents codes de statut
        if response.status_code == 200:
            return {
                "success": True,
                "court": response.json()
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "error": "Salle non trouvée"
            }
        else:
            return {
                "success": False,
                "error": f"Erreur HTTP {response.status_code}",
                "status_code": response.status_code
            }
            
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Erreur de connexion réseau"
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Délai d'attente dépassé"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Erreur de requête: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}"
        }
