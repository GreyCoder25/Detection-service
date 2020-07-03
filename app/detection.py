import cv2
import torch
import numpy as np
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor


model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)


def read_image(path):
    img = cv2.imread(path)[:,:,::-1]
    img = cv2.resize(img, (100, 100), interpolation=cv2.INTER_AREA)
    return img


def plot_preds(numpy_img, preds):
  boxes = preds['boxes'].detach().cpu().numpy()
  for box in boxes:
    numpy_img = cv2.rectangle(
        numpy_img, 
        (box[0],box[1]),
        (box[2],box[3]), 
        255,
        3
    )
  #  print('Box drawn')
  # print(type(numpy_img))
  return numpy_img if type(numpy_img) is np.ndarray else numpy_img.get()


def perform_detection(img_numpy):
    global model
    model = model.eval()
    img = torch.from_numpy(img_numpy.astype('float32')).permute(2,0,1)
    img = img / 255.
    with torch.no_grad():
        print("Detection started...")
        predictions = model(img[None,...])
        print("Detection completed...")
        CONF_THRESH = 0.5
        boxes = predictions[0]['boxes'][predictions[0]['scores'] > CONF_THRESH]
        boxes_dict = {}
        boxes_dict['boxes'] = boxes
        img_with_boxes = plot_preds(img_numpy, boxes_dict).astype('uint')
    return img_with_boxes


def save_image(path, image):
    cv2.imwrite(path, image[:,:,::-1])


def detect(input_path, output_path):
    img = read_image(input_path)
    img_with_boxes = perform_detection(img)
    save_image(output_path, img_with_boxes)   



