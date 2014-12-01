/**
-----------------------------------------------------------------------------
@file    wgs84.cpp
----------------------------------------------------------------------------
         @@
       @@@@@@
      @```@@@@
     @`  `@@@@@@
   @@`   `@@@@@@@@
  @@`    `@@@@@@@@@           Tohoku University
  @` `   `@@@@@@@@@       SPACE ROBOTICS LABORATORY
  @`` ## `@@@@@@@@@    http://www.astro.mech.tohoku.ac.jp/
  @` #..#`@@@@@@@@@        Planetary Robotics Group
  @` #..#`@@@@@@@@@
  @` ### `@@@@@@@@@          Professor Kazuya Yoshida
  @` ###``@@@@@@@@@      Associate Professor Keiji Nagatani
   @### ``@@@@@@@@
   ###  ` @@@@@@@
  ###  @  @@@@@                 Creation Date:
 ###    @@@@@               @date Nov. 21. 2014
 /-\     @@
|   |      %%                      Authors:
 \-/##    %%%%%             @author Kei Nakata
   #### %%%                  menschenjager.mark.neun@gmail.com
     ###%%       *
      ##%%     *****
       #%%      ***
        %%     *   *
         %%
          %%%%%
           %%%
-----------------------------------------------------------------------------
@brief wgs84 manipulation functions for gps data analysis
-----------------------------------------------------------------------------
*/
#include "wgs84.hpp"
#include <cmath>
#include <vector>
using std::sqrt;
using std::sin;
using std::cos;
using std::atan2;
using std::vector;
using std::copysign;
/**
 *  Global variables of Earth's geometric constants
 */
const double A = 6378137.0; /**< Equational Radius [m] */
const double B = 6356752.3142; /**< Polar Radius [m]  */
const double F = 1.0 / 298.257223563; /**< flattening */
const double E = sqrt((A * A - B * B)/(A * A)); /**< Eccentricity */
const double Er = sqrt((A * A - B * B)/(B * B)); /**< Second Eccentricity */

/*!
 * Convert radian to degree
 * @param[in] radian angle in radian
 * @return angle in degree
 */
double toDeg(const double& radian)
{
        return radian * 180 / M_PI;
}

/*!
 * Convert degree to radian
 * @param[in] degree angle in degree
 * @return angle in radian
 */
double toRad(const double& degree)
{
        return degree * M_PI / 180.0;
}

/*!
 * Convert longitude, latitude, height to X, Y, Z in wgs84
 * @param[in] longitude in degree
 * @param[in] latitude in degree
 * @param[in] height in meter
 * @return ecef vector<double> contains X, Y, Z in wgs84
 */
vector<double> llh2ecef(const double& longitude, const double& latitude, const double& height)
{
        vector<double> ecef;
        const double n = A / sqrt(1.0 - E * E * sin(toRad(latitude)) * sin(toRad(latitude)));

        ecef.push_back((n + height) * cos(toRad(longitude)) * cos(toRad(latitude)));
        ecef.push_back((n + height) * sin(toRad(longitude)) * cos(toRad(latitude)));
        ecef.push_back(((n * (1.0 - E * E)) + height) * sin(toRad(latitude)));

        return ecef;
}

/*!
 * Convert X, Y, Z in wgs84 to longitude, latitude, height
 * @param[in] x in meter
 * @param[in] y in meter
 * @param[in] z in meter
 * @return llh vector<double> contains longitude, latitude, height
 */
vector<double> ecef2llh(const double& x, const double& y, const double& z)
{
        double longitude {0.0}; /*< longitude in radian */
        double latitude {0.0}; /*< latitude in radian */
        double height {0.0}; /*< height in meter */

        double p = sqrt((x * x) + (y * y));
        double theta = atan2((z * A), (p * B));

        /* Avoid 0 division error */
        if(x == 0.0 && y == 0.0) {
                vector<double>
                llh {0.0, copysign(90.0,z), z - copysign(B,z)};
                return llh;
        } else {

                latitude = atan2(
                                   (z + (Er * Er * B * pow(sin(theta), 3))),
                                   (p - (E * E * A * pow(cos(theta), 3)))
                           );
                longitude = atan2(y, x);
                double n = A / sqrt(1.0 - E * E * sin(latitude) * sin(latitude));
                height = p / cos(latitude) - n;

                vector<double>
                llh {toDeg(longitude), toDeg(latitude), height};

                return llh;
        }
}
