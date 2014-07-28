INSERT INTO packages VALUES (SELECT DISTINCT pkg_name FROM files);

ALTER TABLE files
ADD CONSTRAINT fk_pkg FOREIGN KEY (pkg_name)
    REFERENCES packages(pkg_name);
