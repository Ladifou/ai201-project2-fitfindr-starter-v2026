# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

This project implements an agent that lets users query a desired outfit by providing brief description and optionally price ceiling and size (i.e: "a vintage graphic tee under $30, size M"). The agent searches listings, works out a suggestion, and writes a caption for it into a card.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Search the listing list based on description and optionally a size and a price ceiling
- **Inputs:** 'description' (string), 'size' (string), 'max_price' (float)
- **Returns:** Returns a list of matching listing/item dictionaries
- **When it has nothing:** It returns an empty list

### `suggest_outfit`

- **What it does:** Suggests one or two outfits based on the provided item and the user's wardrobe.
- **Inputs:** 'new_item' (dictionary), 'wardrobe' (dictionary)
- **Returns:** A string witht the outfit suggestion
- **When it has nothing:** Returns a general styling advice

### `create_fit_card`

- **What it does:** Writes a short caption someone would actually post about the find.
- **Inputs:** 'outfit' (string), 'new_item' (dictionary)
- **Returns:** A 2-4 sentence caption of the find.
- **When it has nothing:** Returns a descriptive message

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If no user wardrobe and/or item aren't provided as search fields/inputs for suggest_outfits, report on it and ask if the user would like a general suggestion. - agent.py::run_agent

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which --> The query is parsed by asking the model gemini-3.5-flash-lite

**What moves through the session:** <!-- which fields, in what order -->
The agent gets a query (string), parses it and returns description (str), size(str), and max_price(float)
search_listings(...) uses the previously returned fields and returns a list of listings/items (dict) into search_results.
if results exist, the first item is stored in selected_item, which is used by suggest_outfit(selected_item, wardrobe) to write outfit_suggestion (str). create_fit_card(...) uses the previous selected_item (listing) and outfit_suggestion (str) and writes fit_card's caption. if no matches, the session sets error, stops and notify.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'
Found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop

  Outfit:   Here are two ways to style your 2003 tour bootleg graphic tee using pieces from your wardrobe, ranging from a laid-back daytime look to an edgy evening outfit.

### Outfit 1: Effortless Y2K Streetwear (Daytime)
This look leans into the vintage, nostalgic vibe of the graphic tee by pairing it with relaxed denim and sporty layers.

*   **Top:** Graphic Tee (worn over your White ribbed tank top for a layered, textured look with the neckline peeking out).
*   **Bottom:** Baggy straight-leg jeans, dark wash.
*   **Footwear:** Chunky white sneakers.
*   **Outerwear:** Oversized grey crewneck sweatshirt (worn draped loosely over the shoulders or carried, just in case).
*   **Accessories:** Black crossbody bag.
*   **Why it works:** The baggy dark-wash jeans complement the loose, vintage aesthetic of the tour tee. Layering the white tank underneath adds dimension, while the chunky sneakers anchor the 2000s streetwear silhouette.

### Outfit 2: High-Low Contrast (Night Out / Edgy)
This outfit contrasts the casual, faded look of the band tee with tailored trousers and heavy outerwear for a cool, mixed-genre style.

*   **Top:** Graphic Tee (tucked slightly into the trousers).
*   **Bottom:** Wide-leg khaki trousers, paired with the Brown leather belt.
*   **Footwear:** Black combat boots.
*   **Outerwear:** Black cropped zip hoodie layered underneath your Vintage black denim jacket (double outerwear adds great texture and warmth).
*   **Accessories:** Black crossbody bag.
*   **Why it works:** Tucking the graphic tee into the structured wide-leg khakis creates a balanced silhouette that elevates the vintage tee from casual to deliberate. The combination of the brown belt, combat boots, and black denim jacket adds an edgy, rock-and-roll finish that matches the bootleg style.

  Fit card: Channel major 2003 nostalgia with this vintage tour bootleg graphic tee, priced at just $24. Style it casually for the daytime by layering it over a ribbed white tank with baggy dark-wash denim, or dress it up for the evening by tucking it into wide-leg khakis with combat boots. Grab this versatile streetwear staple on Depop to effortlessly elevate your everyday rotation!

1 model calls this session, 2 served from cache, 171 prompt + 32 output tokens

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L','condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navycrewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand':None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; ..."

python -c 'from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))'
Here are two distinct outfits featuring your vintage Levi's 501s and pieces from your wardrobe, playing with proportions and contrasting aesthetics.

