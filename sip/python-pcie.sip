//Define the SIP wrapper to the python-pcie

%Module pcie

%Include vector.sip

class PythonPCIE {

    %TypeHeaderCode
    #include <vector>
    #include "../include/python_pcie.h"
    %End

    public:
        PythonPCIE (bool debug = false);
        ~PythonPCIE ();

        int open_pcie(const char * path, uint64_t size);
        bool is_open();
        int close_pcie();

        int write(uint64_t addr, std::vector<long> data);
        std::vector<long> read(uint64_t addr, uint64_t length);
};

// ************************************************************************
//  uint64_t
// ************************************************************************

%MappedType uint64_t
{
%TypeHeaderCode
#include <stdint.h>
%End

%ConvertFromTypeCode
    PyObject* pSize;
    pSize = PyLong_FromSize_t(*sipCpp);
    return pSize;
%End

%ConvertToTypeCode
    if (sipIsErr == NULL)
    {
        return (PyInt_Check(sipPy));
    }

    if (sipPy == Py_None)
    {
        *sipCppPtr = new uint64_t();
        return 1;
    }

    if (PyInt_Check(sipPy))
    {
        *sipCppPtr = new uint64_t(PyInt_AS_LONG(sipPy));
        return 1;
    }
    return 0;
%End
};

