# `orator`

A tool for generating audiobooks from ebooks. Currently, only `epub` files are supported.

# installation
1. Install espeak
2. `pip install -r requirements.txt`
3. `pip install -e .` in the main repo

# use
The API is primarily presented via a CLI. Currently, there is only one tool available:
```
orator orate --book-path $PATH_TO_BOOK --out-path $PATH_TO_OUTPUT_DIRECTORY
```

# todo
- [ ] Test voice conversion for generation
- [ ] Add Dockerfile to prevent awkward requirements
