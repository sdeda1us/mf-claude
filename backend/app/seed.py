"""Seeds the 6 allow-listed league members and the real league/team data.

Run with: python -m app.seed
Configure real emails via ALLOWED_EMAILS in .env before running, e.g.:
  ALLOWED_EMAILS=alice@example.com,bob@example.com,carol@example.com,dave@example.com,erin@example.com,frank@example.com

The first allow-listed email becomes the commissioner by default.

Team rosters below mirror the "Sports Leagues" reference in the repo's
CLAUDE.md — update both together when a season's rosters change (e.g.
Premier League promotion/relegation each May).
"""

from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models import Team, TeamSeasonResult, User

MLB_TEAMS = [
    "Baltimore Orioles", "Boston Red Sox", "New York Yankees", "Tampa Bay Rays", "Toronto Blue Jays",
    "Chicago White Sox", "Cleveland Guardians", "Detroit Tigers", "Kansas City Royals", "Minnesota Twins",
    "Athletics", "Houston Astros", "Los Angeles Angels", "Seattle Mariners", "Texas Rangers",
    "Atlanta Braves", "Miami Marlins", "New York Mets", "Philadelphia Phillies", "Washington Nationals",
    "Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", "Pittsburgh Pirates", "St. Louis Cardinals",
    "Arizona Diamondbacks", "Colorado Rockies", "Los Angeles Dodgers", "San Diego Padres", "San Francisco Giants",
]

NFL_TEAMS = [
    "Buffalo Bills", "Miami Dolphins", "New England Patriots", "New York Jets",
    "Baltimore Ravens", "Cincinnati Bengals", "Cleveland Browns", "Pittsburgh Steelers",
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Tennessee Titans",
    "Denver Broncos", "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers",
    "Dallas Cowboys", "New York Giants", "Philadelphia Eagles", "Washington Commanders",
    "Chicago Bears", "Detroit Lions", "Green Bay Packers", "Minnesota Vikings",
    "Atlanta Falcons", "Carolina Panthers", "New Orleans Saints", "Tampa Bay Buccaneers",
    "Arizona Cardinals", "Los Angeles Rams", "San Francisco 49ers", "Seattle Seahawks",
]

NBA_TEAMS = [
    "Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers", "Toronto Raptors",
    "Chicago Bulls", "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers", "Milwaukee Bucks",
    "Atlanta Hawks", "Charlotte Hornets", "Miami Heat", "Orlando Magic", "Washington Wizards",
    "Denver Nuggets", "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trail Blazers", "Utah Jazz",
    "Golden State Warriors", "Los Angeles Clippers", "Los Angeles Lakers", "Phoenix Suns", "Sacramento Kings",
    "Dallas Mavericks", "Houston Rockets", "Memphis Grizzlies", "New Orleans Pelicans", "San Antonio Spurs",
]

NHL_TEAMS = [
    "Boston Bruins", "Buffalo Sabres", "Detroit Red Wings", "Florida Panthers", "Montreal Canadiens", "Ottawa Senators", "Tampa Bay Lightning", "Toronto Maple Leafs",
    "Carolina Hurricanes", "Columbus Blue Jackets", "New Jersey Devils", "New York Islanders", "New York Rangers", "Philadelphia Flyers", "Pittsburgh Penguins", "Washington Capitals",
    "Chicago Blackhawks", "Colorado Avalanche", "Dallas Stars", "Minnesota Wild", "Nashville Predators", "St. Louis Blues", "Utah Mammoth", "Winnipeg Jets",
    "Anaheim Ducks", "Calgary Flames", "Edmonton Oilers", "Los Angeles Kings", "San Jose Sharks", "Seattle Kraken", "Vancouver Canucks", "Vegas Golden Knights",
]

EPL_TEAMS = [
    "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton & Hove Albion",
    "Chelsea", "Coventry City", "Crystal Palace", "Everton", "Fulham",
    "Hull City", "Ipswich Town", "Leeds United", "Liverpool", "Manchester City",
    "Manchester United", "Newcastle United", "Nottingham Forest", "Sunderland", "Tottenham Hotspur",
]

