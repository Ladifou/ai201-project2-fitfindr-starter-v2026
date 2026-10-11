"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import config
from trace import step, start_trace, get_trace, check_iterations
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable
import json
import re
from mcp_client import call_tool


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Return the session.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """
    session = new_session(query, wardrobe)
    start_trace()

    # TODO: delete these two lines and build the loop.
    while session["error"] is None and session["fit_card"] is None:
        check_iterations(session.get("iterations", 0))
        
        session["iterations"] = session.get("iterations", 0) + 1

        try:        
            parsed_query = parse_query_with_model(session["query"])
            session["parsed"] = parsed_query
            
            #search_results = search_listings(parsed_query["description"], parsed_query["size"], parsed_query["max_price"])
            search_results = call_tool("search_listings", {
                "description": parsed_query["description"],
                "size": parsed_query["size"],
                "max_price": parsed_query["max_price"],
            })
            session["search_results"] = search_results
            step("search_listings", inputs={"query": query, "description": parsed_query["description"], "size": parsed_query["size"], "max_price": parsed_query["max_price"]}, returned=search_results)

            if not search_results:
                session["error"] = "No results found. Please try a different query."
                return session


            selected_item = search_results[0]
            session["selected_item"] = selected_item

            outfit_suggestion = suggest_outfit(selected_item, session["wardrobe"])
            session["outfit_suggestion"] = outfit_suggestion

            step(f"suggest_outfit: selected item: {selected_item.get('title')}", inputs={"item": selected_item, "wardrobe": session["wardrobe"]}, returned=outfit_suggestion)

            fit_card = create_fit_card(outfit_suggestion, selected_item)
            session["fit_card"] = fit_card

            step("create_fit_card", inputs={"outfit": outfit_suggestion, "item": selected_item}, returned=fit_card)
        except ModelUnavailable as e:
            session["error"] = str(e)
            return session

        
    get_trace()  # Get the trace after the loop ends



    return session

        

def parse_query(query: str) -> dict:
    """
    Parse a user query like:
      "vintage graphic tee under $30, size M"
    into:
      {
        "description": "vintage graphic tee",
        "size": "M",
        "max_price": 30.0
      }
    """
    q = query.strip()

    # 1) extract size
    size_match = re.search(r"\b(?:size|sz)\s*([A-Za-z0-9]+)\b", q, re.IGNORECASE)
    size = size_match.group(1).upper() if size_match else None

    # 2) extract price
    price_match = re.search(
        r"(?:under|up to|budget|max(?:imum)?(?: price)?)\s*\$?\s*(\d+(?:\.\d+)?)",
        q,
        re.IGNORECASE,
    )
    if not price_match:
        price_match = re.search(r"\$(\d+(?:\.\d+)?)", q)

    max_price = float(price_match.group(1)) if price_match else None

    # 3) remove size and price phrases from the description
    description = q
    if size_match:
        description = description[:size_match.start()] + description[size_match.end():]
    if price_match:
        description = description[:price_match.start()] + description[price_match.end():]

    # clean up extra punctuation/spaces
    description = re.sub(r"\s+", " ", description)
    description = description.replace(",", " ").strip(" -;:")
    description = re.sub(r"\s+", " ", description).strip()

    return {
        "description": description,
        "size": size,
        "max_price": max_price,
    }


from generate import generate

def parse_query_with_model(query: str) -> dict:
    """
    Use the model to parse:
      "vintage graphic tee under $30, size M"

    into:
      {
        "description": "vintage graphic tee",
        "size": "M",
        "max_price": 30.0
      }
    """
    system = """
    You convert shopping queries into JSON.

    Return ONLY valid JSON with exactly these keys:
    {
      "description": "short natural-language item description",
      "size": "size string or null",
      "max_price": number or null
    }

    Rules:
    - Keep only the item description in description.
    - If the query mentions a size, put it in size as a one, two, or three-character string capitalized.
    - If the query says "under $30" or "under 30 dollars", put 30.0 in max_price.
    - Use null when a value is missing.
    - Do not include markdown, explanation, or extra text.
    """

    raw = generate(
        prompt=f'Parse this query: "{query}"',
        system=system,
        cache=False,
        temperature=0.0,
    )

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Model returned invalid JSON: {raw}")

    return {
        "description": parsed.get("description") or "",
        "size": parsed.get("size"),
        "max_price": parsed.get("max_price"),
    }

# ── running it directly ───────────────────────────────────────────────────────


def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
