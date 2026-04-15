def check_balance(current_balance: float, cost: float) -> bool:
    """
    Vérifie si le solde est suffisant pour une réservation.
    """
    # TDD : Validation des entrées
    if current_balance < 0:
        raise ValueError("Le solde ne peut être négatif")
    
    if cost < 0:
        raise ValueError("Le coût ne peut être négatif")
    
    # TDD : Logique simple
    return current_balance >= cost

def update_balance(current_balance: float, cost: float) -> float:
    """
    Met à jour le solde après une réservation.
    """
    # TDD : Validation des entrées
    if cost < 0:
        raise ValueError("Le montant ne peut être négatif")
    
    # TDD : Vérification des fonds suffisants
    if current_balance < cost:
        raise ValueError("Fonds insuffisants")
    
    # TDD : Calcul simple pour faire passer les tests
    return current_balance - cost
