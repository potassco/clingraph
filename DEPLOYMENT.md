# Deployment

Releases are deployed on [pypi] whenever a tag of form `vMajor.Minor.Revision`
is pushed. Furthermore, the deployment workflow can be triggered manually to
deploy test releases on [test.pypi].

For this to work, the workflow has to be granted permission to deploy on the
two services. Please follow this packaging [guide] to setup your accounts
accordingly. We also recommend to setup a github [environment] to restrict
which contributors can deploy packages.

## Automatic Documentation Deployment

You can automatically publish project documentation to GitHub Pages on every
new tag. To enable this:

- Go to your repository on GitHub.
- Navigate to **Settings** > **Pages**.
- Under **Build and deployment**, set **Source** to **GitHub Actions**.

This setup ensures your documentation is updated and available online whenever
you create a new release tag via Github workflows.

[environment]: https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment/
[guide]: https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/
[pypi]: https://pypi.org/
[test.pypi]: https://test.pypi.org/