# Every FBS (Football Bowl Subdivision) school — the team pool eligible for a
# Division I bowl game. 2026 conference alignment; see CLAUDE.md for notes on
# the heavy 2026 realignment (Pac-12 rebuilt, Mountain West turnover, etc).
NCAAF_TEAMS = [
    # SEC (16)
    "Alabama Crimson Tide", "Arkansas Razorbacks", "Auburn Tigers", "Florida Gators", "Georgia Bulldogs", "Kentucky Wildcats", "LSU Tigers",
    "Mississippi State Bulldogs", "Missouri Tigers", "Oklahoma Sooners", "Ole Miss Rebels", "South Carolina Gamecocks",
    "Tennessee Volunteers", "Texas Longhorns", "Texas A&M Aggies", "Vanderbilt Commodores",
    # Big Ten (18)
    "Illinois Fighting Illini", "Indiana Hoosiers", "Iowa Hawkeyes", "Maryland Terrapins", "Michigan Wolverines", "Michigan State Spartans",
    "Minnesota Golden Gophers", "Nebraska Cornhuskers", "Northwestern Wildcats", "Ohio State Buckeyes", "Oregon Ducks",
    "Penn State Nittany Lions", "Purdue Boilermakers", "Rutgers Scarlet Knights", "UCLA Bruins", "USC Trojans", "Washington Huskies", "Wisconsin Badgers",
    # ACC (17)
    "Boston College Eagles", "California Golden Bears", "Clemson Tigers", "Duke Blue Devils", "Florida State Seminoles",
    "Georgia Tech Yellow Jackets", "Louisville Cardinals", "Miami (FL) Hurricanes", "NC State Wolfpack", "North Carolina Tar Heels",
    "Pittsburgh Panthers", "SMU Mustangs", "Stanford Cardinal", "Syracuse Orange", "Virginia Cavaliers", "Virginia Tech Hokies",
    "Wake Forest Demon Deacons",
    # Big 12 (16)
    "Arizona Wildcats", "Arizona State Sun Devils", "Baylor Bears", "BYU Cougars", "Cincinnati Bearcats", "Colorado Buffaloes",
    "Houston Cougars", "Iowa State Cyclones", "Kansas Jayhawks", "Kansas State Wildcats", "Oklahoma State Cowboys",
    "TCU Horned Frogs", "Texas Tech Red Raiders", "UCF Knights", "Utah Utes", "West Virginia Mountaineers",
    # Pac-12 (8)
    "Boise State Broncos", "Colorado State Rams", "Fresno State Bulldogs", "Oregon State Beavers",
    "San Diego State Aztecs", "Texas State Bobcats", "Utah State Aggies", "Washington State Cougars",
    # Mountain West (10)
    "Air Force Falcons", "Hawaii Rainbow Warriors", "Nevada Wolf Pack", "New Mexico Lobos", "North Dakota State Bison",
    "Northern Illinois Huskies", "San Jose State Spartans", "UNLV Rebels", "UTEP Miners", "Wyoming Cowboys",
    # American (14)
    "Army Black Knights", "Charlotte 49ers", "East Carolina Pirates", "Florida Atlantic Owls", "Memphis Tigers",
    "Navy Midshipmen", "North Texas Mean Green", "Rice Owls", "South Florida Bulls", "Temple Owls", "Tulane Green Wave",
    "Tulsa Golden Hurricane", "UAB Blazers", "UTSA Roadrunners",
    # Sun Belt (14)
    "Appalachian State Mountaineers", "Arkansas State Red Wolves", "Coastal Carolina Chanticleers",
    "Georgia Southern Eagles", "Georgia State Panthers", "James Madison Dukes", "Louisiana Ragin' Cajuns",
    "Louisiana-Monroe Warhawks", "Louisiana Tech Bulldogs", "Marshall Thundering Herd", "Old Dominion Monarchs",
    "South Alabama Jaguars", "Southern Miss Golden Eagles", "Troy Trojans",
    # MAC (13)
    "Akron Zips", "Ball State Cardinals", "Bowling Green Falcons", "Buffalo Bulls", "Central Michigan Chippewas",
    "Eastern Michigan Eagles", "Kent State Golden Flashes", "Miami (OH) RedHawks", "Ohio Bobcats",
    "Sacramento State Hornets", "Toledo Rockets", "UMass Minutemen", "Western Michigan Broncos",
    # Conference USA (10)
    "Delaware Blue Hens", "FIU Panthers", "Jacksonville State Gamecocks", "Kennesaw State Owls", "Liberty Flames",
    "Middle Tennessee Blue Raiders", "Missouri State Bears", "New Mexico State Aggies", "Sam Houston Bearkats",
    "Western Kentucky Hilltoppers",
    # FBS Independents (2)
    "Notre Dame Fighting Irish", "UConn Huskies",
]

