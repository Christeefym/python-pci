
#include "python_pcie.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string>
#include <vector>
#include <byteswap.h>

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/mman.h>
#include <unistd.h>

#define ERROR_CHECK(x)                                                        \
        do {                                                                  \
                if (x){                                                       \
                  fprintf(stderr, "Error at line %d, file %s (%d) [%s]\n",    \
                      __LINE__, __FILE__, errno, strerror(errno)); exit(1);   \
                }                                                             \
        } while(0)

#define DEBUG if (this->debug)


/* ltoh: little to host */
/* htol: little to host */
#if __BYTE_ORDER == __LITTLE_ENDIAN
#  define ltohl(x)       (x)
#  define ltohs(x)       (x)
#  define htoll(x)       (x)
#  define htols(x)       (x)
#elif __BYTE_ORDER == __BIG_ENDIAN
#  define ltohl(x)     __bswap_32(x)
#  define ltohs(x)     __bswap_16(x)
#  define htoll(x)     __bswap_32(x)
#  define htols(x)     __bswap_16(x)
#endif


//Constructor/Destructor
PythonPCIE::PythonPCIE (bool debug){
  //Configure the class
  //Initialize Variable
  this->fd = -1;
  this->mem = NULL;
  this->debug = false;
  this->size = 0;

  if (debug){
    this->debug = true;
    DEBUG printf("%s: Debug Enabled\n", __FILE__);
  }
}

PythonPCIE::~PythonPCIE (){
}

//Private Functions
int PythonPCIE::_write(uint64_t addr, uint64_t count, long * data){
  //Local Variables
  uint32_t * virt_addr = NULL;

  if (addr > size) {
    DEBUG printf("%s: Requested address is greater than the size of the memory!\n", __FILE__);
    return -1;
  }
  if (count > (size - addr)) {
    count = (size - addr);
    DEBUG printf("%s: Write request is too large, trimming read to %d\n", __FILE__, (unsigned int) count);
    return -2;
  }

  virt_addr = (uint32_t *) this->mem + addr;


  //*((char *) virt_addr) = data;
  //memcpy(virt_addr, data, count);
  for (uint64_t i = 0; i < count; i++){
  	DEBUG printf("%s: Data: 0x%08X \n", __FILE__, (uint32_t) data[i]);
    virt_addr[i] = htoll((uint32_t) data[i]);
  }

  return 0;
}

//The incomming value is the size of count
int PythonPCIE::_read(uint64_t addr, uint64_t count, long *data){
  //Local Variables
  uint32_t * virt_addr = NULL;

  if (addr > size) {
    DEBUG printf("%s: Requested address is greater than the size of the memory!\n", __FILE__);
    return -1;
  }
  if (count > (size - addr)) {
    count = (size - addr);
    DEBUG printf("%s: Read request is too large, trimming read to %d\n",  __FILE__, (unsigned int) count);
    return -2;
  }

  virt_addr = (uint32_t *) this->mem + addr;

  for (uint64_t i = 0; i < count; i++){
    DEBUG printf ("Data Read: 0x%02X\n",  virt_addr[i]);
    data[i] = (long) ltohl(virt_addr[i]);
  }
  //memcpy(data, virt_addr, count);
  return 0;
}

int PythonPCIE::_open_pcie(const char * path, uint64_t size){

  //Open the resource
  this->fd = open(path, O_RDWR | O_SYNC);

  //Now we have a file number
  ERROR_CHECK(this->fd == -1);
  if (this->fd == -1){
    //File number is bad return
    DEBUG printf("%s: Openning File Failed\n", __FILE__);
    return -1;
  }
  DEBUG printf("%s: Opened File: %s\n", __FILE__, path);

  //Have an open file, now map the memory location to our memory base
  this->mem = mmap(0, size, PROT_READ | PROT_WRITE, MAP_SHARED, this->fd, 0x00);
  ERROR_CHECK(this->mem == (void *) -1);
  if (this->mem == (void *) -1){
    DEBUG printf("%s: Failed to get memory, closing file\n", __FILE__);
    close(fd);
    return -2;
  }
  DEBUG printf("%s: Memory mapped successful, memory size: 0x%08X\n", __FILE__, (unsigned int )size);
  this->size = size;

  //Get the memory base
  return 0;
}

//Public Functions
int PythonPCIE::open_pcie(const char * path, uint64_t size){
  return _open_pcie(path, size);
}

int PythonPCIE::close_pcie(){
  if (this->fd == -1) {
    return 0;
  }
  ERROR_CHECK(munmap(this->mem, this->size) == -1);
  DEBUG printf("%s: Unmapped Memory\n", __FILE__);
  close(fd);
  DEBUG printf("%s: Closed File\n", __FILE__);

  return 0;
}

bool PythonPCIE::is_open(){
  return (this->fd != -1);
};

int PythonPCIE::write(uint64_t addr, std::vector<long> data){
  DEBUG printf("%s: in write\n", __FILE__);
  DEBUG printf("%s: Address: 0x%08X\n", __FILE__, (int) addr);
  long * data_arr = (long *) data.data();
  DEBUG printf("%s: Write Length: %d\n", __FILE__, (int) data.size());
  DEBUG printf("%s: write done\n", __FILE__);
  return this->_write(addr, (uint64_t) data.size(), data_arr);
}

std::vector<long> PythonPCIE::read(uint64_t addr, uint64_t length){
  int status = 0;
  DEBUG printf("%s: in read\n", __FILE__);
  DEBUG printf("%s: Address: 0x%08X\n", __FILE__, (int) addr);
  DEBUG printf("%s: Requested Length: %d\n", __FILE__, (int) length);
  std::vector<long> data(length);
  long * data_arr = (long *) data.data();
  DEBUG printf("%s: Vector Size: %d\n", __FILE__, (int) data.size());
  status = this->_read(addr, (uint64_t) data.size(), data_arr);
  if (status != 0)
    data.resize(0);

  DEBUG printf("%s: read done\n", __FILE__);
  return data;
}


