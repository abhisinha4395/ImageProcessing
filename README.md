# ImageProcessing

Use the command below to fulfill the dependencies

```
pip install Pillow
```

## Design Approach
* This module uses the Strategy Design Pattern to structure its code as there can be multiple algorithms that can be used to resize the images.
* The fastest way possible to go through the 1L images is to do bulk processing.
* The module divides the workload equally among all the cores present  w.r.t their sizes in descending order.
* Since AWS S3 API doesn't support bulk upload to S3, the module uses the AWS CLI command to do bulk updates to the storage, thus saving time.  
