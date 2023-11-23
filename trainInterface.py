from bin import run_patchcore_mv
from src.patchcore import utils
import os

def train_by_path(   
        data_name,
        data_path,
        model_save_path,
    ):
        # 参数暂时写死在这，后面改成配置文件
        # 此处定义patchcore模型参数
    methods = []
    methods.append(run_patchcore_mv.patch_core(
        backbone_names=["wideresnet50"],
        layers_to_extract_from=["layer2","layer3"],
        pretrain_embed_dimension=256,
        target_embed_dimension=256,
        patchsize=1,
        anomaly_scorer_num_nn=1,
        faiss_on_gpu=True,
        faiss_num_workers=8,
    ))

    methods.append(run_patchcore_mv.sampler(
        name = "approx_greedy_coreset",
        percentage = 0.1
    ))

    methods.append(run_patchcore_mv.dataset(
        name="mvtec",
        data_path=data_path,
        subdatasets=[data_name],
        train_val_split=1,
        batch_size=1,
        resize=256,
        imagesize=224,
        augment=False,
        num_workers=8,

    ))

    run_patchcore_mv.run(
        methods,
        model_save_path,
        gpu=[0],
        seed=0,
        log_group="group",
        log_project="project",
        save_segmentation_images=True,
        save_patchcore_model=True,

    )

    run_save_path = utils.create_storage_folder(
        model_save_path, "project", "group", mode="iterate"
    )

    model_save_path = os.path.join(
        run_save_path, "models", "mvtevc_" + data_name
                )
    return model_save_path
    

if __name__ == "__main__":
    train_by_path('solarboard',"/home/work/disk1/shipinchao/SynologyDrive/patchcore_data/solarboard/","/home/work/patchcore/model")