# Every Division I men's basketball program — all are NCAA tournament
# eligible (unlike football, D-I basketball has no minimum-wins bowl gate).
# 2026-27 alignment; see CLAUDE.md for realignment notes (Pac-12 rebuilt
# with Gonzaga, WAC dissolved into Big Sky/Big West/United Athletic, etc).
NCAAMB_TEAMS = [
    # America East (9)
    "Albany Great Danes", "Binghamton Bearcats", "Bryant Bulldogs", "Maine Black Bears", "UMBC Retrievers", "UMass Lowell River Hawks",
    "New Hampshire Wildcats", "NJIT Highlanders", "Vermont Catamounts",
    # American (13)
    "Charlotte 49ers", "East Carolina Pirates", "Florida Atlantic Owls", "Memphis Tigers", "North Texas Mean Green",
    "Rice Owls", "South Florida Bulls", "Temple Owls", "Tulane Green Wave", "Tulsa Golden Hurricane", "UAB Blazers", "UTSA Roadrunners",
    "Wichita State Shockers",
    # ACC (18)
    "Boston College Eagles", "California Golden Bears", "Clemson Tigers", "Duke Blue Devils", "Florida State Seminoles",
    "Georgia Tech Yellow Jackets", "Louisville Cardinals", "Miami (FL) Hurricanes", "North Carolina Tar Heels", "NC State Wolfpack",
    "Notre Dame Fighting Irish", "Pittsburgh Panthers", "SMU Mustangs", "Stanford Cardinal", "Syracuse Orange", "Virginia Cavaliers",
    "Virginia Tech Hokies", "Wake Forest Demon Deacons",
    # ASUN (8)
    "Bellarmine Knights", "Florida Gulf Coast Eagles", "Jacksonville Dolphins", "Lipscomb Bisons",
    "North Florida Ospreys", "Queens Royals", "Stetson Hatters", "West Florida Argonauts",
    # Atlantic 10 (14)
    "Davidson Wildcats", "Dayton Flyers", "Duquesne Dukes", "Fordham Rams", "George Mason Patriots",
    "George Washington Revolutionaries", "La Salle Explorers", "Loyola Chicago Ramblers", "Rhode Island Rams",
    "Richmond Spiders", "Saint Joseph's Hawks", "Saint Louis Billikens", "St. Bonaventure Bonnies", "VCU Rams",
    # Big East (11)
    "Butler Bulldogs", "UConn Huskies", "Creighton Bluejays", "DePaul Blue Demons", "Georgetown Hoyas", "Marquette Golden Eagles",
    "Providence Friars", "St. John's Red Storm", "Seton Hall Pirates", "Villanova Wildcats", "Xavier Musketeers",
    # Big Sky (11)
    "Eastern Washington Eagles", "Idaho Vandals", "Idaho State Bengals", "Montana Grizzlies", "Montana State Bobcats",
    "Northern Arizona Lumberjacks", "Northern Colorado Bears", "Portland State Vikings",
    "Southern Utah Thunderbirds", "Utah Tech Trailblazers", "Weber State Wildcats",
    # Big South (9)
    "Charleston Southern Buccaneers", "Gardner-Webb Runnin' Bulldogs", "High Point Panthers", "Longwood Lancers",
    "Presbyterian Blue Hose", "Radford Highlanders", "UNC Asheville Bulldogs", "USC Upstate Spartans", "Winthrop Eagles",
    # Big Ten (18)
    "Illinois Fighting Illini", "Indiana Hoosiers", "Iowa Hawkeyes", "Maryland Terrapins", "Michigan Wolverines", "Michigan State Spartans",
    "Minnesota Golden Gophers", "Nebraska Cornhuskers", "Northwestern Wildcats", "Ohio State Buckeyes", "Oregon Ducks",
    "Penn State Nittany Lions", "Purdue Boilermakers", "Rutgers Scarlet Knights", "UCLA Bruins", "USC Trojans", "Washington Huskies", "Wisconsin Badgers",
    # Big 12 (16)
    "Arizona Wildcats", "Arizona State Sun Devils", "Baylor Bears", "BYU Cougars", "Cincinnati Bearcats", "Colorado Buffaloes",
    "Houston Cougars", "Iowa State Cyclones", "Kansas Jayhawks", "Kansas State Wildcats", "Oklahoma State Cowboys",
    "TCU Horned Frogs", "Texas Tech Red Raiders", "UCF Knights", "Utah Utes", "West Virginia Mountaineers",
    # Big West (12)
    "California Baptist Lancers", "Cal Poly Mustangs", "Cal State Bakersfield Roadrunners",
    "Cal State Fullerton Titans", "Cal State Northridge Matadors", "Long Beach State Beach",
    "Sacramento State Hornets", "UC Irvine Anteaters", "UC Riverside Highlanders", "UC San Diego Tritons",
    "UC Santa Barbara Gauchos", "Utah Valley Wolverines",
    # CAA (13)
    "Campbell Fighting Camels", "Charleston Cougars", "Drexel Dragons", "Elon Phoenix", "Hampton Pirates", "Hofstra Pride",
    "Monmouth Hawks", "NC A&T Aggies", "Northeastern Huskies", "Stony Brook Seawolves", "Towson Tigers",
    "UNC Wilmington Seahawks", "William & Mary Tribe",
    # Conference USA (10)
    "Delaware Blue Hens", "FIU Panthers", "Jacksonville State Gamecocks", "Kennesaw State Owls", "Liberty Flames",
    "Middle Tennessee Blue Raiders", "Missouri State Bears", "New Mexico State Aggies", "Sam Houston Bearkats",
    "Western Kentucky Hilltoppers",
    # Horizon League (12)
    "Cleveland State Vikings", "Detroit Mercy Titans", "Green Bay Phoenix", "IU Indy Jaguars", "Milwaukee Panthers",
    "Northern Illinois Huskies", "Northern Kentucky Norse", "Oakland Golden Grizzlies", "Purdue Fort Wayne Mastodons",
    "Robert Morris Colonials", "Wright State Raiders", "Youngstown State Penguins",
    # Ivy League (8)
    "Brown Bears", "Columbia Lions", "Cornell Big Red", "Dartmouth Big Green", "Harvard Crimson", "Penn Quakers",
    "Princeton Tigers", "Yale Bulldogs",
    # Metro (formerly MAAC) (12)
    "Canisius Golden Griffins", "Fairfield Stags", "Iona Gaels", "Manhattan Jaspers", "Marist Red Foxes", "Merrimack Warriors",
    "Mount St. Mary's Mountaineers", "Niagara Purple Eagles", "Quinnipiac Bobcats", "Rider Broncs", "Sacred Heart Pioneers",
    "Siena Saints",
    # MAC (12)
    "Akron Zips", "Ball State Cardinals", "Bowling Green Falcons", "Buffalo Bulls", "Central Michigan Chippewas",
    "Eastern Michigan Eagles", "Kent State Golden Flashes", "UMass Minutemen", "Miami (OH) RedHawks", "Ohio Bobcats",
    "Toledo Rockets", "Western Michigan Broncos",
    # MEAC (8)
    "Coppin State Eagles", "Delaware State Hornets", "Howard Bison", "Maryland Eastern Shore Hawks",
    "Morgan State Bears", "Norfolk State Spartans", "North Carolina Central Eagles",
    "South Carolina State Bulldogs",
    # Missouri Valley (11)
    "Belmont Bruins", "Bradley Braves", "Drake Bulldogs", "Evansville Purple Aces", "Illinois State Redbirds",
    "Indiana State Sycamores", "Murray State Racers", "Northern Iowa Panthers", "Southern Illinois Salukis",
    "UIC Flames", "Valparaiso Beacons",
    # Mountain West (10)
    "Air Force Falcons", "Grand Canyon Antelopes", "UC Davis Aggies", "Hawaii Rainbow Warriors", "Nevada Wolf Pack", "UNLV Rebels",
    "New Mexico Lobos", "San Jose State Spartans", "UTEP Miners", "Wyoming Cowboys",
    # NEC (9)
    "Central Connecticut Blue Devils", "Chicago State Cougars", "Fairleigh Dickinson Knights",
    "Le Moyne Dolphins", "LIU Sharks", "Mercyhurst Lakers", "New Haven Chargers", "Stonehill Skyhawks", "Wagner Seahawks",
    # OVC (9)
    "Eastern Illinois Panthers", "Lindenwood Lions", "Morehead State Eagles",
    "Southeast Missouri State Redhawks", "SIU Edwardsville Cougars", "Southern Indiana Screaming Eagles",
    "Tennessee State Tigers", "UT Martin Skyhawks", "Western Illinois Leathernecks",
    # Pac-12 (9)
    "Boise State Broncos", "Colorado State Rams", "Fresno State Bulldogs", "Gonzaga Bulldogs",
    "Oregon State Beavers", "San Diego State Aztecs", "Texas State Bobcats", "Utah State Aggies",
    "Washington State Cougars",
    # Patriot League (10)
    "American Eagles", "Army Black Knights", "Boston University Terriers", "Bucknell Bison", "Colgate Raiders",
    "Holy Cross Crusaders", "Lafayette Leopards", "Lehigh Mountain Hawks", "Loyola Maryland Greyhounds", "Navy Midshipmen",
    # SEC (16)
    "Alabama Crimson Tide", "Arkansas Razorbacks", "Auburn Tigers", "Florida Gators", "Georgia Bulldogs", "Kentucky Wildcats",
    "LSU Tigers", "Ole Miss Rebels", "Mississippi State Bulldogs", "Missouri Tigers", "Oklahoma Sooners",
    "South Carolina Gamecocks", "Tennessee Volunteers", "Texas Longhorns", "Texas A&M Aggies", "Vanderbilt Commodores",
    # SoCon (11)
    "Chattanooga Mocs", "The Citadel Bulldogs", "East Tennessee State Buccaneers", "Furman Paladins",
    "Mercer Bears", "Samford Bulldogs", "UNC Greensboro Spartans", "Tennessee Tech Golden Eagles", "VMI Keydets",
    "Western Carolina Catamounts", "Wofford Terriers",
    # Southland (12)
    "East Texas A&M Lions", "Houston Christian Huskies", "Incarnate Word Cardinals", "Lamar Cardinals",
    "New Orleans Privateers", "McNeese State Cowboys", "Nicholls State Colonels", "Northwestern State Demons",
    "Southeastern Louisiana Lions", "Stephen F. Austin Lumberjacks",
    "Texas A&M-Corpus Christi Islanders", "UT Rio Grande Valley Vaqueros",
    # SWAC (12)
    "Alabama A&M Bulldogs", "Alabama State Hornets", "Alcorn State Braves", "Arkansas-Pine Bluff Golden Lions",
    "Bethune-Cookman Wildcats", "Florida A&M Rattlers", "Grambling State Tigers", "Jackson State Tigers",
    "Mississippi Valley State Delta Devils", "Prairie View A&M Panthers", "Southern Jaguars",
    "Texas Southern Tigers",
    # Summit League (8)
    "Kansas City Roos", "North Dakota Fighting Hawks", "North Dakota State Bison", "Omaha Mavericks",
    "Oral Roberts Golden Eagles", "St. Thomas Tommies", "South Dakota Coyotes", "South Dakota State Jackrabbits",
    # Sun Belt (14)
    "Appalachian State Mountaineers", "Coastal Carolina Chanticleers", "Georgia Southern Eagles",
    "Georgia State Panthers", "James Madison Dukes", "Marshall Thundering Herd", "Old Dominion Monarchs",
    "Arkansas State Red Wolves", "Louisiana Ragin' Cajuns", "Louisiana-Monroe Warhawks", "Louisiana Tech Bulldogs",
    "South Alabama Jaguars", "Southern Miss Golden Eagles", "Troy Trojans",
    # United Athletic Conference (9)
    "Abilene Christian Wildcats", "Austin Peay Governors", "Central Arkansas Bears",
    "Eastern Kentucky Colonels", "Little Rock Trojans", "North Alabama Lions", "Tarleton State Texans",
    "UT Arlington Mavericks", "West Georgia Wolves",
    # WCC (10)
    "Denver Pioneers", "Loyola Marymount Lions", "Pacific Tigers", "Pepperdine Waves", "Portland Pilots",
    "Saint Mary's Gaels", "San Diego Toreros", "San Francisco Dons", "Santa Clara Broncos", "Seattle Redhawks",
]

