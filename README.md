py-proxy-protocol
-----------------

This code is based on a fork from https://github.com/efossier/py-proxy-protocol, which implemented version 1 of the protocol. The protocol is based on this specification: [proxy-protocol](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)

I refactored the code for python3 and added a working implementation of version 2 of the protocol with the exception of the Type-Length-Value (TLV vectors).

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
