summershum
----------

A fedmsg consumer that extracts and stores hashes of source files.

summershum is composed of two components:

- A fedmsg consumer plugin that listens for
  ``org.fedoraproject.prod.git.lookaside.new`` messages.  Whenever a
  contributor uploads a new source tarball to the lookaside cache,
  summershum will download that tarball, unpack it, and calculate the
  sha1 sum of every file in the tarball.  Those hashes are then stored in
  a database to be queried later.
- A cli tool ``summershum-cli`` that queries `datagrepper
  <https://apps.fedoraproject.org/datagrepper>`_ for the fedmsg history.
  It then crawls through old lookaside messages to fill in data where it
  was missed.

With the summershum database, we can then make some interesting queries
in short time:

- how many files have this hash sum in all of fedora?  and for which
  packages ?
- we can easily find what is bundling what and generate a programatic list
- we could check the db in taskotron tests
- we could check to see how many packages include the full GPL license
- how many packages have that license but with the old FSF address
