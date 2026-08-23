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
  the grid's own projection. Modified: clipped to a 990 x 818 window of 22 2/9 m cells and
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

### OpenStreetMap street network, Vancouver and the North Shore
- Source: OpenStreetMap, via the Overpass API — https://overpass-api.de/api/interpreter
- Licence: Open Database Licence 1.0 — https://opendatacommons.org/licenses/odbl/1-0/
- Attribution required on screen: "Streets from OpenStreetMap contributors, under the Open
  Database Licence."
- Used in: web/relative-distance
- Added: 2026-08-22
- Notes: extracted 2026-08-22 for 49.25–49.36 N, 123.22–123.00 W. Separately mapped
  sidewalks and pedestrian crossings (`footway=sidewalk`, `footway=crossing` and their
  kin) are dropped; service roads are not included; the rest is split at junctions,
  simplified to 6 m, and reduced to its largest connected part. The shipped `data.js` is
  a derived database and carries the ODbL with it. See
  `tools/relative-distance-extract.py` for the exact filter.

### High Resolution Digital Elevation Model, Lower Mainland 2016 (HRDEM)
- Source: Natural Resources Canada —
  https://ftp.maps.canada.ca/pub/elevation/dem_mne/highresolution_hauteresolution/dtm_mnt/1m/BC/Lower_Mainland_2016/
- Licence: Open Government Licence – Canada 2.0 —
  https://open.canada.ca/en/open-government-licence-canada
- Attribution required on screen: "Slopes from Natural Resources Canada, High Resolution
  Digital Elevation Model (Lower Mainland 2016)."
- Used in: web/relative-distance
- Added: 2026-08-22
- Notes: four 1 m bare-earth tiles (`w_0_145`, `w_0_146`, `w_1_145`, `w_1_146`) averaged
  to a 4 m mosaic. Slope is taken between the two ends of each street segment. Bridges and
  tunnels are forced flat, because a bare-earth model holds the water under a bridge and
  not the deck.

### Canadian Digital Elevation Model, NTS 092G (CDEM)
- Source: Natural Resources Canada —
  https://ftp.maps.canada.ca/pub/nrcan_rncan/elevation/cdem_mnec/092/cdem_dem_092G_tif.zip
- Licence: Open Government Licence – Canada 2.0
- Attribution required on screen: named beside HRDEM in the same footer line.
- Used in: web/relative-distance
- Added: 2026-08-22
- Notes: the fallback for 94 junctions at the northern edge of the window that fall
  outside the LiDAR mosaic, out of 24,410. It was the only elevation source at first, and
  measuring it against the LiDAR is what established that East Vancouver's five per cent
  street grades are real rather than model noise — see `docs/widgets/relative-distance.md`.

### Copernicus Sentinel-2 true-colour imagery, 12 August 2025
- Source: tiles `S2C_10UDV_20250812_0_L2A` and `S2C_10UEV_20250812_0_L2A`, level-2A
  true-colour product, via the AWS Open Data mirror `sentinel-cogs` —
  https://registry.opendata.aws/sentinel-2-l2a-cogs/
- Licence: Copernicus open and free data policy (Commission Delegated Regulation (EU)
  No 1159/2013) — reuse and redistribution permitted with attribution.
- Attribution required on screen: "Contains modified Copernicus Sentinel data 2025."
- Used in: web/relative-distance
- Added: 2026-08-22
- Notes: two tiles from the same satellite on the same day, both at 0% cloud, so there is
  no seam of date or sensor across the middle of the window. One tile alone does not cover
  it: 10UDV's swath stops on a diagonal about a third of the way in from the east. Clipped
  to 483000–501400 E, 5453100–5471200 N at 16 m, then stretched, desaturated and blended
  toward the map's land colour so that street lines survive on top of it — the exact
  numbers, and the contrast measurements that set them, are in
  `tools/relative-distance-extract.py` and `docs/widgets/relative-distance.md`.

### Deliberately not used: TransLink GTFS
- Considered for: a transit traveller, which would be the strongest case the widget could
  make, because the SeaBus turns the North Shore from the furthest part of the map into
  one of the nearest.
- **The first version of this entry said redistribution was not established. It is.** The
  TransLink Open API Terms of Use grant "a limited, revocable and non-exclusive license to
  use, reproduce, and redistribute the Data", and expressly contemplate modifications
  while retaining ownership of them.
- Not shipped because of the *shape* of that permission rather than its absence: revocable,
  gated on a written application naming who will use the data and where it will be
  distributed, capped at a thousand requests a day, terminable on ten days' notice, not
  sublicensable, and carrying a required on-screen disclaimer. A data file built from it
  could be published here and could not be reused by anyone else, which is what
  `principles.md` section 10 exists to protect.
- Unresolved: whether the static GTFS download falls under that instrument at all. The
  Terms define "the Data" as "any Open API".

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

### Added 2026-08-22 for `web/relative-distance`

Checked 2026-08-22 by an agent briefed to falsify, testing each entry three ways: does the
work exist, are the details exact, does it support the claim attached to it.

