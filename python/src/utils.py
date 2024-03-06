import torch
import torchvision
import torchvision.transforms as transforms
import numpy as np

MODEL = torchvision.models.resnet101(pretrained=True)
MODEL.eval().cpu()

TRANSFORM = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

torch.set_num_threads(1)


def classify_image(img_frame: np.array) -> int:
    """Classify the input image with the ResNet101 model.

    :param img_frame: image frame of shape (360, 640, 3) and dtype uint8
    :return: the class index of the predicted class
    """
    img_tensor = TRANSFORM(
        torch.from_numpy(img_frame).permute(2, 0, 1).unsqueeze(0).float() / 255.0
    )

    with torch.no_grad():
        logits = MODEL(img_tensor)
        probs = torch.nn.functional.softmax(logits, dim=1)
        idx = torch.argmax(probs, dim=1)

    return idx.item()
