/* Minimal python24.dll replacement for running CvGameCoreDLL headlessly.
 * The harness reports Python as uninitialized, so events and callbacks are
 * skipped; these functions only need to return well-formed inert objects for
 * the argument lists the DLL still builds before calling into the engine.
 * Nothing here allocates per call (see inert and PyInt_FromLong). */
#include <stdlib.h>
#include <string.h>

typedef struct _typeobject PyTypeObject;
typedef struct _object { int ob_refcnt; PyTypeObject* ob_type; } PyObject;
typedef void (*destructor)(PyObject*);
/* Python 2.4 PyTypeObject prefix up to tp_dealloc; the rest is padding. */
struct _typeobject { int ob_refcnt; PyTypeObject* ob_type; int ob_size; const char* tp_name;
	int tp_basicsize, tp_itemsize; destructor tp_dealloc; char pad[400]; };

static void inert_dealloc(PyObject* o) { (void)o; }

__declspec(dllexport) PyTypeObject PyList_Type = { 1 << 30, 0, 0, "list", 0, 0, inert_dealloc };
__declspec(dllexport) PyTypeObject PyTuple_Type = { 1 << 30, 0, 0, "tuple", 0, 0, inert_dealloc };
static PyTypeObject Inert_Type = { 1 << 30, 0, 0, "inert", 0, 0, inert_dealloc };
/* Integers keep their value so the harness can evaluate callback defaults that
 * depend on arguments (e.g. getExperienceNeeded). Layout: refcnt, type, value. */
static PyTypeObject Int_Type = { 1 << 30, 0, 0, "int", 0, 0, inert_dealloc };
typedef struct { int ob_refcnt; PyTypeObject* ob_type; long ob_ival; } IntObj;
__declspec(dllexport) PyObject _Py_NoneStruct = { 1 << 30, &Inert_Type };

/* One shared inert object: nothing reads it, and its type's dealloc is a no-op.
 * (A fresh allocation per call leaked a few hundred bytes for every Python
 * callback the DLL prepares, which exhausted the address space late in long games.) */
static PyObject g_inert = { 1 << 30, &Inert_Type };
static PyObject* inert(void) { return &g_inert; }

typedef struct { int ob_refcnt; PyTypeObject* ob_type; int ob_size; PyObject* ob_item[1]; } TupleObj;
typedef struct { int ob_refcnt; PyTypeObject* ob_type; int ob_size; PyObject** ob_item; int allocated; } ListObj;

__declspec(dllexport) PyObject* PyTuple_New(int n)
{
	TupleObj* t = (TupleObj*)calloc(1, sizeof(TupleObj) + sizeof(PyObject*) * (n > 0 ? n : 1));
	t->ob_refcnt = 1 << 30; t->ob_type = &PyTuple_Type; t->ob_size = n;
	return (PyObject*)t;
}
__declspec(dllexport) PyObject* PyList_New(int n)
{
	ListObj* l = (ListObj*)calloc(1, sizeof(ListObj));
	l->ob_refcnt = 1 << 30; l->ob_type = &PyList_Type; l->ob_size = n; l->allocated = n;
	l->ob_item = (PyObject**)calloc(n > 0 ? n : 1, sizeof(PyObject*));
	return (PyObject*)l;
}
__declspec(dllexport) int PyList_SetItem(PyObject* l, int i, PyObject* v)
{
	ListObj* p = (ListObj*)l;
	if (i < 0 || i >= p->ob_size) return -1;
	p->ob_item[i] = v;
	return 0;
}
__declspec(dllexport) int PySequence_Size(PyObject* o)
{
	if (o && (o->ob_type == &PyList_Type || o->ob_type == &PyTuple_Type)) return ((ListObj*)o)->ob_size;
	return 0;
}
__declspec(dllexport) PyObject* PySequence_GetItem(PyObject* o, int i)
{
	if (o && o->ob_type == &PyList_Type && i >= 0 && i < ((ListObj*)o)->ob_size && ((ListObj*)o)->ob_item[i]) return ((ListObj*)o)->ob_item[i];
	if (o && o->ob_type == &PyTuple_Type && i >= 0 && i < ((TupleObj*)o)->ob_size && ((TupleObj*)o)->ob_item[i]) return ((TupleObj*)o)->ob_item[i];
	return inert();
}
__declspec(dllexport) long PyInt_AsLong(PyObject* o) { return (o && o->ob_type == &Int_Type) ? ((IntObj*)o)->ob_ival : 0; }
__declspec(dllexport) int PyObject_IsInstance(PyObject* a, PyObject* b) { (void)a; (void)b; return 0; }
__declspec(dllexport) PyObject* PyLong_FromUnsignedLong(unsigned long v) { (void)v; return inert(); }
__declspec(dllexport) PyObject* PyString_FromStringAndSize(const char* s, int n) { (void)s; (void)n; return inert(); }
__declspec(dllexport) PyObject* PyUnicodeUCS2_FromWideChar(const unsigned short* s, int n) { (void)s; (void)n; return inert(); }
__declspec(dllexport) PyObject* PyString_FromString(const char* s) { (void)s; return inert(); }
__declspec(dllexport) PyObject* PyFloat_FromDouble(double d) { (void)d; return inert(); }
/* Integers come from a ring: an argument list is read by the harness right after
 * the DLL builds it, long before the ring wraps. */
static IntObj g_ints[1 << 16];
static unsigned g_nextInt;
__declspec(dllexport) PyObject* PyInt_FromLong(long v)
{
	IntObj* o = &g_ints[g_nextInt++ & ((1 << 16) - 1)];
	o->ob_refcnt = 1 << 30; o->ob_type = &Int_Type; o->ob_ival = v;
	return (PyObject*)o;
}
__declspec(dllexport) PyObject* PyBool_FromLong(long v) { (void)v; return inert(); }