# Same pool as NCAAMB, minus The Citadel and VMI — the only two D-I schools
# that field men's basketball but not women's.
NCAAWB_TEAMS = [t for t in NCAAMB_TEAMS if t not in ("The Citadel Bulldogs", "VMI Keydets")]

# Tennis: the draftable "team" is a country, not a club (see league_rules.py
# compute_score — a country's score sums all of its players' round wins at
# each major). Pool is every country with a currently ATP/WTA-ranked player
# inside the top 200; see CLAUDE.md for the compilation caveat (no single
# clean source enumerates every country at full ranking depth).
ATP_TEAMS = [
    "United States", "France", "Argentina", "Italy", "Spain", "Australia",
    "Great Britain", "Czech Republic", "Russia", "Germany", "Serbia",
    "Belgium", "Kazakhstan", "Portugal", "Hungary", "Netherlands", "Canada",
    "Chile", "Brazil", "Croatia", "Japan", "China", "Poland", "Switzerland",
    "Austria", "Georgia Bulldogs", "Hong Kong", "Bulgaria", "Peru", "Bolivia",
    "Denmark", "Luxembourg", "Greece", "Bosnia and Herzegovina", "Finland",
    "Norway", "Monaco", "Paraguay", "Lithuania", "Slovakia", "Colombia",
    "South Africa", "Ukraine", "Moldova", "Tunisia", "Egypt",
    "Chinese Taipei", "Ecuador", "Mexico", "Algeria", "Lebanon", "Israel",
    "Ivory Coast", "Slovenia", "Ireland", "Uruguay", "Venezuela",
    "Indonesia", "Pakistan", "Morocco", "New Zealand", "Senegal", "Iran",
    "South Korea", "Uzbekistan", "Sweden", "Cyprus", "Estonia",
    "Dominican Republic",
]

