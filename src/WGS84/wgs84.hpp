#pragma once
#include <boost/python.hpp>

struct XYZ {
        double x {0};
        double y {0};
        double z {0};
};

double toDeg(const double& radian);
double toRad(const double& degree);
XYZ blh2ecef(const double& longitude, const double& latitude, const double& height = 0.0);
