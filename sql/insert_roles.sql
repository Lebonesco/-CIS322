INSERT INTO roles ("rolename") 
select
	'Facility Officer'
where not exists (SELECT * FROM roles WHERE rolename = 'Facility Officer');


INSERT INTO roles ("rolename") 
select
	'Logistics Officer'
where not exists (SELECT * FROM roles WHERE rolename = 'Logistics Officer');

