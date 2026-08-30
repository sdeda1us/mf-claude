"""Reference content for the Team History page: a short biography plus
enough real historical season stats to chart "fantasy points" (via
league_rules.compute_score) across the last several seasons a team
actually played in its league.

Deliberately structured like set_ev_defaults.py's FALL_EV_RAW_SCORES --
plain content-as-code, no migration needed. This is a test of the feature
scoped to EPL only; extend TEAM_BIOS/TEAM_HISTORY_STATS/TEAM_LOCATIONS
with the same shape to cover another league.

TEAM_HISTORY_STATS intentionally stops one season short of "now" -- the
most recent season lives in the Team_season_results table already (the
same row Example Scores reads), so the history endpoint reads that live
rather than duplicating it here and letting it drift stale once someone
updates that row for a new season.
"""

# (league, team name) -> (latitude, longitude) of the team's home ground,
# for the "where they play" map. Approximate stadium coordinates.
TEAM_LOCATIONS: dict[tuple[str, str], tuple[float, float]] = {
    ("EPL", "Arsenal"): (51.5549, -0.1084),  # Emirates Stadium, London
    ("EPL", "Aston Villa"): (52.5092, -1.8848),  # Villa Park, Birmingham
    ("EPL", "Bournemouth"): (50.7352, -1.8384),  # Vitality Stadium
    ("EPL", "Brentford"): (51.4907, -0.2886),  # Gtech Community Stadium, London
    ("EPL", "Brighton & Hove Albion"): (50.8617, -0.0837),  # Amex Stadium, Falmer
    ("EPL", "Chelsea"): (51.4816, -0.1910),  # Stamford Bridge, London
    ("EPL", "Coventry City"): (52.4483, -1.4954),  # CBS Arena, Coventry
    ("EPL", "Crystal Palace"): (51.3983, -0.0856),  # Selhurst Park, London
    ("EPL", "Everton"): (53.4483, -2.9925),  # Everton Stadium, Bramley-Moore Dock
    ("EPL", "Fulham"): (51.4749, -0.2217),  # Craven Cottage, London
    ("EPL", "Hull City"): (53.7460, -0.3672),  # MKM Stadium
    ("EPL", "Ipswich Town"): (52.0552, 1.1451),  # Portman Road
    ("EPL", "Leeds United"): (53.7778, -1.5722),  # Elland Road
    ("EPL", "Liverpool"): (53.4308, -2.9608),  # Anfield
    ("EPL", "Manchester City"): (53.4831, -2.2004),  # Etihad Stadium
    ("EPL", "Manchester United"): (53.4631, -2.2913),  # Old Trafford
    ("EPL", "Newcastle United"): (54.9756, -1.6217),  # St James' Park
    ("EPL", "Nottingham Forest"): (52.9400, -1.1328),  # City Ground
    ("EPL", "Sunderland"): (54.9144, -1.3883),  # Stadium of Light
    ("EPL", "Tottenham Hotspur"): (51.6043, -0.0662),  # Tottenham Hotspur Stadium, London
    # --- NFL ---
    ("NFL", "Buffalo Bills"): (42.7738, -78.7870),  # Highmark Stadium, Orchard Park
    ("NFL", "Miami Dolphins"): (25.9580, -80.2389),  # Hard Rock Stadium
    ("NFL", "New England Patriots"): (42.0909, -71.2643),  # Gillette Stadium, Foxborough
    ("NFL", "New York Jets"): (40.8135, -74.0745),  # MetLife Stadium, East Rutherford
    ("NFL", "Baltimore Ravens"): (39.2780, -76.6227),  # M&T Bank Stadium
    ("NFL", "Cincinnati Bengals"): (39.0955, -84.5160),  # Paycor Stadium
    ("NFL", "Cleveland Browns"): (41.5061, -81.6995),  # Huntington Bank Field
    ("NFL", "Pittsburgh Steelers"): (40.4468, -80.0158),  # Acrisure Stadium
    ("NFL", "Houston Texans"): (29.6847, -95.4107),  # NRG Stadium
    ("NFL", "Indianapolis Colts"): (39.7601, -86.1639),  # Lucas Oil Stadium
    ("NFL", "Jacksonville Jaguars"): (30.3239, -81.6373),  # EverBank Stadium
    ("NFL", "Tennessee Titans"): (36.1665, -86.7713),  # Nissan Stadium
    ("NFL", "Denver Broncos"): (39.7439, -105.0201),  # Empower Field at Mile High
    ("NFL", "Kansas City Chiefs"): (39.0489, -94.4839),  # Arrowhead Stadium
    ("NFL", "Las Vegas Raiders"): (36.0909, -115.1833),  # Allegiant Stadium
    ("NFL", "Los Angeles Chargers"): (33.9535, -118.3392),  # SoFi Stadium, Inglewood
    ("NFL", "Dallas Cowboys"): (32.7473, -97.0945),  # AT&T Stadium, Arlington
    ("NFL", "New York Giants"): (40.8135, -74.0745),  # MetLife Stadium
    ("NFL", "Philadelphia Eagles"): (39.9008, -75.1675),  # Lincoln Financial Field
    ("NFL", "Washington Commanders"): (38.9078, -76.8645),  # Northwest Stadium, Landover
    ("NFL", "Chicago Bears"): (41.8623, -87.6167),  # Soldier Field
    ("NFL", "Detroit Lions"): (42.3400, -83.0456),  # Ford Field
    ("NFL", "Green Bay Packers"): (44.5013, -88.0622),  # Lambeau Field
    ("NFL", "Minnesota Vikings"): (44.9738, -93.2581),  # U.S. Bank Stadium
    ("NFL", "Atlanta Falcons"): (33.7554, -84.4008),  # Mercedes-Benz Stadium
    ("NFL", "Carolina Panthers"): (35.2258, -80.8528),  # Bank of America Stadium
    ("NFL", "New Orleans Saints"): (29.9509, -90.0815),  # Caesars Superdome
    ("NFL", "Tampa Bay Buccaneers"): (27.9759, -82.5033),  # Raymond James Stadium
    ("NFL", "Arizona Cardinals"): (33.5276, -112.2626),  # State Farm Stadium, Glendale
    ("NFL", "Los Angeles Rams"): (33.9535, -118.3392),  # SoFi Stadium, Inglewood
    ("NFL", "San Francisco 49ers"): (37.4030, -121.9702),  # Levi's Stadium, Santa Clara
    ("NFL", "Seattle Seahawks"): (47.5952, -122.3316),  # Lumen Field
    # --- NBA ---
    ("NBA", "Boston Celtics"): (42.3662, -71.0621),  # TD Garden
    ("NBA", "Brooklyn Nets"): (40.6826, -73.9754),  # Barclays Center
    ("NBA", "New York Knicks"): (40.7505, -73.9934),  # Madison Square Garden
    ("NBA", "Philadelphia 76ers"): (39.9012, -75.1720),  # Wells Fargo Center
    ("NBA", "Toronto Raptors"): (43.6435, -79.3791),  # Scotiabank Arena
    ("NBA", "Chicago Bulls"): (41.8807, -87.6742),  # United Center
    ("NBA", "Cleveland Cavaliers"): (41.4965, -81.6882),  # Rocket Mortgage FieldHouse
    ("NBA", "Detroit Pistons"): (42.3410, -83.0552),  # Little Caesars Arena
    ("NBA", "Indiana Pacers"): (39.7640, -86.1555),  # Gainbridge Fieldhouse
    ("NBA", "Milwaukee Bucks"): (43.0451, -87.9172),  # Fiserv Forum
    ("NBA", "Atlanta Hawks"): (33.7573, -84.3963),  # State Farm Arena
    ("NBA", "Charlotte Hornets"): (35.2251, -80.8392),  # Spectrum Center
    ("NBA", "Miami Heat"): (25.7814, -80.1870),  # Kaseya Center
    ("NBA", "Orlando Magic"): (28.5392, -81.3839),  # Kia Center
    ("NBA", "Washington Wizards"): (38.8981, -77.0209),  # Capital One Arena
    ("NBA", "Denver Nuggets"): (39.7487, -105.0077),  # Ball Arena
    ("NBA", "Minnesota Timberwolves"): (44.9795, -93.2761),  # Target Center
    ("NBA", "Oklahoma City Thunder"): (35.4634, -97.5151),  # Paycom Center
    ("NBA", "Portland Trail Blazers"): (45.5316, -122.6668),  # Moda Center
    ("NBA", "Utah Jazz"): (40.7683, -111.9011),  # Delta Center
    ("NBA", "Golden State Warriors"): (37.7680, -122.3877),  # Chase Center
    ("NBA", "Los Angeles Clippers"): (33.9459, -118.3410),  # Intuit Dome
    ("NBA", "Los Angeles Lakers"): (34.0430, -118.2673),  # Crypto.com Arena
    ("NBA", "Phoenix Suns"): (33.4457, -112.0712),  # Footprint Center
    ("NBA", "Sacramento Kings"): (38.5802, -121.4997),  # Golden 1 Center
    ("NBA", "Dallas Mavericks"): (32.7905, -96.8103),  # American Airlines Center
    ("NBA", "Houston Rockets"): (29.7508, -95.3621),  # Toyota Center
    ("NBA", "Memphis Grizzlies"): (35.1382, -90.0505),  # FedExForum
    ("NBA", "New Orleans Pelicans"): (29.9490, -90.0821),  # Smoothie King Center
    ("NBA", "San Antonio Spurs"): (29.4270, -98.4375),  # Frost Bank Center
    # --- NHL ---
    ("NHL", "Boston Bruins"): (42.3662, -71.0621),  # TD Garden
    ("NHL", "Buffalo Sabres"): (42.8750, -78.8765),  # KeyBank Center
    ("NHL", "Detroit Red Wings"): (42.3410, -83.0552),  # Little Caesars Arena
    ("NHL", "Florida Panthers"): (26.1584, -80.3255),  # Amerant Bank Arena, Sunrise
    ("NHL", "Montreal Canadiens"): (45.4961, -73.5693),  # Bell Centre
    ("NHL", "Ottawa Senators"): (45.2969, -75.9273),  # Canadian Tire Centre
    ("NHL", "Tampa Bay Lightning"): (27.9427, -82.4518),  # Amalie Arena
    ("NHL", "Toronto Maple Leafs"): (43.6435, -79.3791),  # Scotiabank Arena
    ("NHL", "Carolina Hurricanes"): (35.8033, -78.7219),  # Lenovo Center, Raleigh
    ("NHL", "Columbus Blue Jackets"): (39.9692, -83.0061),  # Nationwide Arena
    ("NHL", "New Jersey Devils"): (40.7336, -74.1710),  # Prudential Center, Newark
    ("NHL", "New York Islanders"): (40.7230, -73.5910),  # UBS Arena, Elmont
    ("NHL", "New York Rangers"): (40.7505, -73.9934),  # Madison Square Garden
    ("NHL", "Philadelphia Flyers"): (39.9012, -75.1720),  # Wells Fargo Center
    ("NHL", "Pittsburgh Penguins"): (40.4395, -79.9895),  # PPG Paints Arena
    ("NHL", "Washington Capitals"): (38.8981, -77.0209),  # Capital One Arena
    ("NHL", "Chicago Blackhawks"): (41.8807, -87.6742),  # United Center
    ("NHL", "Colorado Avalanche"): (39.7487, -105.0077),  # Ball Arena
    ("NHL", "Dallas Stars"): (32.7905, -96.8103),  # American Airlines Center
    ("NHL", "Minnesota Wild"): (44.9448, -93.1011),  # Grand Casino Arena, St. Paul
    ("NHL", "Nashville Predators"): (36.1593, -86.7785),  # Bridgestone Arena
    ("NHL", "St. Louis Blues"): (38.6266, -90.2027),  # Enterprise Center
    ("NHL", "Utah Mammoth"): (40.7683, -111.9011),  # Delta Center, Salt Lake City
    ("NHL", "Winnipeg Jets"): (49.8927, -97.1436),  # Canada Life Centre
    ("NHL", "Anaheim Ducks"): (33.8078, -117.8766),  # Honda Center
    ("NHL", "Calgary Flames"): (51.0374, -114.0519),  # Scotiabank Saddledome
    ("NHL", "Edmonton Oilers"): (53.5469, -113.4977),  # Rogers Place
    ("NHL", "Los Angeles Kings"): (34.0430, -118.2673),  # Crypto.com Arena
    ("NHL", "San Jose Sharks"): (37.3327, -121.9012),  # SAP Center
    ("NHL", "Seattle Kraken"): (47.6221, -122.3540),  # Climate Pledge Arena
    ("NHL", "Vancouver Canucks"): (49.2778, -123.1088),  # Rogers Arena
    ("NHL", "Vegas Golden Knights"): (36.1028, -115.1784),  # T-Mobile Arena
    # --- URC ---
    ("URC", "Leinster"): (53.3282, -6.2270),  # RDS Arena, Dublin
    ("URC", "Munster"): (52.6748, -8.6314),  # Thomond Park, Limerick
    ("URC", "Connacht"): (53.2707, -9.0568),  # The Sportsground, Galway
    ("URC", "Ulster"): (54.5794, -5.8875),  # Kingspan Stadium, Belfast
    ("URC", "Cardiff"): (51.4784, -3.1811),  # Cardiff Arms Park
    ("URC", "Ospreys"): (51.6422, -3.9351),  # Swansea.com Stadium
    ("URC", "Scarlets"): (51.6892, -4.1592),  # Parc y Scarlets, Llanelli
    ("URC", "Dragons"): (51.5836, -2.9092),  # Rodney Parade, Newport
    ("URC", "Bulls"): (-25.7536, 28.2225),  # Loftus Versfeld, Pretoria
    ("URC", "Lions"): (-26.1935, 28.0653),  # Ellis Park, Johannesburg
    ("URC", "Sharks"): (-29.8279, 31.0292),  # Hollywoodbets Kings Park, Durban
    ("URC", "Stormers"): (-33.9036, 18.4108),  # DHL Stadium, Cape Town
    ("URC", "Glasgow Warriors"): (55.8847, -4.3389),  # Scotstoun Stadium
    ("URC", "Edinburgh"): (55.9461, -3.2472),  # Hive Stadium (DAM Health Stadium)
    ("URC", "Benetton"): (45.6867, 12.2497),  # Stadio Comunale di Monigo, Treviso
    ("URC", "Zebre Parma"): (44.8125, 10.3364),  # Stadio Sergio Lanfranchi, Parma

    # --- NCAAF --- top 50 teams by expected fall-auction fantasy points
    # (see set_ev_defaults.FALL_EV_RAW_SCORES) rather than all 138 FBS teams
    # -- covering every program worth owning at auction, without having to
    # research all 138 for teams no one will ever draft.
    ("NCAAF", "Ohio State Buckeyes"): (40.0017, -83.0197),  # Ohio Stadium, Columbus
    ("NCAAF", "Georgia Bulldogs"): (33.9497, -83.3733),  # Sanford Stadium, Athens
    ("NCAAF", "Texas Longhorns"): (30.2839, -97.7327),  # DKR-Texas Memorial Stadium, Austin
    ("NCAAF", "Indiana Hoosiers"): (39.1794, -86.5264),  # Memorial Stadium, Bloomington
    ("NCAAF", "Oregon Ducks"): (44.0582, -123.0685),  # Autzen Stadium, Eugene
    ("NCAAF", "Notre Dame Fighting Irish"): (41.6983, -86.2331),  # Notre Dame Stadium
    ("NCAAF", "Alabama Crimson Tide"): (33.2083, -87.5503),  # Bryant-Denny Stadium, Tuscaloosa
    ("NCAAF", "LSU Tigers"): (30.4118, -91.1837),  # Tiger Stadium, Baton Rouge
    ("NCAAF", "Texas A&M Aggies"): (30.6100, -96.3405),  # Kyle Field, College Station
    ("NCAAF", "Miami (FL) Hurricanes"): (25.9580, -80.2389),  # Hard Rock Stadium, Miami Gardens
    ("NCAAF", "Texas Tech Red Raiders"): (33.5904, -101.8709),  # Jones AT&T Stadium, Lubbock
    ("NCAAF", "Oklahoma Sooners"): (35.2058, -97.4425),  # Gaylord Family Oklahoma Memorial Stadium, Norman
    ("NCAAF", "USC Trojans"): (34.0141, -118.2879),  # LA Memorial Coliseum
    ("NCAAF", "Ole Miss Rebels"): (34.3646, -89.5348),  # Vaught-Hemingway Stadium, Oxford
    ("NCAAF", "Tennessee Volunteers"): (35.9550, -83.9250),  # Neyland Stadium, Knoxville
    ("NCAAF", "Michigan Wolverines"): (42.2658, -83.7487),  # Michigan Stadium, Ann Arbor
    ("NCAAF", "Auburn Tigers"): (32.6023, -85.4900),  # Jordan-Hare Stadium, Auburn
    ("NCAAF", "Florida Gators"): (29.6499, -82.3486),  # Ben Hill Griffin Stadium, Gainesville
    ("NCAAF", "Missouri Tigers"): (38.9358, -92.3331),  # Faurot Field, Columbia
    ("NCAAF", "Penn State Nittany Lions"): (40.8122, -77.8560),  # Beaver Stadium, University Park
    ("NCAAF", "Clemson Tigers"): (34.6834, -82.8433),  # Memorial Stadium, Clemson
    ("NCAAF", "BYU Cougars"): (40.2555, -111.6549),  # LaVell Edwards Stadium, Provo
    ("NCAAF", "South Carolina Gamecocks"): (33.9727, -81.0192),  # Williams-Brice Stadium, Columbia
    ("NCAAF", "Iowa Hawkeyes"): (41.6586, -91.5511),  # Kinnick Stadium, Iowa City
    ("NCAAF", "Washington Huskies"): (47.6503, -122.3017),  # Husky Stadium, Seattle
    ("NCAAF", "SMU Mustangs"): (32.8371, -96.7828),  # Gerald J. Ford Stadium, Dallas
    ("NCAAF", "Vanderbilt Commodores"): (36.1447, -86.8069),  # FirstBank Stadium, Nashville
    ("NCAAF", "Nebraska Cornhuskers"): (40.8206, -96.7056),  # Memorial Stadium, Lincoln
    ("NCAAF", "Florida State Seminoles"): (30.4380, -84.3040),  # Doak Campbell Stadium, Tallahassee
    ("NCAAF", "Louisville Cardinals"): (38.2058, -85.7585),  # L&N Federal Credit Union Stadium
    ("NCAAF", "Utah Utes"): (40.7599, -111.8485),  # Rice-Eccles Stadium, Salt Lake City
    ("NCAAF", "Pittsburgh Panthers"): (40.4468, -80.0158),  # Acrisure Stadium, Pittsburgh
    ("NCAAF", "Virginia Cavaliers"): (38.0309, -78.5127),  # Scott Stadium, Charlottesville
    ("NCAAF", "Virginia Tech Hokies"): (37.2199, -80.4183),  # Lane Stadium, Blacksburg
    ("NCAAF", "Arizona Wildcats"): (32.2288, -110.9491),  # Arizona Stadium, Tucson
    ("NCAAF", "Baylor Bears"): (31.5586, -97.1156),  # McLane Stadium, Waco
    ("NCAAF", "Houston Cougars"): (29.7217, -95.3406),  # TDECU Stadium, Houston
    ("NCAAF", "Kentucky Wildcats"): (38.0233, -84.5060),  # Kroger Field, Lexington
    ("NCAAF", "Illinois Fighting Illini"): (40.0956, -88.2359),  # Memorial Stadium, Champaign
    ("NCAAF", "North Carolina Tar Heels"): (35.9049, -79.0469),  # Kenan Memorial Stadium, Chapel Hill
    ("NCAAF", "Kansas State Wildcats"): (39.2019, -96.5847),  # Bill Snyder Family Stadium, Manhattan
    ("NCAAF", "TCU Horned Frogs"): (32.7095, -97.3688),  # Amon G. Carter Stadium, Fort Worth
    ("NCAAF", "Arkansas Razorbacks"): (36.0678, -94.1786),  # Razorback Stadium, Fayetteville
    ("NCAAF", "Mississippi State Bulldogs"): (33.4552, -88.7934),  # Davis Wade Stadium, Starkville
    ("NCAAF", "Wisconsin Badgers"): (43.0700, -89.4123),  # Camp Randall Stadium, Madison
    ("NCAAF", "Duke Blue Devils"): (36.0009, -78.9412),  # Wallace Wade Stadium, Durham
    ("NCAAF", "Georgia Tech Yellow Jackets"): (33.7724, -84.3928),  # Bobby Dodd Stadium, Atlanta
    ("NCAAF", "NC State Wolfpack"): (35.8010, -78.7197),  # Carter-Finley Stadium, Raleigh
    ("NCAAF", "Arizona State Sun Devils"): (33.4260, -111.9327),  # Mountain America Stadium, Tempe
    ("NCAAF", "Cincinnati Bearcats"): (39.1310, -84.5157),  # Nippert Stadium, Cincinnati
}