| Work | Cited for | Status |
|---|---|---|
| O'Sullivan, D. (2024) *Computing Geographically: Bridging Giscience and Geography*. New York: Guilford Press. | Chapter 2 on relative space; the sentence "It might take longer to travel from A to B than from B to A."; Figure 6.14 as a map of this kind for Santa Barbara. | Verified, with one correction taken — see below. |
| L'Hostis, A. & Abdou, F. (2021) "What Is the Shape of Geographical Time-Space? A Three-Dimensional Model Made of Curves and Cones." *ISPRS International Journal of Geo-Information* 10(5): 340. | That representing travel-time geometries as conventional maps is a hard problem. | Verified on all three tests. O'Sullivan cites this work for the same claim, in the same passage. |
| Tobler, W.R. (1993) "Three Presentations on Geographical Analysis and Modeling." NCGIA Technical Report 93-1. | Walking speed: W = 6 exp(−3.5 |S + 0.05|) km/h, with S the rise over the run. | Verified exactly, formula and constants, from the report itself. Two refinements taken — see below. |
| Wilson, D.G. & Schmidt, T., with contributions by J. Papadopoulos (2020) *Bicycling Science*, 4th edn. Cambridge, MA: MIT Press. | The cycling power equation: power spent on rolling resistance, air drag and climbing. | Verified, chapter 4. Authorship line corrected — see below. |
| US Access Board, *2010 ADA Standards for Accessible Design*, §403.3; CSA B651, *Accessible design for the built environment*. | That 5 in 100 is where a walking surface on an accessible route has to become a ramp. | Verified. **The claim attached to it was wrong and has been rewritten** — see below. |

### What the check caught, 2026-08-22

**The slope claim was wrong in the way that matters.** The page said 5 in 100 was "the
slope an accessible route is built to". It is not a design target; it is a ceiling, and
specifically the point at which a walking surface stops counting as one and has to be
built as a ramp with handrails and landings. Three authorities agree on 1:20 — ADA §403.3
("The running slope of walking surfaces shall not be steeper than 1:20"), CSA B651, and
the BC Building Code Article 3.8.3.2 — and all three allow a *ramp* to reach 1:12, which
the old wording implied was forbidden. Rewritten on the page and in the widget's file.

**Figure 6.14's caption is not what the companion website calls it.** The book's caption
reads "Santa Barbara street network and a redrawing of it based on relative travel times
over the network, from a central location." "Relative time map of the Santa Barbara street
network" is the website's label. Nothing here quotes either as a caption, but the
distinction is recorded so that nobody quotes the wrong one later.

**Tobler's function is scoped, and the page now says so.** He fitted it for walking on
paths in hilly terrain, estimated from Imhof (1950), and gives 3/5 as the multiplier for
off-path travel. Applying it to city pavement is a stretch; the panel now says what the
function is really lending the map is the shape of the curve. Tobler's own figure for
level ground is "5 km/hr"; 5.04 is what the formula computes and is not his number, so the
page says 5.

**Bicycling Science credits three people.** MIT Press's own title page reads "David Gordon
Wilson and Theodor Schmidt, with contributions by Jim Papadopoulos"; Wilson died in 2019,
after submitting the final draft. The citation now carries all three. The book's equation
also keeps a cos(α) on the rolling term and adds bump, acceleration and drivetrain
efficiency terms; what the widget uses is a small-angle, still-air, steady-state
simplification of it, and the widget's file says so.

**What could not be checked.** The checker could not reach a publisher-authorised digital
copy of *Computing Geographically*, so page numbers rest on mirrors whose internal
consistency was good but which are not authoritative. Nothing here cites a page number
from that book. Current editions of CSA B651 (2018 and 2023) are behind a paywall; the
provision was confirmed from the 2004 edition and from the BC Building Code, and the page
cites the standard without an edition-specific clause number.

### What the second round caught, 2026-08-22

The checker was sent after the fixes as well as after the citations, which is
`principles.md` section 5's rule, and it earned its keep three times.

**A framing asserted as a finding.** The widget's file and the extractor both said that
treating `oneway` as binding on foot would lose Vancouver its bridges for walkers. Run as
a counterfactual on the shipped graph, nothing becomes unreachable in either direction and
the largest cost is twelve minutes southbound. The rule is still right and the reason
given for it was invented. Corrected in both places, with the measurement.

**A licence claim that was never checked.** "I could not establish whether a derived
extract may be redistributed" was wrong about TransLink; the Terms address it directly and
permit it. See the entry above.

**A negative claim stated too broadly.** "No openly licensed record of Vancouver traffic
by time of day" is false as written: Statistics Canada tables 98-10-0504-01 and
98-10-0457-01 give commuting duration by time of departure and arrival for the Vancouver
CMA under the Statistics Canada Open Licence. Narrowed to speeds street by street and hour
by hour, which is what is actually missing.

**And one on the fix itself.** The corrected accessibility wording said a ramp needs
"handrails and landings". Landings are unconditional; handrails are required once the rise
exceeds 150 mm (2010 ADA §405.8, CSA B651 4.1.6.1(d)). Corrected on the page.

### What no checker caught, 2026-08-22

Neither adversarial round found this, and neither could have.

OpenStreetMap maps the Lions Gate crossing and its Stanley Park Causeway approach as a
pair of one-way cycleways. Believing that sent a northbound cyclist the long way round,
and `web/relative-distance` reported Park Royal at 57.7 minutes out against 20.0 back,
with the widget's own file explaining the gap as the causeway climb. It was a detour.
Corrected, it is 22.2 out and 20.0 back, and the asymmetry that remains really is hills.

`tools/relative-distance-verify.py` had reproduced the wrong figure to six decimal places,
because it reads the same data file. **An independent implementation tests the arithmetic
and cannot see a wrong input.** Luke, who cycles the bridge, said it takes bikes both ways.

Worth keeping beside `principles.md` section 11, which is about citations: the same failure
mode applies to data. A source can be real, correctly attributed, openly licensed, and
wrong about the thing you are using it for, and no amount of checking your own work will
show it.

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
