# Megafantasy — Project Context

Megafantasy is a private auction fantasy league app (see root `README.md` for
architecture/setup). This file holds reference data used across seasons —
keep it updated as real-world league rosters and schedules change.

Per-league scoring rules (points per win/loss, playoff rounds, etc.) live in
[docs/wiki/](docs/wiki/README.md), separate from the team/season reference
data below.

## Sports Leagues

Reference data for the leagues Megafantasy draws draftable teams from.
Team names here match `backend/app/seed.py`'s `Team.league` / `Team.name`
convention (league abbreviation + official team name). Update this section
and re-run/extend the seed script when rosters or schedules change season
to season (e.g. Premier League promotion/relegation each May).

### MLB (Major League Baseball) — 30 teams

**AL East:** Baltimore Orioles, Boston Red Sox, New York Yankees, Tampa Bay Rays, Toronto Blue Jays
**AL Central:** Chicago White Sox, Cleveland Guardians, Detroit Tigers, Kansas City Royals, Minnesota Twins
**AL West:** Athletics, Houston Astros, Los Angeles Angels, Seattle Mariners, Texas Rangers
**NL East:** Atlanta Braves, Miami Marlins, New York Mets, Philadelphia Phillies, Washington Nationals
**NL Central:** Chicago Cubs, Cincinnati Reds, Milwaukee Brewers, Pittsburgh Pirates, St. Louis Cardinals
**NL West:** Arizona Diamondbacks, Colorado Rockies, Los Angeles Dodgers, San Diego Padres, San Francisco Giants

Note: the Athletics play as "Athletics" (no city name) while transitioning
from Sacramento to a new Las Vegas ballpark; update once relocation completes.

**2026 season:** Opening Day March 25–26, 2026 → World Series concludes by
Oct 31, 2026 (Game 7, if necessary; regular season itself runs through
Sept 27, 2026).
**2027 season (next):** Opening Night March 24, 2027; traditional Opening
Day March 25, 2027 → regular season concludes Sept 26, 2027 (postseason/
World Series dates not yet announced).

### NFL (National Football League) — 32 teams

**AFC East:** Buffalo Bills, Miami Dolphins, New England Patriots, New York Jets
**AFC North:** Baltimore Ravens, Cincinnati Bengals, Cleveland Browns, Pittsburgh Steelers
**AFC South:** Houston Texans, Indianapolis Colts, Jacksonville Jaguars, Tennessee Titans
**AFC West:** Denver Broncos, Kansas City Chiefs, Las Vegas Raiders, Los Angeles Chargers
**NFC East:** Dallas Cowboys, New York Giants, Philadelphia Eagles, Washington Commanders
**NFC North:** Chicago Bears, Detroit Lions, Green Bay Packers, Minnesota Vikings
**NFC South:** Atlanta Falcons, Carolina Panthers, New Orleans Saints, Tampa Bay Buccaneers
**NFC West:** Arizona Cardinals, Los Angeles Rams, San Francisco 49ers, Seattle Seahawks

**2026 season:** Regular season Sept 9, 2026 → Jan 10, 2027; season concludes
with Super Bowl LXI on Feb 14, 2027 (SoFi Stadium, Inglewood, CA).
**2027 season (next):** Regular season expected to open ~Sept 4, 2027
(estimate — full schedule not yet released) → concludes with Super Bowl LXII
on Feb 13, 2028 (Mercedes-Benz Stadium, Atlanta, GA — date/venue confirmed).

### NBA (National Basketball Association) — 30 teams

**Atlantic:** Boston Celtics, Brooklyn Nets, New York Knicks, Philadelphia 76ers, Toronto Raptors
**Central:** Chicago Bulls, Cleveland Cavaliers, Detroit Pistons, Indiana Pacers, Milwaukee Bucks
**Southeast:** Atlanta Hawks, Charlotte Hornets, Miami Heat, Orlando Magic, Washington Wizards
**Northwest:** Denver Nuggets, Minnesota Timberwolves, Oklahoma City Thunder, Portland Trail Blazers, Utah Jazz
**Pacific:** Golden State Warriors, Los Angeles Clippers, Los Angeles Lakers, Phoenix Suns, Sacramento Kings
**Southwest:** Dallas Mavericks, Houston Rockets, Memphis Grizzlies, New Orleans Pelicans, San Antonio Spurs

Note: the NBA is exploring expansion to Seattle and Las Vegas, but commissioner
Adam Silver has targeted the **2028-29** season for that at the earliest — no
impact on the 2026-27 or 2027-28 rosters below.

**2026-27 season:** Regular season expected to open ~Oct 20, 2026 (projected —
opening night traditionally the third Tuesday of October; full schedule
release was still pending as of this writing) → NBA Finals expected to begin
~June 3, 2027 (estimate; best-of-seven, could run to ~June 20 if it goes the
distance).
**2027-28 season (next):** Regular season projected to open ~Oct 19, 2027
(estimate, schedule not yet released). Finals dates not yet available this
far out.

### NHL (National Hockey League) — 32 teams

**Atlantic:** Boston Bruins, Buffalo Sabres, Detroit Red Wings, Florida Panthers, Montreal Canadiens, Ottawa Senators, Tampa Bay Lightning, Toronto Maple Leafs
**Metropolitan:** Carolina Hurricanes, Columbus Blue Jackets, New Jersey Devils, New York Islanders, New York Rangers, Philadelphia Flyers, Pittsburgh Penguins, Washington Capitals
**Central:** Chicago Blackhawks, Colorado Avalanche, Dallas Stars, Minnesota Wild, Nashville Predators, St. Louis Blues, Utah Mammoth, Winnipeg Jets
**Pacific:** Anaheim Ducks, Calgary Flames, Edmonton Oilers, Los Angeles Kings, San Jose Sharks, Seattle Kraken, Vancouver Canucks, Vegas Golden Knights

