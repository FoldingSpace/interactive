# Attributions

Every external dataset, basemap, image, font, icon, and library used in this repository,
with its source and licence. Add the entry when the thing is added, not at the end of
term.

Each entry records: what it is, where it came from (a link that will still resolve),
the licence, the required attribution text, and which widgets use it.

## Our own materials

Code is MIT. Text, figures, and other non-code materials are CC BY 4.0.
See `LICENSE` and `LICENSE-CC-BY-4.0`.

**Credit** reads *Made by Luke Bergmann with Claude*, wherever a page carries a credit.
These widgets were built in conversation, and saying so is both accurate and more useful to
a reader than a single name.

**Copyright** is *Copyright (c) 2026 Luke Bergmann, where applicable* — the qualifier is
in the notice itself, not just described here. The two lines differ deliberately:
credit says who did the work, copyright says who holds the rights, and only the first is
shared. In most jurisdictions copyright requires a human author, so a second name on the
notice would not be generous — it would misstate who owns the work and muddy the licence
for anyone trying to reuse it. "Where applicable" carries its own weight: not everything
here is necessarily copyrightable in the first place.

## Data

### 2016 Census dissemination area and census tract boundaries, Vancouver
- Source: Statistics Canada, 2016 Census boundary files. Supplied inside the GEOG 370
  Lab 3 geodatabase (`MAUP.gdb`), already clipped to the City of Vancouver.
- Licence: Statistics Canada Open Licence,
  <https://www.statcan.gc.ca/en/reference/licence>
- Attribution required on screen: this is a value-added product, so the licence requires
  the *adapted from* wording: "Adapted from Statistics Canada, 2016 Census boundary files
  and census attribute data, 2016. This does not constitute an endorsement by Statistics
  Canada of this product."
- Used in: `web/maup`
- Added: 2026-08-21
- Notes: reprojected? No — kept in EPSG:3005, BC Albers, as supplied. Modified: geometry
  quantised to a 2 m grid and delta-encoded; census tracts are not shipped and are drawn
  by grouping dissemination areas.

### 2016 Census attributes: population, private households, median household income
- Source: Statistics Canada, 2016 Census attribute data, joined to the boundary files in
  the Lab 3 geodatabase.
- Licence: Statistics Canada Open Licence, as above.
- Attribution required on screen: covered by the same *adapted from* sentence.
- Used in: `web/maup`
- Added: 2026-08-21
- Notes: one dissemination area has both figures suppressed and is excluded from every
  model. Income for any grouped area is recomputed as a household-weighted mean of the
  dissemination areas' medians, which is not the published figure for a census tract.

### Police-reported crime incidents, City of Vancouver, 2015–2016
- Source: City of Vancouver Open Data Portal,
  <https://opendata.vancouver.ca/>. Supplied inside the Lab 3 geodatabase.
- Licence: Open Government Licence – Vancouver,
  <https://opendata.vancouver.ca/pages/licence/>
- Attribution required on screen: acknowledge the City of Vancouver as the source and
  name the licence. The widget's footer does both.
- Used in: `web/maup`
- Added: 2026-08-21
- Notes: four categories are counted per dissemination area — Theft of Bicycle (5,698),
  Theft from Vehicle (23,357), Break and Enter Commercial (5,143) and Mischief (8,791).
  The points themselves are not shipped. Incident locations were already generalised to the
  hundred-block level at source. Residential break and enter is deliberately excluded: it is
  the category the course lab asks students to model, and shipping it would publish the
  answers.

### Metro Vancouver Land Use 2016
- Source: "Landuse 2016 - Code Description", Metro Vancouver Open Data Portal,
  <https://open-data-portal-metrovancouver.hub.arcgis.com/>. Fetched from the ArcGIS
  feature service by `tools/lab4-extract.py`.
- Licence: Metro Vancouver Open Government Licence,
  <https://open-data-portal-metrovancouver.hub.arcgis.com/pages/Open%20Government%20Licence>
- Attribution required on screen: Metro Vancouver named as the source, and the licence
  named. The footer does both and adds that the grouping into eight classes is ours.
- Used in: `web/least-cost`
- Added: 2026-08-21
- Notes: not reprojected — it is published in NAD83 / UTM zone 10N (EPSG:26910), which is
  the grid's own projection. Modified: clipped to a 440 x 380 window of 50 m cells and
  the 29 land use codes grouped into 8 classes plus roads. That grouping is an editorial
  choice, is listed in `docs/widgets/least-cost.md`, and the page says it is ours. Cells
  are burned in a fixed order so the narrow and specific overwrite the broad — a school
  inside a park should read as a school.

