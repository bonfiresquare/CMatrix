import database.Database as db
import database.functions as dbf

# builds the database structure
def build():
    queries = [
'''
CREATE TABLE "Currency" (
  Id TEXT NOT NULL,
  Name TEXT NOT NULL,
  Symbol TEXT NOT NULL,
  Type TEXT NOT NULL,
  Active BOOLEAN NOT NULL,
  Rank INTEGER,
  Links TEXT,
  Description TEXT,
  CONSTRAINT "PK_Currency" PRIMARY KEY (Id)
)
''',
'''
CREATE TABLE "OHLC History" (
  CurrencyId TEXT NOT NULL,
  Date TEXT NOT NULL,
  Open NUMERIC NOT NULL,
  High NUMERIC NOT NULL,
  Low NUMERIC NOT NULL,
  Close NUMERIC NOT NULL,
  Volume INTEGER NOT NULL,
  MarketCap INTEGER NOT NULL,
  CONSTRAINT "PK_OHLC History" PRIMARY KEY (CurrencyId, Date),
  FOREIGN KEY (CurrencyId) REFERENCES "Currency" (Id) ON UPDATE CASCADE ON DELETE CASCADE
)
''',
'''
CREATE TABLE "User" (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  UserName TEXT NOT NULL,
  Password TEXT NOT NULL,
  UserFirstName TEXT NOT NULL,
  CONSTRAINT "UQ_UserName" UNIQUE (UserName)
)
''',
'''
CREATE TABLE "Depot" (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  UserId INTEGER NOT NULL,
  Name TEXT DEFAULT "default" NOT NULL,
  ExchangeId TEXT,
  CONSTRAINT "UQ_UserId_Name" UNIQUE (UserID, Name),
  FOREIGN KEY (UserId) REFERENCES "User" (Id) ON UPDATE RESTRICT ON DELETE CASCADE,
  FOREIGN KEY (ExchangeId) REFERENCES "Exchange" (Id) ON UPDATE RESTRICT ON DELETE SET NULL
)
''',
'''
CREATE TABLE "Balance" (
  DepotId INTEGER NOT NULL,
  CurrencyId TEXT NOT NULL,
  Balance DECIMAL,
  CONSTRAINT "PK_Balance" PRIMARY KEY (CurrencyId, DepotId),
  FOREIGN KEY (DepotId) REFERENCES "Depot" (Id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (CurrencyId) REFERENCES "Currency" (Id) ON UPDATE CASCADE
)
''',
'''
CREATE TABLE "Watchlist" (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  UserId INTEGER NOT NULL,
  Name TEXT DEFAULT "default" NOT NULL,
  CONSTRAINT "UQ_Watchlist_User" UNIQUE (Id, UserId),
  FOREIGN KEY (UserId) REFERENCES "User" (Id) ON UPDATE CASCADE ON DELETE CASCADE
)
''',
'''
CREATE TABLE "Watchlist Currency" (
  WatchlistId INTEGER NOT NULL,
  CurrencyId TEXT NOT NULL,
  CONSTRAINT "PK_Watchlist Currency" PRIMARY KEY (CurrencyId, WatchlistId),
  FOREIGN KEY (WatchlistId) REFERENCES "Watchlist" (Id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (CurrencyId) REFERENCES "Currency" (Id) ON UPDATE CASCADE ON DELETE CASCADE
)
''',
'''
CREATE TABLE "Exchange" (
  Id TEXT NOT NULL,
  Name TEXT NOT NULL,
  Active BOOLEAN NOT NULL,
  LastUpdated TEXT NOT NULL,
  Links TEXT,
  MarketsDataFetched BOOLEAN,
  Markets INTEGER,
  Currencies INTEGER,
  ReportedRank INTEGER,
  AdjustedRank INTEGER,
  SessionsPerMonth INTEGER,
  Description TEXT,
  CONSTRAINT "PK_Exchange" PRIMARY KEY (Id)
)
''',
'''
CREATE TABLE "Market" (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  ExchangeId TEXT NOT NULL,
  BaseId TEXT NOT NULL,
  QuoteId TEXT NOT NULL,
  Pair TEXT NOT NULL,
  CONSTRAINT "UQ_Exchange_Base_Quote" UNIQUE (ExchangeId, BaseId, QuoteId),
  FOREIGN KEY (ExchangeId) REFERENCES "Exchange" (Id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (BaseId) REFERENCES "Currency" (Id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (QuoteId) REFERENCES "Currency" (Id) ON UPDATE CASCADE ON DELETE CASCADE
)
''',
'''
CREATE TABLE "Quote" (
  MarketId TEXT NOT NULL,
  CurrencyId TEXT NOT NULL,
  Price NUMERIC NOT NULL,
  Volume24h NUMERIC,
  Time TEXT NOT NULL,
  CONSTRAINT "PK_Quote" PRIMARY KEY (MarketId, CurrencyId),
  FOREIGN KEY (MarketId) REFERENCES "Market" (Id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (CurrencyId) REFERENCES "Currency" (Id) ON UPDATE CASCADE ON DELETE CASCADE
)'''
    ]
    for query in queries:
        db.Database.exec(query)
    return
