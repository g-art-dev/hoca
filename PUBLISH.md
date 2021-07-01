# These are the required steps in order to publish the `hoca` package.

1. Update the version number in `hoca/__init__.py` and `hoca/setup.py`, they must be the same.

2. Change directory to the `hoca` project root (not the hoca package root).

3. Build the source and binary archives:
   ```shell
   $ python setup.py sdist bdist_wheel
   ```
   If you got the `error: invalid command 'bdist_wheel'` message, try to install the
   `wheel` package with `pip install wheel` or by any other means.  

4. Test the package publication on TestPyPi:
   ```shell
   $ twine check dist/*
   ```
   This step supposes you have installed `twine` with `pip install twine` or by any other means.  
   The test should have been PASSED.
   
5. Publish on TestPyPi:
   ```shell
   $ twine upload --repository testpypi dist/*
   ```
   `twine` will prompt you to enter your TestPyPi username and password.  
   If the upload succeeds, take a look at the web page which URL has just been printed
   (something like https://test.pypi.org/project/hoca/version_number/ or https://test.pypi.org/project/hoca/).

6. Publish on PyPi:
   ```shell
   $ twine upload dist/*
   ```
   Again, `twine` will prompt you to enter your PyPi username and password.  
   If the upload succeeds, take a look at the web page which URL has just been printed
   (something like https://pypi.org/project/hoca/version_number/ or https://pypi.org/project/hoca/).
