CREATE TABLE IF NOT EXISTS levels (
	level_pk int,
	abbrv varchar(128),
	PRIMARY KEY (level_pk)
);

CREATE TABLE IF NOT EXISTS compartments (
	compartment_pk int,
	abbrv varchar(128),
	comment varchar(128),
	PRIMARY KEY (compartment_pk)
);

CREATE TABLE IF NOT EXISTS assets (
	asset_pk int,
	product_fk int,
	asset_tag varchar(128),
	alt_description varchar(128),
	description varchar(128),
	PRIMARY KEY (asset_pk),
	FOREIGN KEY (product_fk) REFERENCES products
);

CREATE TABLE IF NOT EXISTS products (
	product_pk int,
	vendor varchar(128),
	description varchar(128),
	alt_description varchar(128),
	PRIMARY KEY (product_pk)
);

CREATE TABLE IF NOT EXISTS vehicles (
	vehicles_pk int,
	asset_fk int,
	PRIMARY KEY (vehicles_pk),
	FOREIGN KEY (asset_fk) REFERENCES assets
);

CREATE TABLE IF NOT EXISTS facilities (
	facilities_pk int,
	fcode varchar(128),
	common_name varchar(128),
	location varchar(128),
	PRIMARY KEY (facilities_pk)
);

CREATE TABLE IF NOT EXISTS asset_at (
	asset_fk int,
	facility_fk int,
	arrive_dt Date,
	depart_dt Date,
	FOREIGN KEY (asset_fk) REFERENCES assets,
	FOREIGN KEY (facility_fk) REFERENCES facilities
);

CREATE TABLE IF NOT EXISTS convoys (
	convoy_pk int,
	request varchar(128),
	source_fk int,
	dest_fk int,
	depart_dt Date,
	arrive_dt Date,
	PRIMARY KEY (convoy_pk),
	FOREIGN KEY (source_fk) REFERENCES facilities
);

CREATE TABLE IF NOT EXISTS used_by (
	vehicle_fk int,
	convoy_fk int,
	FOREIGN KEY (vehicle_fk) REFERENCES vehicles,
	FOREIGN KEY (convoy_fk) REFERENCES convoys
);

CREATE TABLE IF NOT EXISTS asset_on (
	asset_fk int,
	convoy_fk int,
	load_dt Date,
	unload_dt Date,
	FOREIGN KEY (asset_fk) REFERENCES assets,
	FOREIGN KEY (convoy_fk) REFERENCES convoys
);

CREATE TABLE IF NOT EXISTS users (
	user_pk int,
	username varchar(128),
	active BOOLEAN,
	PRIMARY KEY (user_pk)
);

CREATE TABLE IF NOT EXISTS roles (
	role_pk int,
	title varchar(128),
	PRIMARY KEY (role_pk)
);

CREATE TABLE IF NOT EXISTS user_is (
	user_fk int,
	role_fk int,
	FOREIGN KEY (user_fk) REFERENCES users,
	FOREIGN KEY (role_fk) REFERENCES roles
);

CREATE TABLE IF NOT EXISTS user_supports (
	user_fk int,
	facility_fk int,
	FOREIGN KEY (user_fk) REFERENCES users,
	FOREIGN KEY (facility_fk) REFERENCES facilities
);

CREATE TABLE IF NOT EXISTS security_tags (
	tag_pk int,
	level_fk int,
	compartment_fk int,
	user_fk int,
	product_fk int,
	asset_fk int,
	PRIMARY KEY (tag_pk),
	FOREIGN KEY (level_fk) REFERENCES levels,
	FOREIGN KEY (compartment_fk) REFERENCES compartments,
	FOREIGN KEY (user_fk) REFERENCES users,
	FOREIGN KEY (product_fk) REFERENCES products,
	FOREIGN KEY (asset_fk) REFERENCES assets
);


