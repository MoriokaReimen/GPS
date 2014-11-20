#include "wgs84.hpp"
#include <cmath>
#include <vector>
using std::sqrt;
using std::sin;
using std::cos;
using std::atan;
using std::vector;

const double A = 6378137.0;
const double B = 6356752.3142;
const double F = 1.0 / 298.257223563;
const double E = sqrt(2.0 * F - F * F);
const double Er = sqrt((A * A - B * B)/ B * B);

double toDeg(const double& radian)
{
        return radian * 180 / M_PI;
}

double toRad(const double& degree)
{
        return degree * M_PI / 180.0;
}

vector<double> llh2ecef(const double& longitude, const double& latitude, const double& height)
{
        vector<double> ecef;
        const double n = A / sqrt(1.0 - E * E * sin(toRad(latitude)) * sin(toRad(latitude)));

        ecef.push_back((n + height) * cos(toRad(longitude)) * cos(toRad(latitude)));
        ecef.push_back((n + height) * sin(toRad(longitude)) * cos(toRad(latitude)));
        ecef.push_back(((n * (1.0 - E * E)) + height) * sin(toRad(latitude)));

        return ecef;
}

vector<double> ecef2llh(const double& x, const double& y, const double& z)
{
        double longitude{0.0};
        double latitude{0.0};
        double height{0.0};

        double p = sqrt(x * x + y * y);
        double theta = atan(z * A / p / B);

        latitude = atan(
            (z + Er * Er * B * pow(sin(theta), 3)) /
            (p - E * E * A * pow(cos(theta), 3)));
        longitude = atan(y / x);
        double n = A / sqrt(1.0 - E * E * sin(latitude) * sin(latitude));
        height = p / cos(latitude) - n;

        vector<double>
          llh{toDeg(longitude), toDeg(latitude), height};

        return llh;
}
