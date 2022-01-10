# Adding New Measurement Tools to Murakami

Murakami provides a collection of _test runners_, which are Python script
wrappers around various internet measurement tools. If there is a measurement
tool that you would like included in Murakami, you can add it!

To add new measurement tools to Murakami, do the following in a fork or  branch:
* The tool should be built or included in [Dockerfile](https://github.com/m-lab/murakami/blob/master/Dockerfile) and
  [Dockerfile.template](https://github.com/m-lab/murakami/blob/master/Dockerfile.template). Two Dockerfiles are needed to support the two types
  of Murakami deployments: standalone installs (Dockerfile) and Balena.io
  managed installs (Dockerfile.template)
* Add a Python wrapper for the new tool in [murakami/runners/](https://github.com/m-lab/murakami/tree/master/murakami/runners)
* If the new test runner requires an additional configuration file, provide an
  example in
  [murakami/configs/](https://github.com/m-lab/murakami/tree/master/configs).
* Register the test runner for the new tool in
  [pyproject.toml](https://github.com/m-lab/murakami/blob/master/pyproject.toml#L35)
* Document the new test runner:
  * Add a brief description of the new test runner in
    [murakami/README.md](https://github.com/m-lab/murakami#supported-measurement-tests)
  * Describe the new test runner in [murakami/docs/SUPPORTED-TEST-RUNNERS.md](https://github.com/m-lab/murakami/blob/master/docs/SUPPORTED-TEST-RUNNERS.md)
  * Add the new runner's default configuration to Murakami's example  config files:
    * [murakami/configs/murakami.config.example](https://github.com/m-lab/murakami/blob/master/configs/murakami.config.example)
    * [murakami/configs/murakami.toml.example](https://github.com/m-lab/murakami/blob/master/configs/murakami.toml.example)
  * Add a sample output file for the new test runner in:
    * [murakami/docs/example-test-output/](https://github.com/m-lab/murakami/tree/master/docs/example-test-output)
  * If the new test runner requires additional configuration, such as a
    configuration file in `murakami/configs`, summarize this additional
    configuration in [murakami/docs/CONFIGURING-MURAKAMI.md](https://github.com/m-lab/murakami/blob/master/docs/CONFIGURING-MURAKAMI.md)
* Test the new runner and open a Pull Request for your branch or fork, and
  request a review!
  