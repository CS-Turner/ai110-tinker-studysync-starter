"""
StudySync -- Find a Study Spot (Ticket 3, Tinker 3B).

TICKET: none of the ranking logic is implemented yet -- every function
below is a stub.
"""

import csv

NOISE_ORDER = {"quiet": 0, "moderate": 1, "loud": 2}


def load_study_spots(csv_path: str) -> list:
    """
    Load study spots from a CSV into a list of dicts, converting
    "distance_miles" to float and "seats_available" to int.
    """
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        spots = list(csv.DictReader(csv_file))

    for spot in spots:
        spot["distance_miles"] = float(spot["distance_miles"])
        spot["seats_available"] = int(spot["seats_available"])

    return spots


def score_study_spot(profile: dict, spot: dict) -> tuple:
    """
    Score one study spot against a student profile.

    profile example: {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}

    Return (score, reasons) where reasons is a list of short strings
    explaining what contributed to the score, e.g. ["quiet enough", "close enough"].
    """
    score = 0.0
    reasons = []

    noise_level = spot["noise_level"]
    if NOISE_ORDER[noise_level] <= NOISE_ORDER[profile["max_noise"]]:
        noise_points = 2 - NOISE_ORDER[noise_level]
        score += noise_points
        reasons.append(f"{noise_level} noise (+{noise_points})")
    else:
        score -= 1
        reasons.append("too noisy (-1)")

    distance = spot["distance_miles"]
    max_distance = profile["max_distance"]
    if distance <= max_distance:
        if max_distance > 0:
            distance_points = 1 + (max_distance - distance) / max_distance
        else:
            distance_points = 1
        score += distance_points
        reasons.append(f"{distance:.1f} mi away (+{distance_points:.1f})")
    else:
        score -= 1
        reasons.append("too far (-1)")

    if spot["seats_available"] >= profile["min_seats"]:
        score += 1
        reasons.append("enough seats (+1)")
    else:
        score -= 1
        reasons.append("not enough seats (-1)")

    return score, reasons


def rank_study_spots(profile: dict, spots: list, k: int = 3) -> list:
    """
    Score every study spot, then return the top k as (spot, score, reasons)
    tuples, sorted by score descending.
    """
    scored_spots = [
        (spot, *score_study_spot(profile, spot))
        for spot in spots
    ]
    return sorted(scored_spots, key=lambda result: result[1], reverse=True)[:k]


def format_results(ranked: list) -> None:
    """Print each ranked study spot with its score and reasons, one line each."""
    for position, (spot, score, reasons) in enumerate(ranked, start=1):
        print(
            f"{position}. {spot['name']} -- Score: {score:.1f} "
            f"-- Because: {', '.join(reasons)}"
        )


def render_study_spot_tab():
    import streamlit as st

    st.subheader("Find a Study Spot")
    max_noise = st.selectbox("Max noise level", ["quiet", "moderate", "loud"], index=1)
    max_distance = st.slider("Max distance (miles)", 0.0, 3.0, 1.0)
    min_seats = st.number_input("Minimum seats needed", min_value=1, value=4, step=1)

    if st.button("Find spots"):
        profile = {"max_noise": max_noise, "max_distance": max_distance, "min_seats": min_seats}
        try:
            spots = load_study_spots("data/study_spots.csv")
            ranked = rank_study_spots(profile, spots, k=3)
            for spot, score, reasons in ranked:
                st.write(f"**{spot['name']}** -- Score: {score:.1f} -- Because: {', '.join(reasons)}")
        except NotImplementedError:
            st.warning("🚧 Ranking isn't implemented yet -- that's Tinker 3B's ticket.")


if __name__ == "__main__":
    spots = load_study_spots("data/study_spots.csv")
    profile = {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}
    ranked = rank_study_spots(profile, spots, k=3)
    format_results(ranked)
