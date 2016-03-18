//Define the SIP wrapper to the python-pcie

%Module pcie

class PythonPCIE {

    %TypeHeaderCode
    #include "../include/python_pcie.h"
    %End

    public:
        PythonPCIE (bool debug = false);
        ~PythonPCIE ();

        int open_pcie(const char * path, uint64_t size);
        bool is_open();
        int close_pcie();

        int write(uint64_t addr, uint64_t count, const uint8_t * data);
        int read(uint64_t addr, uint64_t count, uint8_t * data);
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



// ************************************************************************
//  uint8_t
// ************************************************************************

%MappedType uint8_t
{
%TypeHeaderCode
#include <stdint.h>
%End

%ConvertFromTypeCode
    PyObject* pSize;
    pSize = PyInt_FromSize_t(*sipCpp);  
    return pSize;
%End

%ConvertToTypeCode
    if (sipIsErr == NULL)
    {
        return (PyInt_Check(sipPy));
    }

    if (sipPy == Py_None)
    {
        *sipCppPtr = new uint8_t();
        return 1;
    }

    if (PyInt_Check(sipPy))
    {
        *sipCppPtr = new uint8_t(PyInt_AS_LONG(sipPy)); 
        return 1;
    }
    return 0;
%End
};