### Deliberately not used: DMTI CanMap Route Logistics (Langley and Surrey)
The GEOG 370 Lab 4 geodatabase is built on DMTI CanMap Route Logistics, Markham, Ontario:
DMTI Spatial Inc. [2018]. DMTI data is licensed to institutions, not openly, so none of it
is shipped or drawn. The `web/least-cost` widget uses Metro Vancouver's open land use
instead. This is why the widget cannot reproduce the lab's own surface, and it turned out
to be a better widget for it: Metro Vancouver has an agricultural class and DMTI does not.

### Deliberately not used: City boundary (DMTI, 2006)
The Lab 3 geodatabase also contains a `City` layer credited to DMTI Spatial. DMTI data is
licensed to institutions, not openly, so it is not shipped and not drawn. The city's
outline in the widget is the outer edge of the dissemination areas.

## Basemaps and tiles

_(none yet)_

## Images and figures

_(none yet)_

## Fonts and icons

_(none yet)_

## Software

See `docs/libraries.md` for what we use and why. Licence text for anything bundled goes
in `vendor/LICENSES/` alongside the code.

---

### Entry template

```
### Name of the thing
- Source: URL
- Licence: name and URL
- Attribution required on screen: "exact text"
- Used in: web/widget-name
- Added: YYYY-MM-DD
- Notes: modifications made, if any
```

---

## Works cited in explanations

Every entry below has been through the adversarial check required by `principles.md`
section 11: a separate agent briefed to falsify each one, confirming the work exists, that
the details are exact, and that it supports the claim attached to it.

Checked 2026-08-20.

| Work | Cited for | Status |
|---|---|---|
| Moran, P.A.P. (1950) "Notes on Continuous Stochastic Phenomena." *Biometrika* 37(1–2): 17–23. | Where the measure comes from. | Verified |
| Tobler, W.R. (1970) "A Computer Movie Simulating Urban Growth in the Detroit Region." *Economic Geography* 46(sup1): 234–240. | Near things being more alike than distant ones. | Verified — the sentence was confirmed in the article text, and `sup1` is the correct issue, not the widely copied `46(2)`. |
| Anselin, L. (1995) "Local Indicators of Spatial Association — LISA." *Geographical Analysis* 27(2): 93–115. | Local Moran's I; that the local values sum to a multiple of the global one; the conditional permutation approach. | Verified, all three |
| Benjamini, Y. & Hochberg, Y. (1995) "Controlling the False Discovery Rate." *JRSS B* 57(1): 289–300. | The false discovery rate and the step-up procedure. | Verified |
| Caldas de Castro, M. & Singer, B.H. (2006) "Controlling the False Discovery Rate…" *Geographical Analysis* 38(2): 180–208. | FDR applied to local spatial statistics, and preferred to Bonferroni. | Verified |
| Cliff, A.D. & Ord, J.K. (1981) *Spatial Processes: Models and Applications*. London: Pion. | The standard treatment of spatial weights, rook's-case and queen's-case contiguity among them, and of the distribution theory behind Moran's I. | Verified after two rounds. Not cited as the origin of the terminology — see below. |

### Added 2026-08-21 for `web/least-cost`

Checked 2026-08-21. Two of the four came back needing the *claim* changed rather than the
citation — the third and worst failure mode in `principles.md` section 11, where the work is
real and cited correctly and does not say what it was put next to.

