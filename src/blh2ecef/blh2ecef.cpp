#include "blh2ecef.hpp"
#include <memory>
#include <utility>
#include <cmath>
using std::sqrt;
using std::sin;
using std::cos;

double toDeg(const double& radian)
{
  return radian * 180 / M_PI;
}

double toRad(const double& degree)
{
  return degree * M_PI / 180.0;
}

XYZ blh2ecef(const double& longitude, const double& latitude, const double& height)
{
  XYZ ecef;
  const double f = 1 / 298.257223563;
  const double e = sqrt(2 * f - f * f);
  double N = 6378137.0 / sqrt(1 - e * e * sin(longitude));

  ecef.x = (N + height) * cos(toRad(longitude)) * cos(toRad(latitude));
  ecef.y = (N + height) * cos(toRad(longitude)) * sin(toRad(latitude));
  ecef.z = (N * (1 - e * e) + height) * sin(toRad(longitude));

  return ecef;
}
