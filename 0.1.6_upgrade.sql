INSERT INTO packages (pkg_name) VALUES (SELECT DISTINCT pkg_name FROM files);

INSERT INTO releases (pkg_name, tarball, tar_sum) VALUES (
    SELECT DISTINCT pkg_name, tar_file, tar_sum FROM files
);

ALTER TABLE files DROP COLUMN pkg_name, tar_file, tar_sum;

ALTER TABLE releases ADD CONSTRAINT fk_pkg FOREIGN KEY (pkg_name)
    REFERENCES packages(pkg_name);

ALTER TABLE files ADD CONSTRAINT fk_pkg FOREIGN KEY (tarball)
    REFERENCES releases(tarball);
