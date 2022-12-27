# Sanic Project

## Setup

`pip install sanic`

## Run

`cd get-image-sanic-project` <br/>
`sanic main.app`

## Demo

### APIs

#### Get Cone Image

GET `http://localhost:8000/get_image` <br/>
Thêm các parameter: <br/>
GET `http://localhost:8000/get_image?position=5&roll=180&azimuth=90&elevation=90`

#### Get Dicom Image

GET `http://localhost:8000/get_image_dicom` <br/>
Thêm các parameter: <br/>
GET `http://localhost:8000/get_image_dicom?position=1000&roll=90&azimuth=90&elevation=90`

## Mô tả

### Gửi Request lên Web Server, Response là một ảnh dạng png

#### Thao tác với camera: <br/>

![picture](./output/camera.png)
xét khoảng clipping range là 0.1...5000 <br/>
xét vị trí ban đầu của camera là (0, 0, 0.1) <br/>
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

Ảnh sau khi xoay quanh theo cả 3 trục tọa độ lần lượt z (roll), y (azimuth), x (elevation): <br/>
![picture](./output/final_image.png)
