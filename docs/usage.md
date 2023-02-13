# Usage

## Help

Getting more information about available commands can be obtained via the `--help` flag.

```console
$ recite --help
```

## Release 

Publishing a release is done via the `release` command and the appropriate release classifier:

```console
$ recite release patch
```

The classifiers are the same as poetry's bump rules of the it's [version command](https://python-poetry.org/docs/cli/#version).

The arguments, that can be supplied to the release command can be shown via:
```console
$ recite release --help
```

In particular it is possible to skip certain checks via the `--skip-checks` flag, supplying a comma-seperated list of the names of the checks you want to skip. This should be done in extraordinary circumstances, if recite's checks fail unreasonably.

## List checks

To list the checks that will be run by default use:

```console
$ recite list-checks
```

More info on the individual steps can be found [here](steps.md).


