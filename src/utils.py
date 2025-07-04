import pycountry


def flag_from_iso3(iso3: str) -> str:
    """
    Converts a 3-letter ISO country code (ISO3) to its corresponding Unicode
    flag emoji.

    Parameters
    ----------
    iso3 : str
        The 3-letter ISO country code (e.g., 'USA', 'BRA', 'FRA').

    Returns
    -------
    str
        The Unicode flag emoji corresponding to the country code.
        Returns "Invalid ISO3 code" if the code is not recognized.
        Returns an error message string if an exception occurs.
    """
    try:
        country = pycountry.countries.get(alpha_3=iso3.upper())
        if not country:
            return "Invalid ISO3 code"
        iso2 = country.alpha_2.upper()
        return ''.join(chr(ord(char) + 127397) for char in iso2)
    except Exception as e:
        return f"Error: {e}"
