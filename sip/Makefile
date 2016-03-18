TARGET = pcie.so
OFILES = sippciecmodule.o sippcieuint8_t.o sippcieuint64_t.o sippciePythonPCIE.o
HFILES = sipAPIpcie.h 

CC = gcc
CXX = g++
LINK = g++
CPPFLAGS = -DNDEBUG -I. -I/home/cospan/anaconda/include/python2.7
CFLAGS = -pipe -fPIC -O2 -Wall -W
CXXFLAGS = -pipe -fPIC -O2 -Wall -W
LFLAGS = -shared -Wl,--version-script=pcie.exp
LIBS = -L../lib -lpypcie
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
	@test -d $(DESTDIR)/home/cospan/anaconda/lib/python2.7/site-packages || mkdir -p $(DESTDIR)/home/cospan/anaconda/lib/python2.7/site-packages
	cp -f $(TARGET) $(DESTDIR)/home/cospan/anaconda/lib/python2.7/site-packages/$(TARGET)
	strip $(DESTDIR)/home/cospan/anaconda/lib/python2.7/site-packages/$(TARGET)

clean:
	-rm -f $(TARGET)
	-rm -f sippciecmodule.o
	-rm -f sippcieuint8_t.o
	-rm -f sippcieuint64_t.o
	-rm -f sippciePythonPCIE.o
	-rm -f pcie.exp