# (league, team name) -> a short factual biography (2-4 sentences):
# founding, home ground, identity/nickname, and a headline moment or two.
TEAM_BIOS: dict[tuple[str, str], str] = {
    ("EPL", "Arsenal"): (
        "Founded in 1886 and based in north London at the Emirates Stadium since 2006 "
        "(previously Highbury), Arsenal are nicknamed the Gunners and hold the record for "
        "most FA Cups won (14). Their 2003-04 \"Invincibles\" remain the only side to go a "
        "full 38-game Premier League season unbeaten."
    ),
    ("EPL", "Aston Villa"): (
        "Founded in 1874 and playing at Villa Park in Birmingham, Aston Villa were a "
        "founding member of both the Football League (1888) and the Premier League (1992). "
        "They remain the last English club outside the traditional \"big clubs\" to win the "
        "European Cup, in 1982."
    ),
    ("EPL", "Bournemouth"): (
        "Founded in 1899 and based at the Vitality Stadium on the English south coast, "
        "Bournemouth reached the Premier League for the first time in their history in 2015 "
        "under manager Eddie Howe, a rapid rise from League Two a decade earlier."
    ),
    ("EPL", "Brentford"): (
        "Founded in 1889 in west London and now playing at the Gtech Community Stadium "
        "(previously Griffin Park), Brentford returned to the top flight in 2021 after a "
        "74-year absence, built on data-driven recruitment under co-owner Matthew Benham."
    ),
    ("EPL", "Brighton & Hove Albion"): (
        "Founded in 1901 and based at the Falmer/American Express Stadium since 2011, "
        "Brighton reached the Premier League in 2017 for the first time since 1983. The "
        "Seagulls have since built a reputation for shrewd recruitment and developing "
        "players who move on to bigger clubs."
    ),
    ("EPL", "Chelsea"): (
        "Founded in 1905 and based at Stamford Bridge in west London, Chelsea have won six "
        "English league titles and two Champions Leagues (2012, 2021). Heavy investment "
        "under owner Roman Abramovich (2003-2022) transformed the club into a regular "
        "trophy contender; a Clearlake/Boehly-led consortium has owned it since 2022."
    ),
    ("EPL", "Coventry City"): (
        "Founded in 1883 and nicknamed the Sky Blues, Coventry's only major honour is the "
        "1987 FA Cup. They spent 34 straight seasons in the top flight from 1967 to 2001 "
        "before relegation; 2026-27 marks their first return to the Premier League since."
    ),
    ("EPL", "Crystal Palace"): (
        "Founded in 1905 and based at Selhurst Park in south London, the Eagles have been "
        "a fixture of the Premier League since promotion in 2013. They won their first "
        "major trophy, the FA Cup, in 2025, beating Manchester City in the final."
    ),
    ("EPL", "Everton"): (
        "Founded in 1878, Everton played at Goodison Park from 1892 before moving to "
        "Everton Stadium at Bramley-Moore Dock in 2025. Nicknamed the Toffees, they held "
        "one of English football's longest unbroken top-flight streaks before eventually "
        "being relegated from it."
    ),
    ("EPL", "Fulham"): (
        "Founded in 1879 and based at Craven Cottage on the Thames in west London, Fulham "
        "are London's oldest professional football club. Nicknamed the Cottagers, they "
        "reached the UEFA Europa League final in 2010 under Roy Hodgson."
    ),
    ("EPL", "Hull City"): (
        "Founded in 1904 and nicknamed the Tigers, Hull City first reached the Premier "
        "League in 2008-09 and reached the FA Cup final in 2014. They last played "
        "top-flight football in 2016-17; 2026-27 marks their return after nearly a decade."
    ),
    ("EPL", "Ipswich Town"): (
        "Founded in 1878 and based at Portman Road, Ipswich won the English league title "
        "in 1961-62 and the UEFA Cup in 1981 under Bobby Robson. After 22 years away, they "
        "were promoted to the Premier League in 2024, relegated after one season back, and "
        "return again for 2026-27."
    ),
    ("EPL", "Leeds United"): (
        "Founded in 1919 and based at Elland Road, Leeds won the old First Division three "
        "times (1969, 1974, 1992) and reached a Champions League semifinal in 2001. A "
        "financial collapse sent them out of the top flight for 16 years (2004-2020); "
        "they've moved between the Premier League and Championship since."
    ),
    ("EPL", "Liverpool"): (
        "Founded in 1892 and based at Anfield, Liverpool are one of England's most "
        "decorated clubs with 19 league titles and six European Cups. Arne Slot has "
        "managed the side since 2024, succeeding the hugely successful Jurgen Klopp era."
    ),
    ("EPL", "Manchester City"): (
        "Founded in 1880 and based at the Etihad Stadium in east Manchester, City became "
        "the dominant force in English football through the 2010s and 2020s under owner "
        "Sheikh Mansour (since 2008) and manager Pep Guardiola (since 2016), completing a "
        "domestic and European treble in 2022-23."
    ),
    ("EPL", "Manchester United"): (
        "Founded in 1878 as Newton Heath and based at Old Trafford, United hold the "
        "record for most English league titles (20). Sir Alex Ferguson's 1986-2013 "
        "tenure, capped by the 1999 treble, is the most successful era in the club's "
        "history; results have been far less consistent since."
    ),
    ("EPL", "Newcastle United"): (
        "Founded in 1892 and based at St James' Park, Newcastle have one of English "
        "football's most passionate fanbases. A Saudi Arabia-backed takeover in 2021 "
        "brought heavy investment, and the Magpies won the League Cup in 2025, their "
        "first major trophy since 1969."
    ),
    ("EPL", "Nottingham Forest"): (
        "Founded in 1865 and based at the City Ground, Forest won back-to-back European "
        "Cups in 1979 and 1980 under Brian Clough, a remarkable feat for a club of their "
        "size. Promoted back to the Premier League in 2022 after 23 years away, they "
        "finished 7th and qualified for Europe in 2024-25."
    ),
    ("EPL", "Sunderland"): (
        "Founded in 1879 and based at the Stadium of Light, Sunderland are six-time "
        "English champions, almost all before the Second World War. After relegation as "
        "far as League One in 2018, the Black Cats worked back up and returned to the "
        "Premier League via the 2025 Championship play-offs."
    ),
    ("EPL", "Tottenham Hotspur"): (
        "Founded in 1882 and based at the Tottenham Hotspur Stadium (opened 2019, "
        "previously White Hart Lane), Spurs were the first English club to win a European "
        "trophy (the 1963 Cup Winners' Cup) and the first to complete the modern domestic "
        "double (1961). They won the UEFA Europa League in 2025, ending a 17-year wait "
        "for a trophy."
    ),
    # --- NFL ---
    ("NFL", "Buffalo Bills"): (
        "Founded in 1960 in the AFL and based at Highmark Stadium in Orchard Park, the "
        "Bills reached four consecutive Super Bowls (XXV-XXVIII, 1991-94) and lost all "
        "four -- the only franchise to do so."
    ),
    ("NFL", "Miami Dolphins"): (
        "Founded in 1966 and based at Hard Rock Stadium, the Dolphins are the only NFL "
        "team to complete a perfect season, going 17-0 and winning Super Bowl VII in 1972."
    ),
    ("NFL", "New England Patriots"): (
        "Founded in 1960 in the AFL as the Boston Patriots and based at Gillette Stadium "
        "in Foxborough, the Patriots' Tom Brady-Bill Belichick era (2001-2019) brought six "
        "Super Bowl titles, tied for the most of any franchise."
    ),
    ("NFL", "New York Jets"): (
        "Founded in 1960 in the AFL and based at MetLife Stadium (shared with the Giants), "
        "Joe Namath's guaranteed win over the heavily-favored Colts in Super Bowl III (1969) "
        "remains the franchise's only championship."
    ),
    ("NFL", "Baltimore Ravens"): (
        "Founded in 1996 from the relocated original Cleveland Browns franchise and based "
        "at M&T Bank Stadium, the Ravens have won two Super Bowls (XXXV in 2001, XLVII in "
        "2013), both built on dominant defenses."
    ),
    ("NFL", "Cincinnati Bengals"): (
        "Founded in 1968 and based at Paycor Stadium, the Bengals have reached three Super "
        "Bowls (1982, 1989, 2022) without a win; Joe Burrow's arrival sparked a return to "
        "contention in the 2020s."
    ),
    ("NFL", "Cleveland Browns"): (
        "Founded in 1946 in the AAFC and based at Huntington Bank Field, the Browns won "
        "four AAFC titles and three NFL championships before the Super Bowl era, but none "
        "since 1964 -- one of the longest droughts in the league."
    ),
    ("NFL", "Pittsburgh Steelers"): (
        "Founded in 1933 and based at Acrisure Stadium, the Steelers have won six Super "
        "Bowls, tied for the most of any franchise, built around the dominant 1970s "
        "\"Steel Curtain\" defense."
    ),
    ("NFL", "Houston Texans"): (
        "Founded in 2002, the NFL's newest franchise, and based at NRG Stadium, the Texans "
        "have no championships yet but won back-to-back division titles behind C.J. Stroud "
        "starting in 2023."
    ),
    ("NFL", "Indianapolis Colts"): (
        "Founded in 1953 from the relocated original Baltimore Colts and based at Lucas Oil "
        "Stadium, the Colts won Super Bowl XLI (2007) under Peyton Manning and Tony Dungy."
    ),
    ("NFL", "Jacksonville Jaguars"): (
        "Founded in 1995 as an expansion team and based at EverBank Stadium, the Jaguars "
        "reached the AFC Championship Game in just their second season (1996) and again in "
        "2017 and 2022, but have never reached a Super Bowl."
    ),
    ("NFL", "Tennessee Titans"): (
        "Founded in 1960 in the AFL as the Houston Oilers and relocated to Tennessee in "
        "1997, the Titans play at Nissan Stadium and reached Super Bowl XXXIV (1999), "
        "falling a yard short of forcing overtime."
    ),
    ("NFL", "Denver Broncos"): (
        "Founded in 1960 in the AFL and based at Empower Field at Mile High, the Broncos "
        "won back-to-back Super Bowls (XXXII, XXXIII) with John Elway, and a third (50) in "
        "2015 behind a dominant defense."
    ),
    ("NFL", "Kansas City Chiefs"): (
        "Founded in 1960 in the AFL and based at Arrowhead Stadium, the Chiefs built a "
        "2020s dynasty under Patrick Mahomes and Andy Reid, winning Super Bowls LIV, LVII, "
        "and LVIII."
    ),
    ("NFL", "Las Vegas Raiders"): (
        "Founded in 1960 in the AFL in Oakland and relocated to Las Vegas in 2020, the "
        "Raiders play at Allegiant Stadium and have three Super Bowl titles (1977, 1981, "
        "1984), historically known for a rebellious \"Just Win, Baby\" identity under Al Davis."
    ),
    ("NFL", "Los Angeles Chargers"): (
        "Founded in 1960 in the AFL in Los Angeles, based in San Diego from 1961-2016 "
        "before returning to LA, the Chargers play at SoFi Stadium and reached Super Bowl "
        "XXIX (1994) as the San Diego Chargers, their only appearance."
    ),
    ("NFL", "Dallas Cowboys"): (
        "Founded in 1960 and based at AT&T Stadium, \"America's Team\" has won five Super "
        "Bowls, with a 1990s dynasty under Jimmy Johnson and Barry Switzer."
    ),
    ("NFL", "New York Giants"): (
        "Founded in 1925, one of the NFL's oldest franchises, and based at MetLife Stadium, "
        "the Giants have won four NFL championships plus Super Bowls XXI, XXV, XLII, and "
        "XLVI -- the latter two upsetting Patriots teams seeking a perfect season."
    ),
    ("NFL", "Philadelphia Eagles"): (
        "Founded in 1933 and based at Lincoln Financial Field, the Eagles won Super Bowl "
        "LII (2018) and Super Bowl LIX (2025), the latter a rout of the Chiefs."
    ),
    ("NFL", "Washington Commanders"): (
        "Founded in 1932 and based at Northwest Stadium in Landover, the franchise won "
        "three Super Bowls (1983, 1988, 1992) during the \"Hogs\" era, and was renamed the "
        "Commanders in 2022 after decades as the Redskins."
    ),
    ("NFL", "Chicago Bears"): (
        "Founded in 1920, one of the NFL's two remaining charter franchises, and based at "
        "Soldier Field, the Bears have nine NFL championships -- the most of any franchise "
        "-- but only one Super Bowl, the dominant 1985 team's Super Bowl XX win."
    ),
    ("NFL", "Detroit Lions"): (
        "Founded in 1930 and based at Ford Field, the Lions won four NFL championships, "
        "all before the Super Bowl era (most recently 1957); the Dan Campbell era of the "
        "2020s has ended decades of irrelevance even without a title yet."
    ),
    ("NFL", "Green Bay Packers"): (
        "Founded in 1919 and based at Lambeau Field, the NFL's only publicly-owned "
        "franchise has a record 13 league championships, including Super Bowls I, II, "
        "XXXI, and XLV."
    ),
    ("NFL", "Minnesota Vikings"): (
        "Founded in 1961 and based at U.S. Bank Stadium, the Vikings reached four Super "
        "Bowls (IV, VIII, IX, XI) without a win."
    ),
    ("NFL", "Atlanta Falcons"): (
        "Founded in 1966 and based at Mercedes-Benz Stadium, the Falcons reached Super Bowl "
        "XXXIII (1998) and Super Bowl LI (2016), the latter infamous for blowing a 28-3 "
        "third-quarter lead to the Patriots."
    ),
    ("NFL", "Carolina Panthers"): (
        "Founded in 1993 as an expansion team and based at Bank of America Stadium, the "
        "Panthers reached Super Bowl XXXVIII (2003) and Super Bowl 50 (2015) without a win."
    ),
    ("NFL", "New Orleans Saints"): (
        "Founded in 1967 and based at the Caesars Superdome, the Saints won Super Bowl "
        "XLIV (2009) behind Drew Brees, the franchise's only championship."
    ),
    ("NFL", "Tampa Bay Buccaneers"): (
        "Founded in 1976 as an expansion team and based at Raymond James Stadium, the "
        "Buccaneers won Super Bowl XXXVII (2002) on a dominant defense, and Super Bowl LV "
        "(2020) at home behind Tom Brady in his first season with the team."
    ),
    ("NFL", "Arizona Cardinals"): (
        "Founded in 1898, one of the oldest continuously operating professional football "
        "franchises in the US, and based at State Farm Stadium in Glendale since relocating "
        "there in 1988, the Cardinals reached Super Bowl XLIII (2008), their only appearance."
    ),
    ("NFL", "Los Angeles Rams"): (
        "Founded in 1936 in Cleveland, moving to LA, then St. Louis (1995-2015), then back "
        "to LA, the Rams play at SoFi Stadium and won Super Bowl LVI (2021) at home, plus "
        "an earlier title as the St. Louis Rams in Super Bowl XXXIV (1999)."
    ),
    ("NFL", "San Francisco 49ers"): (
        "Founded in 1946 and based at Levi's Stadium, the 49ers won five Super Bowls, all "
        "in the Bill Walsh/Joe Montana-Steve Young era (1981-1994)."
    ),
    ("NFL", "Seattle Seahawks"): (
        "Founded in 1976 as an expansion team and based at Lumen Field, the Seahawks won "
        "Super Bowl XLVIII (2013) behind the \"Legion of Boom\" defense, then lost Super "
        "Bowl XLIX the following year on a controversial goal-line interception."
    ),
    # --- NBA ---
    ("NBA", "Boston Celtics"): (
        "Founded in 1946 and based at TD Garden, the Celtics hold an NBA-record 18 "
        "championships, most recently 2024, built on the Bill Russell-era dynasty (11 "
        "titles in 13 years, 1957-1969)."
    ),
    ("NBA", "Brooklyn Nets"): (
        "Founded in 1967 in the ABA as the New Jersey Americans and now based at Barclays "
        "Center in Brooklyn (since 2012), the franchise won two ABA titles (1974, 1976) as "
        "the New York Nets but has no NBA championship."
    ),
    ("NBA", "New York Knicks"): (
        "Founded in 1946, one of the NBA's original teams, and based at Madison Square "
        "Garden, the Knicks have two championships (1970, 1973) and remain one of the "
        "league's most valuable and storied franchises."
    ),
    ("NBA", "Philadelphia 76ers"): (
        "Founded in 1946 as the Syracuse Nationals and based at Wells Fargo Center since "
        "moving to Philadelphia in 1963, the 76ers have three championships (1955, 1967, "
        "1983), the last led by Julius Erving and Moses Malone."
    ),
    ("NBA", "Toronto Raptors"): (
        "Founded in 1995 as an expansion team and based at Scotiabank Arena, the Raptors "
        "are the only franchise outside the US to win an NBA championship, doing so in "
        "2019 behind Kawhi Leonard."
    ),
    ("NBA", "Chicago Bulls"): (
        "Founded in 1966 and based at the United Center, the Bulls won six championships "
        "across two three-peats in the 1990s, all led by Michael Jordan."
    ),
    ("NBA", "Cleveland Cavaliers"): (
        "Founded in 1970 as an expansion team and based at Rocket Mortgage FieldHouse, the "
        "Cavaliers won their only championship in 2016, rallying from a 3-1 Finals deficit "
        "against a 73-win Warriors team."
    ),
    ("NBA", "Detroit Pistons"): (
        "Founded in 1941 as the Fort Wayne Pistons and based at Little Caesars Arena, the "
        "Pistons have three championships (1989, 1990, 2004), the first two via the "
        "physical \"Bad Boys\" teams of the late 1980s."
    ),
    ("NBA", "Indiana Pacers"): (
        "Founded in 1967 in the ABA and based at Gainbridge Fieldhouse, the Pacers won "
        "three ABA championships (1970, 1972, 1973) but have no NBA title, reaching the "
        "2025 NBA Finals."
    ),
    ("NBA", "Milwaukee Bucks"): (
        "Founded in 1968 as an expansion team and based at Fiserv Forum, the Bucks have "
        "two championships: 1971 with a rookie-adjacent Kareem Abdul-Jabbar, and 2021 led "
        "by Giannis Antetokounmpo."
    ),
    ("NBA", "Atlanta Hawks"): (
        "Founded in 1946 and now based at State Farm Arena after stops in Milwaukee and "
        "St. Louis, the Hawks won one championship, in 1958 as the St. Louis Hawks."
    ),
    ("NBA", "Charlotte Hornets"): (
        "Founded in 1988 as an expansion team and based at Spectrum Center, the original "
        "Hornets relocated to New Orleans in 2002; a new franchise (initially the Bobcats) "
        "began in 2004 and reclaimed the Hornets name and history in 2014. No championships."
    ),
    ("NBA", "Miami Heat"): (
        "Founded in 1988 as an expansion team and based at the Kaseya Center, the Heat have "
        "three championships (2006, 2012, 2013), the latter two part of LeBron James' "
        "\"Big Three\" era."
    ),
    ("NBA", "Orlando Magic"): (
        "Founded in 1989 as an expansion team and based at the Kia Center, the Magic have "
        "no championships but reached the NBA Finals twice (1995, 2009) behind Shaquille "
        "O'Neal and Dwight Howard respectively."
    ),
    ("NBA", "Washington Wizards"): (
        "Founded in 1961 as the Chicago Packers and based at Capital One Arena, the "
        "franchise won one championship in 1978 as the Washington Bullets, renaming to "
        "the Wizards in 1997."
    ),
    ("NBA", "Denver Nuggets"): (
        "Founded in 1967 in the ABA as the Denver Rockets and based at Ball Arena, the "
        "Nuggets won their first championship in 2023 behind Nikola Jokic."
    ),
    ("NBA", "Minnesota Timberwolves"): (
        "Founded in 1989 as an expansion team and based at Target Center, the "
        "Timberwolves have no championships but reached their first Western Conference "
        "Finals in 2024."
    ),
    ("NBA", "Oklahoma City Thunder"): (
        "Founded in 1967 as the Seattle SuperSonics and relocated to Oklahoma City in "
        "2008, the Thunder play at Paycom Center, winning a title as the SuperSonics in "
        "1979 and their first as the Thunder in 2025 behind Shai Gilgeous-Alexander."
    ),
    ("NBA", "Portland Trail Blazers"): (
        "Founded in 1970 as an expansion team and based at the Moda Center, the Trail "
        "Blazers won one championship, in 1977."
    ),
    ("NBA", "Utah Jazz"): (
        "Founded in 1974 as the New Orleans Jazz and relocated to Utah in 1979, the Jazz "
        "play at the Delta Center and reached back-to-back NBA Finals in 1997 and 1998 "
        "behind John Stockton and Karl Malone, losing both to the Bulls."
    ),
    ("NBA", "Golden State Warriors"): (
        "Founded in 1946 in Philadelphia and based at Chase Center since moving to San "
        "Francisco, the Warriors have seven championships, four in the 2010s-20s "
        "\"Splash Brothers\" dynasty (2015, 2017, 2018, 2022) under Steph Curry."
    ),
    ("NBA", "Los Angeles Clippers"): (
        "Founded in 1970 as the Buffalo Braves and based at the Intuit Dome since 2024, "
        "the Clippers have no championships and no Finals appearance, historically the "
        "league's least successful franchise despite recent contending teams."
    ),
    ("NBA", "Los Angeles Lakers"): (
        "Founded in 1947 in Minneapolis and based at Crypto.com Arena since moving to LA "
        "in 1960, the Lakers have 17 championships, tied for the NBA record, spanning eras "
        "led by George Mikan, Magic Johnson, Kobe Bryant, and LeBron James."
    ),
    ("NBA", "Phoenix Suns"): (
        "Founded in 1968 as an expansion team and based at the Footprint Center, the Suns "
        "have no championships but reached the NBA Finals three times (1976, 1993, 2021)."
    ),
    ("NBA", "Sacramento Kings"): (
        "Founded in 1923 as the Rochester Royals, one of the NBA's oldest lineages, and "
        "based at the Golden 1 Center, the Kings won one championship in 1951; their "
        "long-running playoff drought ended in 2023."
    ),
    ("NBA", "Dallas Mavericks"): (
        "Founded in 1980 as an expansion team and based at the American Airlines Center, "
        "the Mavericks won their only championship in 2011, upsetting LeBron James' Miami "
        "Heat behind Dirk Nowitzki."
    ),
    ("NBA", "Houston Rockets"): (
        "Founded in 1967 as the San Diego Rockets and based at the Toyota Center since "
        "relocating to Houston in 1971, the Rockets won two championships (1994, 1995) led "
        "by Hakeem Olajuwon."
    ),
    ("NBA", "Memphis Grizzlies"): (
        "Founded in 1995 as the Vancouver Grizzlies and relocated to Memphis in 2001, the "
        "Grizzlies play at FedExForum and have no championships; the \"Grit and Grind\" "
        "era of the early 2010s remains the franchise's high point."
    ),
    ("NBA", "New Orleans Pelicans"): (
        "Founded in 2002 as an expansion team (originally the New Orleans Hornets, "
        "renamed Pelicans in 2013) and based at the Smoothie King Center, with no "
        "championships yet."
    ),
    ("NBA", "San Antonio Spurs"): (
        "Founded in 1967 in the ABA as the Dallas Chaparrals and based at the Frost Bank "
        "Center since relocating to San Antonio in 1973, the Spurs won five championships "
        "(1999, 2003, 2005, 2007, 2014) under head coach Gregg Popovich."
    ),
    # --- NHL ---
    ("NHL", "Boston Bruins"): (
        "Founded in 1924, the oldest NHL team in the US, and based at TD Garden, the "
        "Bruins have six Stanley Cups, most recently 2011, and set a modern NHL record "
        "with 65 wins in 2022-23."
    ),
    ("NHL", "Buffalo Sabres"): (
        "Founded in 1970 as an expansion team and based at the KeyBank Center, the Sabres "
        "have no Stanley Cup, losing in the Final in 1975 and 1999 (the latter on a "
        "controversial overtime goal)."
    ),
    ("NHL", "Detroit Red Wings"): (
        "Founded in 1926 and based at Little Caesars Arena, the Red Wings have 11 Stanley "
        "Cups, tied for second-most in NHL history, including back-to-back titles in 1997 "
        "and 1998 that ended a 42-year drought."
    ),
    ("NHL", "Florida Panthers"): (
        "Founded in 1993 as an expansion team and based at the Amerant Bank Arena in "
        "Sunrise, the Panthers won back-to-back Stanley Cups in 2024 and 2025 after "
        "reaching the Final in 1996."
    ),
    ("NHL", "Montreal Canadiens"): (
        "Founded in 1909, the NHL's oldest team, and based at the Bell Centre, the "
        "Canadiens hold a record 24 Stanley Cups, though none since 1993."
    ),
    ("NHL", "Ottawa Senators"): (
        "Founded in 1992 as an expansion team reviving the name of the original "
        "1883-1934 Senators, and based at the Canadian Tire Centre, the franchise has no "
        "Stanley Cup, reaching the Final in 2007."
    ),
    ("NHL", "Tampa Bay Lightning"): (
        "Founded in 1992 as an expansion team and based at the Amalie Arena, the Lightning "
        "have three Stanley Cups (2004, 2020, 2021), including back-to-back titles during "
        "the COVID-affected seasons."
    ),
    ("NHL", "Toronto Maple Leafs"): (
        "Founded in 1917, one of the NHL's original six teams, and based at Scotiabank "
        "Arena, the Maple Leafs have 13 Stanley Cups but none since 1967, the longest "
        "active drought in the league."
    ),
    ("NHL", "Carolina Hurricanes"): (
        "Founded in 1972 as the New England/Hartford Whalers and relocated to Carolina in "
        "1997, the Hurricanes play at Lenovo Center in Raleigh and won a Stanley Cup in 2006."
    ),
    ("NHL", "Columbus Blue Jackets"): (
        "Founded in 2000 as an expansion team and based at Nationwide Arena, the Blue "
        "Jackets have no Stanley Cup; their only playoff series win came via a 2019 sweep "
        "of the Presidents' Trophy-winning Lightning."
    ),
    ("NHL", "New Jersey Devils"): (
        "Founded in 1974 as the Kansas City Scouts, relocating through Colorado to New "
        "Jersey in 1982, the Devils play at Prudential Center and won three Stanley Cups "
        "(1995, 2000, 2003) under a famously stifling defensive system."
    ),
    ("NHL", "New York Islanders"): (
        "Founded in 1972 as an expansion team and based at UBS Arena, the Islanders won "
        "four consecutive Stanley Cups (1980-1983), a dynasty built around Mike Bossy and "
        "Denis Potvin."
    ),
    ("NHL", "New York Rangers"): (
        "Founded in 1926 and based at Madison Square Garden, the Rangers have four Stanley "
        "Cups, most recently 1994, ending a 54-year drought amid the famous \"Now I can "
        "die in peace\" call."
    ),
    ("NHL", "Philadelphia Flyers"): (
        "Founded in 1967 as an expansion team and based at Wells Fargo Center, the Flyers "
        "won back-to-back Stanley Cups in 1974 and 1975 as the brawling \"Broad Street "
        "Bullies,\" the first expansion-era teams to win it."
    ),
    ("NHL", "Pittsburgh Penguins"): (
        "Founded in 1967 as an expansion team and based at PPG Paints Arena, the Penguins "
        "have five Stanley Cups, spanning the Mario Lemieux era (1991, 1992) and the "
        "Sidney Crosby era (2009, 2016, 2017)."
    ),
    ("NHL", "Washington Capitals"): (
        "Founded in 1974 as an expansion team and based at Capital One Arena, the "
        "Capitals won their only Stanley Cup in 2018, Alex Ovechkin's first title after "
        "years as a playoff also-ran."
    ),
    ("NHL", "Chicago Blackhawks"): (
        "Founded in 1926, one of the NHL's original six, and based at the United Center, "
        "the Blackhawks have six Stanley Cups, including three in six years (2010, 2013, "
        "2015) built around Jonathan Toews and Patrick Kane."
    ),
    ("NHL", "Colorado Avalanche"): (
        "Founded in 1972 as the Quebec Nordiques and relocated to Colorado in 1995, the "
        "Avalanche play at Ball Arena and won a Stanley Cup the year after relocating "
        "(1996), then again in 2001 and 2022."
    ),
    ("NHL", "Dallas Stars"): (
        "Founded in 1967 as the Minnesota North Stars and relocated to Dallas in 1993, the "
        "Stars play at the American Airlines Center and won a Stanley Cup in 1999."
    ),
    ("NHL", "Minnesota Wild"): (
        "Founded in 2000 as an expansion team and based at the Grand Casino Arena in St. "
        "Paul, the Wild have no Stanley Cup and have never advanced past the second round."
    ),
    ("NHL", "Nashville Predators"): (
        "Founded in 1998 as an expansion team and based at Bridgestone Arena, the "
        "Predators have no Stanley Cup, reaching the Final in 2017."
    ),
    ("NHL", "St. Louis Blues"): (
        "Founded in 1967 as an expansion team and based at the Enterprise Center, the "
        "Blues won their only Stanley Cup in 2019, months after sitting dead last in the "
        "entire league in early January that same season."
    ),
    ("NHL", "Utah Mammoth"): (
        "Traces back to the original 1972 Winnipeg Jets, relocating through Phoenix/"
        "Arizona before landing in Salt Lake City in 2024; renamed from the placeholder "
        "\"Utah Hockey Club\" to the Mammoth in 2025. Plays at the Delta Center; no "
        "Stanley Cup under any of its identities."
    ),
    ("NHL", "Winnipeg Jets"): (
        "Founded in 1999 as the original Atlanta Thrashers and relocated to Winnipeg in "
        "2011, reviving the earlier Winnipeg Jets name, the franchise plays at Canada "
        "Life Centre with no Stanley Cup yet."
    ),
    ("NHL", "Anaheim Ducks"): (
        "Founded in 1993 as an expansion team and based at the Honda Center, the Ducks "
        "won their only Stanley Cup in 2007."
    ),
    ("NHL", "Calgary Flames"): (
        "Founded in 1972 as the Atlanta Flames and relocated to Calgary in 1980, the "
        "Flames play at the Scotiabank Saddledome and won a Stanley Cup in 1989."
    ),
    ("NHL", "Edmonton Oilers"): (
        "Founded in 1972 in the WHA and based at Rogers Place, the Oilers won five Stanley "
        "Cups (1984, 1985, 1987, 1988, 1990) during the Wayne Gretzky-led dynasty of the "
        "1980s."
    ),
    ("NHL", "Los Angeles Kings"): (
        "Founded in 1967 as an expansion team and based at Crypto.com Arena, the Kings "
        "won two Stanley Cups, in 2012 and 2014."
    ),
    ("NHL", "San Jose Sharks"): (
        "Founded in 1991 as an expansion team and based at SAP Center, the Sharks have no "
        "Stanley Cup, reaching the Final in 2016."
    ),
    ("NHL", "Seattle Kraken"): (
        "Founded in 2021 as an expansion team and based at Climate Pledge Arena, the "
        "Kraken have no Stanley Cup, reaching the second round in just their second "
        "season (2023)."
    ),
    ("NHL", "Vancouver Canucks"): (
        "Founded in 1970 as an expansion team and based at Rogers Arena, the Canucks have "
        "no Stanley Cup, reaching the Final three times (1982, 1994, 2011)."
    ),
    ("NHL", "Vegas Golden Knights"): (
        "Founded in 2017 as an expansion team and based at T-Mobile Arena, the Golden "
        "Knights reached the Final in their inaugural season (2018) and won a Stanley Cup "
        "in 2023 -- one of the most successful expansion franchises in sports history."
    ),
    # --- URC ---
    ("URC", "Leinster"): (
        "One of Ireland's four professional provinces, based at the RDS Arena in Dublin, "
        "Leinster are the most successful side in the league's history across its Celtic "
        "League/Pro12/Pro14/URC eras, and have won four European Cups (2009, 2011, 2012, "
        "2018)."
    ),
    ("URC", "Munster"): (
        "One of Ireland's four professional provinces, based at Thomond Park in Limerick, "
        "Munster have one of rugby's most passionate fanbases and won two Heineken Cups "
        "(2006, 2008), plus the 2023 URC title."
    ),
    ("URC", "Connacht"): (
        "One of Ireland's four professional provinces, based at the Sportsground in "
        "Galway, historically the smallest and least funded of the four, Connacht won a "
        "surprise Pro12 title in 2016 under Pat Lam."
    ),
    ("URC", "Ulster"): (
        "One of Ireland's four professional provinces, based at Kingspan Stadium in "
        "Belfast, Ulster won the old Heineken Cup in 1999, the first Irish side to do so."
    ),
    ("URC", "Cardiff"): (
        "A Welsh region based at Cardiff Arms Park, with roots in Cardiff RFC (founded "
        "1876, one of the world's oldest rugby clubs) reorganized as a regional side in "
        "2003."
    ),
    ("URC", "Ospreys"): (
        "A Welsh region based at the Swansea.com Stadium, formed in 2003 from a merger of "
        "Neath and Swansea; historically the most domestically successful of the Welsh "
        "regions."
    ),
    ("URC", "Scarlets"): (
        "A Welsh region based at Parc y Scarlets in Llanelli, with roots in Llanelli RFC "
        "(founded 1872), famous pre-regional-era for beating the touring All Blacks in "
        "1972."
    ),
    ("URC", "Dragons"): (
        "A Welsh region based at Rodney Parade in Newport, formed in 2003 as the Newport "
        "Gwent Dragons; historically the least successful of the Welsh regions."
    ),
    ("URC", "Bulls"): (
        "A South African side based at Loftus Versfeld in Pretoria, a dominant force in "
        "Super Rugby through the 2000s and 2010s with four titles, who joined the "
        "rebranded United Rugby Championship in 2021."
    ),
    ("URC", "Lions"): (
        "A South African side based at Ellis Park in Johannesburg, who reached three "
        "straight Super Rugby finals (2016-2018) without winning one, before joining the "
        "United Rugby Championship in 2021."
    ),
    ("URC", "Sharks"): (
        "A South African side based at Hollywoodbets Kings Park in Durban, long known as "
        "Super Rugby's nearly-men after three lost finals (2001, 2007, 2008), who joined "
        "the United Rugby Championship in 2021."
    ),
    ("URC", "Stormers"): (
        "A South African side based at DHL Stadium in Cape Town, the Stormers won the "
        "United Rugby Championship's inaugural title in 2022 and reached back-to-back "
        "finals in 2022 and 2023."
    ),
    ("URC", "Glasgow Warriors"): (
        "A Scottish side based at Scotstoun Stadium, Glasgow won the 2014-15 Pro12 title "
        "and won the United Rugby Championship in 2024, then reached the final again as "
        "runners-up in 2025."
    ),
    ("URC", "Edinburgh"): (
        "A Scottish side based at the Hive Stadium, historically less successful "
        "domestically than fellow Scots Glasgow, Edinburgh reached the European Challenge "
        "Cup final in 2022."
    ),
    ("URC", "Benetton"): (
        "An Italian side based at the Stadio Comunale di Monigo in Treviso, Benetton were "
        "the first Italian side to reach the playoffs regularly in the Pro14/URC era."
    ),
    ("URC", "Zebre Parma"): (
        "An Italian side based in Parma, historically the weaker of Italy's two "
        "professional sides in the league, with no playoff appearance yet."
    ),

    # --- NCAAF --- (top 50 by expected fantasy points, see the note above
    # TEAM_LOCATIONS's NCAAF section)
    ("NCAAF", "Ohio State Buckeyes"): (
        "Founded in 1890 and playing at Ohio Stadium (\"the Horseshoe\") in Columbus, Ohio "
        "State has won eight consensus national titles, most recently the first-ever "
        "12-team CFP crown in January 2025 under Ryan Day."
    ),
    ("NCAAF", "Georgia Bulldogs"): (
        "Founded in 1892 and playing at Sanford Stadium in Athens, Georgia won back-to-back "
        "national titles in 2021 and 2022 under Kirby Smart -- the program's first "
        "championships since 1980."
    ),
    ("NCAAF", "Texas Longhorns"): (
        "Founded in 1893 and playing at Darrell K Royal-Texas Memorial Stadium in Austin, "
        "Texas has won four national titles, most recently 2005, and reached the CFP "
        "semifinals in both 2023 and 2024 under Steve Sarkisian after rejoining the SEC."
    ),
    ("NCAAF", "Indiana Hoosiers"): (
        "Founded in 1887 and playing at Memorial Stadium in Bloomington, Indiana went over "
        "a century as a Big Ten also-ran before Curt Cignetti's 2024 arrival produced an "
        "11-1 season and the program's first-ever College Football Playoff appearance."
    ),
    ("NCAAF", "Oregon Ducks"): (
        "Founded in 1894 and playing at Autzen Stadium in Eugene, Oregon is known for its "
        "Nike-designed uniform variety courtesy of alumnus Phil Knight, and won its first "
        "Big Ten title in 2024 with an unbeaten regular season after leaving the Pac-12."
    ),
    ("NCAAF", "Notre Dame Fighting Irish"): (
        "Founded in 1887 and playing at Notre Dame Stadium in South Bend, Notre Dame has 11 "
        "consensus national titles (tied for most all-time), most recently 1988, and reached "
        "the 2024 CFP championship game under Marcus Freeman before losing to Ohio State."
    ),
    ("NCAAF", "Alabama Crimson Tide"): (
        "Founded in 1892 and playing at Bryant-Denny Stadium in Tuscaloosa, Alabama has won "
        "18 national titles, most of any program; Kalen DeBoer took over in 2024 after Nick "
        "Saban's retirement ended a run of six titles in 17 seasons."
    ),
    ("NCAAF", "LSU Tigers"): (
        "Founded in 1893 and playing at Tiger Stadium (\"Death Valley\") in Baton Rouge, "
        "renowned for its Saturday-night atmosphere, LSU has won four national titles, most "
        "recently the unbeaten 2019 team; Lane Kiffin arrives in 2026 after Brian Kelly's "
        "October 2025 firing."
    ),
    ("NCAAF", "Texas A&M Aggies"): (
        "Founded in 1894 and playing at Kyle Field in College Station, home of the \"12th "
        "Man\" student tradition, Texas A&M has one national title (1939); Mike Elko's 2024 "
        "debut returned the program to the AP top 10 for the first time in years."
    ),
    ("NCAAF", "Miami (FL) Hurricanes"): (
        "Founded in 1926 and playing at Hard Rock Stadium in Miami Gardens, Miami won five "
        "national titles across its 1980s-2000s dynasty years; Cam Ward's 2024 Heisman-"
        "finalist season under Mario Cristobal was the program's best in over a decade."
    ),
    ("NCAAF", "Texas Tech Red Raiders"): (
        "Founded in 1925 and playing at Jones AT&T Stadium in Lubbock, Texas Tech has no "
        "national titles, but heavy transfer-portal investment under Joey McGuire has made "
        "the Red Raiders a preseason top-15 fixture entering 2026."
    ),
    ("NCAAF", "Oklahoma Sooners"): (
        "Founded in 1895 and playing at Gaylord Family Oklahoma Memorial Stadium in Norman, "
        "Oklahoma has won seven national titles; Brent Venables took over in 2022 after "
        "Lincoln Riley departed for USC, and moved the program from the Big 12 to the SEC "
        "in 2024."
    ),
    ("NCAAF", "USC Trojans"): (
        "Founded in 1888 and playing at the LA Memorial Coliseum, USC has won 11 national "
        "titles; Lincoln Riley's Caleb Williams-led 2022 team won 11 games in his debut "
        "season, but the program has struggled since the 2024 move to the Big Ten."
    ),
    ("NCAAF", "Ole Miss Rebels"): (
        "Founded in 1893 and playing at Vaught-Hemingway Stadium in Oxford, Ole Miss has no "
        "national titles since the poll era began, but consecutive 11-win seasons in 2023 "
        "and 2024 under Lane Kiffin made the Rebels a perennial CFP-bubble team before "
        "Kiffin left for LSU after the 2025 regular season."
    ),
    ("NCAAF", "Tennessee Volunteers"): (
        "Founded in 1891 and playing at Neyland Stadium in Knoxville, one of the sport's "
        "largest venues, Tennessee has won six national titles, most recently 1998, and "
        "made the program's first CFP appearance in 2024 under Josh Heupel."
    ),
    ("NCAAF", "Michigan Wolverines"): (
        "Founded in 1879 and playing at Michigan Stadium (\"the Big House\"), the largest "
        "stadium in the US, Michigan claims a record-tying 12 national titles, most "
        "recently the undefeated 2023 champions under Jim Harbaugh; Kyle Whittingham "
        "arrives in 2026 after Sherrone Moore's December 2025 firing."
    ),
    ("NCAAF", "Auburn Tigers"): (
        "Founded in 1892 and playing at Jordan-Hare Stadium in Auburn, Auburn has won two "
        "national titles (1957, 2010); Alex Golesh arrives in 2026 after Hugh Freeze was "
        "fired in November 2025 following a 15-19 tenure."
    ),
    ("NCAAF", "Florida Gators"): (
        "Founded in 1906 and playing at Ben Hill Griffin Stadium (\"the Swamp\") in "
        "Gainesville, Florida has won three national titles under Steve Spurrier and Urban "
        "Meyer; Jon Sumrall arrives in 2026 after Billy Napier's October 2025 firing ended "
        "a mostly middling four-year tenure."
    ),
    ("NCAAF", "Missouri Tigers"): (
        "Founded in 1890 and playing at Faurot Field in Columbia, Missouri has no national "
        "titles, but Eli Drinkwitz's Tigers won 11 and 10 games the last two seasons, the "
        "program's best stretch in over a decade."
    ),
    ("NCAAF", "Penn State Nittany Lions"): (
        "Founded in 1887 and playing at Beaver Stadium in University Park, the second-"
        "largest stadium in the US, Penn State has won two national titles (1982, 1986); "
        "Matt Campbell arrives in 2026 from Iowa State after James Franklin was fired "
        "mid-2025 following a stunning home loss to Northwestern."
    ),
    ("NCAAF", "Clemson Tigers"): (
        "Founded in 1896 and playing at Memorial Stadium (\"Death Valley\") in Clemson, "
        "Clemson has won three national titles, two (2016, 2018) under longtime coach Dabo "
        "Swinney, who enters 2026 needing a bounce-back after a 7-6 2025 finish."
    ),
    ("NCAAF", "BYU Cougars"): (
        "Founded in 1922 and playing at LaVell Edwards Stadium in Provo, BYU won a national "
        "title in 1984 under its namesake coach's undefeated team; Kalani Sitake's program "
        "made a surprise 11-2 run in 2024 in its second Big 12 season."
    ),
    ("NCAAF", "South Carolina Gamecocks"): (
        "Founded in 1892 and playing at Williams-Brice Stadium in Columbia, South Carolina "
        "has no national titles, but Shane Beamer's program reached nine wins in 2024, its "
        "best mark since 2013."
    ),
    ("NCAAF", "Iowa Hawkeyes"): (
        "Founded in 1889 and playing at Kinnick Stadium in Iowa City, Iowa has no national "
        "titles since 1958-59, but Kirk Ferentz, the sport's longest-tenured active head "
        "coach, has kept the Hawkeyes in bowl games in nearly every one of his 27 seasons."
    ),
    ("NCAAF", "Washington Huskies"): (
        "Founded in 1889 and playing at Husky Stadium on Lake Washington in Seattle, "
        "Washington has won two national titles (1960, 1991) and reached the 2023 CFP "
        "championship game under Kalen DeBoer before he left for Alabama, with Jedd Fisch "
        "inheriting a rebuild in the 2024 move to the Big Ten."
    ),
    ("NCAAF", "SMU Mustangs"): (
        "Founded in 1888 and playing at Gerald J. Ford Stadium in Dallas, SMU is remembered "
        "for the sport's only \"death penalty\" (the 1987 NCAA shutdown); Rhett Lashlee's "
        "rebuilt Mustangs reached the ACC title game in both 2023 and 2024, making the CFP "
        "in the latter after joining the conference."
    ),
    ("NCAAF", "Vanderbilt Commodores"): (
        "Founded in 1890 and playing at FirstBank Stadium in Nashville, the SEC's smallest "
        "campus, Vanderbilt has no national titles and is the league's historic also-ran, "
        "but Clark Lea's 2024 team went bowling for the first time since 2018 and beat "
        "Alabama for the first time in decades."
    ),
    ("NCAAF", "Nebraska Cornhuskers"): (
        "Founded in 1890 and playing at Memorial Stadium in Lincoln, home to one of the "
        "sport's longest sellout streaks, Nebraska has won five national titles, all before "
        "1998; Matt Rhule ended a seven-year bowl drought in 2024."
    ),
    ("NCAAF", "Florida State Seminoles"): (
        "Founded in 1947 and playing at Doak Campbell Stadium in Tallahassee, Florida State "
        "has won three national titles; the 2023 team went 13-0 and won the ACC but was "
        "infamously the first undefeated Power-conference champion left out of the CFP, "
        "then collapsed to a historically bad 2024."
    ),
    ("NCAAF", "Louisville Cardinals"): (
        "Founded in 1912 and playing at L&N Federal Credit Union Stadium in Louisville, "
        "Louisville has no national titles, but Jeff Brohm's 2023 arrival produced "
        "back-to-back 10-win-caliber seasons and an ACC title game appearance."
    ),
    ("NCAAF", "Utah Utes"): (
        "Founded in 1892 and playing at Rice-Eccles Stadium in Salt Lake City, Utah has no "
        "national titles, but won back-to-back Pac-12 titles in 2021-22 under Kyle "
        "Whittingham, who left for Michigan after 21 seasons; longtime defensive "
        "coordinator Morgan Scalley now leads the program in the Big 12."
    ),
    ("NCAAF", "Pittsburgh Panthers"): (
        "Founded in 1890 and playing at Acrisure Stadium (shared with the NFL's Steelers), "
        "Pitt claims nine national titles, all before 1937; Kenny Pickett's Heisman-"
        "finalist 2021 team won the program's first ACC title."
    ),
    ("NCAAF", "Virginia Cavaliers"): (
        "Founded in 1888 and playing at Scott Stadium in Charlottesville, Virginia has no "
        "national titles; the program is still rebuilding under Tony Elliott following the "
        "tragic November 2022 shooting deaths of three players, with a breakout 8-5 2024 "
        "season the clearest sign of progress."
    ),
    ("NCAAF", "Virginia Tech Hokies"): (
        "Founded in 1892 and playing at Lane Stadium in Blacksburg, famous for its \"Enter "
        "Sandman\" pregame entrance, Virginia Tech has no national titles despite a 1999 "
        "championship-game appearance; James Franklin arrives in 2026 after Brent Pry's "
        "in-season firing, a year after his own Penn State dismissal."
    ),
    ("NCAAF", "Arizona Wildcats"): (
        "Founded in 1899 and playing at Arizona Stadium in Tucson, Arizona has no national "
        "titles; the program went from a program-worst 1-11 in 2021 to a 10-3 Alamo Bowl-"
        "winning 2023 under Jedd Fisch before he left for Washington, with Brent Brennan "
        "now in charge."
    ),
    ("NCAAF", "Baylor Bears"): (
        "Founded in 1899 and playing at McLane Stadium along the Brazos River in Waco, "
        "Baylor has no national titles; the program won the 2021 Big 12 title and Sugar "
        "Bowl under Dave Aranda before back-to-back losing seasons."
    ),
    ("NCAAF", "Houston Cougars"): (
        "Founded in 1946 and playing at TDECU Stadium in Houston, Houston has no national "
        "titles; Dana Holgorsen's 12-win 2021 American Athletic Conference title season has "
        "given way to consecutive 4-8 finishes since the 2023 move to the Big 12."
    ),
    ("NCAAF", "Kentucky Wildcats"): (
        "Founded in 1881 and playing at Kroger Field in Lexington, a basketball-first "
        "school on the gridiron, Kentucky claims one conference title (1976); Mark Stoops "
        "built the program's winningest modern stretch around 2021 before a recent decline."
    ),
    ("NCAAF", "Illinois Fighting Illini"): (
        "Founded in 1890 and playing at Memorial Stadium in Champaign, Illinois has five "
        "conference titles, all before 1990; Bret Bielema's program broke through with a "
        "10-3 2024 season, its best in over a decade."
    ),
    ("NCAAF", "North Carolina Tar Heels"): (
        "Founded in 1888 and playing at Kenan Memorial Stadium in Chapel Hill, a basketball-"
        "first school on the gridiron, North Carolina has no national titles; Bill "
        "Belichick's stunning 2025 jump to college football produced a rough 4-8 debut "
        "season."
    ),
    ("NCAAF", "Kansas State Wildcats"): (
        "Founded in 1896 and playing at Bill Snyder Family Stadium in Manhattan, named for "
        "the coach who built the sport's most celebrated turnaround, Kansas State claims a "
        "share of the 2003 national title and won the 2022 Big 12 title under Chris "
        "Klieman."
    ),
    ("NCAAF", "TCU Horned Frogs"): (
        "Founded in 1896 and playing at Amon G. Carter Stadium in Fort Worth, TCU claims a "
        "share of the 1938 national title and reached the 2022 CFP championship game in a "
        "worst-to-first run under Sonny Dykes before a rebuilding stretch."
    ),
    ("NCAAF", "Arkansas Razorbacks"): (
        "Founded in 1894 and playing at Donald W. Reynolds Razorback Stadium in "
        "Fayetteville, Arkansas has three conference titles, most recently 1989 in the old "
        "Southwest Conference; Ryan Silverfield arrives in 2026 after Sam Pittman was fired "
        "just five games into 2025."
    ),
    ("NCAAF", "Mississippi State Bulldogs"): (
        "Founded in 1878 and playing at Davis Wade Stadium in Starkville, famous for its "
        "cowbell-ringing crowd noise, Mississippi State claims a share of the 1940 national "
        "title; the program has struggled to replace the late Mike Leach, who died in "
        "December 2022."
    ),
    ("NCAAF", "Wisconsin Badgers"): (
        "Founded in 1889 and playing at Camp Randall Stadium in Madison, site of the \"Jump "
        "Around\" tradition, Wisconsin has no national titles since 1901; the program's "
        "22-year bowl streak ended not long after Luke Fickell's 2023 arrival, a jarring "
        "change after the Alvarez/Chryst-era stability."
    ),
    ("NCAAF", "Duke Blue Devils"): (
        "Founded in 1888 and playing at Wallace Wade Stadium in Durham, a basketball-first "
        "school on the gridiron, Duke has no modern national titles; Mike Elko's 2022-23 "
        "turnaround (16 wins across two seasons) preceded his 2024 departure for Texas "
        "A&M, with Manny Diaz continuing the momentum."
    ),
    ("NCAAF", "Georgia Tech Yellow Jackets"): (
        "Founded in 1885 and playing at Bobby Dodd Stadium in Atlanta, Georgia Tech has won "
        "four national titles, most recently 1990; Brent Key's program broke through with "
        "the school's first bowl win since 2016 in 2023 and a 9-win 2024."
    ),
    ("NCAAF", "NC State Wolfpack"): (
        "Founded in 1892 and playing at Carter-Finley Stadium in Raleigh, NC State claims a "
        "share of the 1979 conference title; Dave Doeren has built steady 9-win seasons "
        "around consistently strong defenses."
    ),
    ("NCAAF", "Arizona State Sun Devils"): (
        "Founded in 1896 and playing at Mountain America Stadium in Tempe, Arizona State "
        "has two Pac-10 titles from the 1980s-90s but no national titles; Kenny "
        "Dillingham's 2024 team won the Big 12 title in just his second season and reached "
        "the CFP quarterfinals."
    ),
    ("NCAAF", "Cincinnati Bearcats"): (
        "Founded in 1897 and playing at Nippert Stadium, one of the oldest stadiums in "
        "college football, Cincinnati has no national titles; the 2021 team went 13-0 and "
        "became the first Group of Five program to reach the CFP under Luke Fickell, who "
        "left for Wisconsin after that season."
    ),
}

