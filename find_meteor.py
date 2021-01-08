# Run python find_meteor.py [input_path] [output_path]
# Run example: python find_meteor.py ./2020-11-11 ./2020-11-11-find

def method1(img_path, mask, show_all_step=False, minimal_lenth=300):
  import cv2
  import numpy as np
  from scipy.spatial import distance as dist

  # (1) Loading image 
  img = cv2.imread(img_path)
  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # (2) Edge detection : Canny
  img_gray_canny = cv2.Canny(img_gray.astype(np.uint8),50,100,apertureSize=3)

  # (3) Apply the mask to the result of edge detection
  img_gray_canny_crop = img_gray_canny*(mask/255)
  img_gray_canny_crop = img_gray_canny_crop.astype(np.uint8)

  # (4) Line dilatation
  kernel = np.ones((3,3), np.uint8)
  dilation = cv2.dilate(img_gray_canny_crop, kernel, iterations = 2)
  # (5) Line erosion
  dilation = cv2.erode(dilation, kernel, iterations = 1)
  # (6) Cloudy detection and mask producing
  cloud_mask = np.zeros(dilation.shape,np.uint8)
  contour,hier = cv2.findContours(dilation,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
  contour_able = 0
  try:
    for cnt in contour:
      area = cv2.contourArea(cnt)
      if area > 1550:
        #print(area)
        contour_able = 1
        cv2.drawContours(cloud_mask,[cnt],0,255,-1)
  except:
    contour_able = 0

  if contour_able==1:
    #print('It\'s Cloudy')
    kernel_dilate = np.ones((7,7), np.uint8)
    #contour_maks = cv2.dilate(cv2.bitwise_not(aa), kernel_dilate, iterations = 1)
    #dilation_mask = dilation * contour_maks
    dilation_mask = dilation * cv2.dilate(cv2.bitwise_not(cloud_mask), kernel_dilate, iterations = 1)
    dilation_mask = 255*dilation_mask
  else: 
    #print('Nice Weather')
    dilation_mask = dilation
  # (7) Line detection
  lines = cv2.HoughLinesP(dilation_mask,3,np.pi/180,100,minimal_lenth,20)
  try:
    # Draw the detected line on the image
    counter = 0
    for i in range(lines.shape[0]):
      for x1,y1,x2,y2 in lines[i]:
        if dist.euclidean((x1, y1), (x2, y2)) > 50:
          counter +=1
          cv2.line(img,(x1,y1),(x2,y2),(0,0,255),10)
    # Show result   
    if counter != 0:
      #print(lines.shape,' After threshold: ',counter)
      if show_all_step:
        #result = cv2.hconcat((cv2.cvtColor(img_gray_canny_crop, cv2.COLOR_GRAY2BGR), cv2.cvtColor(dilation, cv2.COLOR_GRAY2BGR), cv2.cvtColor(aa, cv2.COLOR_GRAY2BGR), cv2.cvtColor(dilation_mask, cv2.COLOR_GRAY2BGR), img))
        result1 = cv2.hconcat((cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR), cv2.cvtColor(img_gray_canny, cv2.COLOR_GRAY2BGR), cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), cv2.cvtColor(img_gray_canny_crop, cv2.COLOR_GRAY2BGR)))
        result2 = cv2.hconcat((cv2.cvtColor(dilation, cv2.COLOR_GRAY2BGR), cv2.cvtColor(Cloud_mask, cv2.COLOR_GRAY2BGR), cv2.cvtColor(dilation_mask, cv2.COLOR_GRAY2BGR),img))
        result = cv2.vconcat([result1, result2])
        cv2_imshow(result)
      return 1
    else: 
      #print('No lines was detected')
      return 0
  except:
    # The error comes from the data type of lines when No lines was detected
    #print('No lines was detected')
    return 0


def find_meteor(file_list, show_result=False, save_image=False, save_csv=False, save_path=None):
  import time
  start_time = time.perf_counter()

  find_list = []
  print(file_list[0])
  mask = mask_generation()
  for img_path in file_list:
    #print(img_path)
    if method1(img_path,mask,show_result): find_list.append(img_path)
  print('Finished')
  finished_time = time.perf_counter()
  spend = finished_time - start_time
  print("Time Consumed：{}s".format(spend))
  #print(find_list)
  print('Find : Total = ',len(find_list),'/',len(file_list),' = ',round(100*len(find_list)/len(file_list),2),'%')

  if save_image:
    import os 
    from shutil import copyfile
    os.makedirs(save_path,exist_ok=True)
    # save image to folder
    for filename in find_list:
      save_file_path= save_path+'/'+os.path.basename(filename)
      copyfile(filename, save_file_path)
    print('Saving the meteor images at the path of : '+save_path)
  
  if save_csv:
    import pandas as pd
    name=['File Name']
    csv=pd.DataFrame(columns=name,data=find_list)
    #print(test)
    csv.to_csv(save_path+'/result.csv',encoding='gbk')
    print('Saving the find_list at the path of : '+save_path+'/result.csv')
  return find_list
  
def mask_generation(high=2080, width=3096):
  print('-------mask generation-----')
  import cv2
  import numpy as np
  mask=np.zeros((high,width),np.uint8)
  cv2.circle(mask,(int(width/2),int(high/2)),1000,(255),-1)
  cv2.circle(mask,(int(width/2),int(high/2)),50,(0),-1)
  mask[0:100,:] = 0
  mask[mask.shape[0]-100:mask.shape[0],:] = 0
  mask[1800:mask.shape[0], 750:850] = 0
  print('-------mask generation Finished-----')
  return mask

if __name__ == '__main__':
  import sys
  import glob

  file_list = glob.glob(sys.argv[1] + '/*__1[7-9]*.jpg')
  file_list.extend(glob.glob(sys.argv[1] + '/*__2[0-3]*.jpg'))
  file_list.extend(glob.glob(sys.argv[1] + '/*__0[0-5]*.jpg'))

  find_list = []
  find_list = find_meteor(file_list, save_path=sys.argv[2],save_image=True,save_csv=True)
