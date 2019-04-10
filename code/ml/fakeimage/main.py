from demo import Demo
import cv2
import matplotlib.pyplot as plt
import numpy as np
from base64 import b64encode
plt.switch_backend('agg')

class FakeImageDetectionModel():

    def __init__(self):
        ckpt_path = './ckpt/exif_final/exif_final.ckpt'
        self.model = Demo(ckpt_path=ckpt_path, use_gpu=0, quality=3.0, num_per_dim=30)

    def process(self, res, orig):                                        
        orig_c = orig.copy()
        res = 255 - res * 255
        res = res.astype(np.uint8)
        kernel = np.ones((5,5),np.uint8)
        ex = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel, iterations=50)
        ret, thresh = cv2.threshold(ex, 127, 255,0)
        cv2.imshow('thresh', thresh); cv2.waitKey(0); cv2.destroyAllWindows()
        _, contours, hierarchy, = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        im_size = res.shape[0] * res.shape[1]
        valid_contours = []
        for i, cnt in enumerate(contours):
            x,y,w,h = cv2.boundingRect(cnt)
            cnt_size = w * h
            cv2.rectangle(orig_c, (x,y), (x+w, y+h), (0, 255, 0), 3)
            valid_contours.append(1)
        print("{} Spliced regions detected".format(len(valid_contours)))
        return orig_c


    def detect(self, im_path)
        im, res = self.model(im_path, dense=True)
        final_img = self.process(res, im)
        cv2.imwrite('demo.png', final_img)
        imageb64 = b64encode.encode(open('demo.png', 'rb'))
        return imageb64

