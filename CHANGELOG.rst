Changelog
=========

0.1.4
-----

- When ingesting a new source file, indicate the package concerned `e7e8189ba <https://github.com/fedora-infra/summershum/commit/e7e8189ba1d2005ae8aa56261aaa9beaa01f45bc>`_
- Fix typo in the log message `4af49902f <https://github.com/fedora-infra/summershum/commit/4af49902f82d067b10d8c25ae44cc9ebf0907d4e>`_
- Log when someone uploads a .jar or a .war file `1951a334a <https://github.com/fedora-infra/summershum/commit/1951a334a535f51b49baf3d85b247773f0d0a135>`_
- Skip symlink `ceefab8cf <https://github.com/fedora-infra/summershum/commit/ceefab8cf36accf2dc4c17a660ef5b6b2c683fb2>`_
- Log when we skip a file because it's a link `ad410542c <https://github.com/fedora-infra/summershum/commit/ad410542c58ad5373b9062df38738491ffb9a95e>`_
- Merge pull request #17 from fedora-infra/feature/log_more_detail `b2dfb8138 <https://github.com/fedora-infra/summershum/commit/b2dfb813877546c0475b8f9273d789da289481dd>`_
- Merge pull request #18 from fedora-infra/feature/handle_jar_war `7a40e15e3 <https://github.com/fedora-infra/summershum/commit/7a40e15e3971a7297c76edfc1ac88290aab2b0b9>`_
- Merge pull request #19 from fedora-infra/feature/handle_symlink `8bc52cdd5 <https://github.com/fedora-infra/summershum/commit/8bc52cdd5dbd3851c08bf0b96fd902f443cd08e8>`_
- Make warning messages out of those. `0da3933c9 <https://github.com/fedora-infra/summershum/commit/0da3933c9075dd5ce0254d3217966fafbe4fd3c6>`_
- Disable the summershum.start message since its just so spammy. `248391f5b <https://github.com/fedora-infra/summershum/commit/248391f5b228cd2126882565f2b6aa4dc3d016c4>`_
- Add spaces for readability. `53b962a60 <https://github.com/fedora-infra/summershum/commit/53b962a60d3809758c3f04cff5b2e91aaa960560>`_
- Use kitchen to_unicode.  Fixes #12. `fc3067c6a <https://github.com/fedora-infra/summershum/commit/fc3067c6aa6edd4c5baee4f717cc0700f29802e7>`_
- Actually ingest files that are not archives (like bare pdfs).  Fixes #10. `ed61a77e5 <https://github.com/fedora-infra/summershum/commit/ed61a77e5f395a778498446ec363b7e0e88c91a0>`_

0.1.3
-----

- Handle logging dictConfig on el6. `48503340d <https://github.com/fedora-infra/summershum/commit/48503340da04afffa2abe6e25ab160c081bbd5f8>`_

0.1.2
-----

- Fix an import that never got refactored. `03b06143a <https://github.com/fedora-infra/summershum/commit/03b06143a412e065b3a28db48ef3d3fb910e511c>`_
- Store our paths as unicode so the db doesn't freak out. `ab0698b13 <https://github.com/fedora-infra/summershum/commit/ab0698b139336ea00300e7cf8578cf13ff4fef2e>`_
- Ignore dist dir. `f758a3e7e <https://github.com/fedora-infra/summershum/commit/f758a3e7e9c7c70e3c62ff271808606ca7cebd9a>`_

0.1.1
-----

- Port summershum to use a real temporary directory instead of this hard-coded one `7ad3436cf <https://github.com/fedora-infra/summershum/commit/7ad3436cf309ec1cc3f00ecd3bf0643f9ac2777a>`_
- Remove un-used imports `b6065140b <https://github.com/fedora-infra/summershum/commit/b6065140b67226d90b539db6a8fcb95349b6cec7>`_
- No need for the downloads folder anymore `886676817 <https://github.com/fedora-infra/summershum/commit/886676817d2583b2c04432d472849ccf09bda88e>`_
- Remove the tmpdir from the filename stored in the DB `40fb257cb <https://github.com/fedora-infra/summershum/commit/40fb257cbd9c3ec139874be980a77d7ed56108f7>`_
- Merge pull request #7 from fedora-infra/feature/tmpdir `ab6feea5b <https://github.com/fedora-infra/summershum/commit/ab6feea5bd120ca2fcb4f5d9b6846b40d78903df>`_
