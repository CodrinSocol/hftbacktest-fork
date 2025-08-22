# Py-HftBacktest

## Prerequisites

Ensure you have the following installed:
- Rust Compiler (downloadable from [rustup.rs](https://rustup.rs/))
- Python (see [main README file](../README.rst) for the required version)
- **Maturin** Python Package (install via `pip install maturin`)


## Building the Shared Library
You can create a local build of the Python library using the `maturin` tool. This will compile the Rust code and generate a Python package that can be used for local testing.

To build the library, run the command below in the `py-hftbacktest` directory:

```bash
maturin build
```
This command will create a `.whl` file in the `target/wheels` directory, which you can then install using pip:

```bash
pip install <path-to-build-file>
```