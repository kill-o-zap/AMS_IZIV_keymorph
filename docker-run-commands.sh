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

docker run \
    --rm \
    -u $UID:$UID \
    -v /home/jernejb/AMS_IZIV_keymorph/deformacije:/input \
    -v /home/jernejb/AMS_IZIV_keymorph/rezultati:/output/ \
    gitlab.lst.fe.uni-lj.si:5050/domenp/deformable-registration \
    python evaluation.py -v



43  docker run     --name keymorph_torch_container     -it     --runtime=nvidia     --shm-size=1g     --ulimit memlock=1     --ulimit stack=67108864     -v /home/jernejb/AMS_IZIV_keymorph:/workspace/AMS_IZIV_keymorph     jernejb-torch     bash
46  docker ps -a
47  docker exec -it keymorph_torch_container bash