Note: expansion beyond 32 teams (Houston/Atlanta/Texas markets floated) is
under discussion but not formally announced — no impact on the 2026-27 or
2027-28 rosters below. Utah's franchise plays as "Utah Mammoth" (renamed
from the placeholder "Utah Hockey Club" in 2025, after relocating from
Arizona in 2024).

**2026-27 season:** Regular season Sept 29, 2026 → April 10, 2027 (84-game
schedule, the first since 1993-94) → Stanley Cup Final expected to conclude
mid-to-late June 2027 (exact date not yet set).
**2027-28 season (next):** Not yet announced — the NHL typically releases
the following season's schedule mid-year; check back closer to mid-2027.

### NCAAF (NCAA Division I FBS College Football) — 138 teams, 2026 season

Team pool is every school eligible for a Division I bowl game, i.e. every
FBS (Football Bowl Subdivision) member — not FCS. Conference realignment
was significant for 2026 (Pac-12 rebuilt to 8 members, Mountain West lost
5 schools/gained 3, two schools moved up from FCS), so this list reflects
2026 alignment specifically; re-verify before reusing in a future season.

**SEC (16):** Alabama Crimson Tide, Arkansas Razorbacks, Auburn Tigers, Florida Gators, Georgia Bulldogs, Kentucky Wildcats, LSU Tigers, Mississippi State Bulldogs, Missouri Tigers, Oklahoma Sooners, Ole Miss Rebels, South Carolina Gamecocks, Tennessee Volunteers, Texas Longhorns, Texas A&M Aggies, Vanderbilt Commodores
**Big Ten (18):** Illinois Fighting Illini, Indiana Hoosiers, Iowa Hawkeyes, Maryland Terrapins, Michigan Wolverines, Michigan State Spartans, Minnesota Golden Gophers, Nebraska Cornhuskers, Northwestern Wildcats, Ohio State Buckeyes, Oregon Ducks, Penn State Nittany Lions, Purdue Boilermakers, Rutgers Scarlet Knights, UCLA Bruins, USC Trojans, Washington Huskies, Wisconsin Badgers
**ACC (17):** Boston College Eagles, California Golden Bears, Clemson Tigers, Duke Blue Devils, Florida State Seminoles, Georgia Tech Yellow Jackets, Louisville Cardinals, Miami (FL) Hurricanes, NC State Wolfpack, North Carolina Tar Heels, Pittsburgh Panthers, SMU Mustangs, Stanford Cardinal, Syracuse Orange, Virginia Cavaliers, Virginia Tech Hokies, Wake Forest Demon Deacons
**Big 12 (16):** Arizona Wildcats, Arizona State Sun Devils, Baylor Bears, BYU Cougars, Cincinnati Bearcats, Colorado Buffaloes, Houston Cougars, Iowa State Cyclones, Kansas Jayhawks, Kansas State Wildcats, Oklahoma State Cowboys, TCU Horned Frogs, Texas Tech Red Raiders, UCF Knights, Utah Utes, West Virginia Mountaineers
**Pac-12 (8):** Boise State Broncos, Colorado State Rams, Fresno State Bulldogs, Oregon State Beavers, San Diego State Aztecs, Texas State Bobcats, Utah State Aggies, Washington State Cougars
**Mountain West (10):** Air Force Falcons, Hawaii Rainbow Warriors, Nevada Wolf Pack, New Mexico Lobos, North Dakota State Bison, Northern Illinois Huskies, San Jose State Spartans, UNLV Rebels, UTEP Miners, Wyoming Cowboys
**American (14):** Army Black Knights, Charlotte 49ers, East Carolina Pirates, Florida Atlantic Owls, Memphis Tigers, Navy Midshipmen, North Texas Mean Green, Rice Owls, South Florida Bulls, Temple Owls, Tulane Green Wave, Tulsa Golden Hurricane, UAB Blazers, UTSA Roadrunners
**Sun Belt (14):** Appalachian State Mountaineers, Arkansas State Red Wolves, Coastal Carolina Chanticleers, Georgia Southern Eagles, Georgia State Panthers, James Madison Dukes, Louisiana Ragin' Cajuns, Louisiana-Monroe Warhawks, Louisiana Tech Bulldogs, Marshall Thundering Herd, Old Dominion Monarchs, South Alabama Jaguars, Southern Miss Golden Eagles, Troy Trojans
**MAC (13):** Akron Zips, Ball State Cardinals, Bowling Green Falcons, Buffalo Bulls, Central Michigan Chippewas, Eastern Michigan Eagles, Kent State Golden Flashes, Miami (OH) RedHawks, Ohio Bobcats, Sacramento State Hornets, Toledo Rockets, UMass Minutemen, Western Michigan Broncos
**Conference USA (10):** Delaware Blue Hens, FIU Panthers, Jacksonville State Gamecocks, Kennesaw State Owls, Liberty Flames, Middle Tennessee Blue Raiders, Missouri State Bears, New Mexico State Aggies, Sam Houston Bearkats, Western Kentucky Hilltoppers
**FBS Independents (2):** Notre Dame Fighting Irish, UConn Huskies

Notable 2026 realignment: Boise State, Colorado State, Fresno State, San
Diego State, and Utah State left Mountain West for the rebuilt Pac-12;
Mountain West backfilled with Northern Illinois and UTEP (both from other
conferences) plus North Dakota State (up from FCS); Sacramento State also
moved up from FCS, replacing Northern Illinois in the MAC; Louisiana Tech
moved from Conference USA to Sun Belt.

**2026 season:** Week 0 starts Thursday Aug 27, 2026 → College Football
Playoff National Championship Jan 25, 2027 (Allegiant Stadium, Las Vegas).
**2027 season (next):** Scheduled to open ~Aug 28, 2027 (Week 0) — though an
NCAA oversight committee has proposed eliminating Week 0 and starting the
season a week earlier starting in 2027, not yet finalized → concludes with
the National Championship Jan 24, 2028 (Caesars Superdome, New Orleans —
confirmed).

