/* 	It's faster to compare id's rather than long strings
	comparing by id's is more standard	
	password field is this length because it is the same as the user name length*/

create table roles (
	role_pk serial primary key,
	rolename varchar(16)
);

create table users (
	user_pk serial primary key,
	username varchar(16),
	password varchar(16)
	role_fk integer REFERENCES roles(role_pk) not null
);

create table assets (
	asset_pk serial primary key,
	asset_tag varchar(16),
	description varchar(122)
);

create table facilities (
	facility_pk serial primary key,
	common_name varchar(32),
	code varchar(6)
);

create table asset_at (
	asset_fk integer REFERENCES assets(asset_pk) not null,
	facility_fk integer REFERENCES facilities(facility_pk) not null,
	depart_dt timestamp,
	arrive_dt timestamp
);
	