WTA_TEAMS = [
    "United States", "Czech Republic", "Russia", "Australia", "Ukraine",
    "Spain", "China", "Germany", "Poland", "France", "Italy",
    "Great Britain", "Austria", "Canada", "Croatia", "Japan", "Switzerland",
    "Uzbekistan", "Romania", "Belgium", "Latvia", "Colombia", "Hungary",
    "Thailand", "Belarus", "Kazakhstan", "Slovenia", "Andorra", "Denmark",
    "Slovakia", "Greece", "Netherlands", "Mexico", "Serbia", "Indonesia",
    "Argentina", "Philippines", "Egypt", "Armenia", "Turkey", "New Zealand",
    "Kenya", "Israel", "Ecuador", "Montenegro", "Albania", "Finland",
]

# Golf: the draftable "team" is a letter of the alphabet — a letter's score
# at a major sums every player in that major's field whose last name starts
# with that letter (see league_rules.py compute_score). Same 26-letter pool
# for both tours; no real-world roster to track season to season.
GOLF_LETTERS = [chr(c) for c in range(ord("A"), ord("Z") + 1)]

# Formula 1: the draftable "team" is a constructor (a works team fielding two
# cars). 2026 grid — 11 constructors, up from 10 in 2025: Cadillac is a new
# entrant, and Sauber's works team rebrands as Audi (see CLAUDE.md for both).
F1_TEAMS = [
    "Red Bull Racing", "Ferrari", "Mercedes", "McLaren", "Aston Martin",
    "Alpine", "Williams", "Racing Bulls", "Audi", "Haas", "Cadillac",
]