### NCAAMB (NCAA Division I Men's Basketball) — 364 teams, 2026-27 season

Team pool is every Division I men's basketball program (all are NCAA
tournament-eligible — unlike bowl eligibility in football, D-I basketball
has no minimum-wins gate). 2026-27 saw heavy realignment (Pac-12 basketball
rebuilt as a 9-team conference including Gonzaga, which fields no football
team; the WAC dissolved into the Big Sky/Big West/new United Athletic
Conference); this list reflects 2026-27 alignment specifically.

**Major conferences** (for roster-cap purposes, see `docs/wiki/game-rules-ncaamb.md`):
SEC, Big Ten, ACC, Big 12, Big East. All other conferences below are minor.

**America East (9):** Albany Great Danes, Binghamton Bearcats, Bryant Bulldogs, Maine Black Bears, UMBC Retrievers, UMass Lowell River Hawks, New Hampshire Wildcats, NJIT Highlanders, Vermont Catamounts
**American (13):** Charlotte 49ers, East Carolina Pirates, Florida Atlantic Owls, Memphis Tigers, North Texas Mean Green, Rice Owls, South Florida Bulls, Temple Owls, Tulane Green Wave, Tulsa Golden Hurricane, UAB Blazers, UTSA Roadrunners, Wichita State Shockers
**ACC (18) — major:** Boston College Eagles, California Golden Bears, Clemson Tigers, Duke Blue Devils, Florida State Seminoles, Georgia Tech Yellow Jackets, Louisville Cardinals, Miami (FL) Hurricanes, North Carolina Tar Heels, NC State Wolfpack, Notre Dame Fighting Irish, Pittsburgh Panthers, SMU Mustangs, Stanford Cardinal, Syracuse Orange, Virginia Cavaliers, Virginia Tech Hokies, Wake Forest Demon Deacons
**ASUN (8):** Bellarmine Knights, Florida Gulf Coast Eagles, Jacksonville Dolphins, Lipscomb Bisons, North Florida Ospreys, Queens Royals, Stetson Hatters, West Florida Argonauts
**Atlantic 10 (14):** Davidson Wildcats, Dayton Flyers, Duquesne Dukes, Fordham Rams, George Mason Patriots, George Washington Revolutionaries, La Salle Explorers, Loyola Chicago Ramblers, Rhode Island Rams, Richmond Spiders, Saint Joseph's Hawks, Saint Louis Billikens, St. Bonaventure Bonnies, VCU Rams
**Big East (11) — major:** Butler Bulldogs, UConn Huskies, Creighton Bluejays, DePaul Blue Demons, Georgetown Hoyas, Marquette Golden Eagles, Providence Friars, St. John's Red Storm, Seton Hall Pirates, Villanova Wildcats, Xavier Musketeers
**Big Sky (11):** Eastern Washington Eagles, Idaho Vandals, Idaho State Bengals, Montana Grizzlies, Montana State Bobcats, Northern Arizona Lumberjacks, Northern Colorado Bears, Portland State Vikings, Southern Utah Thunderbirds, Utah Tech Trailblazers, Weber State Wildcats
**Big South (9):** Charleston Southern Buccaneers, Gardner-Webb Runnin' Bulldogs, High Point Panthers, Longwood Lancers, Presbyterian Blue Hose, Radford Highlanders, UNC Asheville Bulldogs, USC Upstate Spartans, Winthrop Eagles
**Big Ten (18) — major:** Illinois Fighting Illini, Indiana Hoosiers, Iowa Hawkeyes, Maryland Terrapins, Michigan Wolverines, Michigan State Spartans, Minnesota Golden Gophers, Nebraska Cornhuskers, Northwestern Wildcats, Ohio State Buckeyes, Oregon Ducks, Penn State Nittany Lions, Purdue Boilermakers, Rutgers Scarlet Knights, UCLA Bruins, USC Trojans, Washington Huskies, Wisconsin Badgers
**Big 12 (16) — major:** Arizona Wildcats, Arizona State Sun Devils, Baylor Bears, BYU Cougars, Cincinnati Bearcats, Colorado Buffaloes, Houston Cougars, Iowa State Cyclones, Kansas Jayhawks, Kansas State Wildcats, Oklahoma State Cowboys, TCU Horned Frogs, Texas Tech Red Raiders, UCF Knights, Utah Utes, West Virginia Mountaineers
**Big West (12):** California Baptist Lancers, Cal Poly Mustangs, Cal State Bakersfield Roadrunners, Cal State Fullerton Titans, Cal State Northridge Matadors, Long Beach State Beach, Sacramento State Hornets, UC Irvine Anteaters, UC Riverside Highlanders, UC San Diego Tritons, UC Santa Barbara Gauchos, Utah Valley Wolverines
**CAA (13):** Campbell Fighting Camels, Charleston Cougars, Drexel Dragons, Elon Phoenix, Hampton Pirates, Hofstra Pride, Monmouth Hawks, NC A&T Aggies, Northeastern Huskies, Stony Brook Seawolves, Towson Tigers, UNC Wilmington Seahawks, William & Mary Tribe
**Conference USA (10):** Delaware Blue Hens, FIU Panthers, Jacksonville State Gamecocks, Kennesaw State Owls, Liberty Flames, Middle Tennessee Blue Raiders, Missouri State Bears, New Mexico State Aggies, Sam Houston Bearkats, Western Kentucky Hilltoppers
**Horizon League (12):** Cleveland State Vikings, Detroit Mercy Titans, Green Bay Phoenix, IU Indy Jaguars, Milwaukee Panthers, Northern Illinois Huskies, Northern Kentucky Norse, Oakland Golden Grizzlies, Purdue Fort Wayne Mastodons, Robert Morris Colonials, Wright State Raiders, Youngstown State Penguins
**Ivy League (8):** Brown Bears, Columbia Lions, Cornell Big Red, Dartmouth Big Green, Harvard Crimson, Penn Quakers, Princeton Tigers, Yale Bulldogs
**Metro (formerly MAAC) (12):** Canisius Golden Griffins, Fairfield Stags, Iona Gaels, Manhattan Jaspers, Marist Red Foxes, Merrimack Warriors, Mount St. Mary's Mountaineers, Niagara Purple Eagles, Quinnipiac Bobcats, Rider Broncs, Sacred Heart Pioneers, Siena Saints
**MAC (12):** Akron Zips, Ball State Cardinals, Bowling Green Falcons, Buffalo Bulls, Central Michigan Chippewas, Eastern Michigan Eagles, Kent State Golden Flashes, UMass Minutemen, Miami (OH) RedHawks, Ohio Bobcats, Toledo Rockets, Western Michigan Broncos
**MEAC (8):** Coppin State Eagles, Delaware State Hornets, Howard Bison, Maryland Eastern Shore Hawks, Morgan State Bears, Norfolk State Spartans, North Carolina Central Eagles, South Carolina State Bulldogs
**Missouri Valley (11):** Belmont Bruins, Bradley Braves, Drake Bulldogs, Evansville Purple Aces, Illinois State Redbirds, Indiana State Sycamores, Murray State Racers, Northern Iowa Panthers, Southern Illinois Salukis, UIC Flames, Valparaiso Beacons
**Mountain West (10):** Air Force Falcons, Grand Canyon Antelopes, UC Davis Aggies, Hawaii Rainbow Warriors, Nevada Wolf Pack, UNLV Rebels, New Mexico Lobos, San Jose State Spartans, UTEP Miners, Wyoming Cowboys
**NEC (9):** Central Connecticut Blue Devils, Chicago State Cougars, Fairleigh Dickinson Knights, Le Moyne Dolphins, LIU Sharks, Mercyhurst Lakers, New Haven Chargers, Stonehill Skyhawks, Wagner Seahawks
**OVC (9):** Eastern Illinois Panthers, Lindenwood Lions, Morehead State Eagles, Southeast Missouri State Redhawks, SIU Edwardsville Cougars, Southern Indiana Screaming Eagles, Tennessee State Tigers, UT Martin Skyhawks, Western Illinois Leathernecks
**Pac-12 (9):** Boise State Broncos, Colorado State Rams, Fresno State Bulldogs, Gonzaga Bulldogs, Oregon State Beavers, San Diego State Aztecs, Texas State Bobcats, Utah State Aggies, Washington State Cougars
**Patriot League (10):** American Eagles, Army Black Knights, Boston University Terriers, Bucknell Bison, Colgate Raiders, Holy Cross Crusaders, Lafayette Leopards, Lehigh Mountain Hawks, Loyola Maryland Greyhounds, Navy Midshipmen
**SEC (16) — major:** Alabama Crimson Tide, Arkansas Razorbacks, Auburn Tigers, Florida Gators, Georgia Bulldogs, Kentucky Wildcats, LSU Tigers, Ole Miss Rebels, Mississippi State Bulldogs, Missouri Tigers, Oklahoma Sooners, South Carolina Gamecocks, Tennessee Volunteers, Texas Longhorns, Texas A&M Aggies, Vanderbilt Commodores
**SoCon (11):** Chattanooga Mocs, The Citadel Bulldogs, East Tennessee State Buccaneers, Furman Paladins, Mercer Bears, Samford Bulldogs, UNC Greensboro Spartans, Tennessee Tech Golden Eagles, VMI Keydets, Western Carolina Catamounts, Wofford Terriers
**Southland (12):** East Texas A&M Lions, Houston Christian Huskies, Incarnate Word Cardinals, Lamar Cardinals, New Orleans Privateers, McNeese State Cowboys, Nicholls State Colonels, Northwestern State Demons, Southeastern Louisiana Lions, Stephen F. Austin Lumberjacks, Texas A&M-Corpus Christi Islanders, UT Rio Grande Valley Vaqueros
**SWAC (12):** Alabama A&M Bulldogs, Alabama State Hornets, Alcorn State Braves, Arkansas-Pine Bluff Golden Lions, Bethune-Cookman Wildcats, Florida A&M Rattlers, Grambling State Tigers, Jackson State Tigers, Mississippi Valley State Delta Devils, Prairie View A&M Panthers, Southern Jaguars, Texas Southern Tigers
**Summit League (8):** Kansas City Roos, North Dakota Fighting Hawks, North Dakota State Bison, Omaha Mavericks, Oral Roberts Golden Eagles, St. Thomas Tommies, South Dakota Coyotes, South Dakota State Jackrabbits
**Sun Belt (14):** Appalachian State Mountaineers, Coastal Carolina Chanticleers, Georgia Southern Eagles, Georgia State Panthers, James Madison Dukes, Marshall Thundering Herd, Old Dominion Monarchs, Arkansas State Red Wolves, Louisiana Ragin' Cajuns, Louisiana-Monroe Warhawks, Louisiana Tech Bulldogs, South Alabama Jaguars, Southern Miss Golden Eagles, Troy Trojans
**United Athletic Conference (9):** Abilene Christian Wildcats, Austin Peay Governors, Central Arkansas Bears, Eastern Kentucky Colonels, Little Rock Trojans, North Alabama Lions, Tarleton State Texans, UT Arlington Mavericks, West Georgia Wolves
**WCC (10):** Denver Pioneers, Loyola Marymount Lions, Pacific Tigers, Pepperdine Waves, Portland Pilots, Saint Mary's Gaels, San Diego Toreros, San Francisco Dons, Santa Clara Broncos, Seattle Redhawks

