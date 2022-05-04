#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/highgui/highgui.hpp>


void imageCallback(const sensor_msgs::ImageConstPtr &msg)
{
    cv::imshow("listner", cv_bridge::toCvShare(msg, "bgr8")->image);
    cv::waitKey(10);
}

int main(int argc, char *argv[])
{
    /*初始化节点，并设定节点名*/
    ros::init(argc, argv, "img_listener");
    /*设置节点句柄*/  
    ros::NodeHandle n;
    /*设置图像接受的节点*/
    image_transport::ImageTransport it(n);
    /*设置图像订阅者*/
    image_transport::Subscriber sub = it.subscribe("send_pic", 1, imageCallback);

    /*回调响应循环*/
    ros::spin();

    return 0;
}

