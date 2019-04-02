CREATE DATABASE youtube;

\c youtube

CREATE TABLE Video(
	Id varchar(100) PRIMARY KEY,
	Title varchar(100) NOT NULL,
	Description text NULL,
	PublishedAt date NULL,
	Duration varchar(10) NULL,
	ChannelId varchar(25) NULL,
	ChannelTitle varchar(100) NULL
);

CREATE TABLE Thumbnail(
	Id SERIAL PRIMARY KEY,
	Url varchar(100) NOT NULL,
	Width smallint NULL,
	Height smallint NULL,
	VideoId varchar(100) NOT NULL REFERENCES Video(Id) ON DELETE CASCADE
);

CREATE TABLE Statistics(
	Id SERIAL PRIMARY KEY,
	ViewCount integer NULL,
	LikeCount integer NULL,
	DislikeCount integer NULL,
	VideoId varchar(100) NOT NULL REFERENCES Video(Id) ON DELETE CASCADE,
	inserted_at TIMESTAMP without time zone DEFAULT timestamp 'now( )' NOT NULL
);

CREATE TABLE Tag(
	Id SERIAL PRIMARY KEY,
	Value varchar(255) NOT NULL,
	VideoId varchar(100) NOT NULL REFERENCES Video(Id) ON DELETE CASCADE
);

CREATE TABLE Word(
	wordid SERIAL PRIMARY KEY,
	word varchar(100),
	frequency integer NULL
);

CREATE TABLE Posting(
	wordid integer REFERENCES Word(wordid) ON DELETE CASCADE,
	videoId varchar(100) REFERENCES Video(Id) ON DELETE CASCADE,
	PRIMARY KEY(wordid,videoid)
);
