#include "wgs84.hpp"
#include <vector>
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
using namespace boost::python;
using std::vector;

BOOST_PYTHON_MODULE(wgs84)
{
        def("llh2ecef", llh2ecef);
        def("ecef2llh", ecef2llh);
        class_<vector<double>>("vector<double>")
          .def(vector_indexing_suite<vector<double>>());
}