Note: The Citadel and VMI (both SoCon) field men's basketball but not
women's — the only two D-I schools with that asymmetry, hence the 2-team
gap between the men's (364) and women's (362) team counts below.

**2026-27 season:** Nov 1, 2026 → National Championship April 5, 2027 (Ford
Field, Detroit — first year of the expanded 76-team tournament format).
**2027-28 season (next):** Not yet officially scheduled; historically opens
early November with the championship in early April.

### NCAAWB (NCAA Division I Women's Basketball) — 362 teams, 2026-27 season

Same 31 conferences and team pool as NCAAMB above, minus The Citadel and
VMI (see note above) — every other program fields both a men's and women's
D-I team, so rather than duplicate all 362 names here, treat NCAAWB's roster
as NCAAMB's list minus those two schools. Major/minor conference split for
the roster cap is identical to NCAAMB's.

**2026-27 season:** Nov 1, 2026 → National Championship April 4, 2027
(Nationwide Arena, Columbus — also the first expanded 76-team field).
**2027-28 season (next):** Not yet officially scheduled.

### EPL (English Premier League) — 20 teams, 2026/27 season

Arsenal, Aston Villa, Bournemouth, Brentford, Brighton & Hove Albion,
Chelsea, Coventry City, Crystal Palace, Everton, Fulham, Hull City,
Ipswich Town, Leeds United, Liverpool, Manchester City, Manchester United,
Newcastle United, Nottingham Forest, Sunderland, Tottenham Hotspur

