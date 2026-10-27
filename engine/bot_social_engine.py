import os
from urllib.parse import urlencode

MARKER = os.environ.get("TRAVEL_PAYOUT_MARKER", "787950")


def build_tpst_link(domain: str, slug: str, label: str) -> str:
    base = f"https://{domain}.tp.st/{slug}"
    params = urlencode({"marker": MARKER, "sub_id": f"{label}_{MARKER}"})
    return f"{base}?{params}"


def generate_social_links():
    return {
        "airalo": build_tpst_link("airalo", "ZZoQC7Mz", "guide_airalo"),
        "airhelp": build_tpst_link("airhelp", "3ItXS0E4", "guide_airhelp"),
        "kiwitaxi": build_tpst_link("kiwitaxi", "tIZcbMOB", "guide_kiwitaxi"),
        "aviasales": build_tpst_link("aviasales", "Fb8U9yav", "guide_aviasales"),
        "tripcom": build_tpst_link("tripcom", "h3LrTZcS", "guide_tripcom"),
    }


def main():
    links = generate_social_links()
    print("TRTT Social Engine")
    print(f"Marker locked: {MARKER}")
    for name, link in links.items():
        print(f"{name}: {link}")


if __name__ == "__main__":
    main()
