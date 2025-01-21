#! /bin/bash
source .env
curl -H "Authorization: Bearer $CANVAS_ACCESS_TOKEN" "https://canvas.instructure.com/api/v1/courses" && echo "Successfully accessed Canvas API"
# sshpass -p$CC_PASSWORD ssh $CC_USERNAME@mcscn.cs.coloradocollege.edu
