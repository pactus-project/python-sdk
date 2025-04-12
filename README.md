# Pactus Python SDK

The Pactus Python SDK provides a set of utilities to seamlessly interact with the [Pactus](https://pactus.org) blockchain.
With this SDK, you can easily create transactions, sign messages, generate cryptographic keys, and more.

## Installation

You can install the SDK using `pip`:

```bash
pip install pactus-sdk
```

## Examples

To help you get started, we've included an `examples` folder that contains various scripts demonstrating how to
use the SDK for different tasks. These examples cover key generation, transaction creation, message signing, and more.

To run an example, navigate to the `examples` directory and execute the script using Python:

```bash
cd examples
python  example_key_generation.py
```

Explore the `examples` folder for more detailed usage scenarios.

## Development Setup

For local development, you can install the package in editable mode, which allows you to make changes and test them immediately:

```bash
python3 -m pip install .
```

After making changes, it's important to ensure all tests pass by running:

```bash
python3 -m unittest discover tests
```

Maintaining code quality is crucial. Use [Ruff](https://docs.astral.sh/ruff/) to format and lint your code:

```bash
ruff format # formatting code style
ruff check # running linter
```

## Contributing

Contributions are welcome! Feel free to add features, fix bugs, or improve documentation via pull requests.

## Publishing to PyPI

To deploy `pactus-sdk` and create a release, tag the new version and push it to GitHub.
Ensure the version matches the one specified in `setup.py`.

```bash
git tag -s -a v1.x.y -m "Version 1.x.y"
git push origin v1.x.y
```

After publishing, update the version number in `setup.py` accordingly.
For reference, see [this PR](https://github.com/pactus-project/python-sdk/pull/24).

## License

This project is licensed under the [MIT License](./LICENSE).
By contributing, you agree to license your contributions under the same terms.
