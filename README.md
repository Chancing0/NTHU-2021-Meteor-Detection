# NTHU-2021-Meteor
### Google colab Version: Meteor.ipynb
#### https://drive.google.com/file/d/1u_BQHLNkfTSnRBD2Spj-0l0nZp4zg4I8/view?usp=sharing
# Usage ： find_meteor.py
    python find_meteor.py [input_path] [output_path]  
    example: python find_meteor.py ./2020-11-11 ./2020-11-11-find  

## 方法流程：  
1.讀取灰階圖  
2.canny邊緣偵測  
3.將手動繪製的mask,罩到（2）的canny結果上  
4.因爲canny的結果綫是不連續或者中空，所以使用膨脹算法兩次，讓綫和中空補起來。  
5.再將（4）進行侵蝕一次，防止noise也被膨脹太大，放大其對測直綫的不良影響。并且本次侵蝕不會讓（4）的綫再斷開或者中空，而且把邊緣綫稍微變細一點。  
6.初步去除雲霧：通過先找到（5）許多contour點，然後把每組點填充滿為白色並進行一次膨脹去減少邊緣綫，這樣就有了雲霧的大面積遮罩，並計算其面積，設定單個面積大於 1550 才保留該遮罩，然後將這個遮罩應用到（5）上，這樣就可以把雲霧的綫初步除掉，留下相對乾净的邊緣綫。  
7.根據是否找到面積大於 1550 的遮罩去決定使用（5）還是（6）的結果去做直綫偵測。如果測到還有直綫存在，就當作可能有流星，然後保存下來檔名，或者直接存這些圖下來。  
| processing  |  example 1 |example 2|
|---|---|---|
| (0) Raw iamge|  ![](https://i.imgur.com/Rganqfw.png)|![](https://i.imgur.com/8Yb2kSU.png)|
| (1) Loading image  |  ![](https://i.imgur.com/di9KnR2.png) |  ![](https://i.imgur.com/KtbXhrD.png) |
| (2) Edge detection : Canny |  ![](https://i.imgur.com/mS1lLdA.png) | ![](https://i.imgur.com/pobFtF1.png)  |
| (3) Apply the mask to the result of edge detection  |![](https://i.imgur.com/wWNwwql.png)![](https://i.imgur.com/tYwkhXm.png)  | ![](https://i.imgur.com/TD1lgmI.png)![](https://i.imgur.com/w7zdha8.png)  |
|(4) Line dilatation:  dilate|  ![](https://i.imgur.com/17sEB8F.png) |![](https://i.imgur.com/EDxZmaH.png)|
|(6) Cloudy detection and mask producing:  findContours , drawContours|  ![](https://i.imgur.com/w9mI4hl.png)![](https://i.imgur.com/GHuT2oG.png)   |![](https://i.imgur.com/6MM1DbS.png)![](https://i.imgur.com/hJ2kZ1N.png)|
|(7) Line detection :  HoughLinesP|  ![](https://i.imgur.com/qSOWlFi.png)  |![](https://i.imgur.com/HNgRMFk.png)|
