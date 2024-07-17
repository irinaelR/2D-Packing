from utils.best_fit import best_fit
from utils.brute_force import brute_force, brute_force_2
from utils.brute_force_rotation import brute_force_rotation
from utils.next_fit import next_fit_dh
from utils.first_fit import first_fit_dh

class Utilitaire:

    @staticmethod
    def choose_fit(fit_string, rectangles, W, H):
        match fit_string:
            case "Next fit decreasing height (NFDH)":
                return next_fit_dh(rectangles, W, H)
            case "First fit decreasing height (FFDH)":
                return first_fit_dh(rectangles, W, H)
            case "Best fit":
                return best_fit(rectangles, W, H)
            case "Brute force":
                return brute_force(rectangles, W, H)
            case "Brute force avec rotation":
                return brute_force_rotation(rectangles, W, H)