/* -*- mode:c++ -*- */

/** @file

This is the SIP interface definition for std::vector

Copyright (C)  2002-2004  The Board of Trustees of
The Leland Stanford Junior University.  All Rights Reserved.

$Id: vector.sip,v 1.10 2005/06/17 18:08:00 pfkeb Exp $

@author Paul_Kunz@slac.stanford.edu

*/


%MappedType std::vector<long>
{
%TypeHeaderCode
#include <vector>
%End

%ConvertFromTypeCode
	// Handle no list.

	if (!sipCpp)
		return PyList_New(0);

	// Convert to a Python list of ints

	PyObject *l;

	// Create the list.
	int size = static_cast < int > ( sipCpp -> size () );
	if ( ( l = PyList_New ( size ) ) == NULL)
		return NULL;

	// Get it.

	for ( unsigned int i = 0; i < sipCpp -> size(); ++i) {
          long j = sipCpp -> operator [] ( i );
          if ( PyList_SetItem ( l, i, PyInt_FromLong ( j ) ) < 0 )
		{
			Py_DECREF(l);

			return NULL;
		}
	}
	return l;
%End

%ConvertToTypeCode
	// Convert a Python list of int to a vector<long> on the heap.

	if (sipIsErr == NULL)
		return PyList_Check(sipPy);

	if (sipPy == Py_None)
	{
		*sipCppPtr = NULL;

		return 0;
	}
        int size = PyList_GET_SIZE(sipPy);
        std::vector <long> *qvl = new std::vector <long> ( size );
	PyErr_Clear();

	for (int i = 0; i < size; ++i)
	{
	  long j = ((long)PyInt_AsLong(PyList_GET_ITEM(sipPy,i)));

		if (PyErr_Occurred() != NULL)
		{
			delete qvl;
			*sipIsErr = 1;

			return 0;
		}
		qvl -> operator [] (i) = j;
	}

	*sipCppPtr = qvl;

	return 1;
%End
};


%MappedType std::vector<int>
{
%TypeHeaderCode
#include <vector>
%End

%ConvertFromTypeCode
	// Handle no list.

	if (!sipCpp)
		return PyList_New(0);

	// Convert to a Python list of ints

	PyObject *l;

	// Create the list.
	int size = static_cast < int > ( sipCpp -> size () );
	if ( ( l = PyList_New ( size ) ) == NULL)
		return NULL;

	// Get it.

	for ( unsigned int i = 0; i < sipCpp -> size(); ++i) {
          long j = sipCpp -> operator [] ( i );
          if ( PyList_SetItem ( l, i, PyInt_FromLong ( j ) ) < 0 )
		{
			Py_DECREF(l);

			return NULL;
		}
	}
	return l;
%End

%ConvertToTypeCode
	// Convert a Python list of int to a vector<int> on the heap.

	if (sipIsErr == NULL)
		return PyList_Check(sipPy);

	if (sipPy == Py_None)
	{
		*sipCppPtr = NULL;

		return 0;
	}
        int size = PyList_GET_SIZE(sipPy);
        std::vector < int> *qvl = new std::vector < int > ( size );
	PyErr_Clear();

	for (int i = 0; i < size; ++i)
	{
	  long j = ((long)PyInt_AsLong(PyList_GET_ITEM(sipPy,i)));

		if (PyErr_Occurred() != NULL)
		{
			delete qvl;
			*sipIsErr = 1;

			return 0;
		}
		qvl -> operator [] (i) = j;
	}

	*sipCppPtr = qvl;

	return 1;
%End
};




%MappedType std::vector<char>
{
%TypeHeaderCode
#include <vector>
%End

%ConvertFromTypeCode
	// Handle no list.

	if (!sipCpp)
		return PyList_New(0);

	// Convert to a Python list of ints

	PyObject *l;

	// Create the list.
	int size = static_cast < int > ( sipCpp -> size () );
	if ( ( l = PyList_New ( size ) ) == NULL)
		return NULL;

	// Get it.

	for ( unsigned int i = 0; i < sipCpp -> size(); ++i) {
          long j = sipCpp -> operator [] ( i );
          if ( PyList_SetItem ( l, i, PyInt_FromLong ( j ) ) < 0 )
		{
			Py_DECREF(l);

			return NULL;
		}
	}
	return l;
%End

%ConvertToTypeCode
	// Convert a Python list of int to a vector<int> on the heap.

	if (sipIsErr == NULL)
		return PyList_Check(sipPy);

	if (sipPy == Py_None)
	{
		*sipCppPtr = NULL;

		return 0;
	}
        int size = PyList_GET_SIZE(sipPy);
        std::vector<char>*qvl = new std::vector<char>( size );
	PyErr_Clear();

	for (int i = 0; i < size; ++i)
	{
	  long j = ((long)PyInt_AsLong(PyList_GET_ITEM(sipPy,i)));

		if (PyErr_Occurred() != NULL)
		{
			delete qvl;
			*sipIsErr = 1;

			return 0;
		}
		qvl -> operator [] (i) = (char) j;
	}

	*sipCppPtr = qvl;

	return 1;
%End
};