# WNBA: Portland Fire and Toronto Tempo are brand-new 2026 expansion
# franchises (added via an April 2026 expansion draft) with no 2025 history.
WNBA_TEAMS = [
    "Atlanta Dream", "Chicago Sky", "Connecticut Sun", "Dallas Wings",
    "Golden State Valkyries", "Indiana Fever", "Las Vegas Aces",
    "Los Angeles Sparks", "Minnesota Lynx", "New York Liberty",
    "Phoenix Mercury", "Portland Fire", "Seattle Storm", "Toronto Tempo",
    "Washington Mystics",
]

# MLS: 30 teams, no conference split in the Team pool itself (conferences
# only matter for playoff seeding, tracked in seed_historical_results.py).
MLS_TEAMS = [
    "Atlanta United FC", "Austin FC", "CF Montréal", "Charlotte FC",
    "Chicago Fire FC", "Colorado Rapids", "Columbus Crew", "D.C. United",
    "FC Cincinnati", "FC Dallas", "Houston Dynamo FC", "Inter Miami CF",
    "LA Galaxy", "Los Angeles FC", "Minnesota United FC",
    "Nashville SC", "New England Revolution", "New York City FC",
    "New York Red Bulls", "Orlando City SC", "Philadelphia Union",
    "Portland Timbers", "Real Salt Lake", "San Diego FC",
    "San Jose Earthquakes", "Seattle Sounders FC", "Sporting Kansas City",
    "St. Louis City SC", "Toronto FC", "Vancouver Whitecaps FC",
]