### Outfit 1: Casual '90s Off-Duty (Sporty & Relaxed)
This look leans into the vintage Americana vibe of the 501s, contrasting the fitted, structured denim with relaxed, cozy layers.

*   **Top Layer:** Oversized grey crewneck sweatshirt
*   **Base Layer:** White ribbed tank top (let the white hem peek out slightly from under the grey crewneck for a styled layering effect)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag (worn high across the chest for a modern, urban touch)

*Why it works:* The medium wash of the 501s pairs naturally with grey and white for a clean, effortless palette. The oversized crewneck balances the straight, classic fit of the vintage jeans, while the chunky sneakers tie the casual, retro aesthetic together.

***

### Outfit 2: Edgy Contrast (Streetwear & Tough Textures)
This look juxtaposes the classic, timeless medium-wash denim with hard black accessories and cropped tailoring for a sharper, more directional silhouette.

*   **Top Layer:** Black cropped zip hoodie worn over the White ribbed tank top (leaving the bottom zip slightly open to show the white tank and waistline).
*   **Outerwear:** Vintage black denim jacket (layered over the hoodie for a double-denim texture play).
*   **Footwear:** Black combat boots (let the hems of the 501s break slightly over the tops of the boots).
*   **Accessories:** Brown leather belt (adding a warm contrast to the heavy black elements) and Black crossbody bag.

*Why it works:* Pairing medium-wash blue denim with black outerwear creates a high-contrast look. The cropped hoodie breaks up the torso and highlights the high waist of the 501s (accentuated by the brown belt), while the combat boots ground the outfit with a tough edge.
```

```
$ python -c "from tools import create_fit_card; ..."

 python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Nothing beats the classic fit of vintage Levi’s 501s in a timeless medium wash. Style them effortlessly with crisp white sneakers for that quintessential, off-duty cool look. Grab this wardrobe staple for just $38 before it's gone!
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- _What I asked for:_ I asked Copilot to implement a function that parses a query using a model to get descriptions, sizes, and max_price.
- _What came back:_ It produced a fairly accurate function that didn't account for fields formating. size as (S, M, L...)
- _What I changed:_ I updated a the rules that governed formatting such that a string 'small', 'medium', and large would translate to 'S', 'M', and 'L' respectively.

**Moment 2**

When attempting to test my parsing function with the command

```
python -c "from agent import parse_query_with_model; print(parse_query_with_model('vintage graphic tee under $30, size M'))"
```

The price was hilighted (green) different from other text and the output always had price as none.

- _What I asked for:_ I told Copilot that including the '$' (from a command it previously provided) causes the result to have max price as none/null.
- _What came back:_ It implemented a new function to normalize the input.
- _What I changed:_ I modified my prompt to include my command and mentioned that the '$' sign was hilighted.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion                                                                                                                                        | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | ----- | ----- | ----- | ----- | ----- | ------- |
| 1. matching query completes                                                                                                                      | 4 of 5 | pass  | pass  | pass  | pass  | pass  | MET     |
| 2. impossible query stops early                                                                                                                  | 5 of 5 | pass  | pass  | pass  | pass  | pass  | MET     |
| empty wardrobe _(diagnostic — not one of your five)_                                                                                             |        |       |       |       |       |       |         |
| 3. the selected item, from search listing, stored in session should be the same item passed to suggest_outfit in 5 of 5 tries                    | 5 of 5 | pass  | pass  | pass  | pass  | pass  | MET     |
| 4. if the query includes a price ceiling, at least 4 of 5 fit cards mention the item's price and that price is less than or equal to the ceiling | 4 od 5 | pass  | pass  | pass  | pass  | pass  | MET     |
| 5. the agent returns a clear “no items available” message instead of calling the model or crashing in 5 of 5 tries.                              | 5 of 5 | fail  | fail  | fail  | fail  | fail  | MISSED  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

**criteria 1:**

- File: agent.py
- Function: run_agent()

