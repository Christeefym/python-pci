#ifndef __NYSA_PCIE__
#define __NYSA_PCIE__

#include <stdint.h>

class PythonPCIE {
  private:
    //Private Variables
    int fd;
    void * mem;
    bool debug;
    uint64_t size;

    //Low Level interface
    int _write(uint64_t addr, uint64_t count, const uint8_t * data);
    int _read(uint64_t addr, uint64_t count, uint8_t * data);

    int _open_pcie(const char * path, uint64_t size);

  public:
    PythonPCIE (bool debug = false);
    ~PythonPCIE ();

    int open_pcie(const char * path, uint64_t size);

    bool is_open();
    int close_pcie();

    int write(uint64_t addr, uint64_t count, const uint8_t * data);
    int read(uint64_t addr, uint64_t count, uint8_t * data);



};

#endif //__NYSA_PCIE__
