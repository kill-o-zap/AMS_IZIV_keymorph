# AMS IZZIV - final report
Jernej Bončina

Keymorph

LINK TO YOUR PROJECT https://github.com/kill-o-zap/AMS_IZIV_keymorph.git

## Method Explanation
Describe the method used in your project in your own words. Explain the key concepts and steps involved. If applicable, include figures. 

## Results
My results tested by evaluation function. The presented results were achived with the 40 epochs training weights.

```bash
 aggregated_results:
        LogJacDetStd        : 0.00000 +- 0.00000 | 30%: 0.00000
        TRE_kp              : 10.10584 +- 2.75292 | 30%: 11.64474
        TRE_lm              : 10.73980 +- 3.48737 | 30%: 11.44389
        DSC                 : 0.26998 +- 0.07663 | 30%: 0.22750
        HD95                : 49.11014 +- 13.33247 | 30%: 37.55394
```
epoch 20
aggregated_results:
        LogJacDetStd        : 0.00000 +- 0.00000 | 30%: 0.00000
        TRE_kp              : 10.14191 +- 2.84550 | 30%: 11.59536
        TRE_lm              : 10.82394 +- 3.60681 | 30%: 11.54599
        DSC                 : 0.26884 +- 0.07868 | 30%: 0.22567
        HD95                : 49.08807 +- 13.29403 | 30%: 37.61366


## Docker Information
Provide information on how to set up and use Docker for this project. Be very specific when writing about Docker installation. Include step-by-step instructions, commands, and any necessary configurations. 

## Data Preparation
For data preparation I had to organize images and masks into specific folders and with specific names. The data type and size was not changed. 
For data training preparation I parceled the data to three folders based on the last for numbers representing the imaging technic. The main folder for the data used was named "data" and had a subfolder named "processed_IXI". In this subfolder I reorganized the data. The data folders were PD (end 0002), T1 (end 0001) and T2 (end 0000). I did not resize or changed the images in any way except to change the names. Because the model I am using need all names to be the same I deleted for example "_0000" at the end. For masks I created the same folders in the "processed_IXI" folder, but each had an append of "_mask". Same for the actual masks of the images. EXAMPLE AS FOLLOW


## Train Commands
To initiate traning I used the following command below. Important parameters for training are log_interval and epochs, because the model saves the checkpoints of training when epochs%log_interval == 0. To get the checkpoint needed for registration these two parameters should be taken into the account. If not defined the following happens -> epochs = 2000, log_interval = 25. Some of the parameters are also used for registration (test) later on so they need to be remembered. Command --save_dir will create a folder or point to one if it is already made and in it save checpoints, images if a --visualize command is enabled and json file of all arguments for this traning session.
Below is the example, how to run `train.py`:

```bash
python scripts/run.py    --run_mode train  --backbone unet --num_levels_for_unet 2    --log_interval 40    --num_keypoints 128   --loss_fn mse    --transform_type affine    --train_dataset ixi    --data_path ./data/processed_IXI     --epochs 41   --save_dir ./Here you can input you file name
```


## Test Commands
To test or register the moving and fixed image I used two commands below. It is important to register the pictures with the same num_keypoints, backbone, num_levels_for_unet (depends on the backbone), list_of_metrics has to be mse because for other scores I would need segmentations. Load paths depends on the save_dir of Train function. It has to me manualy replaced.


```bash
KOMANDA_1
python scripts/register.py    --num_keypoints 128    --backbone unet --num_levels_for_unet 2    --load_path ./utez/__training__keymorph_keypoints128_batch1_lr3e-06/checkpoints/epoch20_trained_model.pth.tar    --moving ./val_data/centered_IXI/T2    --fixed ./val_data/centered_IXI/T1    --list_of_aligns affine    --list_of_metrics mse --save_eval_to_disk --save_dir ./registracija_T2m_T1f

KOMANDA_2

python scripts/register.py    --num_keypoints 128    --backbone unet --num_levels_for_unet 2    --load_path ./utez/__training__keymorph_keypoints128_batch1_lr3e-06/checkpoints/epoch20_trained_model.pth.tar    --moving ./val_data/centered_IXI/T2    --fixed ./val_data/centered_IXI/PD    --list_of_aligns affine    --list_of_metrics mse --save_eval_to_disk --save_dir ./registracija_T2m_PDf
```

## Eval preprocessing
To resize the registered (test) output, to the correct shape and also the correct name, I used the following command. In it the program goes through the output folders of Registration. If you need the input path or output path to be different it has to be changed manualy in the code. Currently all outputs / inputs paths are in corect way to call upon one another. 
```bash
python resize_koncni.py
```