```
Here are two distinct outfits using the graphic tee and pieces from your wardrobe:

### Outfit 1: Streetwear Edge (Casual & Cool)
*This look leans into the vintage band-tee aesthetic by pairing it with denim and layering pieces for texture.*

*   **Top:** Graphic Tee (worn normally or slightly cropped)
*   **Bottoms:** Baggy straight-leg jeans with the Brown leather belt
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Bag:** Black crossbody bag
*   *Styling Tip:* Leave the denim jacket unbuttoned to show off the graphic, and let the baggy fit of the jeans pool slightly over the chunky sneakers for a 90s-inspired silhouette.

### Outfit 2: High-Low Contrast (Effortless & Elevated)
*This look juxtaposes the casual, worn-in feel of the graphic tee with tailored trousers for a modern, styled-without-trying look.*

*   **Top:** Graphic Tee (tucked in)
*   **Bottoms:** Wide-leg khaki trousers with the Brown leather belt
*   **Outerwear:** Black cropped zip hoodie (worn open or semi-zipped over the tee)
*   **Shoes:** Black combat boots
*   **Bag:** Black crossbody bag
*   *Styling Tip:* Tucking the graphic tee into the wide-leg khakis defines the waist, while the cropped hoodie adds a modern proportion play. Finishing with combat boots grounds the lighter khaki color.
Fit card:

Channel major 2000s tour energy with this vintage-style graphic tee, featuring that perfectly worn-in look we all search for. Dress it down with baggy denim and a black denim jacket for effortless streetwear vibes, or elevate it by tucking it into wide-leg khakis with combat boots.

**Price:** $24.00 | **Condition:** Thrifted & Mint 🎸✨
Trace:

[1] search_listings
      in:  dict with keys: query, description, size, max_price
      out: 8 items: Graphic Tee — 2003 Tour Bootleg Style, Y2K Baby Tee — Butterfly Print, Oversized Crewneck Sweatshirt — Vintage Navy … +5 more
[2] suggest_outfit: selected item Graphic Tee — 2003 Tour Bootleg Style
      in:  dict with keys: item, wardrobe
      out: Here are two distinct outfits using the graphic tee and pieces from your wardrobe:  ### Outfit 1: Streetwear E…
[3] create_fit_card
      in:  dict with keys: outfit, item
      out: Channel major 2000s tour energy with this vintage-style graphic tee, featuring that perfectly worn-in look we …

```

**Criteria 2: Impossible query stops early**

- File: agent.py
- Function: run_agent()

```
impossible query stops early
Query: designer ballgown size XXS under $5
Wardrobe: example
Try 1

stopped early: yes — No results found. Please try a different query.
selected_item: (none)
search_results: 0
Trace:

[1] search_listings
      in:  dict with keys: query, description, size, max_price
      out: [] (empty)
```

**Criteria 3: the selected item, from search listing, stored in session should be the same item passed to suggest_outfit in 5 of 5 tries**

- File: agent.py
- Function: run_agent()

```
Query: denim jacket under $50
Wardrobe: example
Try 1

stopped early: no
selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
search_results: 5
Outfit suggestion:

Here are two stylish ways to style your light wash cropped denim jacket using pieces from your wardrobe, playing with contrasting washes and silhouettes.

### Outfit 1: Effortless Streetwear (High-Contrast Denim)
*This look leans into the trendy "double denim" look by pairing the light wash jacket with your dark wash jeans, creating a balanced contrast.*

*   **Top:** White ribbed tank top (tucked in to define the waist).
*   **Bottoms:** Baggy straight-leg jeans (dark wash).
*   **Jacket:** Light wash cropped denim jacket (worn on top to highlight the high waist and contrast the dark wash).
*   **Footwear:** Chunky white sneakers.
*   **Accessories:** Black crossbody bag and the brown leather belt (to break up the look and add a touch of warmth).

### Outfit 2: Casual Cool (Layered & Textural)
*This outfit balances the structured, cropped nature of the jacket with relaxed, wide-leg trousers for an effortless, high-low aesthetic.*

*   **Top:** Oversized grey crewneck sweatshirt (let the bottom hem peek out slightly for dimension).
*   **Bottoms:** Wide-leg khaki trousers.
*   **Jacket:** Light wash cropped denim jacket (layered right over the grey crewneck to add structure and a pop of blue against the grey and khaki).
*   **Footwear:** Black combat boots (adds a slight edge to the softer khaki trousers).
*   **Accessories:** Black crossbody bag.
Fit card:

Elevate your wardrobe with this versatile light wash cropped denim jacket, priced at just $42! Perfectly structured to highlight the waist, it's easily styled up or down—whether you're rocking the trendy double-denim look with dark wash jeans or layering it over an oversized sweatshirt and khakis. Grab this thrifted staple on Poshmark to effortlessly nail that cool, high-low aesthetic!
Trace:

[1] search_listings
      in:  dict with keys: query, description, size, max_price
      out: 5 items: Denim Jacket — Light Wash, Cropped, 90s Track Jacket — Navy/White Stripe, High-Waisted Denim Shorts — Cutoff … +2 more
[2] suggest_outfit: selected item Denim Jacket — Light Wash, Cropped
      in:  dict with keys: item, wardrobe
      out: Here are two stylish ways to style your light wash cropped denim jacket using pieces from your wardrobe, playi…
[3] create_fit_card
      in:  dict with keys: outfit, item
      out: Elevate your wardrobe with this versatile light wash cropped denim jacket, priced at just $42! Perfectly struc…
```

