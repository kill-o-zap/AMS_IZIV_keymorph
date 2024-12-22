# AMS IZZIV - final report
Jernej Bončina

Keymorph

LINK TO YOUR PROJECT https://github.com/kill-o-zap/AMS_IZIV_keymorph.git

## Method Explanation
KeyMorph is an unsupervised method for image registration that aligns two images by detecting and using keypoints. The process involves three main steps:

    Keypoint Detection: The method automatically identifies keypoints in both images. These points correspond to important regions that help guide the alignment. The detection is designed to be consistent under transformations and symmetric with respect to input image order.
    Keypoint Matching: Keypoints from one image are matched to their counterparts in the other image to establish correspondences.
    Affine Transformation: Using the matched keypoints, KeyMorph computes an optimal affine transformation (including translation, rotation, and scaling) to align the images.

This approach is robust to large misalignments, works well with multi-modal data (e.g., MRI and CT scans), and provides interpretability by showing which regions of the images drive the alignment.
## Results
My results tested by evaluation function. The presented results were achived with the 40 epochs training weights.

```bash         40 epoch trained model results
 aggregated_results:
        LogJacDetStd        : 0.00000 +- 0.00000 | 30%: 0.00000
        TRE_kp              : 10.10584 +- 2.75292 | 30%: 11.64474
        TRE_lm              : 10.73980 +- 3.48737 | 30%: 11.44389
        DSC                 : 0.26998 +- 0.07663 | 30%: 0.22750
        HD95                : 49.11014 +- 13.33247 | 30%: 37.55394
```
```bash         20 epoch trained model results
aggregated_results:
        LogJacDetStd        : 0.00000 +- 0.00000 | 30%: 0.00000
        TRE_kp              : 10.14191 +- 2.84550 | 30%: 11.59536
        TRE_lm              : 10.82394 +- 3.60681 | 30%: 11.54599
        DSC                 : 0.26884 +- 0.07868 | 30%: 0.22567
        HD95                : 49.08807 +- 13.29403 | 30%: 37.61366
```

## Docker Information
 

## Data Preparation
The only data preparation I did for this was to run the scrip data_preparation.py . By running it, a folder was created that is later used for training and validating of this method. Check input and output folders in data_preparation.py before running it. Example how to run `data_preparation.py`
```bash
python data_preparation.py
```


## Train Commands
To initiate traning I used the following command below. Important parameters for training are log_interval and epochs, because the model saves the checkpoints of training when epochs%log_interval == 0. To get the checkpoint needed for registration these two parameters should be taken into the account. If not defined the following happens -> epochs = 2000, log_interval = 25. Some of the parameters are also used for registration (test) later on so they need to be remembered. Command --save_dir will create a folder or point to one if it is already made and in it save checpoints, images if a --visualize command is enabled and json file of all arguments for this traning session. In --save_dir the map where it will be saved can be changed, but for this example commands they should stay as they are.
Below is the example, how to run `train.py`:

```bash
python scripts/run.py    --run_mode train  --backbone unet --num_levels_for_unet 2    --log_interval 40    --num_keypoints 128   --loss_fn mse    --transform_type affine    --train_dataset ixi    --data_path ./data_prepared/centered_IXI     --epochs 41   --save_dir ./utez
```


## Test Commands
To test or register the moving and fixed image I used two commands below. It is important to register the pictures with the same num_keypoints, backbone, num_levels_for_unet (depends on the backbone), list_of_metrics has to be mse because for other scores I would need segmentations. Load paths depends on the save_dir of Train function.
It has to me manualy replaced. For fixed and moving image you have to choose the correct ones. The register function needs to have validation images.



```bash Command 1 T2 -> T1

python scripts/register.py    --num_keypoints 128    --backbone unet --num_levels_for_unet 2    --load_path ./utez/__training__keymorph_keypoints128_batch1_lr3e-06/checkpoints/epoch40_trained_model.pth.tar    --moving ./data/validation_data/T2    --fixed ./data_prepared/validation_data/T1    --list_of_aligns affine    --list_of_metrics mse --save_eval_to_disk --save_dir ./registracija_T2m_T1f
```
```bash Command 2 T2 -> PD

python scripts/register.py    --num_keypoints 128    --backbone unet --num_levels_for_unet 2    --load_path ./utez/__training__keymorph_keypoints128_batch1_lr3e-06/checkpoints/epoch40_trained_model.pth.tar    --moving ./data/validation_data/T2    --fixed ./data_prepared/validation_data/PD    --list_of_aligns affine    --list_of_metrics mse --save_eval_to_disk --save_dir ./registracija_T2m_PDf
```

## Eval preprocessing
To resize the registered (test) output, to the correct shape and also the correct name, I used the following command. In it the program goes through the output folders of Registration. If you need the input path or output path to be different it has to be changed manualy in the code. Currently all outputs / inputs paths are in corect way to call upon one another.
```bash
python resize_koncni.py
```

## Evaluation
For input the path to the input and output has to be changed. For input the path must be to the output of the function resize_koncni.py.
```bash
docker run --rm -u $UID:$UID -v ./input:/input -v ./output:/output/ gitlab.lst.fe.uni-lj.si:5050/domenp/deformable-registration python evaluation.py -v
```
## Example of evaluation
```bash
docker run     --rm     -u $UID:$UID     -v /home/jernejb/AMS_IZIV_keymorph/deformacije:/input     -v /home/jernejb/AMS_IZIV_keymorph/rezultati:/output/     gitlab.lst.fe.uni-lj.si:5050/domenp/deformable-registration     python evaluation.py -v
```