Promoted from the Championship for 2026/27: Coventry City, Ipswich Town,
Hull City — replacing relegated West Ham United, Burnley, and Wolverhampton
Wanderers.

**2026/27 season:** Aug 21, 2026 → May 30, 2027 (final matchday, all games
kick off simultaneously).
**2027/28 season (next):** Not yet officially announced — the Premier
League typically confirms next-season dates and releases fixtures around
June of the preceding season. Historically starts mid-to-late August.

### ATP (Men's Tennis) — 69 countries, Grand Slams only

Unlike the other leagues, the draftable "team" is a **country**, not a club
— a country's fantasy score aggregates all of that country's players'
results at each major (see `docs/wiki/game-rules-tennis-mens.md`). Pool is
every country with a currently ATP-ranked player inside the **top 200**
(there's no clean single source enumerating literal "any ranked player" out
to rank ~2000, so top 200 was used as the practical cutoff — see that wiki
page for the tradeoff). Compiled from multiple overlapping rankings-by-country
sources rather than one authoritative list; treat as a solid best-effort
approximation, not a guaranteed-exhaustive one — a handful of countries
with a single player deep in ranks 150-200 could be missing.

United States, France, Argentina, Italy, Spain, Australia, Great Britain,
Czech Republic, Russia, Germany, Serbia, Belgium, Kazakhstan, Portugal,
Hungary, Netherlands, Canada, Chile, Brazil, Croatia, Japan, China, Poland,
Switzerland, Austria, Georgia, Hong Kong, Bulgaria, Peru, Bolivia, Denmark,
Luxembourg, Greece, Bosnia and Herzegovina, Finland, Norway, Monaco,
Paraguay, Lithuania, Slovakia, Colombia, South Africa, Ukraine, Moldova,
Tunisia, Egypt, Chinese Taipei, Ecuador, Mexico, Algeria, Lebanon, Israel,
Ivory Coast, Slovenia, Ireland, Uruguay, Venezuela, Indonesia, Pakistan,
Morocco, New Zealand, Senegal, Iran, South Korea, Uzbekistan, Sweden,
Cyprus, Estonia, Dominican Republic

**2026 majors (all 4 already scheduled):** Australian Open Jan 12 – Feb 1
→ French Open May 24 – Jun 7 → Wimbledon Jun 29 – Jul 12 → US Open Aug 31 –
Sep 13 (the only one not yet complete as of this writing).
**2027 majors (next):** Australian Open expected early-to-mid January 2027;
exact dates and the rest of the 2027 calendar not yet officially announced.

### WTA (Women's Tennis) — 47 countries, Grand Slams only

Same structure as ATP above — countries, not clubs, top-200-ranked-player
cutoff, same caveat about approximate compilation. Own country pool (WTA
representation differs from ATP's).

United States, Czech Republic, Russia, Australia, Ukraine, Spain, China,
Germany, Poland, France, Italy, Great Britain, Austria, Canada, Croatia,
Japan, Switzerland, Uzbekistan, Romania, Belgium, Latvia, Colombia,
Hungary, Thailand, Belarus, Kazakhstan, Slovenia, Andorra, Denmark,
Slovakia, Greece, Netherlands, Mexico, Serbia, Indonesia, Argentina,
Philippines, Egypt, Armenia, Turkey, New Zealand, Kenya, Israel, Ecuador,
Montenegro, Albania, Finland

**2026/2027 majors:** same calendar as ATP above (all 4 majors are shared
men's/women's events, just separate singles draws).

### PGA (Men's Golf) — 26 teams ("A" through "Z"), majors only

The draftable "team" here is even more abstract than tennis's countries: a
**letter of the alphabet**. A letter's fantasy score at a major sums the
scores of every player in that major's field whose last name starts with
that letter (see `docs/wiki/game-rules-golf.md` for the per-player scoring
and how it aggregates). Team pool is simply all 26 letters, A-Z — no
real-world roster to research or realign season to season, unlike every
other league here.

Majors: The Masters, PGA Championship, U.S. Open, The Open Championship.

**2026 majors (all 4 complete):** Masters Apr 9–12 → PGA Championship
May 14–17 → U.S. Open Jun 18–21 → The Open Championship Jul 16–19.
**2027 majors (next):** Not yet officially scheduled.

### LPGA (Women's Golf) — 26 teams ("A" through "Z"), 4 of 5 majors

Same letter-based structure as PGA above. The LPGA technically runs 5
majors; to keep parity with the men's 4, only these 4 count (Amundi Evian
Championship is excluded — a deliberate choice, not an oversight):
**The Chevron Championship**, **U.S. Women's Open**, **KPMG Women's PGA
Championship**, **AIG Women's Open**.