**criteria 4:**

```
Query: denim jacket under $50
Wardrobe: example
Try 1

stopped early: no
selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
search_results: 5
Outfit suggestion:

Here are two stylish ways to style your light wash cropped denim jacket using pieces from your wardrobe:

### Outfit 1: Casual & Contrast-Play (Denim-on-Denim)
*This look plays with proportions by pairing the cropped light-wash jacket with voluminous, dark-wash denim for an effortless streetwear vibe.*

*   **Top:** White ribbed tank top
*   **Bottom:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Light wash, cropped denim jacket
*   **Footwear:** Chunky white sneakers
*   **Accessories:** Black crossbody bag, Brown leather belt (optional, to define the waist)

**Why it works:** The contrast between the light wash jacket and dark wash jeans creates visual interest, while the cropped length of the jacket balances the baggy fit of the trousers.

---

### Outfit 2: Elevated Smart-Casual
*This outfit balances relaxed elements with tailored trousers for a chic, high-low everyday look.*

*   **Top:** White ribbed tank top (layered under the black cropped zip hoodie worn open, or just the tank on its own depending on the weather)
*   **Bottom:** Wide-leg khaki trousers
*   **Outerwear:** Light wash, cropped denim jacket
*   **Footwear:** Black combat boots
*   **Accessories:** Black crossbody bag, Brown leather belt

**Why it works:** Khaki and light wash denim are a classic, earthy color combination. Tucking in the white tank with a brown belt adds polish, and the black combat boots ground the lighter tones of the outfit with a bit of edge.
Fit card:

Elevate your everyday wardrobe with this versatile light-wash, cropped denim jacket, priced at just $42! Perfectly proportioned for effortless layering, it pairs just as easily with baggy dark-wash denim for streetwear cool as it does with tailored khaki trousers for a smart-casual vibe. Grab this wardrobe staple today and unlock endless styling potential!
Trace:

[1] search_listings
      in:  dict with keys: query, description, size, max_price
      out: 5 items: Denim Jacket — Light Wash, Cropped, 90s Track Jacket — Navy/White Stripe, High-Waisted Denim Shorts — Cutoff … +2 more
[2] suggest_outfit: selected item Denim Jacket — Light Wash, Cropped
      in:  dict with keys: item, wardrobe
      out: Here are two stylish ways to style your light wash cropped denim jacket using pieces from your wardrobe:  ### …
[3] create_fit_card
      in:  dict with keys: outfit, item
      out: Elevate your everyday wardrobe with this versatile light-wash, cropped denim jacket, priced at just $42! Perfe…
```

**criteria 5:**

- File: agent.py
- Function: run_agent()

