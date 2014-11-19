#include "blh2ecef.hpp"
using namespace boost::python;

BOOST_PYTHON_MODULE(ecef)
{
  class_<XYZ>("XYZ")
    .def_readwrite("x", &XYZ::x)
    .def_readwrite("y", &XYZ::y)
    .def_readwrite("z", &XYZ::z);

  def("blh2ecef", blh2ecef);
}