**2026 majors (all 4 counted ones complete):** Chevron Championship
Apr 23–26 → U.S. Women's Open Jun 4–7 → KPMG Women's PGA Championship
week of Jun 28 → AIG Women's Open Jul 30–Aug 2.
**2027 majors (next):** Not yet officially scheduled.

### F1 (Formula 1) — 11 teams

Unlike every other league, the draftable "team" is a constructor (a works
team fielding two cars all season), not a club with a fixed roster of
players — see `docs/wiki/game-rules-f1.md` for how the two cars' results
combine into one team score.

Red Bull Racing, Ferrari, Mercedes, McLaren, Aston Martin, Alpine,
Williams, Racing Bulls, Audi, Haas, Cadillac

Note: two changes from the 10-team 2025 grid. **Cadillac** is a brand-new
entrant for 2026 — the first new constructor since Haas joined in 2016 —
so it has no 2025 result in the app's historical data. **Audi** is Sauber's
works team competing under its new manufacturer identity for 2026 (branded
"Audi Revolut F1 Team"); the FIA's entry list still shows the legal entity
as Sauber Motorsport AG pending the corporate rename, but the racing brand
going forward is Audi, so that's the name used here. **Racing Bulls** has
raced under that name since 2025 (dropped "RB"/VCARB/AlphaTauri) — no
change for 2026, just a note in case older sources still say "RB."

**2026 season (in progress):** Australian GP March 6–8, 2026 → 24 Grands
Prix → season finale at the Abu Dhabi GP Dec 4–6, 2026.
**2027 season (next):** Not yet officially scheduled — F1 typically
releases the following year's calendar in the preceding autumn; historically
opens with the Australian GP in early-to-mid March.

### WNBA (Women's National Basketball Association) — 15 teams

Atlanta Dream, Chicago Sky, Connecticut Sun, Dallas Wings, Golden State
Valkyries, Indiana Fever, Las Vegas Aces, Los Angeles Sparks, Minnesota
Lynx, New York Liberty, Phoenix Mercury, Portland Fire, Seattle Storm,
Toronto Tempo, Washington Mystics

Note: two brand-new expansion franchises join for 2026 via an April 2026
expansion draft — **Portland Fire** and **Toronto Tempo** (the league's
first Canadian franchise) — bringing the league from 13 to 15 teams;
neither has a 2025 result. Golden State Valkyries, by contrast, already
played their debut season in 2025 (the prior expansion, 12→13 teams). The
league has used a single unified standings table with no conferences
since 2022 — playoff seeding is 1-8 by overall record (1v8, 2v7, 3v6,
4v5) — and the Finals moved from best-of-5 to **best-of-7** starting in
2025.

**2026 season (in progress):** Regular season May 8 – Sept 24, 2026
(44 games/team) → playoffs late Sept/October (exact 2026 Finals dates
not yet announced).
**2027 season (next):** Not yet officially scheduled.

### MLS (Major League Soccer) — 30 teams

Atlanta United FC, Austin FC, CF Montréal, Charlotte FC, Chicago Fire FC,
Colorado Rapids, Columbus Crew, D.C. United, FC Cincinnati, FC Dallas,
Houston Dynamo FC, Inter Miami CF, LA Galaxy, Los Angeles FC, Minnesota
United FC, Nashville SC, New England Revolution, New York City FC, New
York Red Bulls, Orlando City SC, Philadelphia Union, Portland Timbers,
Real Salt Lake, San Diego FC, San Jose Earthquakes, Seattle Sounders FC,
Sporting Kansas City, St. Louis City SC, Toronto FC, Vancouver Whitecaps FC

Split into Eastern and Western Conferences (15 each) for playoff seeding
only — the Team pool itself and the Supporters' Shield (best overall
record) don't distinguish conference. Top 9 of each conference make the
playoffs (18 teams); seeds 8-9 play a single-game Wild Card round, then
Round One is a best-of-3 series, with the Conference Semifinal, Conference
Final, and MLS Cup itself all single matches.

Note: MLS is switching from its longtime Feb/March-December calendar to a
**July-May calendar** starting in 2027, aligning with the international
schedule the way EPL and most European leagues already do (motivated by
FIFA international windows and the global transfer calendar). A one-off
shortened "transition campaign" bridges the gap — Feb-May 2027, a 14-game
regular season plus its own playoffs and MLS Cup — before the first full
season under the new calendar kicks off in **mid-to-late July 2027**,
running with a winter break (mid-December-January) through to the MLS Cup
in May 2028.