| Work | Cited for | Status |
|---|---|---|
| Goodchild, M.F. (1977) "An evaluation of lattice solutions to the problem of corridor location." *Environment and Planning A* 9(7): 727–738. | That a path found on a lattice does not converge on the continuous-space path, and that the difference depends on which moves the lattice permits. | Verified with correction. The check found the citation exact and the claim supported, but flagged that Goodchild compares several move sets rather than assuming eight, so the eight-neighbour case is an instance of his argument and not its premise. The panel was rewritten to separate our grid's eight directions from his general point. Abstract obtained independently from RePEc and from OpenAlex, agreeing word for word; the publisher page returns 403. |
| Pinto, N. & Keitt, T.H. (2009) "Beyond the least-cost path: evaluating corridor redundancy using a graph-theoretic approach." *Landscape Ecology* 24(2): 253–266. | That standard analysis reports one path although alternatives of comparable cost exist; and the two-way accumulated-cost method (Conditional Minimum Transit Cost). | Verified. The strongest of the four: the claim is close to the article's own sentence, "only a single path is identified, even though alternative paths with comparable costs might exist." Checked against the full PDF, not metadata. |
| Sieber, R. (2006) "Public participation geographic information systems: a literature review and framework." *Annals of the Association of American Geographers* 96(3): 491–507. | That whether a map widens a decision or only appears to is a long-running argument with its own literature, the "illusion of control" objection among its sharper forms. | Verified after correction. The claim first attached to it — that GIS opens a decision to the people affected — is the field's *contested* question, not Sieber's finding; she reports at length the objection that GIS "lends the illusion of control over decision making when actual control remains within the governing class." The widget now cites the argument rather than one side of it, and says so on screen. Checked against the full PDF. |
| Elwood, S. (2006) "Critical issues in participatory GIS: deconstructions, reconstructions, and new research directions." *Transactions in GIS* 10(5): 693–708. | That participatory GIS carries its own unresolved problems of access, equity and whose knowledge is represented, so participation is not by itself a fix. | Verified. Access, equity and the representation of spatial knowledge are named in the abstract and framing them as persistent is the paper's thesis. Abstract via OpenAlex; Wiley returns 403. |

### What the check caught

Two entries failed on the first round, and one more claim failed on the second. The
process is worth recording, because the second round changed the answer twice.

**Getis & Aldstadt (2004)** was cited for the consequences of choosing a spatial weights
matrix. The paper exists, its details were exact, and it does not make that argument — it
is a *constructive* paper proposing a way to **build** a weights matrix. **A real paper
attached to a claim it never made**, which is precisely the failure that survives a casual
read, and the reason this rule exists at all. Removed.

**Its proposed replacement, Getis (2009)**, was not accepted on the checker's word, because
proposing is not verifying. Sent back, it found the details exact but the piece to be a
short reflective commentary in a themed anniversary issue, closed access, with an abstract
merely *compatible* with the claim. It declined to certify from an abstract and reported
CANNOT CONFIRM. **Removed rather than hedged**, per the rule. The widget makes the point
by demonstration instead: checkerboard reads −1.00 under rook and −0.03 under queen.

**"Where the rook and queen terminology comes from" was dropped as a claim entirely.**
The second round found the terms in Cliff & Ord's own text — but also found them
presenting the chess names as a borrowed convention, and crediting rook's case to Moran
(1948) and Krishna Iyer (1949) and queen's case to Dacey (1965). No origination claim is
now attached to anything. The panel says the names come from chess, which is true and
claims nothing about who coined them.

**The checker retracted two of its own round-one findings.** It had recommended switching
to Cliff & Ord (1973) on the grounds that the 1981 volume might not contain the material;
on the second pass it read the 1981 text, found it there, and withdrew the recommendation —
so the original citation stands. It had also said Moran (1950) was not the origin of the
*test*; having obtained the full paper, it withdrew that too, since Moran defines I, names
it, derives its first two moments and argues asymptotic normality. What Cliff and Ord added
was the general weights matrix for irregular lattices.

An adversarial checker that will not correct itself is only half a check.

### Verified, then dropped

Both were cited on the extent control while it changed resolution. Once the control became
a clipped window, holding the square size fixed, they stopped being relevant: the
modifiable areal unit problem is about the size and drawing of the units, and clipping
changes neither. Rather than stretch them to fit, they were removed, and the extent panel
now carries no citation at all — which is the right answer when there is nothing verified
to point at.

| Work | Was cited for | Status |
|---|---|---|
| Openshaw, S. (1984) *The Modifiable Areal Unit Problem*. CATMOG 38. Norwich: Geo Books. | The scale effect. | Verified from the document itself; no longer cited. Some catalogues date it 1983. |
| Fotheringham, A.S. & Wong, D.W.S. (1991) *Environment and Planning A* 23(7): 1025–1044. | Results varying with scale and zoning. | Verified; no longer cited. Some databases corrupt the second author to "Wong, M.S."; D.W.S. is correct. |

### Cited in the documentation only

| Work | Cited for | Status |
|---|---|---|
| Benjamini, Y. & Yekutieli, D. (2001) *Annals of Statistics* 29(4): 1165–1188. | That BH controls FDR under positive regression dependency, which is why it is defensible for spatial data. | Verified |
| Westfall, P.H. & Young, S.S. (1993) *Resampling-Based Multiple Testing*. New York: Wiley. | The permutation minP/maxT procedures that account for dependence. | Verified. The short labels minP and maxT were popularised later, in the microarray literature; the procedures are theirs. |