```
Query: denim jacket under $50
Wardrobe: example
Try 1

stopped early: no
selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
search_results: 5
Outfit suggestion:

Here are two stylish ways to style your light-wash cropped denim jacket using pieces from your wardrobe:

### Outfit 1: Casual & Layered (Streetwear Vibe)
*This look plays with proportions by pairing the cropped jacket with relaxed bottoms and layered textures.*

*   **Top:** White ribbed tank top (base layer) layered under the Oversized grey crewneck sweatshirt (with the collar and hem peeking out).
*   **Bottoms:** Baggy straight-leg jeans (dark wash) with the Brown leather belt to define the waist.
*   **Shoes:** Chunky white sneakers.
*   **Accessory:** Black crossbody bag.
*   **The Vibe:** Throw the **light-wash cropped denim jacket** over the oversized crewneck. The contrast between the dark wash jeans, light wash jacket, and grey sweatshirt creates a great denim-on-denim/neutral balance.

### Outfit 2: Elevated Contrast (Smart-Casual)
*This look balances the slouchy, professional feel of the wide-leg trousers with edgy, fitted layers.*

*   **Top:** White ribbed tank top tucked in.
*   **Bottoms:** Wide-leg khaki trousers with the Brown leather belt.
*   **Shoes:** Black combat boots (to add a tough edge to the clean trousers).
*   **Accessory:** Black crossbody bag.
*   **The Vibe:** Wear the **light-wash cropped denim jacket** buttoned or unbuttoned over the tank top. The cropped length of the jacket will hit right at the high waist of the wide-leg trousers, accentuating your waist while keeping the overall silhouette effortless and cool.
Fit card:

Upgrade your wardrobe with this versatile, light-wash cropped denim jacket, priced at just $42! Perfectly proportioned, it transitions effortlessly from a streetwear-inspired layered look with baggy jeans to a smart-casual vibe with wide-leg trousers. Grab this staple piece on Poshmark and instantly elevate your everyday style!
Trace:

[1] search_listings
      in:  dict with keys: query, description, size, max_price
      out: 5 items: Denim Jacket — Light Wash, Cropped, 90s Track Jacket — Navy/White Stripe, High-Waisted Denim Shorts — Cutoff … +2 more
[2] suggest_outfit: selected item Denim Jacket — Light Wash, Cropped
      in:  dict with keys: item, wardrobe
      out: Here are two stylish ways to style your light-wash cropped denim jacket using pieces from your wardrobe:  ### …
[3] create_fit_card
      in:  dict with keys: outfit, item
      out: Upgrade your wardrobe with this versatile, light-wash cropped denim jacket, priced at just $42! Perfectly prop…
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| #   | Criterion                                                                                                                  | Target | Verdict | How I decided                                                                                                           |
| --- | -------------------------------------------------------------------------------------------------------------------------- | ------ | ------- | ----------------------------------------------------------------------------------------------------------------------- |
| 1   | matching query completes                                                                                                   | 4 of 5 | MET     | All five tries completed after the query had a match in the wardrobe, which satisfies the 4 of 5 target                 |
| 2   | impossible query stops early                                                                                               | 4 of 5 | MET     | All five queries stopped early after the search_listing returned an empty list.                                         |
| 3   | the selected item, from search listing, stored in session should be the same item passed to suggest_outfit in 5 of 5 tries | 5 of 5 | MET     | Five tries had the suggest_outfit() tool have a selection from the list returned from search listing                    |
| 4   | at least 4 of 5 fit cards mention the item's price and that price is less than or equal to the mentioned ceiling           | 4 of 5 | MET     | All five tries from every matching query produced a fit_card with that mentioned the price, which was below the ceiling |
| 5   | the agent returns a clear “no items available” message instead of calling the model or crashing in 5 of 5 tries            | 5 of 5 | FAILED  | No tries were interupted early and neither produced a message of unavailability.                                        |

**Diagnoses**

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

(.venv) PS F:\CODEPATHAI201\ai201-project2-fitfindr-starter-v2026> python app.py ask 'tee under $30' --trace
[1] search_listings
      in:  dict with keys: query, description, size, max_price
      out: 5 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Low-Rise Cargo Pants — Khaki … +2 more
[2] suggest_outfit
      in:  dict with keys: item, wardrobe
      out: Here are two distinct outfits using your Y2K butterfly baby tee and pieces from your wardrobe:  ### Outfit 1: …
[3] create_fit_card
      in:  dict with keys: outfit, item
      out: Channel your inner 2000s icon with this nostalgic Y2K butterfly baby tee, featuring a cropped, fitted silhouet…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop
```

**Empty search**

```

(.venv) PS F:\CODEPATHAI201\ai201-project2-fitfindr-starter-v2026> python app.py ask '...' --trace
[1] search_listings
      in:  dict with keys: query, description, size, max_price
      out: [] (empty)

  No results found. Please try a different query.

1 model calls this session, 169 prompt + 25 output tokens

```

**On the MCP move:**

<!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
| --------- | ------ | ----- | ----- | ----- | ----- | ----- | ------- |
| 1.        |        |       |       |       |       |       |         |
| 2.        |        |       |       |       |       |       |         |
| 3.        |        |       |       |       |       |       |         |
| 4.        |        |       |       |       |       |       |         |
| 5.        |        |       |       |       |       |       |         |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

```

```
