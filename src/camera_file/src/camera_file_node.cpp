#include <sensor_msgs/Image.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/opencv.hpp>
#include <ros/ros.h>

using namespace cv;


int main(int argc, char* argv[]) {
    ros::init(argc, argv, "img_puber");
    ros::NodeHandle nh;
    image_transport::ImageTransport it(nh);
    image_transport::Publisher publisher = it.advertise("send_pic", 1);
    cv::VideoCapture capture;
	capture = cv::VideoCapture(0);
    capture.set(3,640);
    capture.set(4,480);
    
    ros::Rate rate(30);
    cv::Mat img;
    while(ros::ok())
    {
        capture >> img;
        //cv::imshow("RAW", img);
        std_msgs::Header header;
	    sensor_msgs::ImagePtr msg = cv_bridge::CvImage(header, "bgr8", img).toImageMsg();
        publisher.publish(msg);
        //if(cv::waitKey(10) == 27)
        //{
        //    break;    
        //}
        ros::spinOnce();
        rate.sleep();
    }
}