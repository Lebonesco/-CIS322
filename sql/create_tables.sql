/* 	It's faster to compare id's rather than long strings
	comparing by id's is more standard	
	password field is this length because it is the same as the user name length*/
create table users (
	user_pk serial primary key,
	username varchar(16),
	password varchar(16)
);
	