**2025 season (most recently complete, old calendar):** Feb/March 2025 →
MLS Cup Dec 6, 2025 (Inter Miami CF champions; Philadelphia Union won the
Supporters' Shield).
**2026 season (in progress, last season on the old calendar):** Feb/March
2026 → MLS Cup expected December 2026.
**2027 (transition + new calendar):** Transition campaign Feb-May 2027 →
new-format season kicks off mid-to-late July 2027 → runs through a winter
break into a May 2028 MLS Cup.

### NWSL (National Women's Soccer League) — 16 teams

Angel City FC, Bay FC, Boston Legacy FC, Chicago Stars FC, Denver Summit
FC, Gotham FC, Houston Dash, Kansas City Current, North Carolina Courage,
Orlando Pride, Portland Thorns FC, Racing Louisville FC, San Diego Wave
FC, Seattle Reign FC, Utah Royals, Washington Spirit

Note: Boston Legacy FC and Denver Summit FC are brand-new 2026 expansion
franchises (bringing the league from 14 to 16 teams), so neither has a
2025 result in this app's historical data. Single unified standings table,
no conferences — top 8 make the playoffs (Quarterfinal → Semifinal →
Championship, all single matches, higher seed hosts), plus an NWSL Shield
for the best regular-season record.

**2026 season (in progress):** March 13 – Nov 1, 2026 (30 games/team,
first season at 16 teams) → playoffs Nov 6-21, 2026.
**2027 season (next):** Not yet officially scheduled — historically opens
mid-March.

### TDF (Tour de France Team Classification) — 23 teams, 2026 roster

**UCI WorldTeams (18):** Alpecin–Premier Tech, Decathlon CMA CGM, EF
Education–EasyPost, Groupama–FDJ United, Lidl–Trek, Lotto–Intermarché,
Movistar Team, Netcompany INEOS, NSN Cycling Team, Red Bull–Bora–
Hansgrohe, Soudal–Quick-Step, Team Bahrain Victorious, Team Jayco–AlUla,
Team Picnic–PostNL, UAE Team Emirates XRG, Uno-X Mobility, Visma–Lease a
Bike, XDS Astana Team
**UCI ProTeams / wildcards (5):** Caja Rural–Seguros RGA, Cofidis, 
Pinarello–Q36.5 Pro Cycling Team, Team TotalEnergies, Tudor Pro Cycling
Team

The draftable "team" is a professional cycling team; see
`docs/wiki/game-rules-tdf.md` for how each team's daily combined time (best
3 riders per stage) rolls up into the classification.

**Important:** this is the 2026 Tour's startlist, used as a placeholder —
the 2027 Tour de France's actual participating teams (UCI WorldTeam
rosters and sponsor names) won't be formalized until **~January 2027**.
Pro cycling team names/sponsors change often year to year, so re-verify
this list once 2027's rosters are officially announced rather than
assuming it carries over unchanged.

**2026 Tour (most recently complete):** July 2026. Lidl–Trek won the Team
Classification (+36:57 over UAE Team Emirates XRG, with Red Bull–Bora–
Hansgrohe 3rd at +1:06:22); Tadej Pogačar (UAE Team Emirates XRG) won the
General Classification, his 5th title.
**2027 Tour (next):** Not yet officially scheduled — historically opens
early July; team rosters not formalized until ~January 2027.

### URC (United Rugby Championship) — 16 teams

**Irish provinces (4):** Leinster, Munster, Connacht, Ulster
**Welsh regions (4):** Cardiff, Ospreys, Scarlets, Dragons
**South African sides (4):** Bulls, Lions, Sharks, Stormers
**Scottish (2):** Edinburgh, Glasgow Warriors
**Italian (2):** Benetton, Zebre Parma

The 16 clubs split into 4 regional Shield pools (Irish, Welsh, South
African, and a shared Italian/Scottish pool) for scheduling purposes only
— every club still plays a full round-robin-ish season against everyone
else (twice against Shield-pool rivals, once against everyone outside the
pool) and the league table itself is unified, no conference split. Top 8
make the playoffs: Quarterfinal → Semifinal → Grand Final (the higher
seed hosts every round, including the Final — no neutral-venue final the
way some other leagues do it).

**2025-26 season (most recently complete):** Sept 26, 2025 → Grand Final
June 19, 2026 (Leinster beat the Bulls 36-7 at Croke Park, Dublin — an
exact repeat of the 2025 final — for a 2nd straight title and a record
10th overall).
**2026-27 season (next):** Not yet officially scheduled — historically
opens in late September.

### IPL (Indian Premier League) — 10 teams

Chennai Super Kings, Delhi Capitals, Gujarat Titans, Kolkata Knight
Riders, Lucknow Super Giants, Mumbai Indians, Punjab Kings, Rajasthan
Royals, Royal Challengers Bengaluru, Sunrisers Hyderabad