# (league, team name) -> {season_label: stats}, same stats shape
# league_rules.compute_score expects for that league (for EPL:
# standings_points, goal_differential). Only seasons the team actually
# played in this league are listed -- a promoted/relegated club's history
# has real gaps, which is correct, not a data error. Sourced from each
# season's final Premier League table.
TEAM_HISTORY_STATS: dict[tuple[str, str], dict[str, dict]] = {
    ("EPL", "Arsenal"): {
        "2021-22": {"standings_points": 69, "goal_differential": 13},
        "2022-23": {"standings_points": 84, "goal_differential": 45},
        "2023-24": {"standings_points": 89, "goal_differential": 62},
        "2024-25": {"standings_points": 74, "goal_differential": 35},
    },
    ("EPL", "Aston Villa"): {
        "2021-22": {"standings_points": 45, "goal_differential": -2},
        "2022-23": {"standings_points": 61, "goal_differential": 5},
        "2023-24": {"standings_points": 68, "goal_differential": 15},
        "2024-25": {"standings_points": 66, "goal_differential": 7},
    },
    ("EPL", "Bournemouth"): {
        # Relegated after 2019-20; not in the Premier League in 2021-22.
        "2022-23": {"standings_points": 39, "goal_differential": -34},
        "2023-24": {"standings_points": 48, "goal_differential": -13},
        "2024-25": {"standings_points": 56, "goal_differential": 12},
    },
    ("EPL", "Brentford"): {
        "2021-22": {"standings_points": 46, "goal_differential": -8},
        "2022-23": {"standings_points": 59, "goal_differential": 12},
        "2023-24": {"standings_points": 39, "goal_differential": -9},
        "2024-25": {"standings_points": 56, "goal_differential": 9},
    },
    ("EPL", "Brighton & Hove Albion"): {
        "2021-22": {"standings_points": 51, "goal_differential": -2},
        "2022-23": {"standings_points": 62, "goal_differential": 19},
        "2023-24": {"standings_points": 48, "goal_differential": -7},
        "2024-25": {"standings_points": 61, "goal_differential": 7},
    },
    ("EPL", "Chelsea"): {
        "2021-22": {"standings_points": 74, "goal_differential": 43},
        "2022-23": {"standings_points": 44, "goal_differential": -9},
        "2023-24": {"standings_points": 63, "goal_differential": 14},
        "2024-25": {"standings_points": 69, "goal_differential": 21},
    },
    # Coventry City: last played in the top flight in 2000-01, well
    # outside the range of comparable data covered so far -- no recent
    # seasons to chart yet.
    ("EPL", "Crystal Palace"): {
        "2021-22": {"standings_points": 48, "goal_differential": 4},
        "2022-23": {"standings_points": 45, "goal_differential": -9},
        "2023-24": {"standings_points": 49, "goal_differential": -1},
        "2024-25": {"standings_points": 53, "goal_differential": 0},
    },
    ("EPL", "Everton"): {
        "2021-22": {"standings_points": 39, "goal_differential": -23},
        "2022-23": {"standings_points": 36, "goal_differential": -23},
        "2023-24": {"standings_points": 40, "goal_differential": -11},
        "2024-25": {"standings_points": 48, "goal_differential": -2},
    },
    ("EPL", "Fulham"): {
        # Relegated after 2020-21; not in the Premier League in 2021-22.
        "2022-23": {"standings_points": 52, "goal_differential": 2},
        "2023-24": {"standings_points": 47, "goal_differential": -6},
        "2024-25": {"standings_points": 54, "goal_differential": 0},
    },
    # Hull City: last played in the top flight in 2016-17 -- no recent
    # seasons to chart yet.
    ("EPL", "Ipswich Town"): {
        "2024-25": {"standings_points": 22, "goal_differential": -46},
    },
    ("EPL", "Leeds United"): {
        "2021-22": {"standings_points": 38, "goal_differential": -37},
        "2022-23": {"standings_points": 31, "goal_differential": -30},
        # Relegated after 2022-23; spent 2023-24 and 2024-25 in the
        # Championship before promotion back for 2025-26.
    },
    ("EPL", "Liverpool"): {
        "2021-22": {"standings_points": 92, "goal_differential": 68},
        "2022-23": {"standings_points": 67, "goal_differential": 28},
        "2023-24": {"standings_points": 82, "goal_differential": 45},
        "2024-25": {"standings_points": 84, "goal_differential": 45},
    },
    ("EPL", "Manchester City"): {
        "2021-22": {"standings_points": 93, "goal_differential": 73},
        "2022-23": {"standings_points": 89, "goal_differential": 61},
        "2023-24": {"standings_points": 91, "goal_differential": 62},
        "2024-25": {"standings_points": 71, "goal_differential": 28},
    },
    ("EPL", "Manchester United"): {
        "2021-22": {"standings_points": 58, "goal_differential": 0},
        "2022-23": {"standings_points": 75, "goal_differential": 15},
        "2023-24": {"standings_points": 60, "goal_differential": -1},
        "2024-25": {"standings_points": 42, "goal_differential": -10},
    },
    ("EPL", "Newcastle United"): {
        "2021-22": {"standings_points": 49, "goal_differential": -18},
        "2022-23": {"standings_points": 71, "goal_differential": 35},
        "2023-24": {"standings_points": 60, "goal_differential": 23},
        "2024-25": {"standings_points": 66, "goal_differential": 21},
    },
    ("EPL", "Nottingham Forest"): {
        # Promoted for 2022-23; not in the Premier League in 2021-22.
        "2022-23": {"standings_points": 38, "goal_differential": -30},
        "2023-24": {"standings_points": 32, "goal_differential": -18},
        "2024-25": {"standings_points": 65, "goal_differential": 12},
    },
    # Sunderland: promoted for 2025-26 after last playing top-flight
    # football in 2016-17 -- no other recent seasons to chart yet.
    ("EPL", "Tottenham Hotspur"): {
        "2021-22": {"standings_points": 71, "goal_differential": 29},
        "2022-23": {"standings_points": 60, "goal_differential": 7},
        "2023-24": {"standings_points": 66, "goal_differential": 13},
        "2024-25": {"standings_points": 38, "goal_differential": -1},
    },
    # --- NFL --- (season_label is the year the season started, e.g. "2021"
    # for the season that ended with Super Bowl LVI in February 2022,
    # matching the existing TeamSeasonResult convention for this league)
    ("NFL", "Buffalo Bills"): {
        "2021": {"wins": 11, "losses": 6, "won_round1_or_bye": True, "won_round2": False},
        "2022": {"wins": 13, "losses": 3, "won_round1_or_bye": True, "won_round2": False},
        "2023": {"wins": 11, "losses": 6, "won_round1_or_bye": True, "won_round2": False},
        "2024": {"wins": 13, "losses": 4, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": False},
    },
    ("NFL", "Miami Dolphins"): {
        "2021": {"wins": 9, "losses": 8},
        "2022": {"wins": 9, "losses": 8},
        "2023": {"wins": 11, "losses": 6},
        "2024": {"wins": 8, "losses": 9},
    },
    ("NFL", "New England Patriots"): {
        "2021": {"wins": 10, "losses": 7},
        "2022": {"wins": 8, "losses": 9},
        "2023": {"wins": 4, "losses": 13},
        "2024": {"wins": 4, "losses": 13},
    },
    ("NFL", "New York Jets"): {
        "2021": {"wins": 4, "losses": 13},
        "2022": {"wins": 7, "losses": 10},
        "2023": {"wins": 7, "losses": 10},
        "2024": {"wins": 5, "losses": 12},
    },
    ("NFL", "Baltimore Ravens"): {
        "2021": {"wins": 8, "losses": 9},
        "2022": {"wins": 10, "losses": 7},
        "2023": {"wins": 13, "losses": 4, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": False},
        "2024": {"wins": 12, "losses": 5, "won_round1_or_bye": True, "won_round2": False},
    },
    ("NFL", "Cincinnati Bengals"): {
        "2021": {"wins": 10, "losses": 7, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": True, "won_sb": False},
        "2022": {"wins": 12, "losses": 4, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": False},
        "2023": {"wins": 9, "losses": 8},
        "2024": {"wins": 9, "losses": 8},
    },
    ("NFL", "Cleveland Browns"): {
        "2021": {"wins": 8, "losses": 9},
        "2022": {"wins": 7, "losses": 10},
        "2023": {"wins": 11, "losses": 6},
        "2024": {"wins": 3, "losses": 14},
    },
    ("NFL", "Pittsburgh Steelers"): {
        "2021": {"wins": 9, "losses": 8},
        "2022": {"wins": 9, "losses": 8},
        "2023": {"wins": 10, "losses": 7},
        "2024": {"wins": 10, "losses": 7},
    },
    ("NFL", "Houston Texans"): {
        "2021": {"wins": 4, "losses": 13},
        "2022": {"wins": 3, "losses": 13, "ties": 1},
        "2023": {"wins": 10, "losses": 7, "won_round1_or_bye": True, "won_round2": False},
        "2024": {"wins": 10, "losses": 7, "won_round1_or_bye": True, "won_round2": False},
    },
    ("NFL", "Indianapolis Colts"): {
        "2021": {"wins": 9, "losses": 8},
        "2022": {"wins": 4, "losses": 12, "ties": 1},
        "2023": {"wins": 9, "losses": 8},
        "2024": {"wins": 8, "losses": 9},
    },
    ("NFL", "Jacksonville Jaguars"): {
        "2021": {"wins": 2, "losses": 15},
        "2022": {"wins": 9, "losses": 8, "won_round1_or_bye": True, "won_round2": False},
        "2023": {"wins": 9, "losses": 8},
        "2024": {"wins": 4, "losses": 13},
    },
    ("NFL", "Tennessee Titans"): {
        "2021": {"wins": 12, "losses": 5, "won_round1_or_bye": True, "won_round2": False},
        "2022": {"wins": 7, "losses": 10},
        "2023": {"wins": 6, "losses": 11},
        "2024": {"wins": 3, "losses": 14},
    },
    ("NFL", "Denver Broncos"): {
        "2021": {"wins": 7, "losses": 10},
        "2022": {"wins": 5, "losses": 12},
        "2023": {"wins": 8, "losses": 9},
        "2024": {"wins": 10, "losses": 7},
    },
    ("NFL", "Kansas City Chiefs"): {
        "2021": {"wins": 12, "losses": 5, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": False},
        "2022": {"wins": 14, "losses": 3, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": True, "won_sb": True},
        "2023": {"wins": 11, "losses": 6, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": True, "won_sb": True},
        "2024": {"wins": 15, "losses": 2, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": True, "won_sb": False},
    },
    ("NFL", "Las Vegas Raiders"): {
        "2021": {"wins": 10, "losses": 7},
        "2022": {"wins": 6, "losses": 11},
        "2023": {"wins": 8, "losses": 9},
        "2024": {"wins": 4, "losses": 13},
    },
    ("NFL", "Los Angeles Chargers"): {
        "2021": {"wins": 9, "losses": 8},
        "2022": {"wins": 10, "losses": 7},
        "2023": {"wins": 5, "losses": 12},
        "2024": {"wins": 11, "losses": 6},
    },
    ("NFL", "Dallas Cowboys"): {
        "2021": {"wins": 12, "losses": 5},
        "2022": {"wins": 12, "losses": 5, "won_round1_or_bye": True, "won_round2": False},
        "2023": {"wins": 12, "losses": 5},
        "2024": {"wins": 7, "losses": 10},
    },
    ("NFL", "New York Giants"): {
        "2021": {"wins": 4, "losses": 13},
        "2022": {"wins": 9, "losses": 7, "ties": 1, "won_round1_or_bye": True, "won_round2": False},
        "2023": {"wins": 6, "losses": 11},
        "2024": {"wins": 3, "losses": 14},
    },
    ("NFL", "Philadelphia Eagles"): {
        "2021": {"wins": 9, "losses": 8},
        "2022": {"wins": 14, "losses": 3, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": True, "won_sb": False},
        "2023": {"wins": 11, "losses": 6},
        "2024": {"wins": 14, "losses": 3, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": True, "won_sb": True},
    },
    ("NFL", "Washington Commanders"): {
        # Played as the Washington Football Team in 2021, before renaming
        # to the Commanders in 2022.
        "2021": {"wins": 7, "losses": 10},
        "2022": {"wins": 8, "losses": 8, "ties": 1},
        "2023": {"wins": 4, "losses": 13},
        "2024": {"wins": 12, "losses": 5, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": False},
    },
    ("NFL", "Chicago Bears"): {
        "2021": {"wins": 6, "losses": 11},
        "2022": {"wins": 3, "losses": 14},
        "2023": {"wins": 7, "losses": 10},
        "2024": {"wins": 5, "losses": 12},
    },
    ("NFL", "Detroit Lions"): {
        "2021": {"wins": 3, "losses": 14},
        "2022": {"wins": 9, "losses": 8},
        "2023": {"wins": 12, "losses": 5, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": False},
        "2024": {"wins": 15, "losses": 2, "won_round1_or_bye": True, "won_round2": False},
    },
    ("NFL", "Green Bay Packers"): {
        "2021": {"wins": 13, "losses": 4, "won_round1_or_bye": True, "won_round2": False},
        "2022": {"wins": 8, "losses": 9},
        "2023": {"wins": 9, "losses": 8, "won_round1_or_bye": True, "won_round2": False},
        "2024": {"wins": 11, "losses": 6},
    },
    ("NFL", "Minnesota Vikings"): {
        "2021": {"wins": 8, "losses": 9},
        "2022": {"wins": 13, "losses": 4},
        "2023": {"wins": 7, "losses": 10},
        "2024": {"wins": 14, "losses": 3},
    },
    ("NFL", "Atlanta Falcons"): {
        "2021": {"wins": 7, "losses": 10},
        "2022": {"wins": 7, "losses": 10},
        "2023": {"wins": 7, "losses": 10},
        "2024": {"wins": 8, "losses": 9},
    },
    ("NFL", "Carolina Panthers"): {
        "2021": {"wins": 5, "losses": 12},
        "2022": {"wins": 7, "losses": 10},
        "2023": {"wins": 2, "losses": 15},
        "2024": {"wins": 5, "losses": 12},
    },
    ("NFL", "New Orleans Saints"): {
        "2021": {"wins": 9, "losses": 8},
        "2022": {"wins": 7, "losses": 10},
        "2023": {"wins": 9, "losses": 8},
        "2024": {"wins": 5, "losses": 12},
    },
    ("NFL", "Tampa Bay Buccaneers"): {
        "2021": {"wins": 13, "losses": 4, "won_round1_or_bye": True, "won_round2": False},
        "2022": {"wins": 8, "losses": 9},
        "2023": {"wins": 9, "losses": 8, "won_round1_or_bye": True, "won_round2": False},
        "2024": {"wins": 10, "losses": 7},
    },
    ("NFL", "Arizona Cardinals"): {
        "2021": {"wins": 11, "losses": 6},
        "2022": {"wins": 4, "losses": 13},
        "2023": {"wins": 4, "losses": 13},
        "2024": {"wins": 8, "losses": 9},
    },
    ("NFL", "Los Angeles Rams"): {
        "2021": {"wins": 12, "losses": 5, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": True, "won_sb": True},
        "2022": {"wins": 5, "losses": 12},
        "2023": {"wins": 10, "losses": 7},
        "2024": {"wins": 10, "losses": 7, "won_round1_or_bye": True, "won_round2": False},
    },
    ("NFL", "San Francisco 49ers"): {
        "2021": {"wins": 10, "losses": 7, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": False},
        "2022": {"wins": 13, "losses": 4, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": False},
        "2023": {"wins": 12, "losses": 5, "won_round1_or_bye": True, "won_round2": True, "won_conf_champ": True, "won_sb": False},
        "2024": {"wins": 6, "losses": 11},
    },
    ("NFL", "Seattle Seahawks"): {
        "2021": {"wins": 7, "losses": 10},
        "2022": {"wins": 9, "losses": 8},
        "2023": {"wins": 9, "losses": 8},
        "2024": {"wins": 10, "losses": 7},
    },
    # --- NBA --- (season_label is e.g. "2021-22" for the season whose
    # playoffs concluded with the June 2022 NBA Finals)
    ("NBA", "Boston Celtics"): {
        "2021-22": {"wins": 51, "losses": 31, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_nba_champ": False},
        "2022-23": {"wins": 57, "losses": 25, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
        "2023-24": {"wins": 64, "losses": 18, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_nba_champ": True},
        "2024-25": {"wins": 61, "losses": 21, "made_playoffs": True, "won_round1": True, "won_round2": False},
    },
    ("NBA", "Brooklyn Nets"): {
        "2021-22": {"wins": 44, "losses": 38, "made_playoffs": True},
        "2022-23": {"wins": 45, "losses": 37, "made_playoffs": True},
        "2023-24": {"wins": 32, "losses": 50},
        "2024-25": {"wins": 26, "losses": 56},
    },
    ("NBA", "New York Knicks"): {
        "2021-22": {"wins": 37, "losses": 45},
        "2022-23": {"wins": 47, "losses": 35, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2023-24": {"wins": 50, "losses": 32, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2024-25": {"wins": 51, "losses": 31, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
    },
    ("NBA", "Philadelphia 76ers"): {
        "2021-22": {"wins": 51, "losses": 31, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2022-23": {"wins": 54, "losses": 28, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2023-24": {"wins": 47, "losses": 35, "made_playoffs": True},
        "2024-25": {"wins": 24, "losses": 58},
    },
    ("NBA", "Toronto Raptors"): {
        "2021-22": {"wins": 48, "losses": 34, "made_playoffs": True},
        "2022-23": {"wins": 41, "losses": 41},
        "2023-24": {"wins": 25, "losses": 57},
        "2024-25": {"wins": 30, "losses": 52},
    },
    ("NBA", "Chicago Bulls"): {
        "2021-22": {"wins": 46, "losses": 36, "made_playoffs": True},
        "2022-23": {"wins": 40, "losses": 42},
        "2023-24": {"wins": 39, "losses": 43},
        "2024-25": {"wins": 39, "losses": 43},
    },
    ("NBA", "Cleveland Cavaliers"): {
        "2021-22": {"wins": 44, "losses": 38},
        "2022-23": {"wins": 51, "losses": 31, "made_playoffs": True},
        "2023-24": {"wins": 48, "losses": 34, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2024-25": {"wins": 64, "losses": 18, "made_playoffs": True, "won_round1": True, "won_round2": False},
    },
    ("NBA", "Detroit Pistons"): {
        "2021-22": {"wins": 23, "losses": 59},
        "2022-23": {"wins": 17, "losses": 65},
        "2023-24": {"wins": 14, "losses": 68},
        "2024-25": {"wins": 44, "losses": 38, "made_playoffs": True},
    },
    ("NBA", "Indiana Pacers"): {
        "2021-22": {"wins": 25, "losses": 57},
        "2022-23": {"wins": 35, "losses": 47},
        "2023-24": {"wins": 47, "losses": 35, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_nba_champ": False},
        "2024-25": {"wins": 50, "losses": 32, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_nba_champ": False},
    },
    ("NBA", "Milwaukee Bucks"): {
        "2021-22": {"wins": 51, "losses": 31, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2022-23": {"wins": 58, "losses": 24, "made_playoffs": True},
        "2023-24": {"wins": 49, "losses": 33, "made_playoffs": True},
        "2024-25": {"wins": 48, "losses": 34, "made_playoffs": True},
    },
    ("NBA", "Atlanta Hawks"): {
        "2021-22": {"wins": 43, "losses": 39, "made_playoffs": True},
        "2022-23": {"wins": 41, "losses": 41, "made_playoffs": True},
        "2023-24": {"wins": 36, "losses": 46},
        "2024-25": {"wins": 40, "losses": 42},
    },
    ("NBA", "Charlotte Hornets"): {
        "2021-22": {"wins": 43, "losses": 39, "made_playoffs": True},
        "2022-23": {"wins": 27, "losses": 55},
        "2023-24": {"wins": 21, "losses": 61},
        "2024-25": {"wins": 19, "losses": 63},
    },
    ("NBA", "Miami Heat"): {
        "2021-22": {"wins": 53, "losses": 29, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
        "2022-23": {"wins": 44, "losses": 38, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_nba_champ": False},
        "2023-24": {"wins": 46, "losses": 36, "made_playoffs": True},
        "2024-25": {"wins": 37, "losses": 45, "made_playoffs": True},
    },
    ("NBA", "Orlando Magic"): {
        "2021-22": {"wins": 22, "losses": 60},
        "2022-23": {"wins": 34, "losses": 48},
        "2023-24": {"wins": 47, "losses": 35, "made_playoffs": True},
        "2024-25": {"wins": 41, "losses": 41, "made_playoffs": True},
    },
    ("NBA", "Washington Wizards"): {
        "2021-22": {"wins": 35, "losses": 47},
        "2022-23": {"wins": 35, "losses": 47},
        "2023-24": {"wins": 15, "losses": 67},
        "2024-25": {"wins": 18, "losses": 64},
    },
    ("NBA", "Denver Nuggets"): {
        "2021-22": {"wins": 48, "losses": 34, "made_playoffs": True},
        "2022-23": {"wins": 53, "losses": 29, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_nba_champ": True},
        "2023-24": {"wins": 57, "losses": 25, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2024-25": {"wins": 50, "losses": 32, "made_playoffs": True, "won_round1": True, "won_round2": False},
    },
    ("NBA", "Minnesota Timberwolves"): {
        "2021-22": {"wins": 46, "losses": 36, "made_playoffs": True},
        "2022-23": {"wins": 42, "losses": 40},
        "2023-24": {"wins": 56, "losses": 26, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
        "2024-25": {"wins": 49, "losses": 33, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
    },
    ("NBA", "Oklahoma City Thunder"): {
        "2021-22": {"wins": 24, "losses": 58},
        "2022-23": {"wins": 40, "losses": 42},
        "2023-24": {"wins": 57, "losses": 25, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2024-25": {"wins": 68, "losses": 14, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_nba_champ": True},
    },
    ("NBA", "Portland Trail Blazers"): {
        "2021-22": {"wins": 27, "losses": 55},
        "2022-23": {"wins": 33, "losses": 49},
        "2023-24": {"wins": 21, "losses": 61},
        "2024-25": {"wins": 36, "losses": 46},
    },
    ("NBA", "Utah Jazz"): {
        "2021-22": {"wins": 49, "losses": 33, "made_playoffs": True},
        "2022-23": {"wins": 37, "losses": 45},
        "2023-24": {"wins": 31, "losses": 51},
        "2024-25": {"wins": 17, "losses": 65},
    },
    ("NBA", "Golden State Warriors"): {
        "2021-22": {"wins": 53, "losses": 29, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_nba_champ": True},
        "2022-23": {"wins": 44, "losses": 38, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2023-24": {"wins": 46, "losses": 36},
        "2024-25": {"wins": 48, "losses": 34, "made_playoffs": True, "won_round1": True, "won_round2": False},
    },
    ("NBA", "Los Angeles Clippers"): {
        "2021-22": {"wins": 42, "losses": 40},
        "2022-23": {"wins": 44, "losses": 38, "made_playoffs": True},
        "2023-24": {"wins": 51, "losses": 31, "made_playoffs": True},
        "2024-25": {"wins": 50, "losses": 32, "made_playoffs": True},
    },
    ("NBA", "Los Angeles Lakers"): {
        "2021-22": {"wins": 33, "losses": 49},
        "2022-23": {"wins": 43, "losses": 39, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
        "2023-24": {"wins": 47, "losses": 35, "made_playoffs": True},
        "2024-25": {"wins": 50, "losses": 32, "made_playoffs": True},
    },
    ("NBA", "Phoenix Suns"): {
        "2021-22": {"wins": 64, "losses": 18, "made_playoffs": True},
        "2022-23": {"wins": 45, "losses": 37, "made_playoffs": True},
        "2023-24": {"wins": 49, "losses": 33, "made_playoffs": True},
        "2024-25": {"wins": 36, "losses": 46},
    },
    ("NBA", "Sacramento Kings"): {
        "2021-22": {"wins": 30, "losses": 52},
        "2022-23": {"wins": 48, "losses": 34, "made_playoffs": True},
        "2023-24": {"wins": 46, "losses": 36},
        "2024-25": {"wins": 40, "losses": 42},
    },
    ("NBA", "Dallas Mavericks"): {
        "2021-22": {"wins": 52, "losses": 30, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
        "2022-23": {"wins": 38, "losses": 44},
        "2023-24": {"wins": 50, "losses": 32, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_nba_champ": False},
        "2024-25": {"wins": 39, "losses": 43},
    },
    ("NBA", "Houston Rockets"): {
        "2021-22": {"wins": 20, "losses": 62},
        "2022-23": {"wins": 22, "losses": 60},
        "2023-24": {"wins": 41, "losses": 41},
        "2024-25": {"wins": 52, "losses": 30, "made_playoffs": True, "won_round1": True, "won_round2": False},
    },
    ("NBA", "Memphis Grizzlies"): {
        "2021-22": {"wins": 56, "losses": 26, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2022-23": {"wins": 51, "losses": 31, "made_playoffs": True},
        "2023-24": {"wins": 27, "losses": 55},
        "2024-25": {"wins": 48, "losses": 34, "made_playoffs": True},
    },
    ("NBA", "New Orleans Pelicans"): {
        "2021-22": {"wins": 36, "losses": 46, "made_playoffs": True},
        "2022-23": {"wins": 42, "losses": 40},
        "2023-24": {"wins": 49, "losses": 33, "made_playoffs": True},
        "2024-25": {"wins": 21, "losses": 61},
    },
    ("NBA", "San Antonio Spurs"): {
        "2021-22": {"wins": 34, "losses": 48},
        "2022-23": {"wins": 22, "losses": 60},
        "2023-24": {"wins": 22, "losses": 60},
        "2024-25": {"wins": 34, "losses": 48},
    },
    # --- NHL --- (season_label is e.g. "2021-22" for the season whose
    # playoffs concluded with the June 2022 Stanley Cup Final)
    ("NHL", "Boston Bruins"): {
        "2021-22": {"wins": 51, "reg_losses": 26, "ot_losses": 5, "made_playoffs": True},
        "2022-23": {"wins": 65, "reg_losses": 12, "ot_losses": 5, "made_playoffs": True},
        "2023-24": {"wins": 47, "reg_losses": 20, "ot_losses": 15, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2024-25": {"wins": 33, "reg_losses": 39, "ot_losses": 10},
    },
    ("NHL", "Buffalo Sabres"): {
        "2021-22": {"wins": 32, "reg_losses": 39, "ot_losses": 11},
        "2022-23": {"wins": 42, "reg_losses": 33, "ot_losses": 7},
        "2023-24": {"wins": 39, "reg_losses": 37, "ot_losses": 6},
        "2024-25": {"wins": 36, "reg_losses": 39, "ot_losses": 7},
    },
    ("NHL", "Detroit Red Wings"): {
        "2021-22": {"wins": 32, "reg_losses": 40, "ot_losses": 10},
        "2022-23": {"wins": 35, "reg_losses": 37, "ot_losses": 10},
        "2023-24": {"wins": 41, "reg_losses": 32, "ot_losses": 9},
        "2024-25": {"wins": 39, "reg_losses": 35, "ot_losses": 8},
    },
    ("NHL", "Florida Panthers"): {
        "2021-22": {"wins": 58, "reg_losses": 18, "ot_losses": 6, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2022-23": {"wins": 42, "reg_losses": 32, "ot_losses": 8, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_cup": False},
        "2023-24": {"wins": 52, "reg_losses": 24, "ot_losses": 6, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_cup": True},
        "2024-25": {"wins": 47, "reg_losses": 31, "ot_losses": 4, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_cup": True},
    },
    ("NHL", "Montreal Canadiens"): {
        "2021-22": {"wins": 22, "reg_losses": 49, "ot_losses": 11},
        "2022-23": {"wins": 31, "reg_losses": 45, "ot_losses": 6},
        "2023-24": {"wins": 30, "reg_losses": 36, "ot_losses": 16},
        "2024-25": {"wins": 40, "reg_losses": 31, "ot_losses": 11, "made_playoffs": True},
    },
    ("NHL", "Ottawa Senators"): {
        "2021-22": {"wins": 33, "reg_losses": 42, "ot_losses": 7},
        "2022-23": {"wins": 39, "reg_losses": 35, "ot_losses": 8},
        "2023-24": {"wins": 37, "reg_losses": 41, "ot_losses": 4},
        "2024-25": {"wins": 45, "reg_losses": 30, "ot_losses": 7, "made_playoffs": True},
    },
    ("NHL", "Tampa Bay Lightning"): {
        "2021-22": {"wins": 51, "reg_losses": 23, "ot_losses": 8, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_cup": False},
        "2022-23": {"wins": 46, "reg_losses": 30, "ot_losses": 6, "made_playoffs": True},
        "2023-24": {"wins": 45, "reg_losses": 29, "ot_losses": 8, "made_playoffs": True},
        "2024-25": {"wins": 47, "reg_losses": 27, "ot_losses": 8, "made_playoffs": True},
    },
    ("NHL", "Toronto Maple Leafs"): {
        "2021-22": {"wins": 54, "reg_losses": 21, "ot_losses": 7, "made_playoffs": True},
        "2022-23": {"wins": 50, "reg_losses": 21, "ot_losses": 11, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2023-24": {"wins": 46, "reg_losses": 26, "ot_losses": 10, "made_playoffs": True},
        "2024-25": {"wins": 52, "reg_losses": 26, "ot_losses": 4, "made_playoffs": True, "won_round1": True, "won_round2": False},
    },
    ("NHL", "Carolina Hurricanes"): {
        "2021-22": {"wins": 54, "reg_losses": 20, "ot_losses": 8, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2022-23": {"wins": 52, "reg_losses": 21, "ot_losses": 9, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
        "2023-24": {"wins": 52, "reg_losses": 23, "ot_losses": 7, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2024-25": {"wins": 47, "reg_losses": 30, "ot_losses": 5, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
    },
    ("NHL", "Columbus Blue Jackets"): {
        "2021-22": {"wins": 37, "reg_losses": 38, "ot_losses": 7},
        "2022-23": {"wins": 25, "reg_losses": 48, "ot_losses": 9},
        "2023-24": {"wins": 27, "reg_losses": 43, "ot_losses": 12},
        "2024-25": {"wins": 40, "reg_losses": 33, "ot_losses": 9},
    },
    ("NHL", "New Jersey Devils"): {
        "2021-22": {"wins": 27, "reg_losses": 46, "ot_losses": 9},
        "2022-23": {"wins": 52, "reg_losses": 22, "ot_losses": 8, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2023-24": {"wins": 38, "reg_losses": 39, "ot_losses": 5},
        "2024-25": {"wins": 42, "reg_losses": 33, "ot_losses": 7, "made_playoffs": True, "won_round1": True, "won_round2": False},
    },
    ("NHL", "New York Islanders"): {
        "2021-22": {"wins": 37, "reg_losses": 35, "ot_losses": 10},
        "2022-23": {"wins": 42, "reg_losses": 31, "ot_losses": 9, "made_playoffs": True},
        "2023-24": {"wins": 39, "reg_losses": 27, "ot_losses": 16, "made_playoffs": True},
        "2024-25": {"wins": 35, "reg_losses": 35, "ot_losses": 12},
    },
    ("NHL", "New York Rangers"): {
        "2021-22": {"wins": 52, "reg_losses": 24, "ot_losses": 6, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
        "2022-23": {"wins": 47, "reg_losses": 22, "ot_losses": 13, "made_playoffs": True},
        "2023-24": {"wins": 55, "reg_losses": 23, "ot_losses": 4, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
        "2024-25": {"wins": 39, "reg_losses": 36, "ot_losses": 7},
    },
    ("NHL", "Philadelphia Flyers"): {
        "2021-22": {"wins": 25, "reg_losses": 46, "ot_losses": 11},
        "2022-23": {"wins": 31, "reg_losses": 38, "ot_losses": 13},
        "2023-24": {"wins": 38, "reg_losses": 33, "ot_losses": 11},
        "2024-25": {"wins": 33, "reg_losses": 39, "ot_losses": 10},
    },
    ("NHL", "Pittsburgh Penguins"): {
        "2021-22": {"wins": 46, "reg_losses": 25, "ot_losses": 11, "made_playoffs": True},
        "2022-23": {"wins": 40, "reg_losses": 31, "ot_losses": 11},
        "2023-24": {"wins": 38, "reg_losses": 32, "ot_losses": 12},
        "2024-25": {"wins": 34, "reg_losses": 36, "ot_losses": 12},
    },
    ("NHL", "Washington Capitals"): {
        "2021-22": {"wins": 44, "reg_losses": 26, "ot_losses": 12, "made_playoffs": True},
        "2022-23": {"wins": 35, "reg_losses": 37, "ot_losses": 10},
        "2023-24": {"wins": 40, "reg_losses": 31, "ot_losses": 11, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2024-25": {"wins": 51, "reg_losses": 22, "ot_losses": 9, "made_playoffs": True, "won_round1": True, "won_round2": False},
    },
    ("NHL", "Chicago Blackhawks"): {
        "2021-22": {"wins": 28, "reg_losses": 42, "ot_losses": 12},
        "2022-23": {"wins": 26, "reg_losses": 49, "ot_losses": 7},
        "2023-24": {"wins": 23, "reg_losses": 53, "ot_losses": 6},
        "2024-25": {"wins": 25, "reg_losses": 46, "ot_losses": 11},
    },
    ("NHL", "Colorado Avalanche"): {
        "2021-22": {"wins": 56, "reg_losses": 19, "ot_losses": 7, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_cup": True},
        "2022-23": {"wins": 51, "reg_losses": 24, "ot_losses": 7, "made_playoffs": True},
        "2023-24": {"wins": 50, "reg_losses": 25, "ot_losses": 7, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2024-25": {"wins": 49, "reg_losses": 29, "ot_losses": 4, "made_playoffs": True},
    },
    ("NHL", "Dallas Stars"): {
        "2021-22": {"wins": 46, "reg_losses": 30, "ot_losses": 6, "made_playoffs": True},
        "2022-23": {"wins": 47, "reg_losses": 21, "ot_losses": 14, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
        "2023-24": {"wins": 52, "reg_losses": 21, "ot_losses": 9, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
        "2024-25": {"wins": 50, "reg_losses": 26, "ot_losses": 6, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
    },
    ("NHL", "Minnesota Wild"): {
        "2021-22": {"wins": 53, "reg_losses": 22, "ot_losses": 7, "made_playoffs": True},
        "2022-23": {"wins": 46, "reg_losses": 25, "ot_losses": 11, "made_playoffs": True},
        "2023-24": {"wins": 39, "reg_losses": 34, "ot_losses": 9},
        "2024-25": {"wins": 45, "reg_losses": 30, "ot_losses": 7, "made_playoffs": True, "won_round1": False},
    },
    ("NHL", "Nashville Predators"): {
        "2021-22": {"wins": 45, "reg_losses": 30, "ot_losses": 7, "made_playoffs": True},
        "2022-23": {"wins": 42, "reg_losses": 32, "ot_losses": 8},
        "2023-24": {"wins": 47, "reg_losses": 30, "ot_losses": 5, "made_playoffs": True},
        "2024-25": {"wins": 30, "reg_losses": 44, "ot_losses": 8},
    },
    ("NHL", "St. Louis Blues"): {
        "2021-22": {"wins": 49, "reg_losses": 22, "ot_losses": 11, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2022-23": {"wins": 37, "reg_losses": 38, "ot_losses": 7},
        "2023-24": {"wins": 43, "reg_losses": 33, "ot_losses": 6},
        "2024-25": {"wins": 44, "reg_losses": 30, "ot_losses": 8, "made_playoffs": True},
    },
    ("NHL", "Utah Mammoth"): {
        # Franchise history as the Arizona Coyotes through 2023-24 (last
        # season in Arizona), then the placeholder "Utah Hockey Club" in
        # 2024-25 before the 2025 Mammoth rename -- same continuous
        # franchise, attributed here to its current name.
        "2021-22": {"wins": 25, "reg_losses": 50, "ot_losses": 7},
        "2022-23": {"wins": 28, "reg_losses": 40, "ot_losses": 14},
        "2023-24": {"wins": 36, "reg_losses": 41, "ot_losses": 5},
        "2024-25": {"wins": 38, "reg_losses": 31, "ot_losses": 13},
    },
    ("NHL", "Winnipeg Jets"): {
        "2021-22": {"wins": 39, "reg_losses": 32, "ot_losses": 11},
        "2022-23": {"wins": 46, "reg_losses": 33, "ot_losses": 3, "made_playoffs": True},
        "2023-24": {"wins": 52, "reg_losses": 24, "ot_losses": 6, "made_playoffs": True, "won_round1": False},
        "2024-25": {"wins": 56, "reg_losses": 22, "ot_losses": 4, "made_playoffs": True, "won_round1": True, "won_round2": False},
    },
    ("NHL", "Anaheim Ducks"): {
        "2021-22": {"wins": 31, "reg_losses": 37, "ot_losses": 14},
        "2022-23": {"wins": 23, "reg_losses": 47, "ot_losses": 12},
        "2023-24": {"wins": 27, "reg_losses": 50, "ot_losses": 5},
        "2024-25": {"wins": 35, "reg_losses": 37, "ot_losses": 10},
    },
    ("NHL", "Calgary Flames"): {
        "2021-22": {"wins": 50, "reg_losses": 21, "ot_losses": 11, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2022-23": {"wins": 38, "reg_losses": 27, "ot_losses": 17},
        "2023-24": {"wins": 38, "reg_losses": 39, "ot_losses": 5},
        "2024-25": {"wins": 41, "reg_losses": 27, "ot_losses": 14},
    },
    ("NHL", "Edmonton Oilers"): {
        "2021-22": {"wins": 49, "reg_losses": 27, "ot_losses": 6, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": False},
        "2022-23": {"wins": 50, "reg_losses": 23, "ot_losses": 9, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2023-24": {"wins": 49, "reg_losses": 27, "ot_losses": 6, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_cup": False},
        "2024-25": {"wins": 48, "reg_losses": 29, "ot_losses": 5, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_cup": False},
    },
    ("NHL", "Los Angeles Kings"): {
        "2021-22": {"wins": 44, "reg_losses": 27, "ot_losses": 11, "made_playoffs": True},
        "2022-23": {"wins": 47, "reg_losses": 25, "ot_losses": 10, "made_playoffs": True},
        "2023-24": {"wins": 44, "reg_losses": 27, "ot_losses": 11, "made_playoffs": True},
        "2024-25": {"wins": 48, "reg_losses": 25, "ot_losses": 9, "made_playoffs": True},
    },
    ("NHL", "San Jose Sharks"): {
        "2021-22": {"wins": 32, "reg_losses": 37, "ot_losses": 13},
        "2022-23": {"wins": 22, "reg_losses": 44, "ot_losses": 16},
        "2023-24": {"wins": 19, "reg_losses": 54, "ot_losses": 9},
        "2024-25": {"wins": 20, "reg_losses": 50, "ot_losses": 12},
    },
    ("NHL", "Seattle Kraken"): {
        "2021-22": {"wins": 27, "reg_losses": 49, "ot_losses": 6},
        "2022-23": {"wins": 46, "reg_losses": 28, "ot_losses": 8, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2023-24": {"wins": 34, "reg_losses": 35, "ot_losses": 13},
        "2024-25": {"wins": 35, "reg_losses": 41, "ot_losses": 6},
    },
    ("NHL", "Vancouver Canucks"): {
        "2021-22": {"wins": 40, "reg_losses": 30, "ot_losses": 12},
        "2022-23": {"wins": 38, "reg_losses": 37, "ot_losses": 7},
        "2023-24": {"wins": 50, "reg_losses": 23, "ot_losses": 9, "made_playoffs": True, "won_round1": True, "won_round2": False},
        "2024-25": {"wins": 38, "reg_losses": 30, "ot_losses": 14},
    },
    ("NHL", "Vegas Golden Knights"): {
        "2021-22": {"wins": 43, "reg_losses": 31, "ot_losses": 8},
        "2022-23": {"wins": 51, "reg_losses": 22, "ot_losses": 9, "made_playoffs": True, "won_round1": True, "won_round2": True, "won_conf_champ": True, "won_cup": True},
        "2023-24": {"wins": 45, "reg_losses": 29, "ot_losses": 8, "made_playoffs": True},
        "2024-25": {"wins": 50, "reg_losses": 22, "ot_losses": 10, "made_playoffs": True, "won_round1": True, "won_round2": False},
    },
    # --- URC --- (season_label is e.g. "2021-22" for the season whose
    # Grand Final concluded that June; 2021-22 was the URC's first season,
    # replacing the old Pro14 and adding the four South African sides)
    ("URC", "Leinster"): {
        "2021-22": {"table_points": 67, "points_difference": 270, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": False},
        "2022-23": {"table_points": 79, "points_difference": 217, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": False},
        "2023-24": {"table_points": 65, "points_difference": 204, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": False},
        "2024-25": {"table_points": 76, "points_difference": 286, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": True, "won_final": True},
    },
    ("URC", "Munster"): {
        "2021-22": {"table_points": 56, "points_difference": 183, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": False},
        "2022-23": {"table_points": 55, "points_difference": 113, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": True, "won_final": True},
        "2023-24": {"table_points": 68, "points_difference": 165, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": False},
        "2024-25": {"table_points": 51, "points_difference": 15, "made_playoffs": True, "won_quarterfinal": False},
    },
    ("URC", "Connacht"): {
        "2021-22": {"table_points": 41, "points_difference": -103},
        "2022-23": {"table_points": 50, "points_difference": 30, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": False},
        "2023-24": {"table_points": 45, "points_difference": -28},
        "2024-25": {"table_points": 39, "points_difference": -52},
    },
    ("URC", "Ulster"): {
        "2021-22": {"table_points": 59, "points_difference": 115, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": False},
        "2022-23": {"table_points": 68, "points_difference": 176, "made_playoffs": True, "won_quarterfinal": False},
        "2023-24": {"table_points": 54, "points_difference": 28, "made_playoffs": True, "won_quarterfinal": False},
        "2024-25": {"table_points": 38, "points_difference": -92},
    },
    ("URC", "Cardiff"): {
        "2021-22": {"table_points": 32, "points_difference": -208},
        "2022-23": {"table_points": 44, "points_difference": -45},
        "2023-24": {"table_points": 32, "points_difference": -26},
        "2024-25": {"table_points": 47, "points_difference": -68},
    },
    ("URC", "Ospreys"): {
        "2021-22": {"table_points": 46, "points_difference": -52},
        "2022-23": {"table_points": 35, "points_difference": -114},
        "2023-24": {"table_points": 50, "points_difference": -35, "made_playoffs": True, "won_quarterfinal": False},
        "2024-25": {"table_points": 40, "points_difference": -17},
    },
    ("URC", "Scarlets"): {
        "2021-22": {"table_points": 45, "points_difference": -40},
        "2022-23": {"table_points": 34, "points_difference": -71},
        "2023-24": {"table_points": 27, "points_difference": -262},
        "2024-25": {"table_points": 48, "points_difference": 45, "made_playoffs": True, "won_quarterfinal": False},
    },
    ("URC", "Dragons"): {
        "2021-22": {"table_points": 19, "points_difference": -242},
        "2022-23": {"table_points": 24, "points_difference": -143},
        "2023-24": {"table_points": 16, "points_difference": -311},
        "2024-25": {"table_points": 9, "points_difference": -302},
    },
    ("URC", "Bulls"): {
        "2021-22": {"table_points": 58, "points_difference": 130, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": True, "won_final": False},
        "2022-23": {"table_points": 53, "points_difference": 165, "made_playoffs": True, "won_quarterfinal": False},
        "2023-24": {"table_points": 66, "points_difference": 206, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": True, "won_final": False},
        "2024-25": {"table_points": 68, "points_difference": 181, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": True, "won_final": False},
    },
    ("URC", "Lions"): {
        "2021-22": {"table_points": 41, "points_difference": -42},
        "2022-23": {"table_points": 45, "points_difference": -84},
        "2023-24": {"table_points": 50, "points_difference": 128},
        "2024-25": {"table_points": 40, "points_difference": -38},
    },
    ("URC", "Sharks"): {
        "2021-22": {"table_points": 57, "points_difference": 145, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": False},
        "2022-23": {"table_points": 48, "points_difference": 6, "made_playoffs": True, "won_quarterfinal": False},
        "2023-24": {"table_points": 25, "points_difference": -88},
        "2024-25": {"table_points": 62, "points_difference": 34, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": False},
    },
    ("URC", "Stormers"): {
        "2021-22": {"table_points": 61, "points_difference": 153, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": True, "won_final": True},
        "2022-23": {"table_points": 68, "points_difference": 140, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": True, "won_final": False},
        "2023-24": {"table_points": 59, "points_difference": 120, "made_playoffs": True, "won_quarterfinal": False},
        "2024-25": {"table_points": 55, "points_difference": 89, "made_playoffs": True, "won_quarterfinal": False},
    },
    ("URC", "Glasgow Warriors"): {
        "2021-22": {"table_points": 50, "points_difference": 33, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": False},
        "2022-23": {"table_points": 63, "points_difference": 95, "made_playoffs": True, "won_quarterfinal": False},
        "2023-24": {"table_points": 65, "points_difference": 166, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": True, "won_final": True},
        "2024-25": {"table_points": 59, "points_difference": 141, "made_playoffs": True, "won_quarterfinal": True, "won_semifinal": False},
    },
    ("URC", "Edinburgh"): {
        "2021-22": {"table_points": 54, "points_difference": 103, "made_playoffs": True, "won_quarterfinal": False},
        "2022-23": {"table_points": 38, "points_difference": -1},
        "2023-24": {"table_points": 49, "points_difference": 19},
        "2024-25": {"table_points": 49, "points_difference": 64, "made_playoffs": True, "won_quarterfinal": False},
    },
    ("URC", "Benetton"): {
        "2021-22": {"table_points": 35, "points_difference": -76},
        "2022-23": {"table_points": 41, "points_difference": -93},
        "2023-24": {"table_points": 54, "points_difference": 11, "made_playoffs": True, "won_quarterfinal": False},
        "2024-25": {"table_points": 46, "points_difference": -85},
    },
    ("URC", "Zebre Parma"): {
        "2021-22": {"table_points": 9, "points_difference": -369},
        "2022-23": {"table_points": 11, "points_difference": -391},
        "2023-24": {"table_points": 15, "points_difference": -298},
        "2024-25": {"table_points": 29, "points_difference": -201},
    },

    # --- NCAAF --- (season_label is the year the season was played, matching
    # seed_historical_results.py's convention -- the live "2025" row picks up
    # from where this leaves off). Compiled from each team's Wikipedia
    # season-by-season records plus the four CFP brackets' actual results;
    # less-covered programs' plain win-loss (no CFP appearance) is best
    # effort and could be off by a game in a couple of spots, same caveat as
    # this file's other proxy/approximate sections.
    ("NCAAF", "Ohio State Buckeyes"): {
        "2021": {"wins": 11, "reg_season_losses": 1},
        "2022": {"wins": 11, "reg_season_losses": 1, "playoff_bid": True, "playoff_wins": 0},
        "2023": {"wins": 11, "reg_season_losses": 1},
        "2024": {"wins": 14, "reg_season_losses": 2, "playoff_bid": True, "playoff_wins": 3, "championship_bid": True, "championship_win": True},
    },
    ("NCAAF", "Georgia Bulldogs"): {
        "2021": {"wins": 14, "reg_season_losses": 1, "playoff_bid": True, "playoff_wins": 1, "championship_bid": True, "championship_win": True},
        "2022": {"wins": 15, "reg_season_losses": 0, "playoff_bid": True, "playoff_wins": 1, "championship_bid": True, "championship_win": True},
        "2023": {"wins": 13, "reg_season_losses": 1},
        "2024": {"wins": 11, "reg_season_losses": 2, "playoff_bid": True, "playoff_bye": True, "playoff_wins": 0},
    },
    ("NCAAF", "Texas Longhorns"): {
        "2021": {"wins": 5, "reg_season_losses": 7},
        "2022": {"wins": 8, "reg_season_losses": 5},
        "2023": {"wins": 12, "reg_season_losses": 1, "playoff_bid": True, "playoff_wins": 0},
        "2024": {"wins": 13, "reg_season_losses": 2, "playoff_bid": True, "playoff_wins": 2},
    },
    ("NCAAF", "Indiana Hoosiers"): {
        "2021": {"wins": 2, "reg_season_losses": 10},
        "2022": {"wins": 4, "reg_season_losses": 8},
        "2023": {"wins": 3, "reg_season_losses": 9},
        "2024": {"wins": 11, "reg_season_losses": 1, "playoff_bid": True, "playoff_wins": 0},
    },
    ("NCAAF", "Oregon Ducks"): {
        "2021": {"wins": 10, "reg_season_losses": 3},
        "2022": {"wins": 10, "reg_season_losses": 3},
        "2023": {"wins": 12, "reg_season_losses": 2},
        "2024": {"wins": 13, "reg_season_losses": 0, "playoff_bid": True, "playoff_bye": True, "playoff_wins": 0},
    },
    ("NCAAF", "Notre Dame Fighting Irish"): {
        "2021": {"wins": 11, "reg_season_losses": 1},
        "2022": {"wins": 9, "reg_season_losses": 4},
        "2023": {"wins": 10, "reg_season_losses": 1},
        "2024": {"wins": 14, "reg_season_losses": 1, "playoff_bid": True, "playoff_wins": 3, "championship_bid": True, "championship_win": False},
    },
    ("NCAAF", "Alabama Crimson Tide"): {
        "2021": {"wins": 13, "reg_season_losses": 1, "playoff_bid": True, "playoff_wins": 1, "championship_bid": True, "championship_win": False},
        "2022": {"wins": 11, "reg_season_losses": 2},
        "2023": {"wins": 12, "reg_season_losses": 1, "playoff_bid": True, "playoff_wins": 0},
        "2024": {"wins": 9, "reg_season_losses": 4},
    },
    ("NCAAF", "LSU Tigers"): {
        "2021": {"wins": 6, "reg_season_losses": 6},
        "2022": {"wins": 10, "reg_season_losses": 4},
        "2023": {"wins": 10, "reg_season_losses": 3},
        "2024": {"wins": 10, "reg_season_losses": 3},
    },
    ("NCAAF", "Texas A&M Aggies"): {
        "2021": {"wins": 8, "reg_season_losses": 4},
        "2022": {"wins": 5, "reg_season_losses": 7},
        "2023": {"wins": 7, "reg_season_losses": 5},
        "2024": {"wins": 8, "reg_season_losses": 4},
    },
    ("NCAAF", "Miami (FL) Hurricanes"): {
        "2021": {"wins": 7, "reg_season_losses": 5},
        "2022": {"wins": 5, "reg_season_losses": 7},
        "2023": {"wins": 7, "reg_season_losses": 5},
        "2024": {"wins": 10, "reg_season_losses": 2},
    },
    ("NCAAF", "Texas Tech Red Raiders"): {
        "2021": {"wins": 7, "reg_season_losses": 6},
        "2022": {"wins": 8, "reg_season_losses": 5},
        "2023": {"wins": 7, "reg_season_losses": 6},
        "2024": {"wins": 8, "reg_season_losses": 5},
    },
    ("NCAAF", "Oklahoma Sooners"): {
        "2021": {"wins": 11, "reg_season_losses": 1},
        "2022": {"wins": 6, "reg_season_losses": 6},
        "2023": {"wins": 10, "reg_season_losses": 3},
        "2024": {"wins": 6, "reg_season_losses": 7},
    },
    ("NCAAF", "USC Trojans"): {
        "2021": {"wins": 4, "reg_season_losses": 8},
        "2022": {"wins": 11, "reg_season_losses": 2},
        "2023": {"wins": 8, "reg_season_losses": 4},
        "2024": {"wins": 6, "reg_season_losses": 7},
    },
    ("NCAAF", "Ole Miss Rebels"): {
        "2021": {"wins": 10, "reg_season_losses": 2},
        "2022": {"wins": 8, "reg_season_losses": 4},
        "2023": {"wins": 11, "reg_season_losses": 2},
        "2024": {"wins": 11, "reg_season_losses": 2},
    },
    ("NCAAF", "Tennessee Volunteers"): {
        "2021": {"wins": 7, "reg_season_losses": 5},
        "2022": {"wins": 11, "reg_season_losses": 1},
        "2023": {"wins": 9, "reg_season_losses": 4},
        "2024": {"wins": 10, "reg_season_losses": 2, "playoff_bid": True, "playoff_wins": 0},
    },
    ("NCAAF", "Michigan Wolverines"): {
        "2021": {"wins": 12, "reg_season_losses": 1, "playoff_bid": True, "playoff_wins": 0},
        "2022": {"wins": 13, "reg_season_losses": 0, "playoff_bid": True, "playoff_wins": 0},
        "2023": {"wins": 15, "reg_season_losses": 0, "playoff_bid": True, "playoff_wins": 1, "championship_bid": True, "championship_win": True},
        "2024": {"wins": 8, "reg_season_losses": 4},
    },
    ("NCAAF", "Auburn Tigers"): {
        "2021": {"wins": 6, "reg_season_losses": 6},
        "2022": {"wins": 5, "reg_season_losses": 7},
        "2023": {"wins": 6, "reg_season_losses": 7},
        "2024": {"wins": 5, "reg_season_losses": 7},
    },
    ("NCAAF", "Florida Gators"): {
        "2021": {"wins": 6, "reg_season_losses": 7},
        "2022": {"wins": 6, "reg_season_losses": 7},
        "2023": {"wins": 5, "reg_season_losses": 7},
        "2024": {"wins": 8, "reg_season_losses": 5},
    },
    ("NCAAF", "Missouri Tigers"): {
        "2021": {"wins": 6, "reg_season_losses": 6},
        "2022": {"wins": 6, "reg_season_losses": 6},
        "2023": {"wins": 11, "reg_season_losses": 2},
        "2024": {"wins": 10, "reg_season_losses": 3},
    },
    ("NCAAF", "Penn State Nittany Lions"): {
        "2021": {"wins": 7, "reg_season_losses": 5},
        "2022": {"wins": 11, "reg_season_losses": 2},
        "2023": {"wins": 10, "reg_season_losses": 2},
        "2024": {"wins": 13, "reg_season_losses": 2, "playoff_bid": True, "playoff_wins": 2},
    },
    ("NCAAF", "Clemson Tigers"): {
        "2021": {"wins": 10, "reg_season_losses": 2},
        "2022": {"wins": 11, "reg_season_losses": 2},
        "2023": {"wins": 9, "reg_season_losses": 4},
        "2024": {"wins": 10, "reg_season_losses": 3, "playoff_bid": True, "playoff_wins": 0},
    },
    ("NCAAF", "BYU Cougars"): {
        "2021": {"wins": 10, "reg_season_losses": 2},
        "2022": {"wins": 8, "reg_season_losses": 5},
        "2023": {"wins": 5, "reg_season_losses": 7},
        "2024": {"wins": 11, "reg_season_losses": 2},
    },
    ("NCAAF", "South Carolina Gamecocks"): {
        "2021": {"wins": 7, "reg_season_losses": 6},
        "2022": {"wins": 8, "reg_season_losses": 4},
        "2023": {"wins": 5, "reg_season_losses": 7},
        "2024": {"wins": 9, "reg_season_losses": 2},
    },
    ("NCAAF", "Iowa Hawkeyes"): {
        "2021": {"wins": 11, "reg_season_losses": 1},
        "2022": {"wins": 10, "reg_season_losses": 3},
        "2023": {"wins": 10, "reg_season_losses": 3},
        "2024": {"wins": 8, "reg_season_losses": 4},
    },
    ("NCAAF", "Washington Huskies"): {
        "2021": {"wins": 4, "reg_season_losses": 8},
        "2022": {"wins": 11, "reg_season_losses": 2},
        "2023": {"wins": 14, "reg_season_losses": 0, "playoff_bid": True, "playoff_wins": 1, "championship_bid": True, "championship_win": False},
        "2024": {"wins": 6, "reg_season_losses": 6},
    },
    ("NCAAF", "SMU Mustangs"): {
        "2021": {"wins": 8, "reg_season_losses": 4},
        "2022": {"wins": 7, "reg_season_losses": 5},
        "2023": {"wins": 11, "reg_season_losses": 2},
        "2024": {"wins": 11, "reg_season_losses": 1, "playoff_bid": True, "playoff_wins": 0},
    },
    ("NCAAF", "Vanderbilt Commodores"): {
        "2021": {"wins": 2, "reg_season_losses": 10},
        "2022": {"wins": 5, "reg_season_losses": 7},
        "2023": {"wins": 6, "reg_season_losses": 7},
        "2024": {"wins": 7, "reg_season_losses": 6},
    },
    ("NCAAF", "Nebraska Cornhuskers"): {
        "2021": {"wins": 3, "reg_season_losses": 9},
        "2022": {"wins": 4, "reg_season_losses": 8},
        "2023": {"wins": 5, "reg_season_losses": 7},
        "2024": {"wins": 7, "reg_season_losses": 6},
    },
    ("NCAAF", "Florida State Seminoles"): {
        "2021": {"wins": 5, "reg_season_losses": 7},
        "2022": {"wins": 10, "reg_season_losses": 3},
        "2023": {"wins": 13, "reg_season_losses": 0},
        "2024": {"wins": 2, "reg_season_losses": 10},
    },
    ("NCAAF", "Louisville Cardinals"): {
        "2021": {"wins": 6, "reg_season_losses": 6},
        "2022": {"wins": 8, "reg_season_losses": 5},
        "2023": {"wins": 10, "reg_season_losses": 3},
        "2024": {"wins": 9, "reg_season_losses": 4},
    },
    ("NCAAF", "Utah Utes"): {
        "2021": {"wins": 10, "reg_season_losses": 3},
        "2022": {"wins": 10, "reg_season_losses": 3},
        "2023": {"wins": 8, "reg_season_losses": 5},
        "2024": {"wins": 5, "reg_season_losses": 7},
    },
    ("NCAAF", "Pittsburgh Panthers"): {
        "2021": {"wins": 11, "reg_season_losses": 2},
        "2022": {"wins": 9, "reg_season_losses": 4},
        "2023": {"wins": 3, "reg_season_losses": 9},
        "2024": {"wins": 7, "reg_season_losses": 5},
    },
    ("NCAAF", "Virginia Cavaliers"): {
        "2021": {"wins": 6, "reg_season_losses": 6},
        "2022": {"wins": 3, "reg_season_losses": 7},
        "2023": {"wins": 3, "reg_season_losses": 9},
        "2024": {"wins": 8, "reg_season_losses": 5},
    },
    ("NCAAF", "Virginia Tech Hokies"): {
        "2021": {"wins": 6, "reg_season_losses": 6},
        "2022": {"wins": 7, "reg_season_losses": 6},
        "2023": {"wins": 4, "reg_season_losses": 8},
        "2024": {"wins": 6, "reg_season_losses": 6},
    },
    ("NCAAF", "Arizona Wildcats"): {
        "2021": {"wins": 1, "reg_season_losses": 11},
        "2022": {"wins": 5, "reg_season_losses": 7},
        "2023": {"wins": 10, "reg_season_losses": 3},
        "2024": {"wins": 6, "reg_season_losses": 6},
    },
    ("NCAAF", "Baylor Bears"): {
        "2021": {"wins": 12, "reg_season_losses": 2},
        "2022": {"wins": 6, "reg_season_losses": 6},
        "2023": {"wins": 3, "reg_season_losses": 9},
        "2024": {"wins": 8, "reg_season_losses": 4},
    },
    ("NCAAF", "Houston Cougars"): {
        "2021": {"wins": 12, "reg_season_losses": 2},
        "2022": {"wins": 8, "reg_season_losses": 5},
        "2023": {"wins": 4, "reg_season_losses": 8},
        "2024": {"wins": 4, "reg_season_losses": 8},
    },
    ("NCAAF", "Kentucky Wildcats"): {
        "2021": {"wins": 10, "reg_season_losses": 3},
        "2022": {"wins": 7, "reg_season_losses": 6},
        "2023": {"wins": 6, "reg_season_losses": 6},
        "2024": {"wins": 4, "reg_season_losses": 8},
    },
    ("NCAAF", "Illinois Fighting Illini"): {
        "2021": {"wins": 5, "reg_season_losses": 7},
        "2022": {"wins": 8, "reg_season_losses": 4},
        "2023": {"wins": 5, "reg_season_losses": 7},
        "2024": {"wins": 10, "reg_season_losses": 3},
    },
    ("NCAAF", "North Carolina Tar Heels"): {
        "2021": {"wins": 6, "reg_season_losses": 6},
        "2022": {"wins": 9, "reg_season_losses": 4},
        "2023": {"wins": 8, "reg_season_losses": 4},
        "2024": {"wins": 5, "reg_season_losses": 8},
    },
    ("NCAAF", "Kansas State Wildcats"): {
        "2021": {"wins": 8, "reg_season_losses": 5},
        "2022": {"wins": 10, "reg_season_losses": 3},
        "2023": {"wins": 9, "reg_season_losses": 4},
        "2024": {"wins": 9, "reg_season_losses": 4},
    },
    ("NCAAF", "TCU Horned Frogs"): {
        "2021": {"wins": 5, "reg_season_losses": 7},
        "2022": {"wins": 13, "reg_season_losses": 1, "playoff_bid": True, "playoff_wins": 1, "championship_bid": True, "championship_win": False},
        "2023": {"wins": 5, "reg_season_losses": 7},
        "2024": {"wins": 9, "reg_season_losses": 4},
    },
    ("NCAAF", "Arkansas Razorbacks"): {
        "2021": {"wins": 9, "reg_season_losses": 4},
        "2022": {"wins": 7, "reg_season_losses": 6},
        "2023": {"wins": 4, "reg_season_losses": 8},
        "2024": {"wins": 7, "reg_season_losses": 6},
    },
    ("NCAAF", "Mississippi State Bulldogs"): {
        "2021": {"wins": 7, "reg_season_losses": 5},
        "2022": {"wins": 9, "reg_season_losses": 4},
        "2023": {"wins": 5, "reg_season_losses": 7},
        "2024": {"wins": 5, "reg_season_losses": 6},
    },
    ("NCAAF", "Wisconsin Badgers"): {
        "2021": {"wins": 9, "reg_season_losses": 4},
        "2022": {"wins": 7, "reg_season_losses": 6},
        "2023": {"wins": 7, "reg_season_losses": 5},
        "2024": {"wins": 5, "reg_season_losses": 7},
    },
    ("NCAAF", "Duke Blue Devils"): {
        "2021": {"wins": 3, "reg_season_losses": 9},
        "2022": {"wins": 9, "reg_season_losses": 4},
        "2023": {"wins": 7, "reg_season_losses": 6},
        "2024": {"wins": 9, "reg_season_losses": 3},
    },
    ("NCAAF", "Georgia Tech Yellow Jackets"): {
        "2021": {"wins": 3, "reg_season_losses": 9},
        "2022": {"wins": 5, "reg_season_losses": 7},
        "2023": {"wins": 7, "reg_season_losses": 6},
        "2024": {"wins": 9, "reg_season_losses": 3},
    },
    ("NCAAF", "NC State Wolfpack"): {
        "2021": {"wins": 9, "reg_season_losses": 3},
        "2022": {"wins": 8, "reg_season_losses": 4},
        "2023": {"wins": 9, "reg_season_losses": 4},
        "2024": {"wins": 6, "reg_season_losses": 6},
    },
    ("NCAAF", "Arizona State Sun Devils"): {
        "2021": {"wins": 8, "reg_season_losses": 4},
        "2022": {"wins": 3, "reg_season_losses": 9},
        "2023": {"wins": 3, "reg_season_losses": 9},
        "2024": {"wins": 11, "reg_season_losses": 2, "playoff_bid": True, "playoff_bye": True, "playoff_wins": 0},
    },
    ("NCAAF", "Cincinnati Bearcats"): {
        "2021": {"wins": 13, "reg_season_losses": 0, "playoff_bid": True, "playoff_wins": 0},
        "2022": {"wins": 9, "reg_season_losses": 3},
        "2023": {"wins": 3, "reg_season_losses": 9},
        "2024": {"wins": 5, "reg_season_losses": 7},
    },
}

# (league, team name) -> a short outlook for the team's next season, based
# on real preseason reporting (offseason moves, coaching changes, odds/
# projections) gathered in mid-to-late August 2026: EPL's 2026-27 season
# (already under way -- kicked off Aug 21, 2026), NFL's 2026 season
# (opens Sept 9), NBA's and NHL's 2026-27 seasons (open ~Oct 20 and Sept
# 29 respectively), and URC's 2026-27 season (opens Sept 19). This is
# necessarily a snapshot, not a permanent record -- preseason expectations
# age quickly once games are actually played, so revisit each entry once
# a season is well under way rather than trusting it indefinitely.
TEAM_PROGNOSES: dict[tuple[str, str], str] = {
    # --- EPL (2026-27) ---
    ("EPL", "Arsenal"): (
        "Defending their first title since 2003-04, Arsenal reportedly widened the gap on "
        "the rest of the division over the summer and are the consensus favorites to repeat."
    ),
    ("EPL", "Aston Villa"): (
        "Likely to come back down to earth after outperforming their underlying numbers in "
        "recent campaigns, with Champions League football adding a heavy workload."
    ),
    ("EPL", "Bournemouth"): (
        "Marco Rose's side are set for their first-ever European campaign, which "
        "historically drags down a club's league form the following season."
    ),
    ("EPL", "Brentford"): (
        "One of the league's best-run clubs, strengthened over the summer without losing "
        "any of their key men, and tipped to push for a European spot with no continental "
        "football of their own to juggle."
    ),
    ("EPL", "Brighton & Hove Albion"): (
        "A run in one of the European competitions could pull focus away from their league "
        "campaign this season."
    ),
    ("EPL", "Chelsea"): (
        "Xabi Alonso's arrival has sharply improved expectations, with Cole Palmer, Morgan "
        "Rogers, and Joao Pedro leading a talented attack, and no European football to "
        "distract from a title push."
    ),
    ("EPL", "Coventry City"): (
        "Back in the top flight under new boss Frank Lampard, considered the best-fancied "
        "of the three promoted sides but still tipped for a real relegation fight."
    ),
    ("EPL", "Crystal Palace"): (
        "Pierre Sage takes over during a transition period, with continental football "
        "adding to the strain on a squad also fighting to stay clear of trouble."
    ),
    ("EPL", "Everton"): (
        "David Moyes provides continuity, with the club expected to settle into a secure "
        "mid-table season."
    ),
    ("EPL", "Fulham"): (
        "A talented squad with a mid-table ceiling; question marks remain over Alvaro "
        "Arbeloa's managerial pedigree at this level."
    ),
    ("EPL", "Hull City"): (
        "Considered the biggest underdog of the three promoted teams, with the furthest "
        "gap to bridge to survive."
    ),
    ("EPL", "Ipswich Town"): (
        "Gary O'Neil's previous Premier League track record is a real concern for a side "
        "already fighting the drop."
    ),
    ("EPL", "Leeds United"): (
        "The signing of goalkeeper James Trafford underpins a solid platform following "
        "their promotion back to the top flight."
    ),
    ("EPL", "Liverpool"): (
        "Andoni Iraola inherits a squad still adjusting to life after Mohamed Salah's "
        "departure, with real questions over depth and how quickly his methods click."
    ),
    ("EPL", "Manchester City"): (
        "Enzo Maresca replaces Pep Guardiola, and after Rodri's move to Barcelona there "
        "are genuine doubts about whether City can go toe-to-toe with Arsenal over a full "
        "season."
    ),
    ("EPL", "Manchester United"): (
        "Michael Carrick's first full season in charge; still viewed as top-four "
        "contenders despite thin squad depth and a heavier fixture list from European "
        "football."
    ),
    ("EPL", "Newcastle United"): (
        "A transitional season follows Eddie Howe's departure, with Matthias Jaissle "
        "tasked with rebuilding after key sales."
    ),
    ("EPL", "Nottingham Forest"): (
        "Oliver Glasner inherits a deep, talented squad and is expected to push for "
        "another European finish."
    ),
    ("EPL", "Sunderland"): (
        "Back in the top flight after last year's play-off promotion, expected to come "
        "back to earth after overperforming, with a congested fixture list adding to the "
        "challenge."
    ),
    ("EPL", "Tottenham Hotspur"): (
        "Roberto De Zerbi's appointment signals a fresh direction and has some tipping "
        "Spurs as this season's dark horses, helped by no European football to distract "
        "from the league."
    ),
    # --- NFL (2026) ---
    ("NFL", "Buffalo Bills"): (
        "Widely seen as the AFC's best shot at the Super Bowl behind Josh Allen, projected "
        "among the league's handful of 10-11+ win teams."
    ),
    ("NFL", "Miami Dolphins"): (
        "Tied for the league's lowest projected win total, facing a difficult season."
    ),
    ("NFL", "New England Patriots"): (
        "Fresh off a Super Bowl LX appearance, but oddsmakers see real regression -- the "
        "first Super Bowl team in one major metric's history to open a season ranked "
        "outside the top 10; the A.J. Brown addition offers some hope."
    ),
    ("NFL", "New York Jets"): (
        "Widely tipped to finish with the league's worst record and a strong claim on the "
        "No. 1 overall pick."
    ),
    ("NFL", "Baltimore Ravens"): (
        "Tied for the league's highest projected win total, squarely in the Super Bowl "
        "conversation."
    ),
    ("NFL", "Cincinnati Bengals"): (
        "Projected as a playoff-caliber team, in the thick of the AFC wild-card race."
    ),
    ("NFL", "Cleveland Browns"): (
        "Near the bottom of most projections, another rebuilding season likely."
    ),
    ("NFL", "Pittsburgh Steelers"): (
        "Some models have them winning a competitive AFC North."
    ),
    ("NFL", "Houston Texans"): (
        "Favored by several models to repeat as AFC South champions."
    ),
    ("NFL", "Indianapolis Colts"): (
        "In the mix for a division title or wild-card spot in a wide-open AFC South."
    ),
    ("NFL", "Jacksonville Jaguars"): (
        "Squarely in the AFC wild-card conversation."
    ),
    ("NFL", "Tennessee Titans"): (
        "Projected near the bottom of a weak AFC South."
    ),
    ("NFL", "Denver Broncos"): (
        "Coming off a strong 2025, but models expect real regression, calling last year's "
        "close-game success rate unsustainable."
    ),
    ("NFL", "Kansas City Chiefs"): (
        "Carry their worst preseason ranking since 2018 after offensive struggles and "
        "defensive losses, but Patrick Mahomes and Andy Reid keep them squarely in the "
        "conversation."
    ),
    ("NFL", "Las Vegas Raiders"): (
        "Near the bottom of the league in projected wins."
    ),
    ("NFL", "Los Angeles Chargers"): (
        "In the thick of a contested AFC West race."
    ),
    ("NFL", "Dallas Cowboys"): (
        "Right on the playoff bubble in most projections."
    ),
    ("NFL", "New York Giants"): (
        "Projected for a middling season."
    ),
    ("NFL", "Philadelphia Eagles"): (
        "Among the very best teams in the league again, tied for the NFC's top projected "
        "record."
    ),
    ("NFL", "Washington Commanders"): (
        "In the playoff mix, but not viewed as a top-tier team."
    ),
    ("NFL", "Chicago Bears"): (
        "Coming off a surprise 2025 breakthrough, but models expect real regression -- "
        "under a 1-in-5 shot at repeating as division contenders."
    ),
    ("NFL", "Detroit Lions"): (
        "Narrow favorites in a stacked NFC North."
    ),
    ("NFL", "Green Bay Packers"): (
        "Right there with the Lions atop a deep NFC North."
    ),
    ("NFL", "Minnesota Vikings"): (
        "In the projected playoff picture as part of that same crowded division."
    ),
    ("NFL", "Atlanta Falcons"): (
        "Tipped by some models to win a wide-open NFC South."
    ),
    ("NFL", "Carolina Panthers"): (
        "Projected for a middling record in that same weak division."
    ),
    ("NFL", "New Orleans Saints"): (
        "Hovering around .500 in the NFC South scramble."
    ),
    ("NFL", "Tampa Bay Buccaneers"): (
        "Also squarely in that NFC South mix."
    ),
    ("NFL", "Arizona Cardinals"): (
        "Tied for the league's lowest projected win total, facing a tough year."
    ),
    ("NFL", "Los Angeles Rams"): (
        "The overall Super Bowl favorite, grading first in the league on both offense and "
        "defense behind Matthew Stafford, newly acquired Myles Garrett, and a contract-year "
        "Puka Nacua."
    ),
    ("NFL", "San Francisco 49ers"): (
        "Among the top projected teams in a loaded NFC West."
    ),
    ("NFL", "Seattle Seahawks"): (
        "Coming off their Super Bowl LX appearance, though models actually project some "
        "defensive regression."
    ),
    # --- NBA (2026-27) ---
    ("NBA", "Boston Celtics"): (
        "Traded Jaylen Brown and added Paul George and Duncan Robinson, prioritizing "
        "long-term cap flexibility over an immediate repeat push."
    ),
    ("NBA", "Brooklyn Nets"): (
        "Accelerated their rebuild by adding Julius Randle and a lottery pick, still "
        "assembling a young core."
    ),
    ("NBA", "New York Knicks"): (
        "Reigning conference finalists made only modest moves (swapping Mitchell "
        "Robinson for Andre Drummond) while staying under the second tax apron."
    ),
    ("NBA", "Philadelphia 76ers"): (
        "A blockbuster overhaul added Jaylen Brown and LeBron James alongside Joel Embiid "
        "and Tyrese Maxey, giving them one of the league's most talked-about new starting "
        "lineups and real title-favorite buzz."
    ),
    ("NBA", "Toronto Raptors"): (
        "Offseason left in a holding pattern pending the conclusion of a Kawhi "
        "Leonard-Clippers investigation."
    ),
    ("NBA", "Chicago Bulls"): (
        "Developing around a promising rookie class alongside Matas Buzelis as part of a "
        "young core still finding its direction."
    ),
    ("NBA", "Cleveland Cavaliers"): (
        "A quiet offseason built around re-signing James Harden, with an eye on a "
        "potential LeBron reunion down the line."
    ),
    ("NBA", "Detroit Pistons"): (
        "Made only modest additions after leading the East in wins a year ago."
    ),
    ("NBA", "Indiana Pacers"): (
        "Set to welcome back Tyrese Haliburton from injury alongside newly-acquired Ivica "
        "Zubac, forming what could be one of the league's best starting lineups."
    ),
    ("NBA", "Milwaukee Bucks"): (
        "A new era begins after trading Giannis Antetokounmpo, with a deep rotation but a "
        "full rebuild ahead and no first-round pick of their own next year."
    ),
    ("NBA", "Atlanta Hawks"): (
        "Added Luguentz Dort and Andrew Wiggins for elite perimeter defense to pair with "
        "Dyson Daniels."
    ),
    ("NBA", "Charlotte Hornets"): (
        "Lost LaMelo Ball and Miles Bridges but picked up extra draft capital, rebuilding "
        "around Brandon Miller and Kon Knueppel."
    ),
    ("NBA", "Miami Heat"): (
        "Landed Giannis Antetokounmpo in a blockbuster trade, though still need more "
        "shooting to space the floor around their stars."
    ),
    ("NBA", "Orlando Magic"): (
        "Hired Sean Sweeney as head coach and brought Nikola Vucevic back for depth and "
        "floor spacing around their young core."
    ),
    ("NBA", "Washington Wizards"): (
        "The No. 1 pick, AJ Dybantsa, plus veteran additions Deandre Ayton and Khris "
        "Middleton join an otherwise rebuilding young core."
    ),
    ("NBA", "Denver Nuggets"): (
        "Little roster turnover for a third straight year since their 2023 title, with the "
        "front office facing real pressure to reverse the team's gradual slide."
    ),
    ("NBA", "Minnesota Timberwolves"): (
        "Broke up their conference-finals roster in a boom-or-bust swap for LaMelo Ball, "
        "pairing him with Anthony Edwards in pursuit of a first-ever Finals trip."
    ),
    ("NBA", "Oklahoma City Thunder"): (
        "The defending champions and preseason favorites again, banking on Jalen Williams "
        "and Ajay Mitchell returning healthy while shedding some luxury-tax money via "
        "trades."
    ),
    ("NBA", "Portland Trail Blazers"): (
        "Acquired Ja Morant without giving up any draft picks, pairing him with Damian "
        "Lillard in a bold backcourt experiment."
    ),
    ("NBA", "Utah Jazz"): (
        "Lost defensive anchor Walker Kessler in a sign-and-trade, which lowers their "
        "ceiling even as other young pieces continue to develop."
    ),
    ("NBA", "Golden State Warriors"): (
        "Running back largely the same core that won 37 games last season, with a "
        "promising rookie addition unlikely to be enough for a real turnaround on its own."
    ),
    ("NBA", "Los Angeles Clippers"): (
        "A pending Kawhi Leonard trade investigation left the offseason in limbo, with a "
        "pivot toward a youth movement building around Brandon Ingram."
    ),
    ("NBA", "Los Angeles Lakers"): (
        "Lost LeBron James but pulled off an aggressive sign-and-trade for Walker Kessler, "
        "mortgaging future assets in the process."
    ),
    ("NBA", "Phoenix Suns"): (
        "Added Miles Bridges and shed money in trades, banking on a key piece returning "
        "healthy from a hamstring injury."
    ),
    ("NBA", "Sacramento Kings"): (
        "Fully committed to a youth movement after DeMar DeRozan and Russell Westbrook "
        "departed, leaning on a rookie-heavy roster."
    ),
    ("NBA", "Dallas Mavericks"): (
        "New president Masai Ujiri is taking a patient, long-term approach building "
        "around Cooper Flagg, adding more youth via this year's draft."
    ),
    ("NBA", "Houston Rockets"): (
        "Added Marcus Smart and Bojan Bogdanovic for depth after injuries undercut last "
        "season."
    ),
    ("NBA", "Memphis Grizzlies"): (
        "Completed their rebuild by trading Ja Morant, banking a massive haul of draft "
        "picks (13 first-rounders over the next seven drafts) around a young core led by "
        "Zach Edey."
    ),
    ("NBA", "New Orleans Pelicans"): (
        "A stagnant, widely-criticized offseason left an already-shaky roster largely "
        "unchanged."
    ),
    ("NBA", "San Antonio Spurs"): (
        "Running back their surprise Finals-run core with a healthy Victor Wembanyama, "
        "who signed a team-friendly extension; co-favorites with Oklahoma City for the "
        "title."
    ),
    # --- NHL (2026-27) ---
    ("NHL", "Boston Bruins"): (
        "Added JJ Peterka and more defensive depth in a solid, well-rounded offseason."
    ),
    ("NHL", "Buffalo Sabres"): (
        "Lost key players and are banking on internal development while still awaiting a "
        "decision on pending free agent goaltender Connor Hellebuyck."
    ),
    ("NHL", "Detroit Red Wings"): (
        "Enter the season without a general manager in place and real uncertainty hanging "
        "over captain Dylan Larkin's future with the club."
    ),
    ("NHL", "Florida Panthers"): (
        "Set to have Aleksander Barkov and the rest of last year's injury-hit roster back "
        "healthy, plus a blockbuster addition of Brady Tkachuk -- among the favorites for "
        "a three-peat."
    ),
    ("NHL", "Montreal Canadiens"): (
        "A quiet, low-key offseason after locking up Ivan Demidov to a long-term "
        "extension."
    ),
    ("NHL", "Ottawa Senators"): (
        "A difficult summer after captain Brady Tkachuk requested a trade out of town; "
        "the return of Claude Giroux hasn't been enough to offset the loss."
    ),
    ("NHL", "Tampa Bay Lightning"): (
        "Added veteran John Carlson to a core that's still considered a real Stanley Cup "
        "threat."
    ),
    ("NHL", "Toronto Maple Leafs"): (
        "Won this year's draft lottery, hired a new GM, and made a series of calculated "
        "moves (including landing Sergei Bobrovsky) widely seen as one of the league's "
        "most improved offseasons."
    ),
    ("NHL", "Carolina Hurricanes"): (
        "Bring back almost the exact roster that made them Stanley Cup favorites, with "
        "only minor tweaks."
    ),
    ("NHL", "Columbus Blue Jackets"): (
        "Facing morale concerns after star players signaled they won't re-sign long-term."
    ),
    ("NHL", "New Jersey Devils"): (
        "A busy summer highlighted by locking up Nico Hischier to a long-term extension."
    ),
    ("NHL", "New York Islanders"): (
        "A confusing offseason with minimal additions after losing Anders Lee, leaving "
        "their scoring questions unaddressed."
    ),
    ("NHL", "New York Rangers"): (
        "Finally trending in the right direction after adding Pavel Dorofeyev and "
        "shoring up the blue line."
    ),
    ("NHL", "Philadelphia Flyers"): (
        "A failed offer sheet for Leo Carlsson was the highlight of an otherwise low-key "
        "summer."
    ),
    ("NHL", "Pittsburgh Penguins"): (
        "Struck a deliberate balance between the present and the future rather than "
        "making any drastic moves."
    ),
    ("NHL", "Washington Capitals"): (
        "The league's most aggressive offseason, adding Alex Tuch, Jordan Kyrou, and "
        "Boone Jenner around a returning Alex Ovechkin for one more Cup run -- considered "
        "the Metropolitan's clear second-best team behind Carolina."
    ),
    ("NHL", "Chicago Blackhawks"): (
        "Locked up Connor Bedard to a five-year extension and brought Patrick Kane back "
        "on a two-year deal, leaning into a nostalgic, feel-good offseason as the young "
        "core matures."
    ),
    ("NHL", "Colorado Avalanche"): (
        "A quiet summer focused on getting a Cale Makar extension done rather than adding "
        "pieces, among the Cup favorites regardless."
    ),
    ("NHL", "Dallas Stars"): (
        "Breathed a sigh of relief after signing Jason Robertson to a one-year extension, "
        "averting a potential crisis."
    ),
    ("NHL", "Minnesota Wild"): (
        "Lost scoring depth and still haven't found the elite center they need, leaving "
        "the roster feeling incomplete."
    ),
    ("NHL", "Nashville Predators"): (
        "A new GM has made some encouraging moves, headlined by trading for Mavrik "
        "Bourque, in hopes of escaping the Central Division's murky middle."
    ),
    ("NHL", "St. Louis Blues"): (
        "Shifted focus to the future by trading Jordan Kyrou, a clear step into a "
        "rebuild."
    ),
    ("NHL", "Utah Mammoth"): (
        "Won the Vincent Trocheck sweepstakes and added goaltender Sebastian Cossa, "
        "continuing a steady climb after jumping from 77 to 92 points across the last two "
        "seasons."
    ),
    ("NHL", "Winnipeg Jets"): (
        "An offseason that's \"impossible to evaluate\" while a decision on pending free "
        "agent Connor Hellebuyck hangs over everything."
    ),
    ("NHL", "Anaheim Ducks"): (
        "Paid a steep price to keep Leo Carlsson, leaving them cap-strapped with "
        "restricted free agents still unsigned."
    ),
    ("NHL", "Calgary Flames"): (
        "Signaled a full rebuild by trading away Rasmus Andersson and Nazem Kadri, "
        "banking nearly $19 million in cap space and eight picks in the first three "
        "rounds of the next few drafts."
    ),
    ("NHL", "Edmonton Oilers"): (
        "Shed cap constraints and added goaltender Frederik Andersen, positioning the "
        "roster to win now."
    ),
    ("NHL", "Los Angeles Kings"): (
        "Signed a run of aging veterans (Corey Perry, Erik Haula, Mats Zuccarello), seen "
        "by some as the wrong direction for a team that needs to get younger."
    ),
    ("NHL", "San Jose Sharks"): (
        "Locked up Macklin Celebrini to a record-setting extension worth $18.8 million a "
        "year, the centerpiece of a rebuild that still has real cap space to work with."
    ),
    ("NHL", "Seattle Kraken"): (
        "A disappointing summer after a Jason Robertson sign-and-trade offer was "
        "rejected, leaving them still searching for a true star."
    ),
    ("NHL", "Vancouver Canucks"): (
        "A stable, low-key offseason (bringing hometown favorite Brendan Gallagher back) "
        "as the rebuild continues under new coach Manny Malhotra."
    ),
    ("NHL", "Vegas Golden Knights"): (
        "Lost Pavel Dorofeyev and overpaid to keep Rasmus Andersson, leaving the roster "
        "with less financial flexibility than in past years."
    ),
    # --- URC (2026-27) ---
    ("URC", "Leinster"): (
        "Preseason favorites to retain the title and reach double figures in "
        "championships; lost all-time leading try-scorer James Lowe but replaced him by "
        "bringing back fly-half Joey Carbery from Bordeaux."
    ),
    ("URC", "Munster"): (
        "Prioritized forward reinforcements (Jack Aungier, Kieran Brookes, Marnus van der "
        "Merwe) to offset the departures of Jean Kleyn and others."
    ),
    ("URC", "Connacht"): (
        "Strengthened significantly by raiding provincial rivals Leinster for Jerry "
        "Cahir, Will Connors, and fly-half Ciaran Frawley."
    ),
    ("URC", "Ulster"): (
        "Added depth across the squad (Jamie Benson, Matt Devine, Ben Donnell, Eli "
        "Snyman) aiming to get back into playoff contention."
    ),
    ("URC", "Cardiff"): (
        "Brought in experienced prop Scott Sio during a critical season for the club "
        "amid wider turmoil in Welsh rugby."
    ),
    ("URC", "Ospreys"): (
        "Lost Wales captains Dewi Lake and Jac Morgan to Gloucester, but strengthened "
        "their back three with Tom Rogers after finishing 11th a year ago."
    ),
    ("URC", "Scarlets"): (
        "Lost Jac Morgan but brought in fly-half Gareth Anscombe and lock Cullen Grace to "
        "freshen up the squad."
    ),
    ("URC", "Dragons"): (
        "Building on a promising campaign with new arrivals including wing Anzelo "
        "Tuitavuki and back-rower Terrell Peita."
    ),
    ("URC", "Bulls"): (
        "Runners-up in three of the last four finals and the bookmakers' next-best bet "
        "behind Leinster, despite losing try-scoring winger Kurt-Lee Arendse to Japan."
    ),
    ("URC", "Lions"): (
        "Enter the season as reigning South African Shield champions for the first time, "
        "having strengthened further with several new signings."
    ),
    ("URC", "Sharks"): (
        "Lost two-time World Cup captain Siya Kolisi to the Stormers, but replaced him up "
        "front with English tighthead Thomas du Toit."
    ),
    ("URC", "Stormers"): (
        "Landed two Springbok World Cup winners in Siya Kolisi and Cheslin Kolbe, "
        "instantly becoming one of the sides tipped to challenge Leinster for the title."
    ),
    ("URC", "Glasgow Warriors"): (
        "Lost strike winger Huw Jones to France but added Scotland international Jamie "
        "Ritchie for leadership and versatility."
    ),
    ("URC", "Edinburgh"): (
        "Added promising scrum-half Louie Chapman from the Crusaders' famed development "
        "system."
    ),
    ("URC", "Benetton"): (
        "Lost established internationals Thomas Gallo and Eli Snyman but added overseas "
        "talent from Australia, South Africa, and Argentina to remain Italy's flagship "
        "side."
    ),
    ("URC", "Zebre Parma"): (
        "Continuing to build one of the league's youngest squads, doubling down on "
        "developing Italian-qualified talent as the 2027 World Cup approaches."
    ),

    # --- NCAAF (2026 season) ---
    ("NCAAF", "Ohio State Buckeyes"): (
        "Preseason No. 1 in both the AP poll and SP+, defending national champions with "
        "Julian Sayin at quarterback -- the clear favorite to repeat."
    ),
    ("NCAAF", "Georgia Bulldogs"): (
        "Preseason No. 3 (AP) / No. 4 (SP+); Kirby Smart's roster reloads as usual and the "
        "Bulldogs are viewed as Ohio State's top challenger."
    ),
    ("NCAAF", "Texas Longhorns"): (
        "Preseason No. 5 (AP) / No. 6 (SP+) behind Arch Manning's third year as starter; "
        "considered a clear playoff contender in Steve Sarkisian's fifth season."
    ),
    ("NCAAF", "Indiana Hoosiers"): (
        "Preseason No. 6, the highest ranking in program history, as Curt Cignetti looks "
        "to prove 2024's breakout was no fluke."
    ),
    ("NCAAF", "Oregon Ducks"): (
        "Preseason No. 2 in the AP poll, with Dante Moore succeeding Dillon Gabriel at "
        "quarterback -- considered Ohio State's stiffest national competition."
    ),
    ("NCAAF", "Notre Dame Fighting Irish"): (
        "Preseason No. 4, with C.J. Carr back after last year's championship-game run; "
        "expected to contend for a return trip to the playoff."
    ),
    ("NCAAF", "Alabama Crimson Tide"): (
        "Preseason No. 13 (AP), with SP+ notably higher at No. 6; Kalen DeBoer's biggest "
        "fall-camp storyline was an open quarterback battle between Austin Mack and "
        "five-star Keelon Russell."
    ),
    ("NCAAF", "LSU Tigers"): (
        "Preseason No. 11, entering the Lane Kiffin era on a record $91 million contract "
        "after Brian Kelly's October 2025 firing -- considerable buzz but a true unknown "
        "until Kiffin's first games."
    ),
    ("NCAAF", "Texas A&M Aggies"): (
        "Preseason No. 8, coming off Mike Elko's strong 2024-25 debut seasons; expected to "
        "contend in a stacked SEC."
    ),
    ("NCAAF", "Miami (FL) Hurricanes"): (
        "Preseason No. 7, and per SP+ the favorite to win an ACC where the runner-up race "
        "is a jumbled six-team cluster."
    ),
    ("NCAAF", "Texas Tech Red Raiders"): (
        "Preseason No. 12, considered the Big 12's most established team by SP+ despite "
        "lingering questions at quarterback."
    ),
    ("NCAAF", "Oklahoma Sooners"): (
        "Preseason No. 10, with Brent Venables looking to build on a bounce-back 2025 "
        "after two rocky opening SEC seasons."
    ),
    ("NCAAF", "USC Trojans"): (
        "Preseason No. 15, with Lincoln Riley aiming to stabilize a program that has swung "
        "between 11-win and losing seasons since the Big Ten move."
    ),
    ("NCAAF", "Ole Miss Rebels"): (
        "Preseason No. 9, now under first-time head coach Pete Golding after Lane Kiffin's "
        "abrupt in-season departure for LSU during the 2025 CFP run."
    ),
    ("NCAAF", "Tennessee Volunteers"): (
        "Preseason No. 20, replacing its starting quarterback for a fifth consecutive "
        "season after Joey Aguilar's eligibility expired."
    ),
    ("NCAAF", "Michigan Wolverines"): (
        "Preseason No. 16, opening the Kyle Whittingham era on September 5 after Sherrone "
        "Moore's stunning December 2025 firing and arrest."
    ),
    ("NCAAF", "Auburn Tigers"): (
        "Outside the AP top 25 but received votes; new coach Alex Golesh arrives from "
        "South Florida after Hugh Freeze's November 2025 firing."
    ),
    ("NCAAF", "Florida Gators"): (
        "Outside the AP top 25 but received votes; new coach Jon Sumrall arrives from "
        "Tulane with an open quarterback competition after Billy Napier's October 2025 "
        "firing."
    ),
    ("NCAAF", "Missouri Tigers"): (
        "Preseason No. 25, with Eli Drinkwitz looking to sustain the program's best "
        "two-year stretch in over a decade."
    ),
    ("NCAAF", "Penn State Nittany Lions"): (
        "Preseason No. 18, with new coach Matt Campbell arriving from Iowa State after "
        "James Franklin's shocking mid-2025 firing following a 3-3 start."
    ),
    ("NCAAF", "Clemson Tigers"): (
        "Outside the AP top 25 but received the most votes of any unranked team; Dabo "
        "Swinney needs a bounce-back after a 7-6 2025 finish and Cade Klubnik's departure "
        "leaves a quarterback vacancy."
    ),
    ("NCAAF", "BYU Cougars"): (
        "Preseason No. 14, with SP+ notably cooler (No. 21); Kalani Sitake's program looks "
        "to build on 2024's surprise 11-2 season."
    ),
    ("NCAAF", "South Carolina Gamecocks"): (
        "Outside the AP top 25 but SP+ has them at No. 24, with Shane Beamer's program "
        "trending upward after back-to-back nine-plus-win seasons."
    ),
    ("NCAAF", "Iowa Hawkeyes"): (
        "Preseason No. 22, with Kirk Ferentz's typically stout defense again expected to "
        "carry an offense that's lagged in recent years."
    ),
    ("NCAAF", "Washington Huskies"): (
        "Preseason No. 17, with Jedd Fisch aiming to build on a difficult first Big Ten "
        "season as the Huskies try to recapture their 2023 CFP-run form."
    ),
    ("NCAAF", "SMU Mustangs"): (
        "Preseason No. 19, with Rhett Lashlee's Mustangs looking to get back to the ACC "
        "title game after a first-round CFP exit in 2024."
    ),
    ("NCAAF", "Vanderbilt Commodores"): (
        "Outside the AP top 25 but SP+ has them at No. 29, with Clark Lea's program riding "
        "real momentum after 2024's breakthrough and an upset of Alabama."
    ),
    ("NCAAF", "Nebraska Cornhuskers"): (
        "Outside the AP top 25 but SP+ has them at No. 33, with Matt Rhule's program "
        "looking for a second straight bowl season after ending a seven-year drought in "
        "2024."
    ),
    ("NCAAF", "Florida State Seminoles"): (
        "Outside the AP top 25 but SP+ has them at No. 35, looking to rebound after an "
        "infamous 2023 CFP snub was followed by the program's worst season in half a "
        "century in 2024."
    ),
    ("NCAAF", "Louisville Cardinals"): (
        "Preseason No. 24, with Jeff Brohm's program looking to build on back-to-back "
        "10-win-caliber seasons and an ACC title game appearance."
    ),
    ("NCAAF", "Utah Utes"): (
        "Preseason No. 21, opening the Morgan Scalley era after Kyle Whittingham's "
        "21-season tenure ended with his move to Michigan."
    ),
    ("NCAAF", "Pittsburgh Panthers"): (
        "Outside the AP top 25 but SP+ has them at No. 41, with the program still "
        "searching for the consistency of Kenny Pickett's 2021 ACC title season."
    ),
    ("NCAAF", "Virginia Cavaliers"): (
        "Outside the AP top 25 but SP+ has them at No. 37, with Tony Elliott's program "
        "looking to build on 2024's breakthrough as it continues rebuilding in the wake of "
        "the 2022 team shooting tragedy."
    ),
    ("NCAAF", "Virginia Tech Hokies"): (
        "Outside the AP top 25 but SP+ has them at No. 36 and projects an 18.7-point "
        "rebound behind new coach James Franklin, who arrives after his own Penn State "
        "dismissal to replace the in-season-fired Brent Pry."
    ),
    ("NCAAF", "Arizona Wildcats"): (
        "Received AP preseason votes just outside the top 25, with Brent Brennan looking "
        "to recapture the form of 2023's 10-win Alamo Bowl season."
    ),
    ("NCAAF", "Baylor Bears"): (
        "Outside the AP top 25 but SP+ has them at No. 54, with Dave Aranda under pressure "
        "to return to 2021 Big 12 title-game form."
    ),
    ("NCAAF", "Houston Cougars"): (
        "Preseason No. 23, though SP+ is notably cooler at No. 38; Dana Holgorsen looks to "
        "end back-to-back 4-8 finishes since the Big 12 move."
    ),
    ("NCAAF", "Kentucky Wildcats"): (
        "Outside the AP top 25 but SP+ has them at No. 47, with Mark Stoops under pressure "
        "after the program's early-2020s momentum faded."
    ),
    ("NCAAF", "Illinois Fighting Illini"): (
        "Outside the AP top 25 but SP+ has them at No. 28, with Bret Bielema looking to "
        "build on 2024's 10-win breakthrough, the program's best season in over a decade."
    ),
    ("NCAAF", "North Carolina Tar Heels"): (
        "Outside the AP top 25 but SP+ has them at No. 56, with Bill Belichick's second "
        "season aiming to improve on a rough 4-8 debut in his jump from the NFL."
    ),
    ("NCAAF", "Kansas State Wildcats"): (
        "Outside the AP top 25 but SP+ has them at No. 34, with Chris Klieman's program "
        "looking to return to its 2022 Big 12 title-game form."
    ),
    ("NCAAF", "TCU Horned Frogs"): (
        "Received AP preseason votes just outside the top 25, with Sonny Dykes looking to "
        "rebuild toward the level of the 2022 CFP-runner-up team."
    ),
    ("NCAAF", "Arkansas Razorbacks"): (
        "Outside the AP top 25 but SP+ has them at No. 44, opening the Ryan Silverfield "
        "era after Sam Pittman's firing just five games into 2025."
    ),
    ("NCAAF", "Mississippi State Bulldogs"): (
        "Outside the AP top 25 but SP+ has them at No. 52, with Jeff Lebby's rebuild still "
        "finding its footing three seasons after Mike Leach's death."
    ),
    ("NCAAF", "Wisconsin Badgers"): (
        "Outside the AP top 25 but SP+ has them at No. 53, with Luke Fickell looking to "
        "reverse a jarring decline since the program's 22-year bowl streak ended."
    ),
    ("NCAAF", "Duke Blue Devils"): (
        "Outside the AP top 25 but SP+ has them at No. 45, with Manny Diaz aiming to "
        "sustain the momentum Mike Elko built before his 2024 departure for Texas A&M."
    ),
    ("NCAAF", "Georgia Tech Yellow Jackets"): (
        "Outside the AP top 25 but SP+ has them at No. 42, with Brent Key's program "
        "looking to build on consecutive winning seasons for the first time in years."
    ),
    ("NCAAF", "NC State Wolfpack"): (
        "Outside the AP top 25 but SP+ has them at No. 43, with Dave Doeren's steady, "
        "defense-first program again projected for a mid-tier ACC finish."
    ),
    ("NCAAF", "Arizona State Sun Devils"): (
        "Outside the AP top 25 but SP+ has them at No. 51, looking to prove 2024's Big 12 "
        "title and CFP quarterfinal run under Kenny Dillingham was sustainable rather than "
        "a one-off."
    ),
    ("NCAAF", "Cincinnati Bearcats"): (
        "Outside the AP top 25 but SP+ has them at No. 59, with the program still "
        "searching for the form of its 2021 CFP season under Scott Satterfield."
    ),
}
