# Sanic Project

## Setup

`pip install sanic`

## Run

`git clone https://github.com/dobatruong1111/sanic_project.git`
`cd sanic_project` <br/>
`sanic main.app`

## Demo

### APIs

#### Get Cone Image

GET `http://localhost:8000/get_image` <br/>
GET `http://localhost:8000/get_image?position=5&roll=180&azimuth=90&elevation=90`

#### Get Dicom Image

GET `http://localhost:8000/get_image_dicom` <br/>
GET `http://localhost:8000/get_image_dicom?position=500&roll=90&azimuth=90&elevation=90`

## Mô tả

### Thao tác với camera: <br/>

![picture](./output/camera.png)
<br/>

Xét khoảng clipping range là: 0.1...5000 <br/>
Xét vị trí ban đầu của camera là: (0, 0, 0.1) <br/>

Ảnh ban đầu: <br/>
![picture](./output/original_image.png)

Ảnh sau khi xét position bằng 500: <br/>
![picture](./output/setposition.png)

Ảnh sau khi xoay 90 độ quanh trục z (roll): <br/>
![picture](./output/roll90.png)

Ảnh sau khi xoay 90 độ quanh trục y (azimuth): <br/>
![picture](./output/azimuth90.png)

Ảnh sau khi xoay 90 độ quanh trục x (elevation): <br/>
![picture](./output/ele90.png)

Ảnh sau khi xoay 90 độ quanh theo cả 3 trục tọa độ lần lượt z (roll), y (azimuth), x (elevation): <br/>
![picture](./output/final_image.png)
