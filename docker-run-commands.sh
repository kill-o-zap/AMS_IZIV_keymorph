docker run \
    --name keymorph_torch_container \
    -it \
    --runtime=nvidia \
    --shm-size=1g \
    --ulimit memlock=1 \
    --ulimit stack=67108864 \
    -v /home/jernejb/AMS_IZIV_keymorph:/workspace/AMS_IZIV_keymorph \
    jernejb-torch \
    bash
    # -d \
    # --user 1010 \


43  docker run     --name keymorph_torch_container     -it     --runtime=nvidia     --shm-size=1g     --ulimit memlock=1     --ulimit stack=67108864     -v /home/jernejb/AMS_IZIV_keymorph:/workspace/AMS_IZIV_keymorph     jernejb-torch     bash
46  docker ps -a
47  docker exec -it keymorph_torch_container bash