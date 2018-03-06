#!/bin/bash
set -x
 
bash linux_build.sh
bash linux_makebin.sh
bash blog-tool.sh
