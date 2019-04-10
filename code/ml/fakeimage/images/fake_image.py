import numpy as np
import cv2

from demo import Demo

model_path = './ckpt/exif_final/exif_final.ckpt'
model = Demo(ckpt_path=model_path, use_gpu=0, quality=3.0, num_per_dim=30)

def viz_spliced_region(res, orig):                                        
    orig_c = orig.copy()
    res = 255 - res * 255
    res = res.astype(np.uint8)
    cv2.imshow('res1', res); cv2.waitKey(0); cv2.destroyAllWindows()
    ex = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel, iterations=50)
    ret, thresh = cv2.threshold(ex, 127, 255,0)
    cv2.imshow('thresh', thresh); cv2.waitKey(0); cv2.destroyAllWindows()
    _, contours, hierarchy, = cv2.findContours(255-thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    im_size = res.shape[0] * res.shape[1]
    valid_contours = []
    print(contours)
    for i, cnt in enumerate(contours):
        x,y,w,h = cv2.boundingRect(cnt)
        cnt_size = w * h
        print(cnt_size, " - ", im_size)
        if cnt_size > 0.05 * im_size:
            cv2.rectangle(orig_c, (x,y), (x+w, y+h), (0, 255, 0), 3)
    print(len(valid_contours))
    return orig_c


if __name__ == '__main__':
    im_test = './images/demo.png'
    orig_img, res = model(im_test, dense=True)
    spliced_img = viz_spliced_region(res, orig_img)
    cv2.imshow('im', ret)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

