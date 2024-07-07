from utils.best_fit import best_fit
from utils.brute_force import brute_force
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