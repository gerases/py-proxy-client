py-proxy-protocol
-----------------

The protocol is based on this specification: [proxy-protocol](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt). The code was originally based on a fork from https://github.com/efossier/py-proxy-protocol, which implemented version 1 of the protocol. Version 2 was added as a result of a refactoring. The Type-Length-Value (TLV vectors) are not currently implemented.

### Installation

```
# pip-install directly from Github
pip install git+https://github.com/gerases/py-proxy-client
```

### Contributing

To initialize the development environment:

* Clone the repo
* Change to the directory and execute: `make env`. This should create the virtual
  environment and install the module within the environment in the development
  mode.

To run unit, integration and linting tests:
```
$ make test
```
