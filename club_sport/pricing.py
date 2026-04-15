# Tarifs horaires def pour faire passer les tests
HOURLY_RATES = {
    "tennis": 25.0,
    "badminton": 20.0,
    "squash": 30.0
}

def calculate_price(sport: str, duration_hours: float) -> float:
    # Validation des entrées pour faire passer les tests d'exception
    if sport not in HOURLY_RATES:
        raise ValueError("Sport non supporté")
    
    if duration_hours <= 0:
        raise ValueError("La durée doit être positive")
    
    # Calcul simple pour faire passer les tests de base
    hourly_rate = HOURLY_RATES[sport]
    return hourly_rate * duration_hours
