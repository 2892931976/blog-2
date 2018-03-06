#!/bin/bash
 
rm -rf packages.tar.gz
 
tar zcvf packages.tar.gz       blogd_80.service   dist/blog/ static/ templates/

cat linux_install.sh packages.tar.gz > blog-tool.sh

chmod +x blog-tool.sh

rm -rf packages.tar.gz
