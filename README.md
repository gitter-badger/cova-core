COVA Core
========================

[![Join the chat at https://gitter.im/covalent-hq/cova-core](https://badges.gitter.im/covalent-hq/cova-core.svg)](https://gitter.im/covalent-hq/cova-core?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This projecy contains the public facing repo for COVA core.

This repo has four major components: 

1. Cova Routing Node
2. Cova Compute Node
3. Centrifuge and Smart Policy writing toolkit
4. CovaVM, which enforces the smart data policies


To run router nodes:

Make sure you have all the router credentials under `configs/router[i].json`

```sh
# cd dockerfiles/routingnode
docker compose up -d
# cd /path/to/cova-core
docker run -t routingnode -v config/router[i].json:config/usercred.json -p 10000[+i]:10000
```

To run compute nodes:

```sh
# cd dockerfiles/comptuenode
docker compose up -d
docker run -t computenode -p 11000:11000 
```