#  The Green Web Foundation 
Searching the green web with Searx

- *Searx* is an open source, privacy protecting search engine.
- *The Green Web Foundation Plugin* allows to only show green hosted results.

## Installation
### Without Nix
Run `python setup.py install` in the same environment with searx.

### With Nix
When Searx is installed via nix configuration
it is possible to add plugin to both current generation configuration and to flake-based one
- via specifying `nix-flake input`
- import module with "fetchFromGithub" 

See [sample configuration](https://github.com/efim/nix-searx-container-example).

## Development
### With Nix
For local development nix provides environment with installed Searx & required dependencies  
Use `$ nix-shell` or `$ nix develop` (for Nix with flakes enabled) to enter such shell

It will expose command `searx-run` that would start local Searx instance with plugin installed  
Additionally `nix-direnv` can be used to automatically reload environment on file-change

(all dependencies are installed into /nix/store and don't interfere with other parts of OS)
