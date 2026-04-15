"""
Module de gestion des réservations.
TDD Phase 2 : Implémentation pour faire passer les tests d'intégration.
"""
import uuid
from .pricing import calculate_price
from .balance import check_balance, update_balance

def make_reservation(membre: dict, salle: dict, durée: float) -> dict:
    """
    Effectue une réservation complète.
    
    Args:
        membre: Informations de l'adhérent
        salle: Informations de la salle
        durée: Durée en heures
        
    Returns:
        Dictionnaire avec le résultat de la réservation
    """
    try:
        # TDD : Validation des entrées
        if durée <= 0:
            return {
                "success": False,
                "error": "La durée doit être positive"
            }
        
        if not salle.get("available", False):
            return {
                "success": False,
                "error": "Salle indisponible"
            }
        
        # TDD : Calcul du coût
        sport = salle["sport"]
        total_cost = calculate_price(sport, durée)
        
        # TDD : Vérification du solde
        current_balance = membre["balance"]
        if not check_balance(current_balance, total_cost):
            return {
                "success": False,
                "error": "Solde insuffisant"
            }
        
        # TDD : Mise à jour du solde
        new_balance = update_balance(current_balance, total_cost)
        
        # TDD : Réservation réussie
        return {
            "success": True,
            "reservation_id": str(uuid.uuid4()),
            "total_cost": total_cost,
            "remaining_balance": new_balance,
            "member_id": membre["id"],
            "court_id": salle["id"],
            "duration": durée
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur lors de la réservation: {str(e)}"
        }

def check_availability(salle: dict) -> dict:
    """
    Vérifie la disponibilité et la capacité d'une salle.
    
    Args:
        salle: Informations de la salle
        
    Returns:
        Dictionnaire avec les informations de disponibilité
    """
    return {
        "available": salle.get("available", False),
        "capacity": salle.get("capacity", 0),
        "sport": salle.get("sport", "unknown")
    }
