COVA Core
========================

This projecy contains the public facing repo for COVA core.

This repo has four major components: 

1. Cova Routing Node
2. Cova Compute Node
3. Centrifuge and Smart Policy writing toolkit
4. CovaVM, which enforces the smart data policies


To run router nodes:

Make sure you have all the router credentials under `configs/router[i].json`

```bash
# cd dockerfiles/routingnode
docker compose up -d
# cd /path/to/cova-core
docker run -t routingnode -v config/router[i].json:config/usercred.json
```

To run compute nodes:

```bash
# cd dockerfiles/comptuenode
docker compose up -d
docker run -t computenode
```