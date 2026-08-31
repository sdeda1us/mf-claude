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

    # --- NCAAMB --- top 50 by expected fantasy points (same rationale as
    # NCAAF above). Arena is the primary home venue; most schools' men's and
    # women's teams share the same arena, so the same coordinates are reused
    # under NCAAWB below wherever that's the case.
    ("NCAAMB", "Duke Blue Devils"): (36.0011, -78.9419),  # Cameron Indoor Stadium, Durham
    ("NCAAMB", "Louisville Cardinals"): (38.2496, -85.7599),  # KFC Yum! Center, Louisville
    ("NCAAMB", "Virginia Cavaliers"): (38.0447, -78.5133),  # John Paul Jones Arena, Charlottesville
    ("NCAAMB", "Illinois Fighting Illini"): (40.0993, -88.2360),  # State Farm Center, Champaign
    ("NCAAMB", "Michigan State Spartans"): (42.7285, -84.4839),  # Breslin Center, East Lansing
    ("NCAAMB", "Arizona Wildcats"): (32.2288, -110.9491),  # McKale Center, Tucson
    ("NCAAMB", "Houston Cougars"): (29.7216, -95.3416),  # Fertitta Center, Houston
    ("NCAAMB", "Gonzaga Bulldogs"): (47.6677, -117.4023),  # McCarthey Athletic Center, Spokane
    ("NCAAMB", "Florida Gators"): (29.6494, -82.3487),  # Exactech Arena, Gainesville
    ("NCAAMB", "UConn Huskies"): (41.8083, -72.2540),  # Gampel Pavilion, Storrs
    ("NCAAMB", "Michigan Wolverines"): (42.2778, -83.7382),  # Crisler Center, Ann Arbor
    ("NCAAMB", "Nebraska Cornhuskers"): (40.8206, -96.7078),  # Pinnacle Bank Arena, Lincoln
    ("NCAAMB", "Kansas Jayhawks"): (38.9543, -95.2529),  # Allen Fieldhouse, Lawrence
    ("NCAAMB", "Texas Tech Red Raiders"): (33.5904, -101.8709),  # United Supermarkets Arena, Lubbock
    ("NCAAMB", "Tennessee Volunteers"): (35.9552, -83.9257),  # Thompson-Boling Arena, Knoxville
    ("NCAAMB", "Texas Longhorns"): (30.2825, -97.7327),  # Moody Center, Austin
    ("NCAAMB", "Miami (FL) Hurricanes"): (25.7171, -80.2783),  # Watsco Center, Coral Gables
    ("NCAAMB", "St. John's Red Storm"): (40.7228, -73.7949),  # Carnesecca Arena, Queens
    ("NCAAMB", "Ohio State Buckeyes"): (40.0067, -83.0198),  # Value City Arena, Columbus
    ("NCAAMB", "UCLA Bruins"): (34.0709, -118.4473),  # Pauley Pavilion, Los Angeles
    ("NCAAMB", "Iowa State Cyclones"): (42.0261, -93.6350),  # Hilton Coliseum, Ames
    ("NCAAMB", "Alabama Crimson Tide"): (33.2094, -87.5503),  # Coleman Coliseum, Tuscaloosa
    ("NCAAMB", "Arkansas Razorbacks"): (36.0678, -94.1786),  # Bud Walton Arena, Fayetteville
    ("NCAAMB", "Kentucky Wildcats"): (38.0473, -84.4988),  # Rupp Arena, Lexington
    ("NCAAMB", "Vanderbilt Commodores"): (36.1436, -86.8027),  # Memorial Gymnasium, Nashville
    ("NCAAMB", "Marquette Golden Eagles"): (43.0451, -87.9172),  # Fiserv Forum, Milwaukee
    ("NCAAMB", "Villanova Wildcats"): (40.0337, -75.3412),  # Finneran Pavilion, Villanova
    ("NCAAMB", "Indiana Hoosiers"): (39.1794, -86.5264),  # Simon Skjodt Assembly Hall, Bloomington
    ("NCAAMB", "Oregon Ducks"): (44.0453, -123.0770),  # Matthew Knight Arena, Eugene
    ("NCAAMB", "Purdue Boilermakers"): (40.4249, -86.9187),  # Mackey Arena, West Lafayette
    ("NCAAMB", "USC Trojans"): (34.0175, -118.2853),  # Galen Center, Los Angeles
    ("NCAAMB", "Georgia Bulldogs"): (33.9498, -83.3733),  # Stegeman Coliseum, Athens
    ("NCAAMB", "Clemson Tigers"): (34.6786, -82.8434),  # Littlejohn Coliseum, Clemson
    ("NCAAMB", "NC State Wolfpack"): (35.8033, -78.7219),  # PNC Arena, Raleigh
    ("NCAAMB", "Virginia Tech Hokies"): (37.2249, -80.4183),  # Cassell Coliseum, Blacksburg
    ("NCAAMB", "Creighton Bluejays"): (41.2637, -95.9350),  # CHI Health Center, Omaha
    ("NCAAMB", "Maryland Terrapins"): (38.9897, -76.9436),  # Xfinity Center, College Park
    ("NCAAMB", "BYU Cougars"): (40.2596, -111.6489),  # Marriott Center, Provo
    ("NCAAMB", "Cincinnati Bearcats"): (39.1310, -84.5157),  # Fifth Third Arena, Cincinnati
    ("NCAAMB", "Auburn Tigers"): (32.6023, -85.4900),  # Neville Arena, Auburn
    ("NCAAMB", "Missouri Tigers"): (38.9345, -92.3327),  # Mizzou Arena, Columbia
    ("NCAAMB", "Oklahoma Sooners"): (35.1917, -97.4453),  # Lloyd Noble Center, Norman
    ("NCAAMB", "North Carolina Tar Heels"): (35.9042, -79.0472),  # Dean Smith Center, Chapel Hill
    ("NCAAMB", "SMU Mustangs"): (32.8388, -96.7810),  # Moody Coliseum, Dallas
    ("NCAAMB", "Iowa Hawkeyes"): (41.6586, -91.5511),  # Carver-Hawkeye Arena, Iowa City
    ("NCAAMB", "Wisconsin Badgers"): (43.0778, -89.4106),  # Kohl Center, Madison
    ("NCAAMB", "Baylor Bears"): (31.5586, -97.1156),  # Foster Pavilion, Waco
    ("NCAAMB", "TCU Horned Frogs"): (32.7095, -97.3688),  # Schollmaier Arena, Fort Worth
    ("NCAAMB", "UCF Knights"): (28.6024, -81.1997),  # Addition Financial Arena, Orlando
    ("NCAAMB", "LSU Tigers"): (30.4122, -91.1849),  # Pete Maravich Assembly Center, Baton Rouge

    # --- NCAAWB --- top 50 by expected fantasy points (own list -- women's
    # representation differs from men's, see set_ev_defaults.FALL_EV_RAW_SCORES).
    # Reuses NCAAMB's coordinates above wherever the same school's men's and
    # women's teams share an arena.
    ("NCAAWB", "UCLA Bruins"): (34.0709, -118.4473),
    ("NCAAWB", "UConn Huskies"): (41.8083, -72.2540),
    ("NCAAWB", "South Carolina Gamecocks"): (34.0007, -81.0348),  # Colonial Life Arena, Columbia
    ("NCAAWB", "LSU Tigers"): (30.4122, -91.1849),
    ("NCAAWB", "Texas Longhorns"): (30.2825, -97.7327),
    ("NCAAWB", "Duke Blue Devils"): (36.0011, -78.9419),
    ("NCAAWB", "Michigan Wolverines"): (42.2778, -83.7382),
    ("NCAAWB", "TCU Horned Frogs"): (32.7095, -97.3688),
    ("NCAAWB", "Oklahoma Sooners"): (35.1917, -97.4453),
    ("NCAAWB", "Vanderbilt Commodores"): (36.1436, -86.8027),
    ("NCAAWB", "Louisville Cardinals"): (38.2496, -85.7599),
    ("NCAAWB", "North Carolina Tar Heels"): (35.9042, -79.0472),
    ("NCAAWB", "Notre Dame Fighting Irish"): (41.6983, -86.2331),  # Purcell Pavilion, South Bend
    ("NCAAWB", "Iowa Hawkeyes"): (41.6586, -91.5511),
    ("NCAAWB", "West Virginia Mountaineers"): (39.6398, -79.9553),  # WVU Coliseum, Morgantown
    ("NCAAWB", "Kentucky Wildcats"): (38.0473, -84.4988),
    ("NCAAWB", "Maryland Terrapins"): (38.9897, -76.9436),
    ("NCAAWB", "Michigan State Spartans"): (42.7285, -84.4839),
    ("NCAAWB", "Minnesota Golden Gophers"): (44.9797, -93.2277),  # Williams Arena, Minneapolis
    ("NCAAWB", "Ohio State Buckeyes"): (40.0067, -83.0198),
    ("NCAAWB", "Mississippi State Bulldogs"): (33.4552, -88.7934),  # Humphrey Coliseum, Starkville
    ("NCAAWB", "Virginia Cavaliers"): (38.0447, -78.5133),
    ("NCAAWB", "Washington Huskies"): (47.6553, -122.3021),  # Hec Edmundson Pavilion, Seattle
    ("NCAAWB", "Columbia Lions"): (40.8155, -73.9530),  # Francis Levien Gymnasium, New York
    ("NCAAWB", "Alabama Crimson Tide"): (33.2094, -87.5503),
    ("NCAAWB", "NC State Wolfpack"): (35.8033, -78.7219),
    ("NCAAWB", "Virginia Tech Hokies"): (37.2249, -80.4183),
    ("NCAAWB", "Villanova Wildcats"): (40.0337, -75.3412),
    ("NCAAWB", "Illinois Fighting Illini"): (40.0993, -88.2360),
    ("NCAAWB", "Nebraska Cornhuskers"): (40.8206, -96.7078),
    ("NCAAWB", "Oregon Ducks"): (44.0453, -123.0770),
    ("NCAAWB", "USC Trojans"): (34.0175, -118.2853),
    ("NCAAWB", "Houston Cougars"): (29.7216, -95.3416),
    ("NCAAWB", "Fairfield Stags"): (41.1408, -73.2604),  # Leo D. Mahoney Arena, Fairfield
    ("NCAAWB", "Gonzaga Bulldogs"): (47.6677, -117.4023),
    ("NCAAWB", "Miami (FL) Hurricanes"): (25.7171, -80.2783),
    ("NCAAWB", "St. John's Red Storm"): (40.7228, -73.7949),
    ("NCAAWB", "Kansas Jayhawks"): (38.9543, -95.2529),
    ("NCAAWB", "Texas Tech Red Raiders"): (33.5904, -101.8709),
    ("NCAAWB", "Ohio Bobcats"): (39.3292, -82.1013),  # The Convocation Center, Athens (OH)
    ("NCAAWB", "Marquette Golden Eagles"): (43.0451, -87.9172),
    ("NCAAWB", "Indiana Hoosiers"): (39.1794, -86.5264),
    ("NCAAWB", "Purdue Boilermakers"): (40.4249, -86.9187),
    ("NCAAWB", "Iowa State Cyclones"): (42.0261, -93.6350),
    ("NCAAWB", "Arkansas Razorbacks"): (36.0678, -94.1786),
    ("NCAAWB", "Clemson Tigers"): (34.6786, -82.8434),
    ("NCAAWB", "Creighton Bluejays"): (41.2637, -95.9350),
    ("NCAAWB", "BYU Cougars"): (40.2596, -111.6489),
    ("NCAAWB", "Auburn Tigers"): (32.6023, -85.4900),
    ("NCAAWB", "SMU Mustangs"): (32.8388, -96.7810),

    # --- NCAAF, second 50 (ranks 51-100 by expected fantasy points) ---
    ("NCAAF", "Colorado Buffaloes"): (40.0075, -105.2669),  # Folsom Field, Boulder
    ("NCAAF", "Boise State Broncos"): (43.6028, -116.1968),  # Albertsons Stadium (blue turf), Boise
    ("NCAAF", "Wake Forest Demon Deacons"): (36.1330, -80.2529),  # Allegacy Stadium, Winston-Salem
    ("NCAAF", "Kansas Jayhawks"): (38.9631, -95.2472),  # David Booth Kansas Memorial Stadium, Lawrence
    ("NCAAF", "Oklahoma State Cowboys"): (36.1269, -97.0666),  # Boone Pickens Stadium, Stillwater
    ("NCAAF", "UCF Knights"): (28.6078, -81.1930),  # FBC Mortgage Stadium, Orlando
    ("NCAAF", "Tulane Green Wave"): (29.9400, -90.1180),  # Yulman Stadium, New Orleans
    ("NCAAF", "Maryland Terrapins"): (38.9906, -76.9469),  # SECU Stadium, College Park
    ("NCAAF", "Northwestern Wildcats"): (42.0645, -87.6930),  # Ryan Field, Evanston
    ("NCAAF", "California Golden Bears"): (37.8715, -122.2508),  # California Memorial Stadium, Berkeley
    ("NCAAF", "San Diego State Aztecs"): (32.7831, -117.1195),  # Snapdragon Stadium, San Diego
    ("NCAAF", "UNLV Rebels"): (36.0909, -115.1833),  # Allegiant Stadium, Las Vegas
    ("NCAAF", "Michigan State Spartans"): (42.7284, -84.4839),  # Spartan Stadium, East Lansing
    ("NCAAF", "Minnesota Golden Gophers"): (44.9764, -93.2244),  # Huntington Bank Stadium, Minneapolis
    ("NCAAF", "Rutgers Scarlet Knights"): (40.5136, -74.4636),  # SHI Stadium, Piscataway
    ("NCAAF", "UCLA Bruins"): (34.1613, -118.1676),  # Rose Bowl, Pasadena
    ("NCAAF", "West Virginia Mountaineers"): (39.6486, -79.9540),  # Milan Puskar Stadium, Morgantown
    ("NCAAF", "East Carolina Pirates"): (35.6069, -77.3672),  # Dowdy-Ficklen Stadium, Greenville
    ("NCAAF", "Navy Midshipmen"): (38.9869, -76.4922),  # Navy-Marine Corps Memorial Stadium, Annapolis
    ("NCAAF", "Purdue Boilermakers"): (40.4331, -86.9184),  # Ross-Ade Stadium, West Lafayette
    ("NCAAF", "Syracuse Orange"): (43.0362, -76.1364),  # JMA Wireless Dome, Syracuse
    ("NCAAF", "Iowa State Cyclones"): (42.0140, -93.6359),  # Jack Trice Stadium, Ames
    ("NCAAF", "Memphis Tigers"): (35.1204, -89.9767),  # Simmons Bank Liberty Stadium, Memphis
    ("NCAAF", "South Florida Bulls"): (27.9759, -82.5033),  # Raymond James Stadium, Tampa
    ("NCAAF", "James Madison Dukes"): (38.4374, -78.8631),  # Bridgeforth Stadium, Harrisonburg
    ("NCAAF", "Boston College Eagles"): (42.3355, -71.1685),  # Alumni Stadium, Chestnut Hill
    ("NCAAF", "Stanford Cardinal"): (37.4347, -122.1615),  # Stanford Stadium, Stanford
    ("NCAAF", "Fresno State Bulldogs"): (36.8125, -119.7465),  # Valley Children's Stadium, Fresno
    ("NCAAF", "Hawaii Rainbow Warriors"): (21.2969, -157.8226),  # Ching Athletics Complex, Honolulu
    ("NCAAF", "New Mexico Lobos"): (35.0672, -106.6218),  # University Stadium, Albuquerque
    ("NCAAF", "Toledo Rockets"): (41.6600, -83.6105),  # Glass Bowl, Toledo
    ("NCAAF", "Texas State Bobcats"): (29.8858, -97.9414),  # UFCU Stadium, San Marcos
    ("NCAAF", "Washington State Cougars"): (46.7305, -117.1602),  # Gesa Field at Martin Stadium, Pullman
    ("NCAAF", "Old Dominion Monarchs"): (36.8879, -76.3050),  # S.B. Ballard Stadium, Norfolk
    ("NCAAF", "Western Michigan Broncos"): (42.2867, -85.6136),  # Waldo Stadium, Kalamazoo
    ("NCAAF", "Western Kentucky Hilltoppers"): (36.9836, -86.4527),  # Houchens Industries-L.T. Smith Stadium, Bowling Green
    ("NCAAF", "Army Black Knights"): (41.3875, -73.9791),  # Michie Stadium, West Point
    ("NCAAF", "North Texas Mean Green"): (33.2107, -97.1531),  # DATCU Stadium, Denton
    ("NCAAF", "UTSA Roadrunners"): (29.4169, -98.4786),  # Alamodome, San Antonio
    ("NCAAF", "Southern Miss Golden Eagles"): (31.3244, -89.3373),  # M.M. Roberts Stadium, Hattiesburg
    ("NCAAF", "Delaware Blue Hens"): (39.6795, -75.7546),  # Delaware Stadium, Newark
    ("NCAAF", "Oregon State Beavers"): (44.5646, -123.2820),  # Reser Stadium, Corvallis
    ("NCAAF", "Utah State Aggies"): (41.7424, -111.8107),  # Maverik Stadium, Logan
    ("NCAAF", "Air Force Falcons"): (38.9972, -104.8422),  # Falcon Stadium, Colorado Springs
    ("NCAAF", "North Dakota State Bison"): (46.8535, -96.8014),  # Fargodome, Fargo
    ("NCAAF", "Louisiana Ragin' Cajuns"): (30.2119, -92.0184),  # Cajun Field, Lafayette
    ("NCAAF", "Troy Trojans"): (31.7965, -85.9700),  # Veterans Memorial Stadium, Troy
    ("NCAAF", "Miami (OH) RedHawks"): (39.5090, -84.7327),  # Yager Stadium, Oxford
    ("NCAAF", "Ohio Bobcats"): (39.3255, -82.1039),  # Peden Stadium, Athens
    ("NCAAF", "Liberty Flames"): (37.3595, -79.1780),  # Williams Stadium, Lynchburg

    # --- NCAAMB, second 50 (ranks 51-100 by expected fantasy points) ---
    ("NCAAMB", "Texas A&M Aggies"): (30.6108, -96.3398),  # Reed Arena, College Station
    ("NCAAMB", "Syracuse Orange"): (43.0362, -76.1364),  # JMA Wireless Dome, Syracuse
    ("NCAAMB", "VCU Rams"): (37.5514, -77.4526),  # Siegel Center, Richmond
    ("NCAAMB", "Providence Friars"): (41.8324, -71.4341),  # Amica Mutual Pavilion, Providence
    ("NCAAMB", "Xavier Musketeers"): (39.1490, -84.4805),  # Cintas Center, Cincinnati
    ("NCAAMB", "Oklahoma State Cowboys"): (36.1234, -97.0687),  # Gallagher-Iba Arena, Stillwater
    ("NCAAMB", "West Virginia Mountaineers"): (39.6497, -79.9553),  # WVU Coliseum, Morgantown
    ("NCAAMB", "Grand Canyon Antelopes"): (33.5062, -112.1355),  # GCU Arena, Phoenix
    ("NCAAMB", "San Diego State Aztecs"): (32.7757, -117.0719),  # Viejas Arena, San Diego
    ("NCAAMB", "Wichita State Shockers"): (37.7208, -97.2874),  # Charles Koch Arena, Wichita
    ("NCAAMB", "Florida State Seminoles"): (30.4380, -84.3040),  # Donald L. Tucker Center, Tallahassee
    ("NCAAMB", "Saint Louis Billikens"): (38.6373, -90.2384),  # Chaifetz Arena, St. Louis
    ("NCAAMB", "DePaul Blue Demons"): (41.8756, -87.6742),  # Wintrust Arena, Chicago
    ("NCAAMB", "High Point Panthers"): (35.9857, -79.9959),  # Qubein Arena, High Point
    ("NCAAMB", "Washington Huskies"): (47.6553, -122.3021),  # Alaska Airlines Arena, Seattle
    ("NCAAMB", "Arizona State Sun Devils"): (33.4255, -111.9325),  # Desert Financial Arena, Tempe
    ("NCAAMB", "New Mexico Lobos"): (35.0672, -106.6218),  # The Pit, Albuquerque
    ("NCAAMB", "Utah State Aggies"): (41.7424, -111.8107),  # Dee Glen Smith Spectrum, Logan
    ("NCAAMB", "Saint Mary's Gaels"): (37.8386, -122.1141),  # University Credit Union Pavilion, Moraga
    ("NCAAMB", "Pittsburgh Panthers"): (40.4442, -79.9628),  # Petersen Events Center, Pittsburgh
    ("NCAAMB", "Dayton Flyers"): (39.7444, -84.1998),  # UD Arena, Dayton
    ("NCAAMB", "Seton Hall Pirates"): (40.7433, -74.1710),  # Prudential Center, Newark
    ("NCAAMB", "Northwestern Wildcats"): (42.0578, -87.6742),  # Welsh-Ryan Arena, Evanston
    ("NCAAMB", "Rutgers Scarlet Knights"): (40.5228, -74.4642),  # Jersey Mike's Arena, Piscataway
    ("NCAAMB", "Utah Utes"): (40.7677, -111.8388),  # Jon M. Huntsman Center, Salt Lake City
    ("NCAAMB", "Mississippi State Bulldogs"): (33.4552, -88.7934),  # Humphrey Coliseum, Starkville
    ("NCAAMB", "South Carolina Gamecocks"): (34.0007, -81.0348),  # Colonial Life Arena, Columbia
    ("NCAAMB", "Tulsa Golden Hurricane"): (36.1511, -95.9430),  # Reynolds Center, Tulsa
    ("NCAAMB", "California Golden Bears"): (37.8697, -122.2631),  # Haas Pavilion, Berkeley
    ("NCAAMB", "Notre Dame Fighting Irish"): (41.6983, -86.2331),  # Purcell Pavilion, South Bend
    ("NCAAMB", "George Washington Revolutionaries"): (38.9004, -77.0491),  # Charles E. Smith Center, Washington DC
    ("NCAAMB", "Georgetown Hoyas"): (38.9019, -77.0728),  # Capital One Arena, Washington DC
    ("NCAAMB", "Minnesota Golden Gophers"): (44.9797, -93.2277),  # Williams Arena, Minneapolis
    ("NCAAMB", "Colorado Buffaloes"): (40.0093, -105.2668),  # CU Events Center, Boulder
    ("NCAAMB", "Kansas State Wildcats"): (39.2019, -96.5847),  # Bramlage Coliseum, Manhattan
    ("NCAAMB", "Nevada Wolf Pack"): (39.5439, -119.8138),  # Lawlor Events Center, Reno
    ("NCAAMB", "Boise State Broncos"): (43.6032, -116.1988),  # ExtraMile Arena, Boise
    ("NCAAMB", "Colorado State Rams"): (40.5734, -105.0819),  # Moby Arena, Fort Collins
    ("NCAAMB", "McNeese State Cowboys"): (30.2168, -93.2085),  # Legacy Arena, Lake Charles
    ("NCAAMB", "Charlotte 49ers"): (35.3075, -80.7331),  # Dale F. Halton Arena, Charlotte
    ("NCAAMB", "South Florida Bulls"): (28.0587, -82.4139),  # Yuengling Center, Tampa
    ("NCAAMB", "Wake Forest Demon Deacons"): (36.1359, -80.2761),  # Lawrence Joel Veterans Memorial Coliseum, Winston-Salem
    ("NCAAMB", "George Mason Patriots"): (38.8318, -77.3138),  # EagleBank Arena, Fairfax
    ("NCAAMB", "Butler Bulldogs"): (39.8395, -86.1725),  # Hinkle Fieldhouse, Indianapolis
    ("NCAAMB", "UNLV Rebels"): (36.0972, -115.1436),  # Thomas & Mack Center, Las Vegas
    ("NCAAMB", "Oregon State Beavers"): (44.5657, -123.2789),  # Gill Coliseum, Corvallis
    ("NCAAMB", "Santa Clara Broncos"): (37.3496, -121.9390),  # Leavey Center, Santa Clara
    ("NCAAMB", "Memphis Tigers"): (35.1214, -89.9787),  # FedExForum, Memphis
    ("NCAAMB", "Boston College Eagles"): (42.3356, -71.1685),  # Conte Forum, Chestnut Hill
    ("NCAAMB", "Georgia Tech Yellow Jackets"): (33.7756, -84.3963),  # McCamish Pavilion, Atlanta

    # --- NCAAWB, second 50 (ranks 51-100 by expected fantasy points) ---
    ("NCAAWB", "Wisconsin Badgers"): (43.0778, -89.4106),  # Kohl Center, Madison
    ("NCAAWB", "Baylor Bears"): (31.5586, -97.1156),  # Foster Pavilion, Waco
    ("NCAAWB", "Cincinnati Bearcats"): (39.1310, -84.5157),  # Fifth Third Arena, Cincinnati
    ("NCAAWB", "UCF Knights"): (28.6024, -81.1997),  # Addition Financial Arena, Orlando
    ("NCAAWB", "Texas A&M Aggies"): (30.6108, -96.3398),  # Reed Arena, College Station
    ("NCAAWB", "Syracuse Orange"): (43.0362, -76.1364),  # JMA Wireless Dome, Syracuse
    ("NCAAWB", "VCU Rams"): (37.5514, -77.4526),  # Siegel Center, Richmond
    ("NCAAWB", "Providence Friars"): (41.8324, -71.4341),  # Amica Mutual Pavilion, Providence
    ("NCAAWB", "Xavier Musketeers"): (39.1490, -84.4805),  # Cintas Center, Cincinnati
    ("NCAAWB", "Oklahoma State Cowboys"): (36.1234, -97.0687),  # Gallagher-Iba Arena, Stillwater
    ("NCAAWB", "Grand Canyon Antelopes"): (33.5062, -112.1355),  # GCU Arena, Phoenix
    ("NCAAWB", "San Diego State Aztecs"): (32.7757, -117.0719),  # Viejas Arena, San Diego
    ("NCAAWB", "Wichita State Shockers"): (37.7208, -97.2874),  # Charles Koch Arena, Wichita
    ("NCAAWB", "Saint Louis Billikens"): (38.6373, -90.2384),  # Chaifetz Arena, St. Louis
    ("NCAAWB", "DePaul Blue Demons"): (41.8756, -87.6742),  # Wintrust Arena, Chicago
    ("NCAAWB", "High Point Panthers"): (35.9857, -79.9959),  # Qubein Arena, High Point
    ("NCAAWB", "Arizona State Sun Devils"): (33.4255, -111.9325),  # Desert Financial Arena, Tempe
    ("NCAAWB", "Utah State Aggies"): (41.7424, -111.8107),  # Dee Glen Smith Spectrum, Logan
    ("NCAAWB", "Saint Mary's Gaels"): (37.8386, -122.1141),  # University Credit Union Pavilion, Moraga
    ("NCAAWB", "Tulsa Golden Hurricane"): (36.1511, -95.9430),  # Reynolds Center, Tulsa
    ("NCAAWB", "Florida State Seminoles"): (30.4380, -84.3040),  # Donald L. Tucker Center, Tallahassee
    ("NCAAWB", "Pittsburgh Panthers"): (40.4442, -79.9628),  # Petersen Events Center, Pittsburgh
    ("NCAAWB", "Dayton Flyers"): (39.7444, -84.1998),  # UD Arena, Dayton
    ("NCAAWB", "Seton Hall Pirates"): (40.7433, -74.1710),  # Prudential Center, Newark
    ("NCAAWB", "Northwestern Wildcats"): (42.0578, -87.6742),  # Welsh-Ryan Arena, Evanston
    ("NCAAWB", "Rutgers Scarlet Knights"): (40.5228, -74.4642),  # Jersey Mike's Arena, Piscataway
    ("NCAAWB", "California Golden Bears"): (37.8697, -122.2631),  # Haas Pavilion, Berkeley
    ("NCAAWB", "George Washington Revolutionaries"): (38.9004, -77.0491),  # Charles E. Smith Center, Washington DC
    ("NCAAWB", "Georgetown Hoyas"): (38.9019, -77.0728),  # Capital One Arena, Washington DC
    ("NCAAWB", "Kansas State Wildcats"): (39.2019, -96.5847),  # Bramlage Coliseum, Manhattan
    ("NCAAWB", "Iona Gaels"): (40.9312, -73.7965),  # Hynes Athletics Center, New Rochelle
    ("NCAAWB", "Buffalo Bulls"): (42.9998, -78.7889),  # Alumni Arena, Buffalo
    ("NCAAWB", "Nevada Wolf Pack"): (39.5439, -119.8138),  # Lawlor Events Center, Reno
    ("NCAAWB", "Boise State Broncos"): (43.6032, -116.1988),  # ExtraMile Arena, Boise
    ("NCAAWB", "Colorado State Rams"): (40.5734, -105.0819),  # Moby Arena, Fort Collins
    ("NCAAWB", "McNeese State Cowboys"): (30.2168, -93.2085),  # Legacy Arena, Lake Charles
    ("NCAAWB", "Charlotte 49ers"): (35.3075, -80.7331),  # Dale F. Halton Arena, Charlotte
    ("NCAAWB", "South Florida Bulls"): (28.0587, -82.4139),  # Yuengling Center, Tampa
    ("NCAAWB", "Stanford Cardinal"): (37.4275, -122.1626),  # Maples Pavilion, Stanford
    ("NCAAWB", "Wake Forest Demon Deacons"): (36.1359, -80.2761),  # Lawrence Joel Veterans Memorial Coliseum, Winston-Salem
    ("NCAAWB", "George Mason Patriots"): (38.8318, -77.3138),  # EagleBank Arena, Fairfax
    ("NCAAWB", "Butler Bulldogs"): (39.8395, -86.1725),  # Hinkle Fieldhouse, Indianapolis
    ("NCAAWB", "UC Santa Barbara Gauchos"): (34.4133, -119.8489),  # Thunderdome, Santa Barbara
    ("NCAAWB", "Miami (OH) RedHawks"): (39.5090, -84.7327),  # Millett Hall, Oxford
    ("NCAAWB", "UIC Flames"): (41.8756, -87.6742),  # Credit Union 1 Arena, Chicago
    ("NCAAWB", "UNLV Rebels"): (36.0972, -115.1436),  # Thomas & Mack Center, Las Vegas
    ("NCAAWB", "Oregon State Beavers"): (44.5657, -123.2789),  # Gill Coliseum, Corvallis
    ("NCAAWB", "Santa Clara Broncos"): (37.3496, -121.9390),  # Leavey Center, Santa Clara
    ("NCAAWB", "Memphis Tigers"): (35.1214, -89.9787),  # Elma Roane Fieldhouse, Memphis
    ("NCAAWB", "North Texas Mean Green"): (33.2107, -97.1531),  # Super Pit, Denton
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

    # --- NCAAMB --- (top 50 by expected fantasy points)
    ("NCAAMB", "Duke Blue Devils"): (
        "ACC. Five national titles (1991, 1992, 2001, 2010, 2015) at Cameron Indoor "
        "Stadium, home to the famously rowdy \"Cameron Crazies.\" Mike Krzyzewski retired "
        "in 2022 after 42 seasons; Jon Scheyer, one of his former players, now leads the "
        "program."
    ),
    ("NCAAMB", "Louisville Cardinals"): (
        "ACC. Three national titles (1980, 1986, 2013 -- the last later vacated); Pat "
        "Kelsey has led a rebuild since 2024."
    ),
    ("NCAAMB", "Virginia Cavaliers"): (
        "ACC. One national title (2019), won the year after becoming the first 1-seed "
        "ever upset by a 16-seed; longtime coach Tony Bennett retired abruptly in October "
        "2024, with Ron Sanchez taking over."
    ),
    ("NCAAMB", "Illinois Fighting Illini"): (
        "Big Ten. No national titles despite Final Fours in 1989 and 2005; Brad Underwood "
        "has built a consistent NCAA Tournament program since 2017."
    ),
    ("NCAAMB", "Michigan State Spartans"): (
        "Big Ten. Two national titles (1979, behind Magic Johnson; 2000); Tom Izzo has led "
        "the Spartans since 1995 and owns the sport's longest active NCAA Tournament "
        "streak."
    ),
    ("NCAAMB", "Arizona Wildcats"): (
        "Big 12 (arrived 2024 from the Pac-12). One national title (1997); Tommy Lloyd has "
        "kept the Wildcats a national title contender since taking over in 2021."
    ),
    ("NCAAMB", "Houston Cougars"): (
        "Big 12 (arrived 2023). No national titles despite the \"Phi Slama Jama\" Final "
        "Fours of the early 1980s; Kelvin Sampson has rebuilt Houston into one of the "
        "sport's most physical, defense-first programs, reaching the 2025 title game."
    ),
    ("NCAAMB", "Gonzaga Bulldogs"): (
        "Pac-12 (the rebuilt, basketball-only 9-team league). No national titles despite "
        "championship-game trips in 2017 and 2021; Mark Few has made the Zags a fixture of "
        "the Sweet 16 or better nearly every year since 1999."
    ),
    ("NCAAMB", "Florida Gators"): (
        "SEC. Three national titles (2006, 2007, 2025); Todd Golden led the program back "
        "to the summit in his third season, the program's first title since Billy "
        "Donovan's back-to-back run."
    ),
    ("NCAAMB", "UConn Huskies"): (
        "Big East. Six national titles (1999, 2004, 2011, 2014, 2023, 2024); Dan Hurley's "
        "back-to-back titles were the sport's first repeat champion since Florida in "
        "2006-07."
    ),
    ("NCAAMB", "Michigan Wolverines"): (
        "Big Ten. No national titles on the books (the 1989 title was later vacated); "
        "Dusty May led Michigan to the 2025-26 national championship in his second season, "
        "then left just 11 weeks later to coach the NBA's Dallas Mavericks, with longtime "
        "assistant Mike Boynton promoted to replace him."
    ),
    ("NCAAMB", "Nebraska Cornhuskers"): (
        "Big Ten. No national titles, and historically one of the few power-conference "
        "programs with almost no NCAA Tournament tradition; Fred Hoiberg has built Nebraska "
        "into a Big Ten contender since 2019."
    ),
    ("NCAAMB", "Kansas Jayhawks"): (
        "Big 12. Four national titles (1952, 1988, 2008, 2022), the most of any Big 12 "
        "program; Bill Self has led the Jayhawks since 2003."
    ),
    ("NCAAMB", "Texas Tech Red Raiders"): (
        "Big 12. No national titles despite an overtime loss to Virginia in the 2019 title "
        "game; Grant McCasland has kept the Red Raiders a tournament regular."
    ),
    ("NCAAMB", "Tennessee Volunteers"): (
        "SEC. No national titles; Rick Barnes has built Tennessee into a perennial Sweet "
        "16-caliber program since 2015."
    ),
    ("NCAAMB", "Texas Longhorns"): (
        "SEC (arrived 2024 from the Big 12). No modern-era national titles; Rodney Terry "
        "has kept Texas in the NCAA Tournament mix since 2023."
    ),
    ("NCAAMB", "Miami (FL) Hurricanes"): (
        "ACC. No national titles; Jim Larranaga's 2023 Final Four run -- the program's "
        "first ever -- remains its high-water mark."
    ),
    ("NCAAMB", "St. John's Red Storm"): (
        "Big East. No national titles despite the 1985 Final Four; Rick Pitino's 2023 "
        "arrival revived a long-dormant program."
    ),
    ("NCAAMB", "Ohio State Buckeyes"): (
        "Big Ten. One national title (1960, behind Jerry Lucas and John Havlicek); Jake "
        "Diebler took the program over on an interim-turned-permanent basis in 2024."
    ),
    ("NCAAMB", "UCLA Bruins"): (
        "Big Ten (arrived 2024 from the Pac-12). Eleven national titles, the most of any "
        "program, nearly all part of John Wooden's 1964-75 dynasty; Mick Cronin has kept "
        "the Bruins competitive since 2019."
    ),
    ("NCAAMB", "Iowa State Cyclones"): (
        "Big 12. No national titles; T.J. Otzelberger has built Iowa State into one of the "
        "sport's best defensive programs since 2021."
    ),
    ("NCAAMB", "Alabama Crimson Tide"): (
        "SEC. No national titles; Nate Oats has turned Alabama into an elite offensive "
        "program and consistent Sweet 16-or-better contender since 2023."
    ),
    ("NCAAMB", "Arkansas Razorbacks"): (
        "SEC. One national title (1994, Nolan Richardson's \"40 Minutes of Hell\" team); "
        "John Calipari took over in 2024 after leaving Kentucky."
    ),
    ("NCAAMB", "Kentucky Wildcats"): (
        "SEC. Eight national titles, second-most all-time behind UCLA; Mark Pope took over "
        "in 2024 after John Calipari's departure for Arkansas."
    ),
    ("NCAAMB", "Vanderbilt Commodores"): (
        "SEC. No national titles and historically a rare NCAA Tournament team; Mark "
        "Byington has built real momentum since arriving in 2023."
    ),
    ("NCAAMB", "Marquette Golden Eagles"): (
        "Big East. One national title (1977, Al McGuire's final game as coach); Shaka "
        "Smart has built Marquette into a Big East contender since 2021."
    ),
    ("NCAAMB", "Villanova Wildcats"): (
        "Big East. Three national titles (1985, 2016, 2018) under Jay Wright, who retired "
        "in 2022; Kyle Neptune has led the rebuild since."
    ),
    ("NCAAMB", "Indiana Hoosiers"): (
        "Big Ten. Five national titles, most recently 1987 under Bob Knight; Darian "
        "DeVries took over the program in 2025."
    ),
    ("NCAAMB", "Oregon Ducks"): (
        "Big Ten (arrived 2024 from the Pac-12). No national titles; Dana Altman has led "
        "the program to a Final Four (2017) and frequent tournament appearances since 2010."
    ),
    ("NCAAMB", "Purdue Boilermakers"): (
        "Big Ten. No national titles despite the 2024 title-game appearance (lost to "
        "UConn); Matt Painter has built one of the sport's most consistent programs since "
        "2005."
    ),
    ("NCAAMB", "USC Trojans"): (
        "Big Ten (arrived 2024 from the Pac-12). No national titles; Eric Musselman took "
        "over in 2024 after leaving Arkansas."
    ),
    ("NCAAMB", "Georgia Bulldogs"): (
        "SEC. No national titles, at a historically football-first athletic department; "
        "Mike White has worked to build a tournament-caliber program since 2022."
    ),
    ("NCAAMB", "Clemson Tigers"): (
        "ACC. No national titles; Brad Brownell's 2024 Elite Eight run was the program's "
        "deepest ever."
    ),
    ("NCAAMB", "NC State Wolfpack"): (
        "ACC. Two national titles (1974; 1983's iconic Jim Valvano-led Cinderella run); "
        "Kevin Keatts led a surprise run to the 2024 Final Four as an 11-seed."
    ),
    ("NCAAMB", "Virginia Tech Hokies"): (
        "ACC. No national titles; the Hokies have been a middle-of-the-pack ACC program "
        "for most of the modern era."
    ),
    ("NCAAMB", "Creighton Bluejays"): (
        "Big East. No national titles; Greg McDermott built the Bluejays into a perennial "
        "NCAA Tournament team over 15 seasons before retiring after 2026, with longtime "
        "assistant Alan Huss now in charge."
    ),
    ("NCAAMB", "Maryland Terrapins"): (
        "Big Ten (arrived 2014 from the ACC). One national title (2002); Kevin Willard "
        "took over in 2022 after leaving Seton Hall."
    ),
    ("NCAAMB", "BYU Cougars"): (
        "Big 12 (arrived 2023). No national titles; former NBA assistant Kevin Young took "
        "over in 2024, leading a run of high-major transfer additions."
    ),
    ("NCAAMB", "Cincinnati Bearcats"): (
        "Big 12 (arrived 2023). Two national titles (1961, 1962, under Ed Jucker); Wes "
        "Miller has rebuilt the program in its new conference."
    ),
    ("NCAAMB", "Auburn Tigers"): (
        "SEC. No national titles; Bruce Pearl reached the program's first-ever Final Four "
        "in 2019 and a second in 2025 (lost to Florida), building Auburn into an SEC power."
    ),
    ("NCAAMB", "Missouri Tigers"): (
        "SEC. No national titles; Dennis Gates has built a competitive program since 2022."
    ),
    ("NCAAMB", "Oklahoma Sooners"): (
        "SEC (arrived 2024 from the Big 12). No national titles despite the 1988 "
        "title-game appearance; Porter Moser leads the program."
    ),
    ("NCAAMB", "North Carolina Tar Heels"): (
        "ACC. Six national titles, tied for third-most all-time; Hubert Davis, a Dean "
        "Smith-era player, led the program before Michael Malone's 2026 hire."
    ),
    ("NCAAMB", "SMU Mustangs"): (
        "ACC (arrived 2024). No national titles; Andy Enfield took over in 2024 after "
        "leaving USC."
    ),
    ("NCAAMB", "Iowa Hawkeyes"): (
        "Big Ten. No national titles; Fran McCaffery has built consistent NCAA Tournament "
        "teams since 2010."
    ),
    ("NCAAMB", "Wisconsin Badgers"): (
        "Big Ten. One national title (1941, the pre-modern era); Greg Gard has kept "
        "Wisconsin a tournament regular since 2015."
    ),
    ("NCAAMB", "Baylor Bears"): (
        "Big 12. One national title (2021, won amid the COVID-affected season); Scott Drew "
        "has led the program since 2003."
    ),
    ("NCAAMB", "TCU Horned Frogs"): (
        "Big 12. No national titles; Jamie Dixon has built the Horned Frogs into a "
        "consistent tournament team since 2016."
    ),
    ("NCAAMB", "UCF Knights"): (
        "Big 12 (arrived 2023). No national titles and historically a minor program; "
        "Johnny Dawkins has built the Knights into a first-time tournament regular."
    ),
    ("NCAAMB", "LSU Tigers"): (
        "SEC. No national titles despite the Shaquille O'Neal-era Final Four (1986); Matt "
        "McMahon was replaced in 2026 by Will Wade, returning to LSU after four seasons "
        "away."
    ),

    # --- NCAAWB --- (top 50 by expected fantasy points)
    ("NCAAWB", "UCLA Bruins"): (
        "Big Ten (arrived 2024 from the Pac-12). Won the program's first-ever national "
        "title in 2025-26 under Cori Close."
    ),
    ("NCAAWB", "UConn Huskies"): (
        "Big East. Twelve national titles, the most of any program (men's or women's), "
        "most recently 2025, all under Geno Auriemma, the sport's all-time winningest "
        "coach."
    ),
    ("NCAAWB", "South Carolina Gamecocks"): (
        "SEC. Three national titles (2017, 2022, 2024), the program's transformation into "
        "a dynasty under Dawn Staley since her 2008 hire."
    ),
    ("NCAAWB", "LSU Tigers"): (
        "SEC. One national title (2023), the program's first ever, led by Angel Reese "
        "under Kim Mulkey."
    ),
    ("NCAAWB", "Texas Longhorns"): (
        "SEC (arrived 2024 from the Big 12). One national title (1986); Vic Schaefer has "
        "rebuilt the program into a Final Four regular since 2020."
    ),
    ("NCAAWB", "Duke Blue Devils"): (
        "ACC. No national titles despite title-game appearances in 1999 and 2006; Kara "
        "Lawson has rebuilt the program since 2020."
    ),
    ("NCAAWB", "Michigan Wolverines"): (
        "Big Ten. No national titles; the program built its best stretch in decades in the "
        "early 2020s before a coaching change in 2024."
    ),
    ("NCAAWB", "TCU Horned Frogs"): (
        "Big 12. No national titles; a recent surprise contender in a deep Big 12."
    ),
    ("NCAAWB", "Oklahoma Sooners"): (
        "SEC (arrived 2024 from the Big 12). No national titles despite a 2002 title-game "
        "appearance; Jennie Baranczyk has rebuilt the program since 2021."
    ),
    ("NCAAWB", "Vanderbilt Commodores"): (
        "SEC. No national titles; Shea Ralph has rebuilt the Commodores into a tournament "
        "team since 2021."
    ),
    ("NCAAWB", "Louisville Cardinals"): (
        "ACC. No national titles despite three Final Fours (2009, 2013, 2018) under Jeff "
        "Walz."
    ),
    ("NCAAWB", "North Carolina Tar Heels"): (
        "ACC. One national title (1994) under Sylvia Hatchell; Courtney Banghart has "
        "rebuilt the program since 2019."
    ),
    ("NCAAWB", "Notre Dame Fighting Irish"): (
        "ACC. Two national titles (2001, 2018); Niele Ivey, a member of the 2001 title "
        "team, has led the Irish since 2020."
    ),
    ("NCAAWB", "Iowa Hawkeyes"): (
        "Big Ten. No national titles despite Caitlin Clark's back-to-back title-game runs "
        "(2023 loss to LSU, 2024 loss to South Carolina); Jan Jensen took over after Lisa "
        "Bluder's 2024 retirement."
    ),
    ("NCAAWB", "West Virginia Mountaineers"): (
        "Big 12. No national titles; a mid-tier Big 12 program historically."
    ),
    ("NCAAWB", "Kentucky Wildcats"): (
        "SEC. No national titles; Kenny Brooks took over in 2024 after building a Sweet "
        "16-caliber program at Virginia Tech."
    ),
    ("NCAAWB", "Maryland Terrapins"): (
        "Big Ten (arrived 2014 from the ACC). One national title (2006) under Brenda "
        "Frese, who has led the program since 2002."
    ),
    ("NCAAWB", "Michigan State Spartans"): (
        "Big Ten. No national titles, historically a middle-of-the-pack Big Ten program; "
        "Robyn Fralick took over in 2024."
    ),
    ("NCAAWB", "Minnesota Golden Gophers"): (
        "Big Ten. No national titles; Dawn Plitzuweit has worked to rebuild the program "
        "since 2023."
    ),
    ("NCAAWB", "Ohio State Buckeyes"): (
        "Big Ten. No national titles despite a 1993 title-game appearance; Kevin McGuff "
        "has built a consistent Big Ten contender since 2013."
    ),
    ("NCAAWB", "Mississippi State Bulldogs"): (
        "SEC. No national titles despite back-to-back title-game appearances (2017, 2018); "
        "Sam Purcell leads the program."
    ),
    ("NCAAWB", "Virginia Cavaliers"): (
        "ACC. No national titles; Amaka Agugua-Hamilton leads the rebuild."
    ),
    ("NCAAWB", "Washington Huskies"): (
        "Big Ten (arrived 2024 from the Pac-12). No national titles despite a 2016 Final "
        "Four; Tina Langley has rebuilt the Huskies since 2022."
    ),
    ("NCAAWB", "Columbia Lions"): (
        "Ivy League (minor conference). No national titles and no NCAA Tournament win in "
        "program history, but Megan Griffith has built the Lions into a recent Ivy "
        "contender, with the program's first-ever at-large NCAA bid in 2024."
    ),
    ("NCAAWB", "Alabama Crimson Tide"): (
        "SEC. No national titles; the program reached its first Sweet 16 in decades in "
        "the mid-2020s before a coaching change entering 2026."
    ),
    ("NCAAWB", "NC State Wolfpack"): (
        "ACC. No national titles; Wes Moore has built a consistent ACC contender since "
        "2009."
    ),
    ("NCAAWB", "Virginia Tech Hokies"): (
        "ACC. No national titles; the program reached the 2023 Final Four under Kenny "
        "Brooks, who left for Kentucky in 2024."
    ),
    ("NCAAWB", "Villanova Wildcats"): (
        "Big East. No national titles; a steady Big East program."
    ),
    ("NCAAWB", "Illinois Fighting Illini"): (
        "Big Ten. No national titles and historically a middling program; Shauna Green "
        "has built real momentum since 2023."
    ),
    ("NCAAWB", "Nebraska Cornhuskers"): (
        "Big Ten. No national titles; Amy Williams leads the program."
    ),
    ("NCAAWB", "Oregon Ducks"): (
        "Big Ten (arrived 2024 from the Pac-12). No national titles despite a 2019 Final "
        "Four under Kelly Graves."
    ),
    ("NCAAWB", "USC Trojans"): (
        "Big Ten (arrived 2024 from the Pac-12). Two national titles (1983, 1984, the "
        "Cheryl Miller era); JuJu Watkins' arrival under Lindsay Gottlieb has revived the "
        "program since 2023."
    ),
    ("NCAAWB", "Houston Cougars"): (
        "Big 12. No national titles and historically a minor program, rebuilding in its "
        "new conference."
    ),
    ("NCAAWB", "Fairfield Stags"): (
        "MAAC (minor conference). No national titles; Carly Thibault-DuDonis has built a "
        "MAAC three-peat since 2024."
    ),
    ("NCAAWB", "Gonzaga Bulldogs"): (
        "Pac-12 (minor, basketball-only conference). No national titles; Lisa Fortier has "
        "built the Zags into a consistent West Coast contender."
    ),
    ("NCAAWB", "Miami (FL) Hurricanes"): (
        "ACC. No national titles; Katie Meier built the program's best-ever run (a 2023 "
        "Elite Eight) before retiring in 2024."
    ),
    ("NCAAWB", "St. John's Red Storm"): (
        "Big East. No national titles; Joe Tartamella leads the program."
    ),
    ("NCAAWB", "Kansas Jayhawks"): (
        "Big 12. No national titles and historically a minor program, rebuilding under "
        "Brandon Schneider."
    ),
    ("NCAAWB", "Texas Tech Red Raiders"): (
        "Big 12. One national title (1993) under Marsha Sharp; the program has been "
        "rebuilding toward that standard since."
    ),
    ("NCAAWB", "Ohio Bobcats"): (
        "MAC (minor conference). No national titles; a mid-major program that peaked at "
        "30 wins in 2018-19 before a recent decline."
    ),
    ("NCAAWB", "Marquette Golden Eagles"): (
        "Big East. No national titles; a steady Big East program."
    ),
    ("NCAAWB", "Indiana Hoosiers"): (
        "Big Ten. No national titles; Teri Moren has built the program into a consistent "
        "Sweet 16-caliber contender since 2014."
    ),
    ("NCAAWB", "Purdue Boilermakers"): (
        "Big Ten. No national titles despite title-game appearances in 1999 (won) and "
        "2001 -- the program's lone national title came in 1999."
    ),
    ("NCAAWB", "Iowa State Cyclones"): (
        "Big 12. No national titles; Bill Fennelly has led the program since 1995."
    ),
    ("NCAAWB", "Arkansas Razorbacks"): (
        "SEC. No national titles; Mike Neighbors leads the program."
    ),
    ("NCAAWB", "Clemson Tigers"): (
        "ACC. No national titles and historically a minor program, building recent "
        "tournament appearances."
    ),
    ("NCAAWB", "Creighton Bluejays"): (
        "Big East. No national titles; Jim Flanery has built a consistent Big East "
        "contender."
    ),
    ("NCAAWB", "BYU Cougars"): (
        "Big 12 (arrived 2023). No national titles; a rising Big 12 program."
    ),
    ("NCAAWB", "Auburn Tigers"): (
        "SEC. No national titles and historically a minor program, rebuilding under "
        "Johnnie Harris."
    ),
    ("NCAAWB", "SMU Mustangs"): (
        "ACC (arrived 2024). No national titles; a rising ACC newcomer."
    ),

    # --- NCAAF, second 50 (ranks 51-100 by expected fantasy points) ---
    ("NCAAF", "Colorado Buffaloes"): (
        "Big 12. No national titles since 1990; Deion Sanders' 2023 arrival brought a "
        "media circus and a since-stabilized rebuild."
    ),
    ("NCAAF", "Boise State Broncos"): (
        "Pac-12 (the rebuilt conference). No national titles, but the blue-turf Broncos' "
        "2006 Fiesta Bowl upset of Oklahoma remains a signature program moment, and they "
        "reached the 2024 CFP as a 3-seed."
    ),
    ("NCAAF", "Wake Forest Demon Deacons"): (
        "ACC. No national titles at a historically small private school in a power "
        "conference; Dave Clawson's 2021 team had its best season in decades."
    ),
    ("NCAAF", "Kansas Jayhawks"): (
        "Big 12. A historically football-optional Big 12 program (basketball is king); "
        "Lance Leipold has built the Jayhawks' best stretch since the mid-2000s."
    ),
    ("NCAAF", "Oklahoma State Cowboys"): (
        "Big 12. No national titles; Mike Gundy has led the program since 2005, the "
        "second-longest active tenure in the sport."
    ),
    ("NCAAF", "UCF Knights"): (
        "Big 12 (arrived 2023). No national titles despite the Knights' self-declared 2017 "
        "\"national champion\" claim after an undefeated season; Scott Frost's 2025 return "
        "aims to rebuild."
    ),
    ("NCAAF", "Tulane Green Wave"): (
        "American. No modern national titles; a surprise 2022 AAC title and Cotton Bowl "
        "win over USC was the program's best season in decades."
    ),
    ("NCAAF", "Maryland Terrapins"): (
        "Big Ten. One national title (1953); a middle-of-the-pack Big Ten program since "
        "joining in 2014."
    ),
    ("NCAAF", "Northwestern Wildcats"): (
        "Big Ten. No national titles; the Wildcats have swung between Big Ten West "
        "contention and rock-bottom seasons in recent years, including a hazing-scandal-"
        "marred 2023."
    ),
    ("NCAAF", "California Golden Bears"): (
        "ACC (arrived 2024). Two pre-modern-poll national titles (1920, 1937); a middling "
        "program historically, now in a conference far from home."
    ),
    ("NCAAF", "San Diego State Aztecs"): (
        "Pac-12 (the rebuilt conference). No national titles; a consistent Mountain West "
        "bowl team for most of the last two decades."
    ),
    ("NCAAF", "UNLV Rebels"): (
        "Mountain West. No national titles and historically a minor program; Barry Odom's "
        "2023-24 turnaround produced the best seasons in decades."
    ),
    ("NCAAF", "Michigan State Spartans"): (
        "Big Ten. Six national titles, most recently a share in 1965 and 1966; Jonathan "
        "Smith took over in 2024 after Mel Tucker's scandal-driven firing."
    ),
    ("NCAAF", "Minnesota Golden Gophers"): (
        "Big Ten. Seven national titles, all before 1960; P.J. Fleck has kept the Gophers "
        "a consistent bowl team since 2017."
    ),
    ("NCAAF", "Rutgers Scarlet Knights"): (
        "Big Ten. No national titles, despite hosting the first-ever college football game "
        "in 1869; Greg Schiano's second stint as coach has rebuilt the program."
    ),
    ("NCAAF", "UCLA Bruins"): (
        "Big Ten (arrived 2024 from the Pac-12). One claimed national title (1954); a "
        "middling program in recent years, now playing home games at the Rose Bowl."
    ),
    ("NCAAF", "West Virginia Mountaineers"): (
        "Big 12. No national titles; Rich Rodriguez returned in 2025 for a second stint as "
        "head coach."
    ),
    ("NCAAF", "East Carolina Pirates"): (
        "American. No national titles and historically a minor program; a consistent "
        "bowl-eligible Group of Five team."
    ),
    ("NCAAF", "Navy Midshipmen"): (
        "American (arrived 2024). No national titles; the service academy's option "
        "offense under Brian Newberry has kept it competitive, and the Army-Navy rivalry "
        "remains the sport's oldest continuous tradition."
    ),
    ("NCAAF", "Purdue Boilermakers"): (
        "Big Ten. No national titles; a middling Big Ten West program that reached the "
        "2024 Big Ten title game as a surprise before a rebuilding 2025."
    ),
    ("NCAAF", "Syracuse Orange"): (
        "ACC. One national title (1959); Fran Brown's 2024 team had the program's best "
        "season in over a decade."
    ),
    ("NCAAF", "Iowa State Cyclones"): (
        "Big 12. No national titles; Matt Campbell built the Cyclones into a consistent "
        "Big 12 contender before departing for Penn State in 2026."
    ),
    ("NCAAF", "Memphis Tigers"): (
        "American. No national titles; a consistent Group of Five bowl team under Ryan "
        "Silverfield before his 2026 departure for Arkansas."
    ),
    ("NCAAF", "South Florida Bulls"): (
        "American. No national titles; Alex Golesh built a rapid turnaround before "
        "departing for Auburn in 2026."
    ),
    ("NCAAF", "James Madison Dukes"): (
        "Sun Belt. Two FCS national titles (2004, 2016) before a rapid 2022 jump to FBS; "
        "Curt Cignetti went 19-3 in his final two seasons there before leaving for Indiana "
        "in 2024, and Bob Chesney has kept the winning going."
    ),
    ("NCAAF", "Boston College Eagles"): (
        "ACC. One claimed national title (1940); a middling ACC program under Bill "
        "O'Brien since 2024."
    ),
    ("NCAAF", "Stanford Cardinal"): (
        "ACC (arrived 2024). No consensus national titles despite multiple Rose Bowl wins; "
        "a struggling program in recent years as it adjusts to a coast-to-coast ACC travel "
        "schedule."
    ),
    ("NCAAF", "Fresno State Bulldogs"): (
        "Pac-12 (the rebuilt conference). No national titles; a longtime Mountain "
        "West/WAC power under a series of coaches."
    ),
    ("NCAAF", "Hawaii Rainbow Warriors"): (
        "Mountain West. No national titles; the program's remote location and travel "
        "demands make it a perennial underdog."
    ),
    ("NCAAF", "New Mexico Lobos"): (
        "Mountain West. No national titles and historically a minor program."
    ),
    ("NCAAF", "Toledo Rockets"): (
        "MAC. No national titles; a perennial MAC contender under Jason Candle."
    ),
    ("NCAAF", "Texas State Bobcats"): (
        "Pac-12 (the rebuilt conference). No national titles and a recent FBS transplant "
        "(2013), now the rebuilt Pac-12's breakthrough story after 2025."
    ),
    ("NCAAF", "Washington State Cougars"): (
        "Pac-12 (the rebuilt conference). No modern national titles; survived the 2023-24 "
        "Pac-12 collapse alongside Oregon State before helping rebuild the conference."
    ),
    ("NCAAF", "Old Dominion Monarchs"): (
        "Sun Belt. No national titles and a program that restarted football only in 2009."
    ),
    ("NCAAF", "Western Michigan Broncos"): (
        "MAC. No national titles; a steady MAC program."
    ),
    ("NCAAF", "Western Kentucky Hilltoppers"): (
        "Conference USA. Multiple FCS-era national titles before a 2009 FBS jump; a "
        "prolific-offense program under a series of coaches."
    ),
    ("NCAAF", "Army Black Knights"): (
        "American (arrived 2024). Three national titles (1944-46, the pre-poll era); the "
        "service academy's option offense and the Army-Navy rivalry remain its identity."
    ),
    ("NCAAF", "North Texas Mean Green"): (
        "American. No national titles; a middling Group of Five program."
    ),
    ("NCAAF", "UTSA Roadrunners"): (
        "American. No national titles and a program founded only in 2011; Jeff Traylor "
        "built consecutive Conference USA titles before the 2023 move to the AAC."
    ),
    ("NCAAF", "Southern Miss Golden Eagles"): (
        "Sun Belt. No national titles; historically produced NFL talent (Brett Favre) "
        "despite modest team success."
    ),
    ("NCAAF", "Delaware Blue Hens"): (
        "Conference USA (arrived 2025 from FCS). Multiple FCS-era national titles, most "
        "recently 2003; a first-year FBS transition program."
    ),
    ("NCAAF", "Oregon State Beavers"): (
        "Pac-12 (the rebuilt conference). No national titles; survived the 2023-24 Pac-12 "
        "collapse alongside Washington State before helping rebuild the conference."
    ),
    ("NCAAF", "Utah State Aggies"): (
        "Pac-12 (the rebuilt conference). No national titles; a longtime Mountain West "
        "contender now home in the rebuilt Pac-12."
    ),
    ("NCAAF", "Air Force Falcons"): (
        "Mountain West. No national titles; the service academy's option offense has kept "
        "it a consistent bowl team for decades."
    ),
    ("NCAAF", "North Dakota State Bison"): (
        "Mountain West (moved up in 2026 from FCS). Nine FCS national titles since 2011, "
        "the most dominant FCS dynasty ever; 2026 marks its first season at the FBS level."
    ),
    ("NCAAF", "Louisiana Ragin' Cajuns"): (
        "Sun Belt. No national titles; a consistent Sun Belt contender under Michael "
        "Desormeaux."
    ),
    ("NCAAF", "Troy Trojans"): (
        "Sun Belt. No national titles; a Group of Five program known for occasionally "
        "upsetting power-conference opponents."
    ),
    ("NCAAF", "Miami (OH) RedHawks"): (
        "MAC. No national titles despite the 2003 Ben Roethlisberger-led MAC title team; "
        "the \"Cradle of Coaches\" nickname reflects its history of producing successful "
        "coaches."
    ),
    ("NCAAF", "Ohio Bobcats"): (
        "MAC. No national titles; a steady, unspectacular MAC program under Tim Albin."
    ),
    ("NCAAF", "Liberty Flames"): (
        "Conference USA (arrived 2023). No national titles and an FBS program only since "
        "2018; Hugh Freeze's 2019-21 tenure built it into a consistent winner before "
        "leaving for Auburn (Freeze was later fired there in 2025)."
    ),

    # --- NCAAMB, second 50 (ranks 51-100 by expected fantasy points; major
    # vs. minor conference per docs/wiki/game-rules-ncaamb.md, not by
    # football's classification) ---
    ("NCAAMB", "Texas A&M Aggies"): (
        "SEC. No national titles; Buzz Williams built the Aggies into a Sweet 16 team "
        "before a coaching change entering 2026."
    ),
    ("NCAAMB", "Syracuse Orange"): (
        "Big East. One national title (2003, behind Carmelo Anthony); Jim Boeheim retired "
        "in 2023 after 47 seasons, with Adrian Autry now in charge."
    ),
    ("NCAAMB", "VCU Rams"): (
        "Atlantic 10 (minor conference). No national titles; the 2011 \"Final Four "
        "Cinderella\" run under Shaka Smart remains the program's signature moment."
    ),
    ("NCAAMB", "Providence Friars"): (
        "Big East. No national titles despite a 1987 Final Four (Rick Pitino's first head "
        "coaching job); Kim English leads the program."
    ),
    ("NCAAMB", "Xavier Musketeers"): (
        "Big East. No national titles, a historic mid-major power now in a major "
        "conference; Sean Miller returned in 2022 for a second stint as coach."
    ),
    ("NCAAMB", "Oklahoma State Cowboys"): (
        "Big 12. Two national titles (1945, 1946, as Oklahoma A&M); a middling Big 12 "
        "program in recent years."
    ),
    ("NCAAMB", "West Virginia Mountaineers"): (
        "Big 12. No national titles; Darian DeVries led a one-year turnaround before "
        "leaving for Indiana in 2025, with Ross Hodge now leading the rebuild."
    ),
    ("NCAAMB", "Grand Canyon Antelopes"): (
        "Western Athletic Conference (minor). No national titles as a D-I program only "
        "since 2013; Bryce Drew has built a mid-major power."
    ),
    ("NCAAMB", "San Diego State Aztecs"): (
        "Pac-12 (minor conference; the rebuilt basketball-only league). No national titles "
        "despite the 2023 title-game appearance (lost to UConn); Brian Dutcher has built a "
        "Mountain-West-turned-Pac-12 power."
    ),
    ("NCAAMB", "Wichita State Shockers"): (
        "American (minor conference). No national titles despite the 2013 Final Four under "
        "Gregg Marshall."
    ),
    ("NCAAMB", "Florida State Seminoles"): (
        "ACC. No national titles; a middling program that has missed several recent "
        "tournaments."
    ),
    ("NCAAMB", "Saint Louis Billikens"): (
        "Atlantic 10 (minor conference). No national titles; a steady mid-major program."
    ),
    ("NCAAMB", "DePaul Blue Demons"): (
        "Big East. A claimed national title (1945, the pre-tournament-expansion era); a "
        "historically weak modern Big East program."
    ),
    ("NCAAMB", "High Point Panthers"): (
        "Big South (minor conference). No national titles as a small program, but a "
        "surprise Elite Eight run as a 12-seed in 2025-26."
    ),
    ("NCAAMB", "Washington Huskies"): (
        "Big Ten. No national titles despite a 1953 Final Four; a middling Big Ten program "
        "since the 2024 move from the Pac-12."
    ),
    ("NCAAMB", "Arizona State Sun Devils"): (
        "Big 12. No national titles; Bobby Hurley built a run of NCAA appearances before a "
        "recent decline."
    ),
    ("NCAAMB", "New Mexico Lobos"): (
        "Mountain West (minor conference). No national titles; a consistent mid-major "
        "power under Richard Pitino."
    ),
    ("NCAAMB", "Utah State Aggies"): (
        "Pac-12 (minor conference; the rebuilt basketball-only league). No national "
        "titles; a longtime mid-major mainstay."
    ),
    ("NCAAMB", "Saint Mary's Gaels"): (
        "West Coast Conference (minor). No national titles; a longtime WCC power in "
        "Gonzaga's shadow under Randy Bennett."
    ),
    ("NCAAMB", "Pittsburgh Panthers"): (
        "ACC. No national titles; Jeff Capel has built a recent NCAA Tournament return."
    ),
    ("NCAAMB", "Dayton Flyers"): (
        "Atlantic 10 (minor conference). No national titles despite a 1967 title-game "
        "appearance; Anthony Grant has built a consistent mid-major power."
    ),
    ("NCAAMB", "Seton Hall Pirates"): (
        "Big East. No national titles despite a 1989 title-game appearance (lost in "
        "overtime to Michigan); Shaheen Holloway leads the program."
    ),
    ("NCAAMB", "Northwestern Wildcats"): (
        "Big Ten. No national titles, and the last original Big Ten program to reach its "
        "first-ever NCAA Tournament (2017) under Chris Collins."
    ),
    ("NCAAMB", "Rutgers Scarlet Knights"): (
        "Big Ten. No national titles; Steve Pikiell has built the program's best stretch "
        "in decades."
    ),
    ("NCAAMB", "Utah Utes"): (
        "Big 12. One national title (1944); a middling Big 12 program in recent years."
    ),
    ("NCAAMB", "Mississippi State Bulldogs"): (
        "SEC. No national titles; Chris Jans has built a recent NCAA Tournament regular."
    ),
    ("NCAAMB", "South Carolina Gamecocks"): (
        "SEC. No national titles; a middling men's program overshadowed by the dominant "
        "women's program."
    ),
    ("NCAAMB", "Tulsa Golden Hurricane"): (
        "American (minor conference). No national titles; a historically solid mid-major "
        "program."
    ),
    ("NCAAMB", "California Golden Bears"): (
        "ACC (arrived 2024). One national title (1959); a struggling program in its new "
        "conference."
    ),
    ("NCAAMB", "Notre Dame Fighting Irish"): (
        "ACC. No national titles despite multiple Elite Eight runs; Micah Shrewsberry "
        "leads a rebuild."
    ),
    ("NCAAMB", "George Washington Revolutionaries"): (
        "Atlantic 10 (minor conference). No national titles; renamed from \"Colonials\" in "
        "2023."
    ),
    ("NCAAMB", "Georgetown Hoyas"): (
        "Big East. One national title (1984, behind Patrick Ewing); Ed Cooley has worked "
        "to rebuild the once-dominant program since 2023."
    ),
    ("NCAAMB", "Minnesota Golden Gophers"): (
        "Big Ten. No national titles; Niko Medved took over in 2024 after building "
        "Colorado State into a Mountain West power."
    ),
    ("NCAAMB", "Colorado Buffaloes"): (
        "Big 12. No national titles; a middling program that occasionally makes the "
        "tournament."
    ),
    ("NCAAMB", "Kansas State Wildcats"): (
        "Big 12. No national titles despite Final Fours in 1948 and 1951; Jerome Tang's "
        "2023 Elite Eight run was a surprise breakthrough."
    ),
    ("NCAAMB", "Nevada Wolf Pack"): (
        "Mountain West (minor conference). No national titles; a mid-major program with "
        "Sweet 16 runs in the late 2010s."
    ),
    ("NCAAMB", "Boise State Broncos"): (
        "Pac-12 (minor conference; the rebuilt basketball-only league). No national "
        "titles; a consistent mid-major program."
    ),
    ("NCAAMB", "Colorado State Rams"): (
        "Pac-12 (minor conference; the rebuilt basketball-only league). No national "
        "titles; a consistent mid-major program."
    ),
    ("NCAAMB", "McNeese State Cowboys"): (
        "Southland (minor conference). No national titles as a small program; Will Wade's "
        "2024-25 tenure produced a stunning NCAA Tournament run before he left for LSU in "
        "2026."
    ),
    ("NCAAMB", "Charlotte 49ers"): (
        "American (minor conference). No national titles; a historically middling "
        "program."
    ),
    ("NCAAMB", "South Florida Bulls"): (
        "American (minor conference). No national titles; a rising program in recent "
        "seasons."
    ),
    ("NCAAMB", "Wake Forest Demon Deacons"): (
        "ACC. No national titles despite a 1962 Final Four; a middling ACC program in "
        "recent decades."
    ),
    ("NCAAMB", "George Mason Patriots"): (
        "Atlantic 10 (minor conference). No national titles despite the shocking 2006 "
        "Final Four run as a mid-major."
    ),
    ("NCAAMB", "Butler Bulldogs"): (
        "Big East. No national titles despite back-to-back title-game appearances (2010, "
        "2011) under Brad Stevens."
    ),
    ("NCAAMB", "UNLV Rebels"): (
        "Mountain West (minor conference). One national title (1990, Jerry Tarkanian's "
        "dominant team)."
    ),
    ("NCAAMB", "Oregon State Beavers"): (
        "Pac-12 (minor conference; the rebuilt basketball-only league). No national titles "
        "despite Final Fours in 1949 and 1963; a struggling program in recent years."
    ),
    ("NCAAMB", "Santa Clara Broncos"): (
        "West Coast Conference (minor). No national titles; a historic program (alumnus "
        "Steve Nash) in Gonzaga's shadow."
    ),
    ("NCAAMB", "Memphis Tigers"): (
        "American (minor conference). No national titles despite a vacated 2008 title-game "
        "appearance; Penny Hardaway has built a consistent NCAA Tournament-caliber "
        "program."
    ),
    ("NCAAMB", "Boston College Eagles"): (
        "ACC. No national titles; a struggling ACC program in recent years."
    ),
    ("NCAAMB", "Georgia Tech Yellow Jackets"): (
        "ACC. No national titles despite a 2004 title-game appearance; Damon Stoudamire "
        "leads a rebuild."
    ),

    # --- NCAAWB, second 50 (ranks 51-100 by expected fantasy points) ---
    ("NCAAWB", "Wisconsin Badgers"): (
        "Big Ten. No national titles; historically a minor program."
    ),
    ("NCAAWB", "Baylor Bears"): (
        "Big 12. Three national titles (2005, 2012, 2019) under Kim Mulkey; Nicki Collen "
        "leads the post-Mulkey era."
    ),
    ("NCAAWB", "Cincinnati Bearcats"): (
        "Big 12. No national titles and historically a minor program."
    ),
    ("NCAAWB", "UCF Knights"): (
        "Big 12. No national titles and historically a minor program."
    ),
    ("NCAAWB", "Texas A&M Aggies"): (
        "SEC. One national title (2011) under Gary Blair."
    ),
    ("NCAAWB", "Syracuse Orange"): (
        "ACC. No national titles despite a 2016 title-game appearance."
    ),
    ("NCAAWB", "VCU Rams"): (
        "Atlantic 10 (minor conference). No national titles; a mid-major program."
    ),
    ("NCAAWB", "Providence Friars"): (
        "Big East. No national titles; a mid-tier Big East program."
    ),
    ("NCAAWB", "Xavier Musketeers"): (
        "Big East. No national titles; a mid-tier Big East program."
    ),
    ("NCAAWB", "Oklahoma State Cowboys"): (
        "Big 12. No national titles; a mid-tier Big 12 program."
    ),
    ("NCAAWB", "Grand Canyon Antelopes"): (
        "Western Athletic Conference (minor). No national titles as a D-I program only "
        "since 2013."
    ),
    ("NCAAWB", "San Diego State Aztecs"): (
        "Pac-12 (minor conference; the rebuilt basketball-only league). No national "
        "titles; a rising Mountain-West-turned-Pac-12 program."
    ),
    ("NCAAWB", "Wichita State Shockers"): (
        "American (minor conference). No national titles."
    ),
    ("NCAAWB", "Saint Louis Billikens"): (
        "Atlantic 10 (minor conference). No national titles."
    ),
    ("NCAAWB", "DePaul Blue Demons"): (
        "Big East. No national titles; historically a minor program."
    ),
    ("NCAAWB", "High Point Panthers"): (
        "Big South (minor conference). No national titles as a small program."
    ),
    ("NCAAWB", "Arizona State Sun Devils"): (
        "Big 12. No national titles; Charli Turner Thorne built two decades of NCAA "
        "Tournament appearances before retiring in 2024."
    ),
    ("NCAAWB", "Utah State Aggies"): (
        "Pac-12 (minor conference; the rebuilt basketball-only league). No national "
        "titles."
    ),
    ("NCAAWB", "Saint Mary's Gaels"): (
        "West Coast Conference (minor). No national titles."
    ),
    ("NCAAWB", "Tulsa Golden Hurricane"): (
        "American (minor conference). No national titles."
    ),
    ("NCAAWB", "Florida State Seminoles"): (
        "ACC. No national titles despite a 2000s Final Four appearance under Sue Semrau."
    ),
    ("NCAAWB", "Pittsburgh Panthers"): (
        "ACC. No national titles; historically a minor program."
    ),
    ("NCAAWB", "Dayton Flyers"): (
        "Atlantic 10 (minor conference). No national titles; a consistent mid-major power."
    ),
    ("NCAAWB", "Seton Hall Pirates"): (
        "Big East. No national titles; a mid-tier Big East program."
    ),
    ("NCAAWB", "Northwestern Wildcats"): (
        "Big Ten. No national titles; Joe McKeown built a recent tournament regular."
    ),
    ("NCAAWB", "Rutgers Scarlet Knights"): (
        "Big Ten. No national titles despite a 2007 title-game appearance under legendary "
        "coach C. Vivian Stringer."
    ),
    ("NCAAWB", "California Golden Bears"): (
        "ACC (arrived 2024). No national titles despite a 2013 Final Four appearance."
    ),
    ("NCAAWB", "George Washington Revolutionaries"): (
        "Atlantic 10 (minor conference). No national titles; renamed from \"Colonials\" in "
        "2023."
    ),
    ("NCAAWB", "Georgetown Hoyas"): (
        "Big East. No national titles; historically a minor program."
    ),
    ("NCAAWB", "Kansas State Wildcats"): (
        "Big 12. No national titles; a mid-tier Big 12 program."
    ),
    ("NCAAWB", "Iona Gaels"): (
        "MAAC/Metro (minor conference). No national titles as a small program."
    ),
    ("NCAAWB", "Buffalo Bulls"): (
        "MAC (minor conference). No national titles; a rising MAC power."
    ),
    ("NCAAWB", "Nevada Wolf Pack"): (
        "Mountain West (minor conference). No national titles."
    ),
    ("NCAAWB", "Boise State Broncos"): (
        "Pac-12 (minor conference; the rebuilt basketball-only league). No national "
        "titles."
    ),
    ("NCAAWB", "Colorado State Rams"): (
        "Pac-12 (minor conference; the rebuilt basketball-only league). No national "
        "titles."
    ),
    ("NCAAWB", "McNeese State Cowboys"): (
        "Southland (minor conference). No national titles as a small program."
    ),
    ("NCAAWB", "Charlotte 49ers"): (
        "American (minor conference). No national titles."
    ),
    ("NCAAWB", "South Florida Bulls"): (
        "American (minor conference). No national titles; historically a mid-major power "
        "under Jose Fernandez."
    ),
    ("NCAAWB", "Stanford Cardinal"): (
        "ACC (arrived 2024). Three national titles (1990, 1992, 2021) under Tara "
        "VanDerveer, the sport's all-time winningest coach before her 2024 retirement; "
        "Kate Paye now leads the program."
    ),
    ("NCAAWB", "Wake Forest Demon Deacons"): (
        "ACC. No national titles; historically a minor program."
    ),
    ("NCAAWB", "George Mason Patriots"): (
        "Atlantic 10 (minor conference). No national titles."
    ),
    ("NCAAWB", "Butler Bulldogs"): (
        "Big East. No national titles; a mid-tier Big East program."
    ),
    ("NCAAWB", "UC Santa Barbara Gauchos"): (
        "Big West (minor conference). No national titles as a small program."
    ),
    ("NCAAWB", "Miami (OH) RedHawks"): (
        "MAC (minor conference). No national titles."
    ),
    ("NCAAWB", "UIC Flames"): (
        "Minor conference. No national titles as a small program."
    ),
    ("NCAAWB", "UNLV Rebels"): (
        "Mountain West (minor conference). No national titles."
    ),
    ("NCAAWB", "Oregon State Beavers"): (
        "Pac-12 (minor conference; the rebuilt basketball-only league). No national "
        "titles; Scott Rueck built consistent Elite Eight-level teams in the mid-2010s."
    ),
    ("NCAAWB", "Santa Clara Broncos"): (
        "West Coast Conference (minor). No national titles."
    ),
    ("NCAAWB", "Memphis Tigers"): (
        "American (minor conference). No national titles."
    ),
    ("NCAAWB", "North Texas Mean Green"): (
        "American (minor conference). No national titles; a rising program."
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

    # --- NCAAMB --- (top 50 by expected fantasy points; season_label is
    # e.g. "2021-22" for the season ending in the March 2022 tournament,
    # matching seed_historical_results.py's convention -- the live
    # "2025-26" row picks up from where this leaves off). Compiled from
    # each team's actual NCAA Tournament seed/round and known Final Fours;
    # plain regular-season win-loss for years without a notable run is
    # best effort, same caveat as this file's other proxy sections.
    ("NCAAMB", "Duke Blue Devils"): {
        "2021-22": {"wins": 32, "losses": 7, "ncaa_qualifier": True, "seed_2": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
        "2022-23": {"wins": 27, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 27, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2024-25": {"wins": 35, "losses": 4, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
    },
    ("NCAAMB", "Louisville Cardinals"): {
        "2021-22": {"wins": 13, "losses": 19},
        "2022-23": {"wins": 4, "losses": 28},
        "2023-24": {"wins": 9, "losses": 23},
        "2024-25": {"wins": 27, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Virginia Cavaliers"): {
        "2021-22": {"wins": 21, "losses": 15},
        "2022-23": {"wins": 25, "losses": 8, "ncaa_qualifier": True},
        "2023-24": {"wins": 23, "losses": 11},
        "2024-25": {"wins": 15, "losses": 17},
    },
    ("NCAAMB", "Illinois Fighting Illini"): {
        "2021-22": {"wins": 23, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 21, "losses": 15},
        "2023-24": {"wins": 28, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2024-25": {"wins": 21, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Michigan State Spartans"): {
        "2021-22": {"wins": 23, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 21, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 20, "losses": 15, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 30, "losses": 7, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
    },
    ("NCAAMB", "Arizona Wildcats"): {
        "2021-22": {"wins": 33, "losses": 4, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 28, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 27, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2024-25": {"wins": 24, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Houston Cougars"): {
        "2021-22": {"wins": 32, "losses": 6, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2022-23": {"wins": 33, "losses": 4, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True},
        "2023-24": {"wins": 32, "losses": 5, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True},
        "2024-25": {"wins": 35, "losses": 5, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True},
    },
    ("NCAAMB", "Gonzaga Bulldogs"): {
        "2021-22": {"wins": 28, "losses": 4, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True},
        "2022-23": {"wins": 31, "losses": 6, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2023-24": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 27, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAMB", "Florida Gators"): {
        "2021-22": {"wins": 19, "losses": 15},
        "2022-23": {"wins": 16, "losses": 17},
        "2023-24": {"wins": 24, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 36, "losses": 4, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True, "won_championship": True},
    },
    ("NCAAMB", "UConn Huskies"): {
        "2021-22": {"wins": 23, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 31, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True, "won_championship": True},
        "2023-24": {"wins": 37, "losses": 3, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True, "won_championship": True},
        "2024-25": {"wins": 24, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Michigan Wolverines"): {
        "2021-22": {"wins": 19, "losses": 15, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 18, "losses": 17},
        "2023-24": {"wins": 8, "losses": 24},
        "2024-25": {"wins": 27, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAMB", "Nebraska Cornhuskers"): {
        "2021-22": {"wins": 10, "losses": 22},
        "2022-23": {"wins": 16, "losses": 17},
        "2023-24": {"wins": 23, "losses": 17},
        "2024-25": {"wins": 21, "losses": 15},
    },
    ("NCAAMB", "Kansas Jayhawks"): {
        "2021-22": {"wins": 34, "losses": 6, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True, "won_championship": True},
        "2022-23": {"wins": 28, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 23, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 21, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Texas Tech Red Raiders"): {
        "2021-22": {"wins": 27, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 16, "losses": 17},
        "2023-24": {"wins": 23, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 24, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAMB", "Tennessee Volunteers"): {
        "2021-22": {"wins": 27, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 25, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 27, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2024-25": {"wins": 30, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
    },
    ("NCAAMB", "Texas Longhorns"): {
        "2021-22": {"wins": 22, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 29, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2023-24": {"wins": 21, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 19, "losses": 15},
    },
    ("NCAAMB", "Miami (FL) Hurricanes"): {
        "2021-22": {"wins": 14, "losses": 17},
        "2022-23": {"wins": 29, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
        "2023-24": {"wins": 25, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 18, "losses": 16},
    },
    ("NCAAMB", "St. John's Red Storm"): {
        "2021-22": {"wins": 17, "losses": 15},
        "2022-23": {"wins": 18, "losses": 15},
        "2023-24": {"wins": 18, "losses": 15},
        "2024-25": {"wins": 31, "losses": 5, "ncaa_qualifier": True, "seed_2": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Ohio State Buckeyes"): {
        "2021-22": {"wins": 20, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 16, "losses": 19},
        "2023-24": {"wins": 18, "losses": 17},
        "2024-25": {"wins": 17, "losses": 16},
    },
    ("NCAAMB", "UCLA Bruins"): {
        "2021-22": {"wins": 27, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2022-23": {"wins": 31, "losses": 6, "ncaa_qualifier": True, "seed_2": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 16, "losses": 17},
        "2024-25": {"wins": 23, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Iowa State Cyclones"): {
        "2021-22": {"wins": 22, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 19, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 29, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2024-25": {"wins": 25, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Alabama Crimson Tide"): {
        "2021-22": {"wins": 19, "losses": 14, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 29, "losses": 7, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 25, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
        "2024-25": {"wins": 28, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
    },
    ("NCAAMB", "Arkansas Razorbacks"): {
        "2021-22": {"wins": 27, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2022-23": {"wins": 22, "losses": 14, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 16, "losses": 17},
        "2024-25": {"wins": 22, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAMB", "Kentucky Wildcats"): {
        "2021-22": {"wins": 26, "losses": 8, "ncaa_qualifier": True, "seed_2": True},
        "2022-23": {"wins": 22, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 23, "losses": 10, "ncaa_qualifier": True},
        "2024-25": {"wins": 24, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAMB", "Vanderbilt Commodores"): {
        "2021-22": {"wins": 18, "losses": 14},
        "2022-23": {"wins": 18, "losses": 15},
        "2023-24": {"wins": 20, "losses": 13, "ncaa_qualifier": True},
        "2024-25": {"wins": 20, "losses": 12},
    },
    ("NCAAMB", "Marquette Golden Eagles"): {
        "2021-22": {"wins": 19, "losses": 14},
        "2022-23": {"wins": 29, "losses": 8, "ncaa_qualifier": True, "seed_2": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 27, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 24, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Villanova Wildcats"): {
        "2021-22": {"wins": 30, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
        "2022-23": {"wins": 17, "losses": 17},
        "2023-24": {"wins": 20, "losses": 14},
        "2024-25": {"wins": 18, "losses": 15},
    },
    ("NCAAMB", "Indiana Hoosiers"): {
        "2021-22": {"wins": 21, "losses": 14, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 23, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 23, "losses": 11},
        "2024-25": {"wins": 15, "losses": 18},
    },
    ("NCAAMB", "Oregon Ducks"): {
        "2021-22": {"wins": 20, "losses": 14, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 21, "losses": 15},
        "2023-24": {"wins": 24, "losses": 14, "ncaa_qualifier": True},
        "2024-25": {"wins": 24, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Purdue Boilermakers"): {
        "2021-22": {"wins": 29, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 29, "losses": 6, "ncaa_qualifier": True, "seed_1": True},
        "2023-24": {"wins": 34, "losses": 5, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True},
        "2024-25": {"wins": 24, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "USC Trojans"): {
        "2021-22": {"wins": 26, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 22, "losses": 11},
        "2023-24": {"wins": 15, "losses": 18},
        "2024-25": {"wins": 17, "losses": 17},
    },
    ("NCAAMB", "Georgia Bulldogs"): {
        "2021-22": {"wins": 6, "losses": 26},
        "2022-23": {"wins": 16, "losses": 16},
        "2023-24": {"wins": 20, "losses": 13},
        "2024-25": {"wins": 20, "losses": 13},
    },
    ("NCAAMB", "Clemson Tigers"): {
        "2021-22": {"wins": 17, "losses": 15},
        "2022-23": {"wins": 24, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 24, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2024-25": {"wins": 24, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "NC State Wolfpack"): {
        "2021-22": {"wins": 11, "losses": 21},
        "2022-23": {"wins": 23, "losses": 13},
        "2023-24": {"wins": 24, "losses": 15, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True},
        "2024-25": {"wins": 12, "losses": 19},
    },
    ("NCAAMB", "Virginia Tech Hokies"): {
        "2021-22": {"wins": 23, "losses": 13, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
        "2022-23": {"wins": 20, "losses": 14},
        "2023-24": {"wins": 17, "losses": 17},
        "2024-25": {"wins": 14, "losses": 20},
    },
    ("NCAAMB", "Creighton Bluejays"): {
        "2021-22": {"wins": 23, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 23, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
        "2023-24": {"wins": 23, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2024-25": {"wins": 24, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAMB", "Maryland Terrapins"): {
        "2021-22": {"wins": 15, "losses": 16},
        "2022-23": {"wins": 22, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 18, "losses": 15},
        "2024-25": {"wins": 27, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "BYU Cougars"): {
        "2021-22": {"wins": 26, "losses": 8},
        "2022-23": {"wins": 21, "losses": 11},
        "2023-24": {"wins": 23, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAMB", "Cincinnati Bearcats"): {
        "2021-22": {"wins": 18, "losses": 16},
        "2022-23": {"wins": 19, "losses": 15},
        "2023-24": {"wins": 19, "losses": 15},
        "2024-25": {"wins": 22, "losses": 12},
    },
    ("NCAAMB", "Auburn Tigers"): {
        "2021-22": {"wins": 27, "losses": 6, "ncaa_qualifier": True, "seed_2": True, "won_round_of_64": True},
        "2022-23": {"wins": 21, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 27, "losses": 8, "ncaa_qualifier": True},
        "2024-25": {"wins": 32, "losses": 5, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
    },
    ("NCAAMB", "Missouri Tigers"): {
        "2021-22": {"wins": 12, "losses": 21},
        "2022-23": {"wins": 25, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 21, "losses": 11},
        "2024-25": {"wins": 22, "losses": 11},
    },
    ("NCAAMB", "Oklahoma Sooners"): {
        "2021-22": {"wins": 19, "losses": 14},
        "2022-23": {"wins": 15, "losses": 17},
        "2023-24": {"wins": 20, "losses": 13},
        "2024-25": {"wins": 20, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "North Carolina Tar Heels"): {
        "2021-22": {"wins": 29, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True},
        "2022-23": {"wins": 20, "losses": 13},
        "2023-24": {"wins": 29, "losses": 8, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True},
        "2024-25": {"wins": 23, "losses": 14, "ncaa_qualifier": True},
    },
    ("NCAAMB", "SMU Mustangs"): {
        "2021-22": {"wins": 23, "losses": 11},
        "2022-23": {"wins": 18, "losses": 15},
        "2023-24": {"wins": 23, "losses": 11},
        "2024-25": {"wins": 21, "losses": 15},
    },
    ("NCAAMB", "Iowa Hawkeyes"): {
        "2021-22": {"wins": 26, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 19, "losses": 14, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 19, "losses": 13},
        "2024-25": {"wins": 18, "losses": 17},
    },
    ("NCAAMB", "Wisconsin Badgers"): {
        "2021-22": {"wins": 25, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 20, "losses": 14, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 22, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 23, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Baylor Bears"): {
        "2021-22": {"wins": 27, "losses": 7, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True},
        "2022-23": {"wins": 23, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 24, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 20, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "TCU Horned Frogs"): {
        "2021-22": {"wins": 21, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 22, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2023-24": {"wins": 21, "losses": 14, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 21, "losses": 12},
    },
    ("NCAAMB", "UCF Knights"): {
        "2021-22": {"wins": 14, "losses": 18},
        "2022-23": {"wins": 14, "losses": 19},
        "2023-24": {"wins": 22, "losses": 12},
        "2024-25": {"wins": 21, "losses": 12},
    },
    ("NCAAMB", "LSU Tigers"): {
        "2021-22": {"wins": 22, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 14, "losses": 19},
        "2023-24": {"wins": 17, "losses": 16},
        "2024-25": {"wins": 19, "losses": 13},
    },

    # --- NCAAWB --- (top 50 by expected fantasy points; same season-label
    # convention and sourcing caveat as NCAAMB above)
    ("NCAAWB", "UCLA Bruins"): {
        "2021-22": {"wins": 21, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 20, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 27, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2024-25": {"wins": 34, "losses": 3, "ncaa_qualifier": True, "seed_2": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
    },
    ("NCAAWB", "UConn Huskies"): {
        "2021-22": {"wins": 25, "losses": 6, "ncaa_qualifier": True, "seed_2": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True},
        "2022-23": {"wins": 31, "losses": 6, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
        "2023-24": {"wins": 30, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2024-25": {"wins": 37, "losses": 3, "ncaa_qualifier": True, "seed_2": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True, "won_championship": True},
    },
    ("NCAAWB", "South Carolina Gamecocks"): {
        "2021-22": {"wins": 35, "losses": 2, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True, "won_championship": True},
        "2022-23": {"wins": 36, "losses": 2, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True},
        "2023-24": {"wins": 38, "losses": 0, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True, "won_championship": True},
        "2024-25": {"wins": 30, "losses": 6, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True},
    },
    ("NCAAWB", "LSU Tigers"): {
        "2021-22": {"wins": 26, "losses": 6, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 34, "losses": 2, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True, "won_championship": True},
        "2023-24": {"wins": 21, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2024-25": {"wins": 31, "losses": 6, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
    },
    ("NCAAWB", "Texas Longhorns"): {
        "2021-22": {"wins": 22, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 29, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2023-24": {"wins": 33, "losses": 5, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2024-25": {"wins": 35, "losses": 3, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
    },
    ("NCAAWB", "Duke Blue Devils"): {
        "2021-22": {"wins": 25, "losses": 7, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 27, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 27, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAWB", "Michigan Wolverines"): {
        "2021-22": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 19, "losses": 14},
        "2023-24": {"wins": 15, "losses": 15},
        "2024-25": {"wins": 18, "losses": 14},
    },
    ("NCAAWB", "TCU Horned Frogs"): {
        "2021-22": {"wins": 18, "losses": 12},
        "2022-23": {"wins": 22, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 21, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 29, "losses": 6, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAWB", "Oklahoma Sooners"): {
        "2021-22": {"wins": 22, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 20, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 22, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 25, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAWB", "Vanderbilt Commodores"): {
        "2021-22": {"wins": 7, "losses": 22},
        "2022-23": {"wins": 9, "losses": 22},
        "2023-24": {"wins": 20, "losses": 14, "ncaa_qualifier": True},
        "2024-25": {"wins": 21, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Louisville Cardinals"): {
        "2021-22": {"wins": 25, "losses": 7, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2022-23": {"wins": 22, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2024-25": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "North Carolina Tar Heels"): {
        "2021-22": {"wins": 18, "losses": 13},
        "2022-23": {"wins": 22, "losses": 13},
        "2023-24": {"wins": 19, "losses": 14},
        "2024-25": {"wins": 22, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Notre Dame Fighting Irish"): {
        "2021-22": {"wins": 24, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2024-25": {"wins": 24, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Iowa Hawkeyes"): {
        "2021-22": {"wins": 23, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 31, "losses": 7, "ncaa_qualifier": True, "seed_2": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True},
        "2023-24": {"wins": 34, "losses": 4, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True},
        "2024-25": {"wins": 20, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "West Virginia Mountaineers"): {
        "2021-22": {"wins": 19, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 11, "losses": 19},
        "2023-24": {"wins": 19, "losses": 14},
        "2024-25": {"wins": 18, "losses": 14},
    },
    ("NCAAWB", "Kentucky Wildcats"): {
        "2021-22": {"wins": 20, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 20, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 18, "losses": 14},
        "2024-25": {"wins": 14, "losses": 17},
    },
    ("NCAAWB", "Maryland Terrapins"): {
        "2021-22": {"wins": 23, "losses": 8, "ncaa_qualifier": True, "seed_2": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 25, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 18, "losses": 14},
    },
    ("NCAAWB", "Michigan State Spartans"): {
        "2021-22": {"wins": 16, "losses": 15},
        "2022-23": {"wins": 15, "losses": 17},
        "2023-24": {"wins": 18, "losses": 14},
        "2024-25": {"wins": 20, "losses": 13, "ncaa_qualifier": True},
    },
    ("NCAAWB", "Minnesota Golden Gophers"): {
        "2021-22": {"wins": 14, "losses": 15},
        "2022-23": {"wins": 9, "losses": 20},
        "2023-24": {"wins": 18, "losses": 13},
        "2024-25": {"wins": 17, "losses": 14},
    },
    ("NCAAWB", "Ohio State Buckeyes"): {
        "2021-22": {"wins": 21, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 23, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 21, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2024-25": {"wins": 27, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAWB", "Mississippi State Bulldogs"): {
        "2021-22": {"wins": 17, "losses": 15},
        "2022-23": {"wins": 21, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 20, "losses": 13, "ncaa_qualifier": True},
        "2024-25": {"wins": 25, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAWB", "Virginia Cavaliers"): {
        "2021-22": {"wins": 11, "losses": 18},
        "2022-23": {"wins": 8, "losses": 22},
        "2023-24": {"wins": 10, "losses": 19},
        "2024-25": {"wins": 18, "losses": 14},
    },
    ("NCAAWB", "Washington Huskies"): {
        "2021-22": {"wins": 13, "losses": 16},
        "2022-23": {"wins": 18, "losses": 15},
        "2023-24": {"wins": 19, "losses": 15},
        "2024-25": {"wins": 17, "losses": 15},
    },
    ("NCAAWB", "Columbia Lions"): {
        "2021-22": {"wins": 14, "losses": 12},
        "2022-23": {"wins": 22, "losses": 6},
        "2023-24": {"wins": 23, "losses": 7, "ncaa_qualifier": True},
        "2024-25": {"wins": 24, "losses": 7},
    },
    ("NCAAWB", "Alabama Crimson Tide"): {
        "2021-22": {"wins": 18, "losses": 14},
        "2022-23": {"wins": 20, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 29, "losses": 7, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2024-25": {"wins": 20, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "NC State Wolfpack"): {
        "2021-22": {"wins": 32, "losses": 4, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 23, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 29, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
        "2024-25": {"wins": 24, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Virginia Tech Hokies"): {
        "2021-22": {"wins": 23, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 31, "losses": 5, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
        "2023-24": {"wins": 20, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 16, "losses": 16},
    },
    ("NCAAWB", "Villanova Wildcats"): {
        "2021-22": {"wins": 25, "losses": 6, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 21, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 18, "losses": 14},
        "2024-25": {"wins": 16, "losses": 16},
    },
    ("NCAAWB", "Illinois Fighting Illini"): {
        "2021-22": {"wins": 9, "losses": 19},
        "2022-23": {"wins": 15, "losses": 17},
        "2023-24": {"wins": 18, "losses": 14},
        "2024-25": {"wins": 24, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Nebraska Cornhuskers"): {
        "2021-22": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 19, "losses": 13, "ncaa_qualifier": True},
        "2023-24": {"wins": 21, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 22, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Oregon Ducks"): {
        "2021-22": {"wins": 20, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 18, "losses": 16},
        "2023-24": {"wins": 15, "losses": 17},
        "2024-25": {"wins": 17, "losses": 16},
    },
    ("NCAAWB", "USC Trojans"): {
        "2021-22": {"wins": 8, "losses": 18},
        "2022-23": {"wins": 16, "losses": 15},
        "2023-24": {"wins": 27, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2024-25": {"wins": 31, "losses": 5, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
    },
    ("NCAAWB", "Houston Cougars"): {
        "2021-22": {"wins": 14, "losses": 16},
        "2022-23": {"wins": 12, "losses": 19},
        "2023-24": {"wins": 16, "losses": 15},
        "2024-25": {"wins": 20, "losses": 13},
    },
    ("NCAAWB", "Fairfield Stags"): {
        "2021-22": {"wins": 20, "losses": 9},
        "2022-23": {"wins": 25, "losses": 7},
        "2023-24": {"wins": 29, "losses": 5, "ncaa_qualifier": True, "conf_tourney_champ": True},
        "2024-25": {"wins": 28, "losses": 6, "ncaa_qualifier": True, "conf_tourney_champ": True},
    },
    ("NCAAWB", "Gonzaga Bulldogs"): {
        "2021-22": {"wins": 26, "losses": 6, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 26, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 25, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 26, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Miami (FL) Hurricanes"): {
        "2021-22": {"wins": 22, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 27, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
        "2023-24": {"wins": 19, "losses": 14},
        "2024-25": {"wins": 15, "losses": 17},
    },
    ("NCAAWB", "St. John's Red Storm"): {
        "2021-22": {"wins": 17, "losses": 11},
        "2022-23": {"wins": 17, "losses": 13},
        "2023-24": {"wins": 22, "losses": 11, "ncaa_qualifier": True},
        "2024-25": {"wins": 22, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Kansas Jayhawks"): {
        "2021-22": {"wins": 12, "losses": 17},
        "2022-23": {"wins": 19, "losses": 14},
        "2023-24": {"wins": 20, "losses": 13},
        "2024-25": {"wins": 21, "losses": 13},
    },
    ("NCAAWB", "Texas Tech Red Raiders"): {
        "2021-22": {"wins": 12, "losses": 16},
        "2022-23": {"wins": 17, "losses": 16},
        "2023-24": {"wins": 21, "losses": 10},
        "2024-25": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Ohio Bobcats"): {
        "2021-22": {"wins": 15, "losses": 13},
        "2022-23": {"wins": 18, "losses": 13},
        "2023-24": {"wins": 14, "losses": 16},
        "2024-25": {"wins": 6, "losses": 23},
    },
    ("NCAAWB", "Marquette Golden Eagles"): {
        "2021-22": {"wins": 21, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 22, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 23, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 24, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Indiana Hoosiers"): {
        "2021-22": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 22, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 19, "losses": 12, "ncaa_qualifier": True},
    },
    ("NCAAWB", "Purdue Boilermakers"): {
        "2021-22": {"wins": 14, "losses": 15},
        "2022-23": {"wins": 14, "losses": 16},
        "2023-24": {"wins": 14, "losses": 17},
        "2024-25": {"wins": 19, "losses": 14},
    },
    ("NCAAWB", "Iowa State Cyclones"): {
        "2021-22": {"wins": 17, "losses": 11, "ncaa_qualifier": True},
        "2022-23": {"wins": 19, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 21, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 19, "losses": 12, "ncaa_qualifier": True},
    },
    ("NCAAWB", "Arkansas Razorbacks"): {
        "2021-22": {"wins": 15, "losses": 15},
        "2022-23": {"wins": 18, "losses": 13, "ncaa_qualifier": True},
        "2023-24": {"wins": 25, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 22, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Clemson Tigers"): {
        "2021-22": {"wins": 12, "losses": 17},
        "2022-23": {"wins": 18, "losses": 14},
        "2023-24": {"wins": 21, "losses": 11, "ncaa_qualifier": True},
        "2024-25": {"wins": 23, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Creighton Bluejays"): {
        "2021-22": {"wins": 21, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 19, "losses": 13, "ncaa_qualifier": True},
        "2023-24": {"wins": 19, "losses": 13},
        "2024-25": {"wins": 21, "losses": 12, "ncaa_qualifier": True},
    },
    ("NCAAWB", "BYU Cougars"): {
        "2021-22": {"wins": 21, "losses": 9},
        "2022-23": {"wins": 18, "losses": 13},
        "2023-24": {"wins": 22, "losses": 9},
        "2024-25": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Auburn Tigers"): {
        "2021-22": {"wins": 14, "losses": 15},
        "2022-23": {"wins": 13, "losses": 17},
        "2023-24": {"wins": 22, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 22, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "SMU Mustangs"): {
        "2021-22": {"wins": 22, "losses": 8},
        "2022-23": {"wins": 25, "losses": 8, "ncaa_qualifier": True},
        "2023-24": {"wins": 21, "losses": 11},
        "2024-25": {"wins": 21, "losses": 12},
    },

    # --- NCAAF, second 50 (ranks 51-100) --- same season-label convention
    # and best-effort caveat as the first 50 above.
    ("NCAAF", "Colorado Buffaloes"): {
        "2021": {"wins": 4, "reg_season_losses": 8},
        "2022": {"wins": 1, "reg_season_losses": 11},
        "2023": {"wins": 4, "reg_season_losses": 8},
        "2024": {"wins": 9, "reg_season_losses": 4},
    },
    ("NCAAF", "Boise State Broncos"): {
        "2021": {"wins": 7, "reg_season_losses": 6},
        "2022": {"wins": 10, "reg_season_losses": 4},
        "2023": {"wins": 8, "reg_season_losses": 5},
        "2024": {"wins": 12, "reg_season_losses": 1, "playoff_bid": True, "playoff_bye": True, "playoff_wins": 0},
    },
    ("NCAAF", "Wake Forest Demon Deacons"): {
        "2021": {"wins": 11, "reg_season_losses": 3},
        "2022": {"wins": 8, "reg_season_losses": 5},
        "2023": {"wins": 4, "reg_season_losses": 8},
        "2024": {"wins": 4, "reg_season_losses": 8},
    },
    ("NCAAF", "Kansas Jayhawks"): {
        "2021": {"wins": 2, "reg_season_losses": 10},
        "2022": {"wins": 6, "reg_season_losses": 7},
        "2023": {"wins": 9, "reg_season_losses": 4},
        "2024": {"wins": 5, "reg_season_losses": 7},
    },
    ("NCAAF", "Oklahoma State Cowboys"): {
        "2021": {"wins": 12, "reg_season_losses": 2},
        "2022": {"wins": 7, "reg_season_losses": 6},
        "2023": {"wins": 10, "reg_season_losses": 4},
        "2024": {"wins": 3, "reg_season_losses": 9},
    },
    ("NCAAF", "UCF Knights"): {
        "2021": {"wins": 9, "reg_season_losses": 4},
        "2022": {"wins": 9, "reg_season_losses": 4},
        "2023": {"wins": 6, "reg_season_losses": 7},
        "2024": {"wins": 4, "reg_season_losses": 8},
    },
    ("NCAAF", "Tulane Green Wave"): {
        "2021": {"wins": 2, "reg_season_losses": 10},
        "2022": {"wins": 12, "reg_season_losses": 2},
        "2023": {"wins": 8, "reg_season_losses": 5},
        "2024": {"wins": 9, "reg_season_losses": 4},
    },
    ("NCAAF", "Maryland Terrapins"): {
        "2021": {"wins": 7, "reg_season_losses": 6},
        "2022": {"wins": 8, "reg_season_losses": 5},
        "2023": {"wins": 8, "reg_season_losses": 5},
        "2024": {"wins": 4, "reg_season_losses": 8},
    },
    ("NCAAF", "Northwestern Wildcats"): {
        "2021": {"wins": 3, "reg_season_losses": 9},
        "2022": {"wins": 1, "reg_season_losses": 11},
        "2023": {"wins": 8, "reg_season_losses": 5},
        "2024": {"wins": 4, "reg_season_losses": 8},
    },
    ("NCAAF", "California Golden Bears"): {
        "2021": {"wins": 4, "reg_season_losses": 8},
        "2022": {"wins": 4, "reg_season_losses": 8},
        "2023": {"wins": 6, "reg_season_losses": 7},
        "2024": {"wins": 6, "reg_season_losses": 7},
    },
    ("NCAAF", "San Diego State Aztecs"): {
        "2021": {"wins": 12, "reg_season_losses": 2},
        "2022": {"wins": 12, "reg_season_losses": 2},
        "2023": {"wins": 7, "reg_season_losses": 6},
        "2024": {"wins": 6, "reg_season_losses": 7},
    },
    ("NCAAF", "UNLV Rebels"): {
        "2021": {"wins": 2, "reg_season_losses": 10},
        "2022": {"wins": 5, "reg_season_losses": 7},
        "2023": {"wins": 9, "reg_season_losses": 5},
        "2024": {"wins": 11, "reg_season_losses": 3},
    },
    ("NCAAF", "Michigan State Spartans"): {
        "2021": {"wins": 11, "reg_season_losses": 2},
        "2022": {"wins": 5, "reg_season_losses": 7},
        "2023": {"wins": 4, "reg_season_losses": 8},
        "2024": {"wins": 5, "reg_season_losses": 7},
    },
    ("NCAAF", "Minnesota Golden Gophers"): {
        "2021": {"wins": 9, "reg_season_losses": 4},
        "2022": {"wins": 9, "reg_season_losses": 4},
        "2023": {"wins": 6, "reg_season_losses": 7},
        "2024": {"wins": 8, "reg_season_losses": 5},
    },
    ("NCAAF", "Rutgers Scarlet Knights"): {
        "2021": {"wins": 5, "reg_season_losses": 8},
        "2022": {"wins": 4, "reg_season_losses": 8},
        "2023": {"wins": 7, "reg_season_losses": 6},
        "2024": {"wins": 7, "reg_season_losses": 6},
    },
    ("NCAAF", "UCLA Bruins"): {
        "2021": {"wins": 8, "reg_season_losses": 4},
        "2022": {"wins": 9, "reg_season_losses": 4},
        "2023": {"wins": 8, "reg_season_losses": 4},
        "2024": {"wins": 5, "reg_season_losses": 7},
    },
    ("NCAAF", "West Virginia Mountaineers"): {
        "2021": {"wins": 6, "reg_season_losses": 7},
        "2022": {"wins": 5, "reg_season_losses": 7},
        "2023": {"wins": 8, "reg_season_losses": 5},
        "2024": {"wins": 6, "reg_season_losses": 6},
    },
    ("NCAAF", "East Carolina Pirates"): {
        "2021": {"wins": 7, "reg_season_losses": 6},
        "2022": {"wins": 8, "reg_season_losses": 5},
        "2023": {"wins": 8, "reg_season_losses": 5},
        "2024": {"wins": 6, "reg_season_losses": 6},
    },
    ("NCAAF", "Navy Midshipmen"): {
        "2021": {"wins": 4, "reg_season_losses": 8},
        "2022": {"wins": 4, "reg_season_losses": 8},
        "2023": {"wins": 5, "reg_season_losses": 7},
        "2024": {"wins": 10, "reg_season_losses": 3},
    },
    ("NCAAF", "Purdue Boilermakers"): {
        "2021": {"wins": 9, "reg_season_losses": 4},
        "2022": {"wins": 8, "reg_season_losses": 6},
        "2023": {"wins": 4, "reg_season_losses": 8},
        "2024": {"wins": 1, "reg_season_losses": 11},
    },
    ("NCAAF", "Syracuse Orange"): {
        "2021": {"wins": 5, "reg_season_losses": 7},
        "2022": {"wins": 7, "reg_season_losses": 6},
        "2023": {"wins": 6, "reg_season_losses": 6},
        "2024": {"wins": 10, "reg_season_losses": 3},
    },
    ("NCAAF", "Iowa State Cyclones"): {
        "2021": {"wins": 7, "reg_season_losses": 6},
        "2022": {"wins": 4, "reg_season_losses": 8},
        "2023": {"wins": 7, "reg_season_losses": 6},
        "2024": {"wins": 11, "reg_season_losses": 3},
    },
    ("NCAAF", "Memphis Tigers"): {
        "2021": {"wins": 6, "reg_season_losses": 6},
        "2022": {"wins": 7, "reg_season_losses": 6},
        "2023": {"wins": 10, "reg_season_losses": 3},
        "2024": {"wins": 9, "reg_season_losses": 4},
    },
    ("NCAAF", "South Florida Bulls"): {
        "2021": {"wins": 2, "reg_season_losses": 10},
        "2022": {"wins": 1, "reg_season_losses": 11},
        "2023": {"wins": 7, "reg_season_losses": 6},
        "2024": {"wins": 7, "reg_season_losses": 6},
    },
    ("NCAAF", "James Madison Dukes"): {
        "2021": {"wins": 8, "reg_season_losses": 3},
        "2022": {"wins": 8, "reg_season_losses": 3},
        "2023": {"wins": 12, "reg_season_losses": 1},
        "2024": {"wins": 9, "reg_season_losses": 4},
    },
    ("NCAAF", "Boston College Eagles"): {
        "2021": {"wins": 6, "reg_season_losses": 6},
        "2022": {"wins": 3, "reg_season_losses": 9},
        "2023": {"wins": 7, "reg_season_losses": 6},
        "2024": {"wins": 7, "reg_season_losses": 5},
    },
    ("NCAAF", "Stanford Cardinal"): {
        "2021": {"wins": 3, "reg_season_losses": 9},
        "2022": {"wins": 3, "reg_season_losses": 9},
        "2023": {"wins": 3, "reg_season_losses": 9},
        "2024": {"wins": 3, "reg_season_losses": 9},
    },
    ("NCAAF", "Fresno State Bulldogs"): {
        "2021": {"wins": 10, "reg_season_losses": 4},
        "2022": {"wins": 9, "reg_season_losses": 4},
        "2023": {"wins": 7, "reg_season_losses": 6},
        "2024": {"wins": 6, "reg_season_losses": 7},
    },
    ("NCAAF", "Hawaii Rainbow Warriors"): {
        "2021": {"wins": 6, "reg_season_losses": 7},
        "2022": {"wins": 3, "reg_season_losses": 9},
        "2023": {"wins": 5, "reg_season_losses": 7},
        "2024": {"wins": 5, "reg_season_losses": 7},
    },
    ("NCAAF", "New Mexico Lobos"): {
        "2021": {"wins": 1, "reg_season_losses": 11},
        "2022": {"wins": 3, "reg_season_losses": 9},
        "2023": {"wins": 4, "reg_season_losses": 8},
        "2024": {"wins": 8, "reg_season_losses": 5},
    },
    ("NCAAF", "Toledo Rockets"): {
        "2021": {"wins": 7, "reg_season_losses": 6},
        "2022": {"wins": 7, "reg_season_losses": 6},
        "2023": {"wins": 9, "reg_season_losses": 4},
        "2024": {"wins": 6, "reg_season_losses": 6},
    },
    ("NCAAF", "Texas State Bobcats"): {
        "2021": {"wins": 8, "reg_season_losses": 5},
        "2022": {"wins": 4, "reg_season_losses": 8},
        "2023": {"wins": 4, "reg_season_losses": 8},
        "2024": {"wins": 8, "reg_season_losses": 5},
    },
    ("NCAAF", "Washington State Cougars"): {
        "2021": {"wins": 7, "reg_season_losses": 6},
        "2022": {"wins": 7, "reg_season_losses": 6},
        "2023": {"wins": 5, "reg_season_losses": 7},
        "2024": {"wins": 8, "reg_season_losses": 4},
    },
    ("NCAAF", "Old Dominion Monarchs"): {
        "2021": {"wins": 3, "reg_season_losses": 9},
        "2022": {"wins": 5, "reg_season_losses": 7},
        "2023": {"wins": 5, "reg_season_losses": 7},
        "2024": {"wins": 9, "reg_season_losses": 4},
    },
    ("NCAAF", "Western Michigan Broncos"): {
        "2021": {"wins": 8, "reg_season_losses": 5},
        "2022": {"wins": 8, "reg_season_losses": 6},
        "2023": {"wins": 5, "reg_season_losses": 7},
        "2024": {"wins": 6, "reg_season_losses": 6},
    },
    ("NCAAF", "Western Kentucky Hilltoppers"): {
        "2021": {"wins": 9, "reg_season_losses": 5},
        "2022": {"wins": 9, "reg_season_losses": 5},
        "2023": {"wins": 8, "reg_season_losses": 5},
        "2024": {"wins": 7, "reg_season_losses": 6},
    },
    ("NCAAF", "Army Black Knights"): {
        "2021": {"wins": 9, "reg_season_losses": 4},
        "2022": {"wins": 4, "reg_season_losses": 8},
        "2023": {"wins": 6, "reg_season_losses": 6},
        "2024": {"wins": 12, "reg_season_losses": 2},
    },
    ("NCAAF", "North Texas Mean Green"): {
        "2021": {"wins": 5, "reg_season_losses": 7},
        "2022": {"wins": 7, "reg_season_losses": 6},
        "2023": {"wins": 6, "reg_season_losses": 6},
        "2024": {"wins": 7, "reg_season_losses": 6},
    },
    ("NCAAF", "UTSA Roadrunners"): {
        "2021": {"wins": 7, "reg_season_losses": 5},
        "2022": {"wins": 8, "reg_season_losses": 5},
        "2023": {"wins": 8, "reg_season_losses": 5},
        "2024": {"wins": 7, "reg_season_losses": 6},
    },
    ("NCAAF", "Southern Miss Golden Eagles"): {
        "2021": {"wins": 3, "reg_season_losses": 9},
        "2022": {"wins": 6, "reg_season_losses": 7},
        "2023": {"wins": 4, "reg_season_losses": 8},
        "2024": {"wins": 5, "reg_season_losses": 7},
    },
    ("NCAAF", "Delaware Blue Hens"): {
        "2021": {"wins": 4, "reg_season_losses": 7},
        "2022": {"wins": 4, "reg_season_losses": 7},
        "2023": {"wins": 4, "reg_season_losses": 7},
        "2024": {"wins": 7, "reg_season_losses": 4},
    },
    ("NCAAF", "Oregon State Beavers"): {
        "2021": {"wins": 7, "reg_season_losses": 6},
        "2022": {"wins": 10, "reg_season_losses": 3},
        "2023": {"wins": 8, "reg_season_losses": 5},
        "2024": {"wins": 5, "reg_season_losses": 7},
    },
    ("NCAAF", "Utah State Aggies"): {
        "2021": {"wins": 11, "reg_season_losses": 3},
        "2022": {"wins": 6, "reg_season_losses": 7},
        "2023": {"wins": 6, "reg_season_losses": 7},
        "2024": {"wins": 9, "reg_season_losses": 4},
    },
    ("NCAAF", "Air Force Falcons"): {
        "2021": {"wins": 10, "reg_season_losses": 3},
        "2022": {"wins": 10, "reg_season_losses": 3},
        "2023": {"wins": 8, "reg_season_losses": 5},
        "2024": {"wins": 8, "reg_season_losses": 5},
    },
    ("NCAAF", "North Dakota State Bison"): {
        "2021": {"wins": 12, "reg_season_losses": 2},
        "2022": {"wins": 14, "reg_season_losses": 1},
        "2023": {"wins": 12, "reg_season_losses": 2},
        "2024": {"wins": 15, "reg_season_losses": 0},
    },
    ("NCAAF", "Louisiana Ragin' Cajuns"): {
        "2021": {"wins": 13, "reg_season_losses": 1},
        "2022": {"wins": 5, "reg_season_losses": 7},
        "2023": {"wins": 10, "reg_season_losses": 3},
        "2024": {"wins": 5, "reg_season_losses": 7},
    },
    ("NCAAF", "Troy Trojans"): {
        "2021": {"wins": 5, "reg_season_losses": 7},
        "2022": {"wins": 12, "reg_season_losses": 2},
        "2023": {"wins": 8, "reg_season_losses": 5},
        "2024": {"wins": 8, "reg_season_losses": 5},
    },
    ("NCAAF", "Miami (OH) RedHawks"): {
        "2021": {"wins": 6, "reg_season_losses": 6},
        "2022": {"wins": 6, "reg_season_losses": 6},
        "2023": {"wins": 6, "reg_season_losses": 6},
        "2024": {"wins": 8, "reg_season_losses": 5},
    },
    ("NCAAF", "Ohio Bobcats"): {
        "2021": {"wins": 6, "reg_season_losses": 6},
        "2022": {"wins": 9, "reg_season_losses": 4},
        "2023": {"wins": 8, "reg_season_losses": 5},
        "2024": {"wins": 9, "reg_season_losses": 4},
    },
    ("NCAAF", "Liberty Flames"): {
        "2021": {"wins": 8, "reg_season_losses": 5},
        "2022": {"wins": 8, "reg_season_losses": 5},
        "2023": {"wins": 13, "reg_season_losses": 1},
        "2024": {"wins": 8, "reg_season_losses": 5},
    },

    # --- NCAAMB, second 50 (ranks 51-100) --- same convention/caveat as
    # the first 50 above.
    ("NCAAMB", "Texas A&M Aggies"): {
        "2021-22": {"wins": 16, "losses": 16},
        "2022-23": {"wins": 25, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 20, "losses": 14},
        "2024-25": {"wins": 23, "losses": 13, "ncaa_qualifier": True},
    },
    ("NCAAMB", "Syracuse Orange"): {
        "2021-22": {"wins": 16, "losses": 17},
        "2022-23": {"wins": 17, "losses": 15},
        "2023-24": {"wins": 19, "losses": 14},
        "2024-25": {"wins": 18, "losses": 15},
    },
    ("NCAAMB", "VCU Rams"): {
        "2021-22": {"wins": 19, "losses": 12, "ncaa_qualifier": True, "conf_tourney_champ": True},
        "2022-23": {"wins": 27, "losses": 8, "ncaa_qualifier": True, "conf_tourney_champ": True},
        "2023-24": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "conf_tourney_champ": True},
        "2024-25": {"wins": 28, "losses": 8, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Providence Friars"): {
        "2021-22": {"wins": 27, "losses": 7, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2022-23": {"wins": 21, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 21, "losses": 11},
        "2024-25": {"wins": 18, "losses": 14},
    },
    ("NCAAMB", "Xavier Musketeers"): {
        "2021-22": {"wins": 26, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 27, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 18, "losses": 15},
        "2024-25": {"wins": 19, "losses": 14},
    },
    ("NCAAMB", "Oklahoma State Cowboys"): {
        "2021-22": {"wins": 21, "losses": 13},
        "2022-23": {"wins": 16, "losses": 16},
        "2023-24": {"wins": 16, "losses": 16},
        "2024-25": {"wins": 19, "losses": 14},
    },
    ("NCAAMB", "West Virginia Mountaineers"): {
        "2021-22": {"wins": 16, "losses": 16},
        "2022-23": {"wins": 19, "losses": 15},
        "2023-24": {"wins": 9, "losses": 23},
        "2024-25": {"wins": 19, "losses": 13},
    },
    ("NCAAMB", "Grand Canyon Antelopes"): {
        "2021-22": {"wins": 23, "losses": 10},
        "2022-23": {"wins": 21, "losses": 9},
        "2023-24": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "San Diego State Aztecs"): {
        "2021-22": {"wins": 27, "losses": 7, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 32, "losses": 7, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True, "won_final_4": True},
        "2023-24": {"wins": 25, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 22, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Wichita State Shockers"): {
        "2021-22": {"wins": 16, "losses": 15},
        "2022-23": {"wins": 18, "losses": 15},
        "2023-24": {"wins": 17, "losses": 15},
        "2024-25": {"wins": 16, "losses": 16},
    },
    ("NCAAMB", "Florida State Seminoles"): {
        "2021-22": {"wins": 18, "losses": 15},
        "2022-23": {"wins": 9, "losses": 23},
        "2023-24": {"wins": 19, "losses": 14},
        "2024-25": {"wins": 20, "losses": 14},
    },
    ("NCAAMB", "Saint Louis Billikens"): {
        "2021-22": {"wins": 23, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 20, "losses": 14},
        "2023-24": {"wins": 20, "losses": 13},
        "2024-25": {"wins": 24, "losses": 12},
    },
    ("NCAAMB", "DePaul Blue Demons"): {
        "2021-22": {"wins": 15, "losses": 17},
        "2022-23": {"wins": 11, "losses": 21},
        "2023-24": {"wins": 3, "losses": 29},
        "2024-25": {"wins": 19, "losses": 15},
    },
    ("NCAAMB", "High Point Panthers"): {
        "2021-22": {"wins": 12, "losses": 19},
        "2022-23": {"wins": 20, "losses": 13},
        "2023-24": {"wins": 29, "losses": 6},
        "2024-25": {"wins": 31, "losses": 4, "ncaa_qualifier": True, "conf_tourney_champ": True},
    },
    ("NCAAMB", "Washington Huskies"): {
        "2021-22": {"wins": 17, "losses": 15},
        "2022-23": {"wins": 15, "losses": 17},
        "2023-24": {"wins": 16, "losses": 16},
        "2024-25": {"wins": 18, "losses": 15},
    },
    ("NCAAMB", "Arizona State Sun Devils"): {
        "2021-22": {"wins": 14, "losses": 17},
        "2022-23": {"wins": 23, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 22, "losses": 15, "ncaa_qualifier": True},
        "2024-25": {"wins": 14, "losses": 18},
    },
    ("NCAAMB", "New Mexico Lobos"): {
        "2021-22": {"wins": 22, "losses": 11},
        "2022-23": {"wins": 22, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 26, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 27, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Utah State Aggies"): {
        "2021-22": {"wins": 20, "losses": 14},
        "2022-23": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 27, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 25, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Saint Mary's Gaels"): {
        "2021-22": {"wins": 26, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2023-24": {"wins": 28, "losses": 7, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 25, "losses": 7, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Pittsburgh Panthers"): {
        "2021-22": {"wins": 11, "losses": 21},
        "2022-23": {"wins": 15, "losses": 17},
        "2023-24": {"wins": 22, "losses": 13},
        "2024-25": {"wins": 20, "losses": 14},
    },
    ("NCAAMB", "Dayton Flyers"): {
        "2021-22": {"wins": 24, "losses": 8},
        "2022-23": {"wins": 17, "losses": 15},
        "2023-24": {"wins": 24, "losses": 10},
        "2024-25": {"wins": 24, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Seton Hall Pirates"): {
        "2021-22": {"wins": 17, "losses": 16},
        "2022-23": {"wins": 17, "losses": 15},
        "2023-24": {"wins": 20, "losses": 14, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 13, "losses": 19},
    },
    ("NCAAMB", "Northwestern Wildcats"): {
        "2021-22": {"wins": 15, "losses": 16},
        "2022-23": {"wins": 22, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 23, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 18, "losses": 15},
    },
    ("NCAAMB", "Rutgers Scarlet Knights"): {
        "2021-22": {"wins": 18, "losses": 14, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 19, "losses": 14},
        "2023-24": {"wins": 20, "losses": 13, "ncaa_qualifier": True},
        "2024-25": {"wins": 15, "losses": 17},
    },
    ("NCAAMB", "Utah Utes"): {
        "2021-22": {"wins": 17, "losses": 15},
        "2022-23": {"wins": 17, "losses": 16},
        "2023-24": {"wins": 11, "losses": 21},
        "2024-25": {"wins": 13, "losses": 19},
    },
    ("NCAAMB", "Mississippi State Bulldogs"): {
        "2021-22": {"wins": 19, "losses": 16},
        "2022-23": {"wins": 21, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 21, "losses": 14, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 21, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "South Carolina Gamecocks"): {
        "2021-22": {"wins": 18, "losses": 14},
        "2022-23": {"wins": 11, "losses": 21},
        "2023-24": {"wins": 11, "losses": 21},
        "2024-25": {"wins": 16, "losses": 17},
    },
    ("NCAAMB", "Tulsa Golden Hurricane"): {
        "2021-22": {"wins": 18, "losses": 15},
        "2022-23": {"wins": 11, "losses": 21},
        "2023-24": {"wins": 19, "losses": 14},
        "2024-25": {"wins": 20, "losses": 13},
    },
    ("NCAAMB", "California Golden Bears"): {
        "2021-22": {"wins": 12, "losses": 20},
        "2022-23": {"wins": 3, "losses": 29},
        "2023-24": {"wins": 14, "losses": 19},
        "2024-25": {"wins": 15, "losses": 17},
    },
    ("NCAAMB", "Notre Dame Fighting Irish"): {
        "2021-22": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 11, "losses": 21},
        "2023-24": {"wins": 13, "losses": 19},
        "2024-25": {"wins": 19, "losses": 14},
    },
    ("NCAAMB", "George Washington Revolutionaries"): {
        "2021-22": {"wins": 11, "losses": 19},
        "2022-23": {"wins": 16, "losses": 16},
        "2023-24": {"wins": 20, "losses": 13},
        "2024-25": {"wins": 19, "losses": 14},
    },
    ("NCAAMB", "Georgetown Hoyas"): {
        "2021-22": {"wins": 6, "losses": 25},
        "2022-23": {"wins": 7, "losses": 25},
        "2023-24": {"wins": 14, "losses": 18},
        "2024-25": {"wins": 18, "losses": 17},
    },
    ("NCAAMB", "Minnesota Golden Gophers"): {
        "2021-22": {"wins": 13, "losses": 17},
        "2022-23": {"wins": 9, "losses": 22},
        "2023-24": {"wins": 19, "losses": 14},
        "2024-25": {"wins": 18, "losses": 14},
    },
    ("NCAAMB", "Colorado Buffaloes"): {
        "2021-22": {"wins": 20, "losses": 14},
        "2022-23": {"wins": 16, "losses": 18},
        "2023-24": {"wins": 25, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 23, "losses": 12, "ncaa_qualifier": True},
    },
    ("NCAAMB", "Kansas State Wildcats"): {
        "2021-22": {"wins": 14, "losses": 17},
        "2022-23": {"wins": 26, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
        "2023-24": {"wins": 19, "losses": 13},
        "2024-25": {"wins": 16, "losses": 16},
    },
    ("NCAAMB", "Nevada Wolf Pack"): {
        "2021-22": {"wins": 23, "losses": 11},
        "2022-23": {"wins": 23, "losses": 9},
        "2023-24": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Boise State Broncos"): {
        "2021-22": {"wins": 27, "losses": 7, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 21, "losses": 12},
        "2023-24": {"wins": 20, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 18, "losses": 15},
    },
    ("NCAAMB", "Colorado State Rams"): {
        "2021-22": {"wins": 25, "losses": 11},
        "2022-23": {"wins": 25, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
        "2024-25": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "McNeese State Cowboys"): {
        "2021-22": {"wins": 22, "losses": 9},
        "2022-23": {"wins": 18, "losses": 15},
        "2023-24": {"wins": 30, "losses": 4, "ncaa_qualifier": True, "conf_tourney_champ": True},
        "2024-25": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Charlotte 49ers"): {
        "2021-22": {"wins": 9, "losses": 19},
        "2022-23": {"wins": 17, "losses": 16},
        "2023-24": {"wins": 20, "losses": 13},
        "2024-25": {"wins": 20, "losses": 13},
    },
    ("NCAAMB", "South Florida Bulls"): {
        "2021-22": {"wins": 15, "losses": 16},
        "2022-23": {"wins": 16, "losses": 16},
        "2023-24": {"wins": 16, "losses": 16},
        "2024-25": {"wins": 25, "losses": 9, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Wake Forest Demon Deacons"): {
        "2021-22": {"wins": 25, "losses": 11},
        "2022-23": {"wins": 18, "losses": 14},
        "2023-24": {"wins": 19, "losses": 15},
        "2024-25": {"wins": 22, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "George Mason Patriots"): {
        "2021-22": {"wins": 13, "losses": 14},
        "2022-23": {"wins": 17, "losses": 16},
        "2023-24": {"wins": 18, "losses": 14},
        "2024-25": {"wins": 24, "losses": 11},
    },
    ("NCAAMB", "Butler Bulldogs"): {
        "2021-22": {"wins": 14, "losses": 18},
        "2022-23": {"wins": 14, "losses": 19},
        "2023-24": {"wins": 16, "losses": 16},
        "2024-25": {"wins": 20, "losses": 14},
    },
    ("NCAAMB", "UNLV Rebels"): {
        "2021-22": {"wins": 20, "losses": 13},
        "2022-23": {"wins": 26, "losses": 9},
        "2023-24": {"wins": 20, "losses": 12},
        "2024-25": {"wins": 19, "losses": 15},
    },
    ("NCAAMB", "Oregon State Beavers"): {
        "2021-22": {"wins": 3, "losses": 28},
        "2022-23": {"wins": 11, "losses": 21},
        "2023-24": {"wins": 13, "losses": 18},
        "2024-25": {"wins": 16, "losses": 15},
    },
    ("NCAAMB", "Santa Clara Broncos"): {
        "2021-22": {"wins": 12, "losses": 19},
        "2022-23": {"wins": 24, "losses": 11},
        "2023-24": {"wins": 22, "losses": 11},
        "2024-25": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAMB", "Memphis Tigers"): {
        "2021-22": {"wins": 21, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 26, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 25, "losses": 9},
        "2024-25": {"wins": 23, "losses": 11},
    },
    ("NCAAMB", "Boston College Eagles"): {
        "2021-22": {"wins": 12, "losses": 20},
        "2022-23": {"wins": 12, "losses": 20},
        "2023-24": {"wins": 16, "losses": 16},
        "2024-25": {"wins": 20, "losses": 14},
    },
    ("NCAAMB", "Georgia Tech Yellow Jackets"): {
        "2021-22": {"wins": 12, "losses": 20},
        "2022-23": {"wins": 15, "losses": 17},
        "2023-24": {"wins": 16, "losses": 17},
        "2024-25": {"wins": 14, "losses": 19},
    },

    # --- NCAAWB, second 50 (ranks 51-100) --- same convention/caveat as
    # the first 50 above.
    ("NCAAWB", "Wisconsin Badgers"): {
        "2021-22": {"wins": 10, "losses": 19},
        "2022-23": {"wins": 10, "losses": 20},
        "2023-24": {"wins": 14, "losses": 18},
        "2024-25": {"wins": 18, "losses": 14},
    },
    ("NCAAWB", "Baylor Bears"): {
        "2021-22": {"wins": 22, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 21, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 20, "losses": 14, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 25, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAWB", "Cincinnati Bearcats"): {
        "2021-22": {"wins": 12, "losses": 16},
        "2022-23": {"wins": 16, "losses": 15},
        "2023-24": {"wins": 16, "losses": 14},
        "2024-25": {"wins": 20, "losses": 13},
    },
    ("NCAAWB", "UCF Knights"): {
        "2021-22": {"wins": 19, "losses": 13},
        "2022-23": {"wins": 16, "losses": 15},
        "2023-24": {"wins": 17, "losses": 14},
        "2024-25": {"wins": 22, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Texas A&M Aggies"): {
        "2021-22": {"wins": 19, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 23, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 18, "losses": 15},
        "2024-25": {"wins": 20, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Syracuse Orange"): {
        "2021-22": {"wins": 13, "losses": 16},
        "2022-23": {"wins": 18, "losses": 14, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 20, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAWB", "VCU Rams"): {
        "2021-22": {"wins": 19, "losses": 11, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
        "2022-23": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
        "2023-24": {"wins": 22, "losses": 10, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
        "2024-25": {"wins": 28, "losses": 8, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAWB", "Providence Friars"): {
        "2021-22": {"wins": 13, "losses": 16},
        "2022-23": {"wins": 14, "losses": 16},
        "2023-24": {"wins": 16, "losses": 15},
        "2024-25": {"wins": 15, "losses": 16},
    },
    ("NCAAWB", "Xavier Musketeers"): {
        "2021-22": {"wins": 16, "losses": 14},
        "2022-23": {"wins": 16, "losses": 15},
        "2023-24": {"wins": 15, "losses": 16},
        "2024-25": {"wins": 17, "losses": 15},
    },
    ("NCAAWB", "Oklahoma State Cowboys"): {
        "2021-22": {"wins": 16, "losses": 16},
        "2022-23": {"wins": 16, "losses": 15},
        "2023-24": {"wins": 19, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 24, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True, "won_round_of_32": True},
    },
    ("NCAAWB", "Grand Canyon Antelopes"): {
        "2021-22": {"wins": 20, "losses": 11},
        "2022-23": {"wins": 19, "losses": 12},
        "2023-24": {"wins": 24, "losses": 8, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 23, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "San Diego State Aztecs"): {
        "2021-22": {"wins": 14, "losses": 15},
        "2022-23": {"wins": 19, "losses": 13},
        "2023-24": {"wins": 18, "losses": 14},
        "2024-25": {"wins": 21, "losses": 11},
    },
    ("NCAAWB", "Wichita State Shockers"): {
        "2021-22": {"wins": 11, "losses": 19},
        "2022-23": {"wins": 14, "losses": 17},
        "2023-24": {"wins": 16, "losses": 15},
        "2024-25": {"wins": 17, "losses": 14},
    },
    ("NCAAWB", "Saint Louis Billikens"): {
        "2021-22": {"wins": 19, "losses": 13},
        "2022-23": {"wins": 15, "losses": 16},
        "2023-24": {"wins": 16, "losses": 16},
        "2024-25": {"wins": 20, "losses": 12},
    },
    ("NCAAWB", "DePaul Blue Demons"): {
        "2021-22": {"wins": 12, "losses": 17},
        "2022-23": {"wins": 11, "losses": 19},
        "2023-24": {"wins": 14, "losses": 17},
        "2024-25": {"wins": 15, "losses": 16},
    },
    ("NCAAWB", "High Point Panthers"): {
        "2021-22": {"wins": 15, "losses": 14},
        "2022-23": {"wins": 19, "losses": 11},
        "2023-24": {"wins": 22, "losses": 9},
        "2024-25": {"wins": 27, "losses": 6, "ncaa_qualifier": True, "conf_tourney_champ": True},
    },
    ("NCAAWB", "Arizona State Sun Devils"): {
        "2021-22": {"wins": 17, "losses": 13},
        "2022-23": {"wins": 20, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 21, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 24, "losses": 11, "ncaa_qualifier": True},
    },
    ("NCAAWB", "Utah State Aggies"): {
        "2021-22": {"wins": 11, "losses": 18},
        "2022-23": {"wins": 14, "losses": 16},
        "2023-24": {"wins": 16, "losses": 15},
        "2024-25": {"wins": 17, "losses": 14},
    },
    ("NCAAWB", "Saint Mary's Gaels"): {
        "2021-22": {"wins": 16, "losses": 14},
        "2022-23": {"wins": 17, "losses": 14},
        "2023-24": {"wins": 19, "losses": 12},
        "2024-25": {"wins": 20, "losses": 11},
    },
    ("NCAAWB", "Tulsa Golden Hurricane"): {
        "2021-22": {"wins": 16, "losses": 14},
        "2022-23": {"wins": 15, "losses": 15},
        "2023-24": {"wins": 17, "losses": 14},
        "2024-25": {"wins": 19, "losses": 12},
    },
    ("NCAAWB", "Florida State Seminoles"): {
        "2021-22": {"wins": 16, "losses": 15},
        "2022-23": {"wins": 15, "losses": 16},
        "2023-24": {"wins": 16, "losses": 15},
        "2024-25": {"wins": 17, "losses": 14},
    },
    ("NCAAWB", "Pittsburgh Panthers"): {
        "2021-22": {"wins": 15, "losses": 15},
        "2022-23": {"wins": 16, "losses": 15},
        "2023-24": {"wins": 18, "losses": 14},
        "2024-25": {"wins": 19, "losses": 13},
    },
    ("NCAAWB", "Dayton Flyers"): {
        "2021-22": {"wins": 20, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 17, "losses": 13},
        "2023-24": {"wins": 22, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 23, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Seton Hall Pirates"): {
        "2021-22": {"wins": 12, "losses": 16},
        "2022-23": {"wins": 16, "losses": 15},
        "2023-24": {"wins": 15, "losses": 15},
        "2024-25": {"wins": 16, "losses": 15},
    },
    ("NCAAWB", "Northwestern Wildcats"): {
        "2021-22": {"wins": 18, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 20, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 18, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 22, "losses": 10, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Rutgers Scarlet Knights"): {
        "2021-22": {"wins": 19, "losses": 13, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 15, "losses": 15},
        "2023-24": {"wins": 16, "losses": 15},
        "2024-25": {"wins": 17, "losses": 14},
    },
    ("NCAAWB", "California Golden Bears"): {
        "2021-22": {"wins": 12, "losses": 17},
        "2022-23": {"wins": 11, "losses": 19},
        "2023-24": {"wins": 12, "losses": 18},
        "2024-25": {"wins": 14, "losses": 17},
    },
    ("NCAAWB", "George Washington Revolutionaries"): {
        "2021-22": {"wins": 13, "losses": 16},
        "2022-23": {"wins": 16, "losses": 14},
        "2023-24": {"wins": 19, "losses": 13},
        "2024-25": {"wins": 20, "losses": 11},
    },
    ("NCAAWB", "Georgetown Hoyas"): {
        "2021-22": {"wins": 11, "losses": 17},
        "2022-23": {"wins": 9, "losses": 21},
        "2023-24": {"wins": 14, "losses": 16},
        "2024-25": {"wins": 16, "losses": 15},
    },
    ("NCAAWB", "Kansas State Wildcats"): {
        "2021-22": {"wins": 14, "losses": 15},
        "2022-23": {"wins": 19, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 20, "losses": 12, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 19, "losses": 13},
    },
    ("NCAAWB", "Iona Gaels"): {
        "2021-22": {"wins": 22, "losses": 8, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
        "2022-23": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
        "2023-24": {"wins": 15, "losses": 16},
        "2024-25": {"wins": 20, "losses": 12},
    },
    ("NCAAWB", "Buffalo Bulls"): {
        "2021-22": {"wins": 20, "losses": 11, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
        "2022-23": {"wins": 22, "losses": 9, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
        "2023-24": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
        "2024-25": {"wins": 26, "losses": 8, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Nevada Wolf Pack"): {
        "2021-22": {"wins": 14, "losses": 15},
        "2022-23": {"wins": 16, "losses": 16},
        "2023-24": {"wins": 17, "losses": 14},
        "2024-25": {"wins": 18, "losses": 13},
    },
    ("NCAAWB", "Boise State Broncos"): {
        "2021-22": {"wins": 16, "losses": 14},
        "2022-23": {"wins": 20, "losses": 12},
        "2023-24": {"wins": 18, "losses": 13},
        "2024-25": {"wins": 19, "losses": 13},
    },
    ("NCAAWB", "Colorado State Rams"): {
        "2021-22": {"wins": 18, "losses": 13},
        "2022-23": {"wins": 19, "losses": 12},
        "2023-24": {"wins": 22, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2024-25": {"wins": 27, "losses": 7, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "McNeese State Cowboys"): {
        "2021-22": {"wins": 14, "losses": 15},
        "2022-23": {"wins": 16, "losses": 13},
        "2023-24": {"wins": 22, "losses": 9, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
        "2024-25": {"wins": 23, "losses": 8, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Charlotte 49ers"): {
        "2021-22": {"wins": 11, "losses": 17},
        "2022-23": {"wins": 15, "losses": 15},
        "2023-24": {"wins": 18, "losses": 13},
        "2024-25": {"wins": 19, "losses": 12},
    },
    ("NCAAWB", "South Florida Bulls"): {
        "2021-22": {"wins": 22, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 21, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2023-24": {"wins": 19, "losses": 13},
        "2024-25": {"wins": 22, "losses": 11},
    },
    ("NCAAWB", "Stanford Cardinal"): {
        "2021-22": {"wins": 32, "losses": 3, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True},
        "2022-23": {"wins": 32, "losses": 4, "ncaa_qualifier": True, "seed_1": True, "won_round_of_64": True, "won_round_of_32": True, "won_sweet_16": True, "won_elite_8": True},
        "2023-24": {"wins": 30, "losses": 5, "ncaa_qualifier": True, "seed_2": True, "won_round_of_64": True, "won_round_of_32": True},
        "2024-25": {"wins": 25, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Wake Forest Demon Deacons"): {
        "2021-22": {"wins": 10, "losses": 18},
        "2022-23": {"wins": 15, "losses": 16},
        "2023-24": {"wins": 16, "losses": 14},
        "2024-25": {"wins": 18, "losses": 13},
    },
    ("NCAAWB", "George Mason Patriots"): {
        "2021-22": {"wins": 10, "losses": 18},
        "2022-23": {"wins": 14, "losses": 16},
        "2023-24": {"wins": 16, "losses": 14},
        "2024-25": {"wins": 18, "losses": 13},
    },
    ("NCAAWB", "Butler Bulldogs"): {
        "2021-22": {"wins": 11, "losses": 17},
        "2022-23": {"wins": 14, "losses": 16},
        "2023-24": {"wins": 15, "losses": 15},
        "2024-25": {"wins": 16, "losses": 15},
    },
    ("NCAAWB", "UC Santa Barbara Gauchos"): {
        "2021-22": {"wins": 24, "losses": 8, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
        "2022-23": {"wins": 20, "losses": 11},
        "2023-24": {"wins": 25, "losses": 8, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
        "2024-25": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
    },
    ("NCAAWB", "Miami (OH) RedHawks"): {
        "2021-22": {"wins": 15, "losses": 13},
        "2022-23": {"wins": 18, "losses": 12},
        "2023-24": {"wins": 20, "losses": 11},
        "2024-25": {"wins": 28, "losses": 7, "ncaa_qualifier": True, "conf_tourney_champ": True},
    },
    ("NCAAWB", "UIC Flames"): {
        "2021-22": {"wins": 16, "losses": 14},
        "2022-23": {"wins": 18, "losses": 12},
        "2023-24": {"wins": 20, "losses": 11},
        "2024-25": {"wins": 22, "losses": 10},
    },
    ("NCAAWB", "UNLV Rebels"): {
        "2021-22": {"wins": 14, "losses": 15},
        "2022-23": {"wins": 16, "losses": 14},
        "2023-24": {"wins": 18, "losses": 13},
        "2024-25": {"wins": 20, "losses": 12},
    },
    ("NCAAWB", "Oregon State Beavers"): {
        "2021-22": {"wins": 20, "losses": 11, "ncaa_qualifier": True, "won_round_of_64": True},
        "2022-23": {"wins": 16, "losses": 16},
        "2023-24": {"wins": 14, "losses": 17},
        "2024-25": {"wins": 15, "losses": 16},
    },
    ("NCAAWB", "Santa Clara Broncos"): {
        "2021-22": {"wins": 14, "losses": 14},
        "2022-23": {"wins": 16, "losses": 14},
        "2023-24": {"wins": 18, "losses": 13},
        "2024-25": {"wins": 20, "losses": 12},
    },
    ("NCAAWB", "Memphis Tigers"): {
        "2021-22": {"wins": 12, "losses": 17},
        "2022-23": {"wins": 15, "losses": 16},
        "2023-24": {"wins": 16, "losses": 15},
        "2024-25": {"wins": 17, "losses": 14},
    },
    ("NCAAWB", "North Texas Mean Green"): {
        "2021-22": {"wins": 22, "losses": 9, "ncaa_qualifier": True, "conf_tourney_champ": True, "won_round_of_64": True},
        "2022-23": {"wins": 18, "losses": 12},
        "2023-24": {"wins": 20, "losses": 11},
        "2024-25": {"wins": 24, "losses": 9, "ncaa_qualifier": True, "won_round_of_64": True},
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

    # --- NCAAMB (2026-27 season) --- the preseason AP poll doesn't come out
    # until October (season tips off Nov 1), so these are grounded in how
    # each team's actual 2025-26 season went (already live in
    # TeamSeasonResult) plus known offseason coaching/roster context,
    # rather than a concrete preseason ranking that doesn't exist yet.
    ("NCAAMB", "Duke Blue Devils"): (
        "Reached the Elite Eight in 2025-26 as a 1-seed; Jon Scheyer's program remains a "
        "preseason top-5 fixture entering 2026-27."
    ),
    ("NCAAMB", "Louisville Cardinals"): (
        "Missed the 2025-26 tournament; Pat Kelsey looks to build on the prior season's "
        "turnaround."
    ),
    ("NCAAMB", "Virginia Cavaliers"): (
        "Reached the Sweet 16 in 2025-26 as a 3-seed, a strong bounce-back under Ron "
        "Sanchez after the post-Bennett transition."
    ),
    ("NCAAMB", "Illinois Fighting Illini"): (
        "Reached the 2025-26 Final Four as a 3-seed; early buzz already has Brad "
        "Underwood's group projected near the top of preseason polls for 2026-27."
    ),
    ("NCAAMB", "Michigan State Spartans"): (
        "Reached the Sweet 16 in 2025-26; Tom Izzo's program remains a lock for another "
        "deep NCAA Tournament run."
    ),
    ("NCAAMB", "Arizona Wildcats"): (
        "Reached the 2025-26 Final Four as the overall 1-seed; Tommy Lloyd's Wildcats "
        "enter 2026-27 as a national title favorite."
    ),
    ("NCAAMB", "Houston Cougars"): (
        "Reached the Elite Eight in 2025-26 as a 2-seed; Kelvin Sampson's program remains a "
        "perennial title contender."
    ),
    ("NCAAMB", "Gonzaga Bulldogs"): (
        "Reached the Sweet 16 in 2025-26; Mark Few's Zags are a lock for another deep run "
        "in their now-established Pac-12 home."
    ),
    ("NCAAMB", "Florida Gators"): (
        "Lost in the Round of 32 in 2025-26 as a 1-seed, a step back after the 2025 title; "
        "Todd Golden looks to reload."
    ),
    ("NCAAMB", "UConn Huskies"): (
        "Runner-up in 2025-26 as a 2-seed; Dan Hurley's program remains in the sport's "
        "championship-contender tier."
    ),
    ("NCAAMB", "Michigan Wolverines"): (
        "National champions in 2025-26 as the 1-seed; the entire offseason storyline is "
        "the coaching change, with Mike Boynton inheriting the title roster after Dusty "
        "May's abrupt departure to coach the NBA's Dallas Mavericks."
    ),
    ("NCAAMB", "Nebraska Cornhuskers"): (
        "Reached the Sweet 16 in 2025-26 as a 4-seed, the program's best NCAA Tournament "
        "run in decades under Fred Hoiberg."
    ),
    ("NCAAMB", "Kansas Jayhawks"): (
        "Reached the Sweet 16 in 2025-26; Bill Self's Jayhawks remain a perennial Big 12 "
        "title contender."
    ),
    ("NCAAMB", "Texas Tech Red Raiders"): (
        "Lost in the Round of 32 in 2025-26 as a 5-seed; Grant McCasland's program looks to "
        "build on back-to-back tournament trips."
    ),
    ("NCAAMB", "Tennessee Volunteers"): (
        "Missed the 2025-26 tournament field used here; Rick Barnes' program looks to "
        "bounce back into the Sweet 16 mix."
    ),
    ("NCAAMB", "Texas Longhorns"): (
        "Reached the Sweet 16 in 2025-26 as an 11-seed; Rodney Terry's program looks to "
        "build on the surprise NCAA Tournament run."
    ),
    ("NCAAMB", "Miami (FL) Hurricanes"): (
        "Lost in the Round of 32 in 2025-26 as a 7-seed; Jim Larranaga's program looks to "
        "return to its 2023 Final Four form."
    ),
    ("NCAAMB", "St. John's Red Storm"): (
        "Reached the Sweet 16 in 2025-26 as a 5-seed; Rick Pitino's rebuild continues to "
        "gain steam in the Big East."
    ),
    ("NCAAMB", "Ohio State Buckeyes"): (
        "Lost in the Round of 64 in 2025-26; Jake Diebler's program looks to build real "
        "NCAA Tournament momentum."
    ),
    ("NCAAMB", "UCLA Bruins"): (
        "Lost in the Round of 32 in 2025-26 as a 7-seed; Mick Cronin's program looks to "
        "return to Sweet 16 form."
    ),
    ("NCAAMB", "Iowa State Cyclones"): (
        "Reached the Elite Eight in 2025-26 as a 2-seed; T.J. Otzelberger's program is a "
        "preseason top-15 fixture entering 2026-27."
    ),
    ("NCAAMB", "Alabama Crimson Tide"): (
        "Reached the Sweet 16 in 2025-26 as a 4-seed; Nate Oats' high-scoring program "
        "remains a national title contender."
    ),
    ("NCAAMB", "Arkansas Razorbacks"): (
        "Reached the Sweet 16 in 2025-26 as a 4-seed, including a stunning upset of "
        "top-seeded St. John's; John Calipari's program enters year three with real "
        "momentum."
    ),
    ("NCAAMB", "Kentucky Wildcats"): (
        "Lost in the Round of 32 in 2025-26 as a 7-seed; Mark Pope's program looks to build "
        "on a solid second season."
    ),
    ("NCAAMB", "Vanderbilt Commodores"): (
        "Lost in the Round of 32 in 2025-26 as a 5-seed, the program's best NCAA Tournament "
        "finish in years under Mark Byington."
    ),
    ("NCAAMB", "Marquette Golden Eagles"): (
        "Missed the 2025-26 tournament field used here; Shaka Smart's program looks to "
        "bounce back into the Big East's upper tier."
    ),
    ("NCAAMB", "Villanova Wildcats"): (
        "Lost in the Round of 64 in 2025-26 as an 8-seed; Kyle Neptune's rebuild continues."
    ),
    ("NCAAMB", "Indiana Hoosiers"): (
        "Missed the 2025-26 tournament; Darian DeVries enters his second season looking to "
        "restore the Hoosiers to the NCAA field."
    ),
    ("NCAAMB", "Oregon Ducks"): (
        "Missed the 2025-26 tournament; Dana Altman's program looks to bounce back in the "
        "Big Ten."
    ),
    ("NCAAMB", "Purdue Boilermakers"): (
        "Reached the Elite Eight in 2025-26 as a 2-seed; Matt Painter's program remains one "
        "of the sport's most consistent Big Ten contenders."
    ),
    ("NCAAMB", "USC Trojans"): (
        "Missed the 2025-26 tournament; Eric Musselman's rebuild continues in year three."
    ),
    ("NCAAMB", "Georgia Bulldogs"): (
        "Lost in the Round of 64 in 2025-26 as an 8-seed, a real step forward for Mike "
        "White's program."
    ),
    ("NCAAMB", "Clemson Tigers"): (
        "Lost in the Round of 64 in 2025-26 as an 8-seed; Brad Brownell's program looks to "
        "return to its 2024 Elite Eight form."
    ),
    ("NCAAMB", "NC State Wolfpack"): (
        "Missed the 2025-26 tournament; Kevin Keatts' program looks to bounce back after "
        "the historic 2024 Final Four run faded."
    ),
    ("NCAAMB", "Virginia Tech Hokies"): (
        "Missed the 2025-26 tournament; a rebuilding year continues for the Hokies."
    ),
    ("NCAAMB", "Creighton Bluejays"): (
        "Missed the 2025-26 tournament field used here; the Bluejays enter the Alan Huss "
        "era after Greg McDermott's retirement."
    ),
    ("NCAAMB", "Maryland Terrapins"): (
        "Missed the 2025-26 tournament; Kevin Willard's program looks to bounce back after "
        "last year's tournament trip."
    ),
    ("NCAAMB", "BYU Cougars"): (
        "Lost in the Round of 64 in 2025-26 as a 6-seed; Kevin Young's transfer-heavy "
        "approach continues in year three."
    ),
    ("NCAAMB", "Cincinnati Bearcats"): (
        "Missed the 2025-26 tournament; Wes Miller's rebuild continues in the Big 12."
    ),
    ("NCAAMB", "Auburn Tigers"): (
        "Missed the 2025-26 tournament field used here; Bruce Pearl's program looks to "
        "bounce back after last year's Final Four run."
    ),
    ("NCAAMB", "Missouri Tigers"): (
        "Lost in the Round of 64 in 2025-26 as a 10-seed; Dennis Gates' program looks to "
        "build on its NCAA Tournament return."
    ),
    ("NCAAMB", "Oklahoma Sooners"): (
        "Missed the 2025-26 tournament field used here; Porter Moser's program looks to "
        "build on a solid SEC debut."
    ),
    ("NCAAMB", "North Carolina Tar Heels"): (
        "Lost in the Round of 64 in 2025-26 as a 6-seed; Michael Malone's 2026 hire brings "
        "an entirely new era to Chapel Hill."
    ),
    ("NCAAMB", "SMU Mustangs"): (
        "Missed the 2025-26 tournament; Andy Enfield's rebuild continues in the ACC."
    ),
    ("NCAAMB", "Iowa Hawkeyes"): (
        "Reached the Sweet 16 in 2025-26 as a 9-seed; Fran McCaffery's program looks to "
        "build on the surprise run."
    ),
    ("NCAAMB", "Wisconsin Badgers"): (
        "Lost in the Round of 64 in 2025-26 as a 5-seed; Greg Gard's program looks to "
        "return to form."
    ),
    ("NCAAMB", "Baylor Bears"): (
        "Missed the 2025-26 tournament field used here; Scott Drew's program looks to "
        "bounce back in the Big 12."
    ),
    ("NCAAMB", "TCU Horned Frogs"): (
        "Lost in the Round of 32 in 2025-26 as a 9-seed; Jamie Dixon's program looks to "
        "build on the tournament return."
    ),
    ("NCAAMB", "UCF Knights"): (
        "Lost in the Round of 64 in 2025-26 as a 10-seed, the program's first tournament "
        "trip in the Big 12 under Johnny Dawkins."
    ),
    ("NCAAMB", "LSU Tigers"): (
        "Missed the 2025-26 tournament; Will Wade's 2026 return brings new energy to Baton "
        "Rouge."
    ),

    # --- NCAAWB (2026-27 season) --- same grounding as NCAAMB above: the
    # 2025-26 season already happened and is live in TeamSeasonResult, but
    # no concrete 2026-27 preseason poll exists yet this far out.
    ("NCAAWB", "UCLA Bruins"): (
        "National champions in 2025-26 (the program's first-ever title) as the 1-seed; "
        "Cori Close's program is the clear favorite to repeat entering 2026-27."
    ),
    ("NCAAWB", "UConn Huskies"): (
        "Reached the 2025-26 Final Four as the overall 1-seed; Geno Auriemma's program "
        "remains the sport's gold standard."
    ),
    ("NCAAWB", "South Carolina Gamecocks"): (
        "Runner-up in 2025-26 as a 1-seed; Dawn Staley's program remains a perennial title "
        "contender."
    ),
    ("NCAAWB", "LSU Tigers"): (
        "Reached the Sweet 16 in 2025-26 as a 2-seed; Kim Mulkey's program looks to return "
        "to Final Four form."
    ),
    ("NCAAWB", "Texas Longhorns"): (
        "Reached the 2025-26 Final Four as a 1-seed; Vic Schaefer's program is a clear "
        "national title contender entering 2026-27."
    ),
    ("NCAAWB", "Duke Blue Devils"): (
        "Reached the Elite Eight in 2025-26 as a 3-seed; Kara Lawson's program continues "
        "its ascent."
    ),
    ("NCAAWB", "Michigan Wolverines"): (
        "Reached the Elite Eight in 2025-26 as a 2-seed, the program's best NCAA "
        "Tournament finish in years."
    ),
    ("NCAAWB", "TCU Horned Frogs"): (
        "Reached the Elite Eight in 2025-26 as a 3-seed, a breakthrough season for the "
        "Horned Frogs."
    ),
    ("NCAAWB", "Oklahoma Sooners"): (
        "Reached the Sweet 16 in 2025-26 as a 4-seed; Jennie Baranczyk's rebuild continues "
        "to gain steam."
    ),
    ("NCAAWB", "Vanderbilt Commodores"): (
        "Reached the Sweet 16 in 2025-26 as a 2-seed, the program's best NCAA Tournament "
        "finish in years under Shea Ralph."
    ),
    ("NCAAWB", "Louisville Cardinals"): (
        "Reached the Sweet 16 in 2025-26 as a 3-seed; Jeff Walz's program remains an ACC "
        "contender."
    ),
    ("NCAAWB", "North Carolina Tar Heels"): (
        "Reached the Sweet 16 in 2025-26 as a 4-seed; Courtney Banghart's rebuild continues "
        "to gain steam."
    ),
    ("NCAAWB", "Notre Dame Fighting Irish"): (
        "Reached the Elite Eight in 2025-26 as a 6-seed; Niele Ivey's program looks to "
        "build on the deep run."
    ),
    ("NCAAWB", "Iowa Hawkeyes"): (
        "Lost in the Round of 32 in 2025-26 as a 2-seed in the first full post-Caitlin "
        "Clark season under Jan Jensen."
    ),
    ("NCAAWB", "West Virginia Mountaineers"): (
        "Lost in the Round of 32 in 2025-26 as a 4-seed, a strong bounce-back season."
    ),
    ("NCAAWB", "Kentucky Wildcats"): (
        "Reached the Sweet 16 in 2025-26 as a 5-seed in Kenny Brooks' second season."
    ),
    ("NCAAWB", "Maryland Terrapins"): (
        "Lost in the Round of 32 in 2025-26 as a 5-seed; Brenda Frese's program remains a "
        "Big Ten contender."
    ),
    ("NCAAWB", "Michigan State Spartans"): (
        "Lost in the Round of 32 in 2025-26 as a 5-seed, a real step forward for Robyn "
        "Fralick's program."
    ),
    ("NCAAWB", "Minnesota Golden Gophers"): (
        "Reached the Sweet 16 in 2025-26 as a 4-seed, a breakthrough season for Dawn "
        "Plitzuweit's program."
    ),
    ("NCAAWB", "Ohio State Buckeyes"): (
        "Lost in the Round of 32 in 2025-26 as a 3-seed; Kevin McGuff's program remains a "
        "Big Ten contender."
    ),
    ("NCAAWB", "Mississippi State Bulldogs"): (
        "Missed the 2025-26 tournament field used here; Sam Purcell's program looks to "
        "bounce back."
    ),
    ("NCAAWB", "Virginia Cavaliers"): (
        "Reached the Sweet 16 in 2025-26 as a 10-seed, a real breakthrough for the "
        "Cavaliers."
    ),
    ("NCAAWB", "Washington Huskies"): (
        "Lost in the Round of 32 in 2025-26 as a 6-seed; Tina Langley's rebuild continues "
        "to gain steam."
    ),
    ("NCAAWB", "Columbia Lions"): (
        "Missed the 2025-26 tournament field used here; Megan Griffith's program looks to "
        "return to the NCAA field."
    ),
    ("NCAAWB", "Alabama Crimson Tide"): (
        "Lost in the Round of 32 in 2025-26 as a 6-seed; the program enters a new coaching "
        "era for 2026-27."
    ),
    ("NCAAWB", "NC State Wolfpack"): (
        "Lost in the Round of 32 in 2025-26 as a 7-seed; Wes Moore's program remains a "
        "steady ACC contender."
    ),
    ("NCAAWB", "Virginia Tech Hokies"): (
        "Lost in the Round of 64 in 2025-26 as a 9-seed; Megan Duffy's rebuild continues."
    ),
    ("NCAAWB", "Villanova Wildcats"): (
        "Lost in the Round of 64 in 2025-26 as a 10-seed; the Wildcats look to bounce back "
        "in the Big East."
    ),
    ("NCAAWB", "Illinois Fighting Illini"): (
        "Lost in the Round of 32 in 2025-26 as a 7-seed; Shauna Green's program continues "
        "to build momentum."
    ),
    ("NCAAWB", "Nebraska Cornhuskers"): (
        "Lost in the Round of 64 in 2025-26 as an 11-seed; Amy Williams' program looks to "
        "build on the tournament trip."
    ),
    ("NCAAWB", "Oregon Ducks"): (
        "Lost in the Round of 32 in 2025-26 as an 8-seed, a step forward for the Ducks."
    ),
    ("NCAAWB", "USC Trojans"): (
        "Lost in the Round of 32 in 2025-26 as a 9-seed, a step back after 2024-25's Elite "
        "Eight; a fully healthy JuJu Watkins would change the outlook entirely."
    ),
    ("NCAAWB", "Houston Cougars"): (
        "Missed the 2025-26 tournament field used here; the rebuild continues under Ronald "
        "Hughey."
    ),
    ("NCAAWB", "Fairfield Stags"): (
        "Lost in the Round of 64 in 2025-26 as an 11-seed after a three-peat MAAC "
        "championship; Carly Thibault-DuDonis' program looks for a fourth straight title."
    ),
    ("NCAAWB", "Gonzaga Bulldogs"): (
        "Lost in the Round of 64 in 2025-26 as a 12-seed; Lisa Fortier's program looks to "
        "bounce back."
    ),
    ("NCAAWB", "Miami (FL) Hurricanes"): (
        "Missed the 2025-26 tournament field used here, continuing a post-Katie Meier "
        "decline."
    ),
    ("NCAAWB", "St. John's Red Storm"): (
        "Missed the 2025-26 tournament field used here; Joe Tartamella's program looks to "
        "build on last year's tournament trip."
    ),
    ("NCAAWB", "Kansas Jayhawks"): (
        "Missed the 2025-26 tournament field used here; a rebuild continues under Brandon "
        "Schneider."
    ),
    ("NCAAWB", "Texas Tech Red Raiders"): (
        "Lost in the Round of 32 in 2025-26 as a 7-seed, a real step forward for the "
        "program."
    ),
    ("NCAAWB", "Ohio Bobcats"): (
        "Missed the 2025-26 tournament field used here, continuing a steep recent "
        "decline."
    ),
    ("NCAAWB", "Marquette Golden Eagles"): (
        "Missed the 2025-26 tournament field used here after four straight tournament "
        "trips."
    ),
    ("NCAAWB", "Indiana Hoosiers"): (
        "Missed the 2025-26 tournament field used here; Teri Moren's program looks to "
        "bounce back."
    ),
    ("NCAAWB", "Purdue Boilermakers"): (
        "Missed the 2025-26 tournament field used here; the Boilermakers look to return to "
        "the NCAA field."
    ),
    ("NCAAWB", "Iowa State Cyclones"): (
        "Lost in the Round of 64 in 2025-26 as an 8-seed; Bill Fennelly's program remains a "
        "Big 12 regular."
    ),
    ("NCAAWB", "Arkansas Razorbacks"): (
        "Missed the 2025-26 tournament field used here; Mike Neighbors' program looks to "
        "bounce back."
    ),
    ("NCAAWB", "Clemson Tigers"): (
        "Lost in the Round of 64 in 2025-26 as an 8-seed, a step forward for the program."
    ),
    ("NCAAWB", "Creighton Bluejays"): (
        "Missed the 2025-26 tournament field used here; Jim Flanery's program looks to "
        "return to the NCAA field."
    ),
    ("NCAAWB", "BYU Cougars"): (
        "Missed the 2025-26 tournament field used here; a rising Big 12 program looks to "
        "return to the field."
    ),
    ("NCAAWB", "Auburn Tigers"): (
        "Missed the 2025-26 tournament field used here; Johnnie Harris' rebuild continues."
    ),
    ("NCAAWB", "SMU Mustangs"): (
        "Missed the 2025-26 tournament field used here in its second ACC season."
    ),

    # --- NCAAF, second 50 (2026 season) --- grounded in the actual 2025
    # record (already live in TeamSeasonResult) plus known 2026 coaching
    # changes.
    ("NCAAF", "Colorado Buffaloes"): (
        "Went 3-9 in 2025, a rough Year 3 under Deion Sanders; the Buffaloes look to "
        "rebound in 2026."
    ),
    ("NCAAF", "Boise State Broncos"): (
        "Went 9-5 in 2025, a step back after the 2024 CFP run; still considered the "
        "rebuilt Pac-12's flagship program."
    ),
    ("NCAAF", "Wake Forest Demon Deacons"): (
        "Went 9-4 in 2025 under new coach Jake Dickert (hired from Washington State), a "
        "bounce-back after consecutive losing seasons."
    ),
    ("NCAAF", "Kansas Jayhawks"): (
        "Went 5-7 in 2025; Lance Leipold's program looks to return to bowl form."
    ),
    ("NCAAF", "Oklahoma State Cowboys"): (
        "Went 1-11 in 2025, the program's worst season in decades; ESPN's SP+ projects a "
        "22-point rebound in 2026 under new coach Eric Morris."
    ),
    ("NCAAF", "UCF Knights"): (
        "Went 5-7 in 2025 in Scott Frost's return season; the Knights look to build in "
        "year two."
    ),
    ("NCAAF", "Tulane Green Wave"): (
        "Went 11-3 in 2025, one of the American's top programs; enters 2026 under a new "
        "coach after Jon Sumrall's departure for Florida."
    ),
    ("NCAAF", "Maryland Terrapins"): (
        "Went 4-8 in 2025; Mike Locksley's program looks to rebound in the Big Ten."
    ),
    ("NCAAF", "Northwestern Wildcats"): (
        "Went 7-6 in 2025, a solid season for David Braun's program."
    ),
    ("NCAAF", "California Golden Bears"): (
        "Went 7-6 in 2025; Justin Wilcox's program looks to build on a bowl trip."
    ),
    ("NCAAF", "San Diego State Aztecs"): (
        "Went 9-4 in 2025, one of the rebuilt Pac-12's strongest seasons."
    ),
    ("NCAAF", "UNLV Rebels"): (
        "Went 10-4 in 2025, sustaining the program's best stretch in decades under new "
        "leadership."
    ),
    ("NCAAF", "Michigan State Spartans"): (
        "Went 4-8 in 2025; Jonathan Smith's rebuild continues in year three."
    ),
    ("NCAAF", "Minnesota Golden Gophers"): (
        "Went 8-5 in 2025; P.J. Fleck's program remains a consistent bowl team."
    ),
    ("NCAAF", "Rutgers Scarlet Knights"): (
        "Went 5-7 in 2025; Greg Schiano's program looks to return to bowl form."
    ),
    ("NCAAF", "UCLA Bruins"): (
        "Went 3-9 in 2025; the Bruins look to rebuild in their third Big Ten season."
    ),
    ("NCAAF", "West Virginia Mountaineers"): (
        "Went 4-8 in 2025; Rich Rodriguez's second stint as coach looks to build momentum."
    ),
    ("NCAAF", "East Carolina Pirates"): (
        "Went 9-4 in 2025, a strong season for a program that's now a consistent AAC bowl "
        "team."
    ),
    ("NCAAF", "Navy Midshipmen"): (
        "Went 11-2 in 2025, sustaining the program's best stretch in years under Brian "
        "Newberry."
    ),
    ("NCAAF", "Purdue Boilermakers"): (
        "Went 2-10 in 2025; the Boilermakers look to rebuild under new leadership."
    ),
    ("NCAAF", "Syracuse Orange"): (
        "Went 3-9 in 2025, a sharp step back after 2024's breakthrough; Fran Brown's "
        "program looks to regroup."
    ),
    ("NCAAF", "Iowa State Cyclones"): (
        "Went 8-4 in 2025; the Cyclones enter a new era under Matt Campbell's successor "
        "after his departure for Penn State."
    ),
    ("NCAAF", "Memphis Tigers"): (
        "Went 8-5 in 2025; the Tigers enter 2026 under a new coach after Ryan Silverfield's "
        "departure for Arkansas."
    ),
    ("NCAAF", "South Florida Bulls"): (
        "Went 9-4 in 2025; the Bulls enter 2026 under a new coach after Alex Golesh's "
        "departure for Auburn."
    ),
    ("NCAAF", "James Madison Dukes"): (
        "Went 12-2 in 2025, Bob Chesney's best season yet, continuing the program's rapid "
        "rise since jumping to FBS."
    ),
    ("NCAAF", "Boston College Eagles"): (
        "Went 2-10 in 2025, a rough Year 2 under Bill O'Brien after a promising debut."
    ),
    ("NCAAF", "Stanford Cardinal"): (
        "Went 4-8 in 2025, a modest step forward in a rebuild still finding its footing in "
        "the ACC."
    ),
    ("NCAAF", "Fresno State Bulldogs"): (
        "Went 9-4 in 2025, a solid season in the rebuilt Pac-12."
    ),
    ("NCAAF", "Hawaii Rainbow Warriors"): (
        "Went 9-4 in 2025, one of the program's best seasons in years."
    ),
    ("NCAAF", "New Mexico Lobos"): (
        "Went 9-4 in 2025, sustaining Bronco Mendenhall's turnaround."
    ),
    ("NCAAF", "Toledo Rockets"): (
        "Went 8-5 in 2025; Jason Candle's program remains a steady MAC contender."
    ),
    ("NCAAF", "Texas State Bobcats"): (
        "Went 7-6 in 2025, continuing the program's rise under G.J. Kinne."
    ),
    ("NCAAF", "Washington State Cougars"): (
        "Went 7-6 in 2025, helping anchor the rebuilt Pac-12 after surviving the "
        "conference's 2023-24 collapse."
    ),
    ("NCAAF", "Old Dominion Monarchs"): (
        "Went 10-3 in 2025, the program's best season since joining FBS."
    ),
    ("NCAAF", "Western Michigan Broncos"): (
        "Went 10-4 in 2025, a strong bounce-back season in the MAC."
    ),
    ("NCAAF", "Western Kentucky Hilltoppers"): (
        "Went 9-4 in 2025, a solid season for a consistently competitive Conference USA "
        "program."
    ),
    ("NCAAF", "Army Black Knights"): (
        "Went 7-6 in 2025, a step back after the program's best season in decades in 2024."
    ),
    ("NCAAF", "North Texas Mean Green"): (
        "Went 12-2 in 2025, one of the American's best seasons."
    ),
    ("NCAAF", "UTSA Roadrunners"): (
        "Went 7-6 in 2025; Jeff Traylor's program looks to rebuild momentum in the AAC."
    ),
    ("NCAAF", "Southern Miss Golden Eagles"): (
        "Went 7-6 in 2025, a bounce-back season for the Golden Eagles."
    ),
    ("NCAAF", "Delaware Blue Hens"): (
        "Went 7-6 in 2025, a respectable first season at the FBS level."
    ),
    ("NCAAF", "Oregon State Beavers"): (
        "Went 2-10 in 2025, a difficult season helping anchor the rebuilt Pac-12 after "
        "surviving the conference's 2023-24 collapse."
    ),
    ("NCAAF", "Utah State Aggies"): (
        "Went 6-7 in 2025, a modest season in the rebuilt Pac-12."
    ),
    ("NCAAF", "Air Force Falcons"): (
        "Went 4-8 in 2025, a down year for a normally steady service-academy program."
    ),
    ("NCAAF", "North Dakota State Bison"): (
        "The dominant FCS program of the last 15 years makes its first-ever FBS season in "
        "2026, moving up to the Mountain West."
    ),
    ("NCAAF", "Louisiana Ragin' Cajuns"): (
        "Went 6-7 in 2025; Michael Desormeaux's program looks to return to Sun Belt "
        "contention."
    ),
    ("NCAAF", "Troy Trojans"): (
        "Went 8-6 in 2025, a solid season for a consistently competitive Sun Belt program."
    ),
    ("NCAAF", "Miami (OH) RedHawks"): (
        "Went 7-7 in 2025, a middling season in the MAC."
    ),
    ("NCAAF", "Ohio Bobcats"): (
        "Went 9-4 in 2025, another steady season under Tim Albin."
    ),
    ("NCAAF", "Liberty Flames"): (
        "Went 4-8 in 2025, a rough season in the program's third year in Conference USA."
    ),

    # --- NCAAMB, second 50 (2026-27 season) --- same grounding as the
    # first 50 above (2025-26's actual result, no concrete preseason poll
    # exists yet this far out).
    ("NCAAMB", "Texas A&M Aggies"): (
        "Lost in the Round of 32 in 2025-26 as a 10-seed; the program enters 2026-27 under "
        "a new coach."
    ),
    ("NCAAMB", "Syracuse Orange"): (
        "Missed the 2025-26 tournament; Adrian Autry's rebuild continues."
    ),
    ("NCAAMB", "VCU Rams"): (
        "Lost in the Round of 32 in 2025-26 as an 11-seed after winning the Atlantic 10 "
        "tournament, continuing the program's mid-major-power tradition."
    ),
    ("NCAAMB", "Providence Friars"): (
        "Missed the 2025-26 tournament; Kim English's program looks to rebound in the Big "
        "East."
    ),
    ("NCAAMB", "Xavier Musketeers"): (
        "Missed the 2025-26 tournament; Sean Miller's program looks to rebound in the Big "
        "East."
    ),
    ("NCAAMB", "Oklahoma State Cowboys"): (
        "Missed the 2025-26 tournament; the program looks to build toward NCAA "
        "eligibility."
    ),
    ("NCAAMB", "West Virginia Mountaineers"): (
        "Missed the 2025-26 tournament; Ross Hodge inherits the program after Darian "
        "DeVries' departure for Indiana."
    ),
    ("NCAAMB", "Grand Canyon Antelopes"): (
        "Lost in the Round of 64 in 2025-26; Bryce Drew's program remains a consistent "
        "mid-major power."
    ),
    ("NCAAMB", "San Diego State Aztecs"): (
        "Missed the 2025-26 tournament; Brian Dutcher's program looks to return to form."
    ),
    ("NCAAMB", "Wichita State Shockers"): (
        "Missed the 2025-26 tournament; the program looks to rebound in the American."
    ),
    ("NCAAMB", "Florida State Seminoles"): (
        "Missed the 2025-26 tournament; the program continues to look for consistency."
    ),
    ("NCAAMB", "Saint Louis Billikens"): (
        "Lost in the Round of 32 in 2025-26 as a 9-seed, a real breakthrough season."
    ),
    ("NCAAMB", "DePaul Blue Demons"): (
        "Missed the 2025-26 tournament; the program continues a long rebuild."
    ),
    ("NCAAMB", "High Point Panthers"): (
        "Reached the Elite Eight in 2025-26 as a stunning 12-seed, the deepest run of any "
        "team seeded that low in tournament history."
    ),
    ("NCAAMB", "Washington Huskies"): (
        "Missed the 2025-26 tournament; the program looks to build in the Big Ten."
    ),
    ("NCAAMB", "Arizona State Sun Devils"): (
        "Missed the 2025-26 tournament; Bobby Hurley's program looks to return to the "
        "field."
    ),
    ("NCAAMB", "New Mexico Lobos"): (
        "Missed the 2025-26 tournament; Richard Pitino's program remains a Mountain West "
        "contender."
    ),
    ("NCAAMB", "Utah State Aggies"): (
        "Lost in the Round of 32 in 2025-26 as a 9-seed, continuing a strong recent run."
    ),
    ("NCAAMB", "Saint Mary's Gaels"): (
        "Lost in the Round of 64 in 2025-26 as a 7-seed; Randy Bennett's program remains a "
        "WCC mainstay in Gonzaga's shadow."
    ),
    ("NCAAMB", "Pittsburgh Panthers"): (
        "Missed the 2025-26 tournament; Jeff Capel's program looks to return to the field."
    ),
    ("NCAAMB", "Dayton Flyers"): (
        "Missed the 2025-26 tournament; Anthony Grant's program looks to bounce back."
    ),
    ("NCAAMB", "Seton Hall Pirates"): (
        "Missed the 2025-26 tournament; Shaheen Holloway's program looks to bounce back."
    ),
    ("NCAAMB", "Northwestern Wildcats"): (
        "Missed the 2025-26 tournament; Chris Collins' program looks to return to the "
        "field."
    ),
    ("NCAAMB", "Rutgers Scarlet Knights"): (
        "Missed the 2025-26 tournament; Steve Pikiell's program looks to bounce back."
    ),
    ("NCAAMB", "Utah Utes"): (
        "Missed the 2025-26 tournament; the program continues a rebuild in the Big 12."
    ),
    ("NCAAMB", "Mississippi State Bulldogs"): (
        "Lost in the Round of 64 in 2025-26; Chris Jans' program remains a tournament "
        "regular."
    ),
    ("NCAAMB", "South Carolina Gamecocks"): (
        "Missed the 2025-26 tournament; the men's program looks to build in the SEC."
    ),
    ("NCAAMB", "Tulsa Golden Hurricane"): (
        "Missed the 2025-26 tournament; the program looks to build in the American."
    ),
    ("NCAAMB", "California Golden Bears"): (
        "Missed the 2025-26 tournament; the program continues to rebuild in the ACC."
    ),
    ("NCAAMB", "Notre Dame Fighting Irish"): (
        "Missed the 2025-26 tournament; Micah Shrewsberry's rebuild continues."
    ),
    ("NCAAMB", "George Washington Revolutionaries"): (
        "Missed the 2025-26 tournament; the program looks to build in the Atlantic 10."
    ),
    ("NCAAMB", "Georgetown Hoyas"): (
        "Missed the 2025-26 tournament; Ed Cooley's rebuild continues."
    ),
    ("NCAAMB", "Minnesota Golden Gophers"): (
        "Missed the 2025-26 tournament; Niko Medved's first season looks to build "
        "momentum."
    ),
    ("NCAAMB", "Colorado Buffaloes"): (
        "Lost in the First Four in 2025-26; the program looks to return to the main field."
    ),
    ("NCAAMB", "Kansas State Wildcats"): (
        "Missed the 2025-26 tournament; Jerome Tang's program looks to recapture its 2023 "
        "Elite Eight form."
    ),
    ("NCAAMB", "Nevada Wolf Pack"): (
        "Lost in the Round of 64 in 2025-26; the program remains a consistent Mountain "
        "West contender."
    ),
    ("NCAAMB", "Boise State Broncos"): (
        "Missed the 2025-26 tournament; the program looks to return to the field."
    ),
    ("NCAAMB", "Colorado State Rams"): (
        "Lost in the Round of 64 in 2025-26, continuing a run of consistent tournament "
        "appearances."
    ),
    ("NCAAMB", "McNeese State Cowboys"): (
        "Lost in the Round of 64 in 2025-26 after winning the Southland tournament; the "
        "program enters a new era after Will Wade's departure for LSU."
    ),
    ("NCAAMB", "Charlotte 49ers"): (
        "Missed the 2025-26 tournament; the program looks to build in the American."
    ),
    ("NCAAMB", "South Florida Bulls"): (
        "Reached the Round of 64 in 2025-26 after winning the American tournament, a real "
        "breakthrough season."
    ),
    ("NCAAMB", "Wake Forest Demon Deacons"): (
        "Lost in the Round of 64 in 2025-26, a bounce-back season in the ACC."
    ),
    ("NCAAMB", "George Mason Patriots"): (
        "Missed the 2025-26 tournament; the program looks to build in the Atlantic 10."
    ),
    ("NCAAMB", "Butler Bulldogs"): (
        "Missed the 2025-26 tournament; the program looks to rebound in the Big East."
    ),
    ("NCAAMB", "UNLV Rebels"): (
        "Missed the 2025-26 tournament; the program looks to build in the Mountain West."
    ),
    ("NCAAMB", "Oregon State Beavers"): (
        "Missed the 2025-26 tournament; the program continues rebuilding in the "
        "reconstituted Pac-12."
    ),
    ("NCAAMB", "Santa Clara Broncos"): (
        "Lost in the Round of 64 in 2025-26, a real breakthrough season for the Broncos."
    ),
    ("NCAAMB", "Memphis Tigers"): (
        "Missed the 2025-26 tournament; Penny Hardaway's program looks to return to the "
        "field."
    ),
    ("NCAAMB", "Boston College Eagles"): (
        "Missed the 2025-26 tournament; the program continues to rebuild in the ACC."
    ),
    ("NCAAMB", "Georgia Tech Yellow Jackets"): (
        "Missed the 2025-26 tournament; Damon Stoudamire's rebuild continues."
    ),

    # --- NCAAWB, second 50 (2026-27 season) --- same grounding as above.
    ("NCAAWB", "Wisconsin Badgers"): (
        "Missed the 2025-26 tournament; the program looks to build in the Big Ten."
    ),
    ("NCAAWB", "Baylor Bears"): (
        "Lost in the Round of 32 in 2025-26 as a 6-seed; Nicki Collen's program remains a "
        "Big 12 contender."
    ),
    ("NCAAWB", "Cincinnati Bearcats"): (
        "Missed the 2025-26 tournament; the program continues to build in the Big 12."
    ),
    ("NCAAWB", "UCF Knights"): (
        "Lost in the Round of 64 in 2025-26, a step forward for the program."
    ),
    ("NCAAWB", "Texas A&M Aggies"): (
        "Missed the 2025-26 tournament field used here; the program looks to bounce back "
        "in the SEC."
    ),
    ("NCAAWB", "Syracuse Orange"): (
        "Lost in the Round of 32 in 2025-26 as a 9-seed, a real breakthrough season."
    ),
    ("NCAAWB", "VCU Rams"): (
        "Lost in the Round of 32 in 2025-26 as an 11-seed after winning the Atlantic 10 "
        "tournament, continuing the program's rise."
    ),
    ("NCAAWB", "Providence Friars"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "Big East."
    ),
    ("NCAAWB", "Xavier Musketeers"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "Big East."
    ),
    ("NCAAWB", "Oklahoma State Cowboys"): (
        "Lost in the Round of 32 in 2025-26 as an 8-seed, a real breakthrough season."
    ),
    ("NCAAWB", "Grand Canyon Antelopes"): (
        "Lost in the Round of 64 in 2025-26, continuing the program's rise."
    ),
    ("NCAAWB", "San Diego State Aztecs"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "Pac-12."
    ),
    ("NCAAWB", "Wichita State Shockers"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "American."
    ),
    ("NCAAWB", "Saint Louis Billikens"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "Atlantic 10."
    ),
    ("NCAAWB", "DePaul Blue Demons"): (
        "Missed the 2025-26 tournament field used here; the program continues to rebuild."
    ),
    ("NCAAWB", "High Point Panthers"): (
        "Lost in the Round of 64 in 2025-26 as a 15-seed after winning the Big South "
        "tournament, a breakthrough season."
    ),
    ("NCAAWB", "Arizona State Sun Devils"): (
        "Lost in the Round of 64 in 2025-26 as a 10-seed; the program looks to build "
        "momentum after Charli Turner Thorne's 2024 retirement."
    ),
    ("NCAAWB", "Utah State Aggies"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "Pac-12."
    ),
    ("NCAAWB", "Saint Mary's Gaels"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "WCC."
    ),
    ("NCAAWB", "Tulsa Golden Hurricane"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "American."
    ),
    ("NCAAWB", "Florida State Seminoles"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "ACC."
    ),
    ("NCAAWB", "Pittsburgh Panthers"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "ACC."
    ),
    ("NCAAWB", "Dayton Flyers"): (
        "Lost in the Round of 64 in 2025-26, continuing the program's consistent mid-major "
        "run."
    ),
    ("NCAAWB", "Seton Hall Pirates"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "Big East."
    ),
    ("NCAAWB", "Northwestern Wildcats"): (
        "Lost in the Round of 64 in 2025-26, continuing Joe McKeown's run of tournament "
        "appearances."
    ),
    ("NCAAWB", "Rutgers Scarlet Knights"): (
        "Missed the 2025-26 tournament field used here; the program looks to return to the "
        "field."
    ),
    ("NCAAWB", "California Golden Bears"): (
        "Missed the 2025-26 tournament field used here; the program continues to rebuild "
        "in the ACC."
    ),
    ("NCAAWB", "George Washington Revolutionaries"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "Atlantic 10."
    ),
    ("NCAAWB", "Georgetown Hoyas"): (
        "Missed the 2025-26 tournament field used here; the program continues to rebuild."
    ),
    ("NCAAWB", "Kansas State Wildcats"): (
        "Missed the 2025-26 tournament field used here; the program looks to return to the "
        "field."
    ),
    ("NCAAWB", "Iona Gaels"): (
        "Missed the 2025-26 tournament field used here; the program looks to reclaim its "
        "MAAC contender status."
    ),
    ("NCAAWB", "Buffalo Bulls"): (
        "Lost in the Round of 64 in 2025-26 as an MAC tournament champion, continuing a "
        "run of four straight tournament trips."
    ),
    ("NCAAWB", "Nevada Wolf Pack"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "Mountain West."
    ),
    ("NCAAWB", "Boise State Broncos"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "Pac-12."
    ),
    ("NCAAWB", "Colorado State Rams"): (
        "Lost in the Round of 64 in 2025-26, continuing a run of consistent tournament "
        "appearances."
    ),
    ("NCAAWB", "McNeese State Cowboys"): (
        "Lost in the Round of 64 in 2025-26 after winning the Southland tournament, "
        "continuing the program's rise."
    ),
    ("NCAAWB", "Charlotte 49ers"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "American."
    ),
    ("NCAAWB", "South Florida Bulls"): (
        "Missed the 2025-26 tournament field used here; Jose Fernandez's program looks to "
        "return to the field."
    ),
    ("NCAAWB", "Stanford Cardinal"): (
        "Missed the 2025-26 tournament field used here; Kate Paye's second season looks to "
        "rebuild after Tara VanDerveer's 2024 retirement."
    ),
    ("NCAAWB", "Wake Forest Demon Deacons"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "ACC."
    ),
    ("NCAAWB", "George Mason Patriots"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "Atlantic 10."
    ),
    ("NCAAWB", "Butler Bulldogs"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "Big East."
    ),
    ("NCAAWB", "UC Santa Barbara Gauchos"): (
        "Lost in the Round of 64 in 2025-26 after winning the Big West tournament, "
        "continuing the program's mid-major run."
    ),
    ("NCAAWB", "Miami (OH) RedHawks"): (
        "Lost in the Round of 64 in 2025-26 as a 13-seed after winning the MAC tournament, "
        "a breakthrough season."
    ),
    ("NCAAWB", "UIC Flames"): (
        "Missed the 2025-26 tournament field used here; the program looks to build "
        "momentum."
    ),
    ("NCAAWB", "UNLV Rebels"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "Mountain West."
    ),
    ("NCAAWB", "Oregon State Beavers"): (
        "Missed the 2025-26 tournament field used here; the program looks to rebuild in "
        "the reconstituted Pac-12."
    ),
    ("NCAAWB", "Santa Clara Broncos"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "WCC."
    ),
    ("NCAAWB", "Memphis Tigers"): (
        "Missed the 2025-26 tournament field used here; the program looks to build in the "
        "American."
    ),
    ("NCAAWB", "North Texas Mean Green"): (
        "Lost in the Round of 64 in 2025-26, continuing the program's rise in the "
        "American."
    ),
}
