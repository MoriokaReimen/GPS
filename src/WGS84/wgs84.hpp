#pragma once
#include <vector>
using std::vector;

double toDeg(const double& radian);
double toRad(const double& degree);
vector<double> llh2ecef(const double& longitude, const double& latitude, const double& height);
vector<double> ecef2llh(const double& x, const double& y, const double& z);
