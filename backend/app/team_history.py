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
}