# NWSL: 16 teams for the 2026 season — Boston Legacy FC and Denver Summit FC
# are brand-new 2026 expansion franchises (no 2025 history, same treatment
# as this app's other mid-cycle expansion teams).
NWSL_TEAMS = [
    "Angel City FC", "Bay FC", "Boston Legacy FC", "Chicago Stars FC",
    "Denver Summit FC", "Gotham FC", "Houston Dash", "Kansas City Current",
    "North Carolina Courage", "Orlando Pride", "Portland Thorns FC",
    "Racing Louisville FC", "San Diego Wave FC", "Seattle Reign FC",
    "Utah Royals", "Washington Spirit",
]

# Tour de France Team Classification: the draftable "team" is a professional
# cycling team (see docs/wiki/game-rules-tdf.md for how team times combine
# into the classification). This is the 2026 Tour's 23-team startlist — the
# most recently completed real edition — since UCI WorldTeam rosters/sponsor
# names for the 2027 Tour (the edition that actually falls in this app's
# current game season) aren't formalized until around January 2027. Expect
# several of these team names to change by then (pro cycling sponsorship
# rebrands are common year to year) and re-verify before reusing this list
# for a future season.
TDF_TEAMS = [
    "Alpecin–Premier Tech", "Decathlon CMA CGM", "EF Education–EasyPost",
    "Groupama–FDJ United", "Lidl–Trek", "Lotto–Intermarché",
    "Movistar Team", "Netcompany INEOS", "NSN Cycling Team",
    "Red Bull–Bora–Hansgrohe", "Soudal–Quick-Step",
    "Team Bahrain Victorious", "Team Jayco–AlUla", "Team Picnic–PostNL",
    "UAE Team Emirates XRG", "Uno-X Mobility", "Visma–Lease a Bike",
    "XDS Astana Team", "Caja Rural–Seguros RGA", "Cofidis",
    "Pinarello–Q36.5 Pro Cycling Team", "Team TotalEnergies",
    "Tudor Pro Cycling Team",
]

