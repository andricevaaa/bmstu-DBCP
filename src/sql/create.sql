CREATE TABLE Artist (
	ArtistID text NOT NULL PRIMARY KEY,
	ArtistType varchar(8),
	MainGroup varchar(20),
	Gender char
);

CREATE TABLE Gift (
	GiftId serial NOT NULL PRIMARY KEY,
	PCName varchar(20)
);

CREATE TABLE Album (
	AlbumID serial NOT NULL PRIMARY KEY,
	ArtistID text REFERENCES Artist(ArtistID),
	AlbumName text,
	AlbumVer text,
	Price int,
	ReleaseDate date,
	QBought int,
	QLeft int,
	Company varchar(10),
	Country varchar(12)
);

CREATE TABLE APG (
	ApGID serial NOT NULL PRIMARY KEY,
	AlbumID int REFERENCES Album(AlbumID),
	GiftID int REFERENCES Gift(GiftID)
);

CREATE TABLE Users (
    Username text NOT NULL PRIMARY KEY,
	Pwd text NOT NULL,
    FirstName varchar(10) NOT NULL,
    LastName varchar(15) NOT NULL,
	Phone bigint NOT NULL,
    Mail text NOT NULL,
	Address text NOT NULL,
	City varchar(12) NOT NULL,
	Country varchar(12) NOT NULL
);

CREATE TABLE Orders (
	OrderID serial NOT NULL PRIMARY KEY,
	OrderDate date,
	OrderType varchar(10)
);

CREATE TABLE OrdAlb (
	OrdAlbID serial NOT NULL PRIMARY KEY,
	OrderID int REFERENCES Orders(OrderID),
	APG int REFERENCES APG(ApGID),
	Username text REFERENCES Users(Username)
);
