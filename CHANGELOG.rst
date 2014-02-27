Changelog
=========

0.1.5
-----

- Add supports for gem archives `ef32e0c49 <https://github.com/fedora-infra/summershum/commit/ef32e0c49e6da8bde83c9d340722fd0918b395ea>`_
- Use os.path.join to join multiple element in one single path `9afe50f44 <https://github.com/fedora-infra/summershum/commit/9afe50f440d40855438b5d82ad7a91440692c271>`_
- Check that the filename retrieved points to a directory `d1887eff1 <https://github.com/fedora-infra/summershum/commit/d1887eff1d2cbb43814cbb4aea681479dc021bd2>`_
- Remove the archive before browsing the extracted files `cbd6bec16 <https://github.com/fedora-infra/summershum/commit/cbd6bec16c6318fe01b1115dcb5bea7181475090>`_
- Remove FIXME now that we fixed it `b824459e6 <https://github.com/fedora-infra/summershum/commit/b824459e6a554addc06f8a8e4b6857da35a14fe4>`_
- Fix figuring out the folder name for zip archive `8c452ba03 <https://github.com/fedora-infra/summershum/commit/8c452ba037242225649d88bead25fa6cbf919533>`_
- Merge pull request #25 from fedora-infra/feature/gems `a6bfbbca8 <https://github.com/fedora-infra/summershum/commit/a6bfbbca88870e2c64bf67a862e367cf315f2276>`_
- Specify what is the msg_id of the message being processed in the logs `cb307ad87 <https://github.com/fedora-infra/summershum/commit/cb307ad874240f311a8ccec602ac51387622f335>`_
- Merge pull request #26 from fedora-infra/feature/msg_id `43e7ae125 <https://github.com/fedora-infra/summershum/commit/43e7ae1250346a43e1d4c54bf3111ffd4da6eb8b>`_
- Add the possibility to process a specific message by giving its msg_id to the cli `d57974cea <https://github.com/fedora-infra/summershum/commit/d57974cea9cc92d0409e739490cd097a9c2e20b6>`_
- Publish a message on the fedmsg bus when encountering an invalid file `6c0039df7 <https://github.com/fedora-infra/summershum/commit/6c0039df74a2de7df80b8729848bb394522e6f5a>`_
- Include the invalid files into the ``ingest.complete`` message `7f50f5121 <https://github.com/fedora-infra/summershum/commit/7f50f512184dce298f10f92e3a627de6110b4f7f>`_
- Use a single function __get_messages whether there are several or just one message to retrieve `1e8a05083 <https://github.com/fedora-infra/summershum/commit/1e8a050837168ad6ac64780a1b91110f38d1fd34>`_
- pep8 fixes `0512cca39 <https://github.com/fedora-infra/summershum/commit/0512cca396ab827720567a768ee8b6a3f931647f>`_
- Merge pull request #27 from fedora-infra/feature/cli_msg_id `767103cc4 <https://github.com/fedora-infra/summershum/commit/767103cc4d44160ad7e2e4898348a9f3f6e30f61>`_
- Merge pull request #23 from fedora-infra/feature/fedmsg_invalid_files `bc03a4db8 <https://github.com/fedora-infra/summershum/commit/bc03a4db89b34f733f8e1f6edf8ac7ac242574b3>`_

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
