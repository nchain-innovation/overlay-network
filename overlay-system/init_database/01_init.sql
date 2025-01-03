CREATE USER 'uaas'@'localhost' IDENTIFIED BY 'uaas-password';
CREATE USER 'maas'@'localhost' IDENTIFIED BY 'maas-password';

CREATE USER 'uaas'@'%' IDENTIFIED BY 'uaas-password';
CREATE USER 'maas'@'%' IDENTIFIED BY 'maas-password';


create database uaas_db;
create database main_uaas_db;

GRANT ALL PRIVILEGES on uaas_db.* to 'uaas'@'localhost';
GRANT ALL PRIVILEGES on main_uaas_db.* to 'maas'@'localhost';

GRANT ALL PRIVILEGES on uaas_db.* to 'uaas'@'%';
GRANT ALL PRIVILEGES on maas_db.* to 'maas'@'%';

