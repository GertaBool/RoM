# FFreeListArray.h

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **66** `FFreeListArray::FFreeListArray<T>()`
- **78** `FFreeListArray::~FFreeListArray<T>()` (virtual)
  - calls: FFreeListArray::uninit
- **85** `FFreeListArray::init(int)` (virtual)
  - calls: FFreeListArray::uninit
  - called by (4): FFreeListArray::Read, FFreeListArray::insert, FFreeListArray::insertAt, FFreeListArray::insertFirst
- **109** `FFreeListArray::uninit()` (virtual)
  - calls: FFreeListArray::removeAll
  - called by (2): FFreeListArray::init, FFreeListArray::~FFreeListArray<T>
- **121** `FFreeListArray::insert(T)`
  - calls: FFreeListArray::init, FFreeListArray::growArray
  - called by (2): FFreeListArray::Read, FFreeListArray::insertFirst
- **154** `FFreeListArray::insertAt(T, int)`
  - calls: FFreeListArray::init, FFreeListArray::growArray
  - called by (1): FFreeListArray::insertFirst
- **221** `FFreeListArray::insertFirst(T)`
  - calls: FFreeListArray::init, FFreeListArray::growArray, FFreeListArray::insertAt, FFreeListArray::insert
- **250** `FFreeListArray::getAt(int)` (virtual)
  - called by (1): FFreeListArray::Write
- **270** `FFreeListArray::getIndex(T)`
- **295** `FFreeListArray::remove(T)`
  - calls: FFreeListArray::removeAt
- **317** `FFreeListArray::removeAt(int)`
  - called by (1): FFreeListArray::remove
- **338** `FFreeListArray::removeAll()` (virtual)
  - called by (1): FFreeListArray::uninit
- **360** `FFreeListArray::growArray()` (virtual)
  - called by (3): FFreeListArray::insert, FFreeListArray::insertAt, FFreeListArray::insertFirst
- **391** `FFreeListArray::Read(FDataStreamBase *)`
  - calls: FDataStreamBase::Read(int *) [FDataStreamBase.h], FFreeListArray::init, FDataStreamBase::Read(int, byte *) [FDataStreamBase.h], FFreeListArray::insert
- **409** `FFreeListArray::Write(FDataStreamBase *)`
  - calls: FDataStreamBase::Write(int) [FDataStreamBase.h], FFreeListArray::getAt, FDataStreamBase::Write(int, const byte *) [FDataStreamBase.h]
- **431** `ReadStreamableFFreeListArray(FFreeListArray<T> &, FDataStreamBase *)`
  - calls: FDataStreamBase::Read(int *) [FDataStreamBase.h]
- **452** `WriteStreamableFFreeListArray(FFreeListArray<T> &, FDataStreamBase *)`
  - calls: FDataStreamBase::Write(int) [FDataStreamBase.h]
