"""
StudySync -- Session Scorer (Ticket 1, Tinker 1B).

TICKET: apply_streak_bonus() works but shouldn't live here -- it belongs in
the shared scoring_helpers module. session_rating() has no test coverage,
and neither function has been checked against bad input.

1. Write a pytest test for session_rating() BEFORE touching anything broken.
2. Move apply_streak_bonus() into scoring_helpers.py and fix the import here.
3. Find 2-3 "breaker" inputs for session_rating() and decide if they need handling.
"""
from scoring_helpers import apply_streak_bonus

def session_rating(combined_score: int) -> str:
    """Rate a study session from its combined minutes+focus score. Correct and tested."""
    if combined_score < 6 or combined_score > 100:
        return "invalid"
    if combined_score >= 90:
        return "Great"
    if combined_score >= 80:
        return "Good"
    if combined_score >= 70:
        return "OK"
    if combined_score >= 60:
        return "Meh"
    return "Skip"


# def apply_streak_bonus(combined_score: int, streak_days: int) -> int:
#     """Add a bonus for consecutive study days, capped at 100. Works fine -- it's just in the wrong file."""
#     boosted = combined_score + streak_days * 2
#     return min(boosted, 100)


def render_session_scorer_tab():
    import streamlit as st

    st.subheader("Score a Session")
    minutes = st.slider("Minutes studied", 0, 60, 30)
    focus = st.slider("Focus (0-60)", 0, 60, 30)
    streak = st.number_input("Current streak (days)", min_value=0, value=0, step=1)

    combined = minutes + focus
    boosted = apply_streak_bonus(combined, streak)
    rating = session_rating(boosted)
    st.metric("Rating", rating, help=f"Combined {combined} -> boosted {boosted}")


def run_demo():
    # sessions = [55, 68, 82, 91, 77]
    sessions = [55, 68, 82, 91, 77, -1, 105, 87.5, "hi", None]
    streak = 3
    for raw in sessions:
        if not isinstance(raw, (int, float)) or isinstance(raw, bool):
            print(f"Raw: {raw} -> Invalid input")
            continue
        boosted = apply_streak_bonus(raw, streak)
        rating = session_rating(boosted)
        print(f"Raw: {raw} -> Boosted: {boosted} -> Rating: {rating}")


if __name__ == "__main__":
    run_demo()
