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


def iso3_to_iso2(iso3_code: str) -> str:
    """
    Convert an ISO 3166-1 alpha-3 country code to its corresponding
    alpha-2 code.

    Parameters
    ----------
    iso3_code : str
        The 3-letter ISO 3166-1 alpha-3 country code (e.g., 'ARG', 'USA').

    Returns
    -------
    str
        The 2-letter ISO 3166-1 alpha-2 country code.
    """
    country = pycountry.countries.get(alpha_3=iso3_code.upper())
    if country is None:
        raise ValueError("Country not found.")
    return country.alpha_2