For 2026 the 10 teams were split into two 5-team groups for scheduling
purposes (fixture generation only) — the points table itself stayed
unified across all 10, no group-based standings. Top 4 advance to a
"page playoff": Qualifier 1 (1st vs 2nd — winner goes straight to the
Final), Eliminator (3rd vs 4th — loser is out), Qualifier 2 (Q1's loser
vs the Eliminator's winner — winner reaches the Final via the back door).

Note: unlike this app's other spring-session leagues, the IPL season runs
entirely within one calendar year (no season spans two years the way
MLB/NHL/EPL do) — "IPL 2026" is fully over well before this app's current
game-season window opens.

**2026 season (complete):** March 28 - May 31, 2026. Royal Challengers
Bengaluru went back-to-back, beating Gujarat Titans in the Final —
becoming only the third team in IPL history to defend a title.
**2027 season (next):** Not yet officially scheduled — historically opens
in late March.

Sources: [2026 NFL season key dates](https://www.seahawks.com/news/nfl-announces-important-dates-for-2026-2027) · [Super Bowl LXII date/venue](https://operations.nfl.com/updates/the-game/atlanta-to-host-super-bowl-lxii-in-2028/) · [MLB 2026 schedule](https://www.mlb.com/news/mlb-2026-schedule-released) · [MLB 2027 schedule](https://www.mlb.com/news/mlb-2027-schedule-released) · [2026 World Series dates](https://www.baseball-almanac.com/ws/yr2026ws.shtml) · [2026/27 Premier League clubs & dates](https://en.wikipedia.org/wiki/2026%E2%80%9327_Premier_League) · [2025/26 relegation confirmation](https://www.premierleague.com/en/news/4657245/202526-premier-league-relegation-faq) · [2026-27 NBA season](https://en.wikipedia.org/wiki/2026%E2%80%9327_NBA_season) · [NBA key dates](https://www.nba.com/news/key-dates) · [NBA Seattle/Las Vegas expansion timeline](https://www.nba.com/news/nba-board-of-governors-exploration-seattle-las-vegas-expansion) · [2026-27 NHL home openers/schedule](https://www.nhl.com/news/nhl-home-openers-for-2026-27-season) · [2026-27 NHL season (Wikipedia)](https://en.wikipedia.org/wiki/2026%E2%80%9327_NHL_season) · [Utah Mammoth official naming](https://www.nhl.com/utah/news/utah-s-nhl-franchise-officially-named-the-utah-mammoth-release-5-7-25) · [NHL expansion speculation](https://russianmachineneverbreaks.com/2026/08/07/nhl-expansion-houston-atlanta-teams-allan-walsh/) · [2026 FBS conference realignment](https://fbschedules.com/college-football-realignment-conference-changes-for-2026-take-effect-today/) · [2026 FBS season (Wikipedia)](https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_season) · [2027 CFP National Championship (New Orleans)](https://www.si.com/college/oregon/football/college-football-playoff-national-championship-location-2027-las-vegas-raiders-allegiant-stadium) · [2027 season start/Week 0 change proposal](https://www.cbssports.com/college-football/news/ncaa-start-college-football-season-one-week-earlier-2027/) · [2026-27 men's CBB conference realignment](https://www.cbssports.com/college-basketball/news/college-basketball-conference-changes-2026-27-gonzaga-pac-12/) · [2026-27 men's/women's CBB season dates](https://www.ncaa.com/news/basketball-men/article/2026-05-07/2027-march-madness-mens-ncaa-tournament-schedule-dates) · [Mountain West Conference (Wikipedia)](https://en.wikipedia.org/wiki/Mountain_West_Conference) · [Pac-12 Conference (Wikipedia)](https://en.wikipedia.org/wiki/Pac-12_Conference) · [Citadel/VMI women's basketball exception](https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_men%27s_basketball_programs) · [2026 Grand Slam calendar](https://en.wikipedia.org/wiki/2026_Australian_Open) · [ATP top-100-by-country](https://www.tennis-x.com/ranking-stats/atp-country.php) · [WTA top-100-by-country](https://www.tennis-x.com/ranking-stats/wta-country.php) · [ATP/WTA top-200 country breakdown (Tennis Abstract)](https://tennisabstract.com/reports/atpRankings.html) · [2026 men's major schedule](https://www.golfchannel.com/news/when-and-where-are-the-2026-mens-golf-majors) · [2026 LPGA major schedule](https://www.golfchannel.com/news/womens-golf-majors-in-2026-schedule-and-locations-for-the-biggest-events) · [2025 F1 constructors' standings](https://www.formula1.com/en/results/2025/team) · [2025 F1 drivers' standings](https://www.formula1.com/en/results/2025/drivers) · [2025 F1 race winners](https://www.formula1.com/en/results/2025/races) · [2025 F1 pole positions](https://gpracingstats.com/seasons/2025-world-championship/pole-positions/) · [2025 F1 podium/fastest-lap stats](https://www.4mula1stats.com/2025/statistics/podium.html) · [2026 F1 calendar](https://www.formula1.com/en/racing/2026) · [2025 Formula One World Championship (Wikipedia)](https://en.wikipedia.org/wiki/2025_Formula_One_World_Championship) · [2025 WNBA season (Wikipedia)](https://en.wikipedia.org/wiki/2025_WNBA_season) · [2025 WNBA playoffs (Wikipedia)](https://en.wikipedia.org/wiki/2025_WNBA_playoffs) · [2025 WNBA Finals (Wikipedia)](https://en.wikipedia.org/wiki/2025_WNBA_Finals) · [Template:2025 WNBA standings (Wikipedia)](https://en.wikipedia.org/wiki/Template:2025_WNBA_standings) · [MLS 2027 calendar change announcement](https://www.mlssoccer.com/news/mls-to-align-calendar-with-top-leagues-around-world) · [2025 MLS season (Wikipedia)](https://en.wikipedia.org/wiki/2025_Major_League_Soccer_season) · [2025 MLS Cup Playoffs (Wikipedia)](https://en.wikipedia.org/wiki/2025_MLS_Cup_Playoffs) · [2026 MLS season (Wikipedia)](https://en.wikipedia.org/wiki/2026_Major_League_Soccer_season) · [2025-26 URC season (Wikipedia)](https://en.wikipedia.org/wiki/2025%E2%80%9326_United_Rugby_Championship) · [2026 URC Grand Final (Wikipedia)](https://en.wikipedia.org/wiki/2026_United_Rugby_Championship_Grand_Final) · [URC 2026 quarterfinal/semifinal results (Kickoff/News24)](https://www.kickoff.com/rugby/urc/urc-quarter-finals-bulls-and-stormers-advance-as-lions-bow-out) · [IPL 2026 points table](https://www.ipl.com/series/indian-premier-league-2026-129908/point-table) · [IPL 2026 season (Wikipedia)](https://en.wikipedia.org/wiki/2026_Indian_Premier_League) · [IPL 2026 Final (Wikipedia)](https://en.wikipedia.org/wiki/2026_Indian_Premier_League_final) · [2026 NWSL season (Wikipedia)](https://en.wikipedia.org/wiki/2026_National_Women%27s_Soccer_League_season) · [2025 NWSL season (Wikipedia)](https://en.wikipedia.org/wiki/2025_National_Women%27s_Soccer_League_season) · [2025 NWSL Championship (ESPN)](https://www.espn.com/soccer/report/_/gameId/760618) · [2026 Tour de France teams (Wikipedia)](https://en.wikipedia.org/wiki/List_of_teams_and_cyclists_in_the_2026_Tour_de_France) · [2026 Tour de France final classifications](https://cyclinguptodate.com/cycling/tour-de-france-2026-final-classifications-pogacar-pedersen-carapaz-and-del-toro-seal-victory-in-paris)
