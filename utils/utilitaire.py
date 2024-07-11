from utils.brute_force import brute_force
from utils.heuristique import heuristique

class Utilitaire:

    @staticmethod
    def choose_fit(fit_string, formes, W, H):
        match fit_string:
            case "Heuristique":
                return heuristique(formes, W, H)
            case "Brute force":
                return brute_force(formes, W, H)