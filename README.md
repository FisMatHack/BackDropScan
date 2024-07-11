# BackDropScan

To determine the version of BackDropCMS that the site has, we can use the following command:

```shell=
python BackDropScan.py --url http://localhost --version
```

If you want to list potential users in BackDropCMS, you can use the following command:

```shell=
python BackDropScan.py --url http://localhost --userslist users.txt --userenum
```

If you want to test the user as a password, you can use the following command (note that having a large list of users may cause you to end up temporarily locked out):

```shell=
python BackDropScan.py --url http://localhost --userslist valid_users.txt --userpass
```