# United Rugby Championship: 16 clubs across 5 countries — 4 Irish
# provinces, 4 Welsh regions, 4 South African sides, 2 Scottish, 2 Italian.
URC_TEAMS = [
    "Benetton", "Bulls", "Cardiff", "Connacht", "Dragons", "Edinburgh",
    "Glasgow Warriors", "Leinster", "Lions", "Munster", "Ospreys",
    "Scarlets", "Sharks", "Stormers", "Ulster", "Zebre Parma",
]

# IPL: 10 franchises, split into two 5-team groups for 2026 scheduling
# purposes only (the points table itself is unified, no group split).
IPL_TEAMS = [
    "Chennai Super Kings", "Delhi Capitals", "Gujarat Titans",
    "Kolkata Knight Riders", "Lucknow Super Giants", "Mumbai Indians",
    "Punjab Kings", "Rajasthan Royals", "Royal Challengers Bengaluru",
    "Sunrisers Hyderabad",
]

LEAGUE_TEAMS = [
    ("MLB", "Baseball", MLB_TEAMS),
    ("NFL", "Football", NFL_TEAMS),
    ("NBA", "Basketball", NBA_TEAMS),
    ("NHL", "Hockey", NHL_TEAMS),
    ("EPL", "Soccer", EPL_TEAMS),
    ("NCAAF", "Football", NCAAF_TEAMS),
    ("NCAAMB", "Basketball", NCAAMB_TEAMS),
    ("NCAAWB", "Basketball", NCAAWB_TEAMS),
    ("ATP", "Tennis", ATP_TEAMS),
    ("WTA", "Tennis", WTA_TEAMS),
    ("PGA", "Golf", GOLF_LETTERS),
    ("LPGA", "Golf", GOLF_LETTERS),
    ("F1", "Motorsport", F1_TEAMS),
    ("WNBA", "Basketball", WNBA_TEAMS),
    ("MLS", "Soccer", MLS_TEAMS),
    ("URC", "Rugby", URC_TEAMS),
    ("IPL", "Cricket", IPL_TEAMS),
    ("NWSL", "Soccer", NWSL_TEAMS),
    ("TDF", "Cycling", TDF_TEAMS),
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        emails = settings.allowed_email_list
        if not emails:
            print("No ALLOWED_EMAILS configured — set it in backend/.env before seeding users.")
        for i, email in enumerate(emails):
            if db.query(User).filter(User.email == email).first():
                continue
            db.add(
                User(
                    email=email,
                    display_name=email.split("@")[0],
                    is_commissioner=(i == 0),
                )
            )
        db.commit()

        team_count = 0
        canonical: set[tuple[str, str]] = set()
        for league, sport, names in LEAGUE_TEAMS:
            for name in names:
                canonical.add((league, name))
                if db.query(Team).filter(Team.league == league, Team.name == name).first():
                    continue
                db.add(Team(league=league, sport=sport, name=name))
                team_count += 1
        db.commit()

        # Drop stale placeholder teams from earlier seeds that aren't part of
        # the current rosters (e.g. old NBA placeholders, renamed teams, or
        # a whole league removed from the app like IndyCar). Their
        # TeamSeasonResult history is deliberately discarded along with
        # them — it's not meaningful once the team itself is gone. Skip any
        # team still referenced by a roster/auction/queue/crib-sheet row
        # (those foreign keys aren't safe to silently discard).
        removed = 0
        for team in db.query(Team).all():
            if (team.league, team.name) in canonical:
                continue
            try:
                db.query(TeamSeasonResult).filter(TeamSeasonResult.team_id == team.id).delete()
                db.delete(team)
                db.commit()
                removed += 1
            except IntegrityError:
                db.rollback()
                print(f"Skipped removing '{team.league} {team.name}' — still referenced by a roster/auction.")

        print(f"Seeded {len(emails)} users, added {team_count} teams, removed {removed} stale teams.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
