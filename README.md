# A Methods Focused Guide to Quantum Error Correction and Fault-Tolerant Quantum Computation

The notebooks for the book are available under the `chapters` directory.

## Building

To build the book, ideally first create a virtual environment, and activate it.
```
virtualenv -p python3.10 envqecft
source ./envorganic/bin/activate
```

Then install dependencies and then run the creation script.
```
pip install -r requirements.txt
python ./bookcreator.py
```
For quickly rebuilding the book, run `make` (after editing any paths inside).


## License
The code cells of this book are licensed under [GPLV3](https://www.gnu.org/licenses/gpl-3.0.txt). The non-code portions are licensed under  [Creative Commons Attribution-NonCommercial-NoDerivs ](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode).
