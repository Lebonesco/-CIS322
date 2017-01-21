CREATE TABLE IF NOT EXISTS levels (
	level_pk SERIAL PRIMARY KEY,
	abbrv varchar(128)
);

CREATE TABLE IF NOT EXISTS compartments (
	compartment_pk SERIAL PRIMARY KEY,
	abbrv varchar(128),
	comment varchar(128)
);
CREATE TABLE IF NOT EXISTS products (
	product_pk SERIAL PRIMARY KEY,
	vendor varchar(128),
	description varchar(128),
	alt_description varchar(128)
);

CREATE TABLE IF NOT EXISTS assets (
	asset_pk SERIAL PRIMARY KEY,
	product_fk integer REFERENCES products(product_pk),
	asset_tag varchar(128),
	alt_description varchar(128),
	description varchar(128)
);

CREATE TABLE IF NOT EXISTS vehicles (
	vehicles_pk SERIAL PRIMARY KEY,
	asset_fk integer REFERENCES assets(asset_pk)
);

CREATE TABLE IF NOT EXISTS facilities (
	facility_pk SERIAL PRIMARY KEY,
	fcode varchar(128),
	common_name varchar(128),
	location varchar(128)
);

CREATE TABLE IF NOT EXISTS asset_at (
	asset_fk integer REFERENCES assets(asset_pk),
	facility_fk integer REFERENCES facilities(facility_pk),
	arrive_dt Date,
	depart_dt Date
);

CREATE TABLE IF NOT EXISTS convoys (
	convoy_pk SERIAL PRIMARY KEY,
	request varchar(128),
	source_fk integer REFERENCES facilities(facility_pk),
	dest_fk integer REFERENCES facilities(facility_pk),
	depart_dt Date,
	arrive_dt Date
);

CREATE TABLE IF NOT EXISTS used_by (
	vehicle_fk integer REFERENCES vehicles(vehicles_pk),
	convoy_fk integer REFERENCES convoys(convoy_pk)
);

CREATE TABLE IF NOT EXISTS asset_on (
	asset_fk integer REFERENCES assets(asset_pk),
	convoy_fk integer REFERENCES convoys(convoy_pk),
	load_dt Date,
	unload_dt Date
);

CREATE TABLE IF NOT EXISTS users (
	user_pk SERIAL PRIMARY KEY,
	username varchar(128),
	active BOOLEAN
);

CREATE TABLE IF NOT EXISTS roles (
	role_pk SERIAL PRIMARY KEY,
	title varchar(128)
);

CREATE TABLE IF NOT EXISTS user_is (
	user_fk integer REFERENCES users(user_pk),
	role_fk integer REFERENCES roles(role_pk)
);

CREATE TABLE IF NOT EXISTS user_supports (
	user_fk integer REFERENCES users(user_pk),
	facility_fk integer REFERENCES facilities(facility_pk)
);

CREATE TABLE IF NOT EXISTS security_tags (
	tag_pk SERIAL PRIMARY KEY,
	level_fk integer REFERENCES levels(level_pk),
	compartment_fk integer REFERENCES compartments(compartment_pk),
	user_fk integer REFERENCES users(user_pk),
	product_fk integer REFERENCES products(product_pk),
	asset_fk integer REFERENCES assets(asset_pk)
);


