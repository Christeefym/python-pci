TARGET = pcie.so
OFILES = sippciecmodule.o sippcieuint64_t.o sippciePythonPCIE.o sippciestdvector1400.o sippciestdvector1800.o sippciestdvector2000.o
HFILES = sipAPIpcie.h 

CC = gcc
CXX = g++
LINK = g++
CPPFLAGS = -DNDEBUG -I. -I/usr/include/python2.7
CFLAGS =  -g -O2 -fstack-protector-strong -Wformat -Werror=format-security  -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -Wall -W
CXXFLAGS =  -g -O2 -fstack-protector-strong -Wformat -Werror=format-security  -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -Wall -W
LFLAGS =  -Wl,-Bsymbolic-functions -Wl,-z,relro -shared -Wl,--version-script=pcie.exp
LIBS = -L../lib
.SUFFIXES: .c .o .cpp .cc .cxx .C


.cpp.o:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

.cc.o:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

.cxx.o:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

.C.o:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

.c.o:
	$(CC) -c $(CFLAGS) $(CPPFLAGS) -o $@ $<

all: $(TARGET)

$(OFILES): $(HFILES)

$(TARGET): $(OFILES)
	@echo '{ global: initpcie; local: *; };' > pcie.exp
	$(LINK) $(LFLAGS) -o $(TARGET) $(OFILES) $(LIBS)

install: $(TARGET)
	@test -d $(DESTDIR)/usr/lib/python2.7/dist-packages || mkdir -p $(DESTDIR)/usr/lib/python2.7/dist-packages
	cp -f $(TARGET) $(DESTDIR)/usr/lib/python2.7/dist-packages/$(TARGET)

clean:
	-rm -f $(TARGET)
	-rm -f sippciecmodule.o
	-rm -f sippcieuint64_t.o
	-rm -f sippciePythonPCIE.o
	-rm -f sippciestdvector1400.o
	-rm -f sippciestdvector1800.o
	-rm -f sippciestdvector2000.o
	-rm -f pcie.exp
