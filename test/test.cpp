
#include <cstdio>
#include "python_pcie.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <sys/types.h>

#define BAR0_OFFSET 0x10


//Byte 0 Significance
#define BAR_IO_SPACE    0x01 << 0

#define BAR_LOCATE_X32  0x00
#define BAR_LOCATE_1MB  0x01
#define BAR_LOCATE_X64  0x02

#define BAR_PREF        0x01 << 3


#define MEM_SIZE        0x0200000

#define MAX_DATA_SIZE   MEM_SIZE

#define DATA_SIZE       2
//#define DATA_ADDR       0x0060000
#define DATA_ADDR       0x0018000

//const char * test_path = "/sys/bus/pci/devices/0000:01:00.0/resource0\0";
const char * test_path = "/dev/xdma/card0/user";
const char * config_path = "/sys/bus/pci/devices/0000:01:00.0/config\0";

int main(){
  PythonPCIE * p = NULL;
  std::ifstream config_file;
  std::streampos config_size;
  char * config_data;
  //char * read_data;
  std::vector<long> read_data; 
  uint32_t test_data = 0;
  uint32_t resource_size = MEM_SIZE;
  int retval;

/*
  printf ("Attempt to open config file: %s\n", config_path);

  config_file.open(config_path, std::ios::binary|std::ios::in|std::ios::ate);
  config_size = config_file.tellg();

//Declare an array that holds the entire data
  config_data = new char [(int) config_size];

  printf ("Config Space Size: %d\n", (int)config_size);
  config_file.seekg(0, std::ios::beg);
  config_file.read(config_data, config_size);
  config_file.close();

  //for (int i = 0; i < config_size; i = i + 4){
  //  printf ("[0x%04X] %02X %02X %02X %02X\n", i, config_data[i + 0], config_data[i + 1], config_data[i + 2], config_data[i + 3]);
  //}

  if (config_data[BAR0_OFFSET + 0] & BAR_IO_SPACE)
    printf ("IO Address Space\n");
  else
    printf ("Mem Address Space\n");

  test_data = (config_data[BAR0_OFFSET + 0] >> 1) & 0x03;
  switch (test_data) {
    case(BAR_LOCATE_X32):
      printf ("Locate in 32-bit address space\n");
      break;
    case(BAR_LOCATE_1MB):
      printf ("Locate in 1MBit address space\n");
      break;
    case(BAR_LOCATE_X64):
      printf ("Locate in 64-bit address space\n");
      break;
    default:
      printf ("Locate Unknown\n");
      break;
  }
*/
  //Get Address Size of memory
  /*
  test_data = config_data[BAR0_OFFSET + 8]
  */


  p = new PythonPCIE(true);
  printf ("Is Open? (Should be False): ");
  if (p->is_open()){
    printf ("True\n");
    return 1;
  }
  else
    printf ("False\n");

  printf ("Resource Size: 0x%08X\n", resource_size);
  printf ("Attempt to open resource %s\n", test_path);
  p->open_pcie(test_path, resource_size);

  printf ("Is Open? (Should be True): ");
  if (p->is_open())
    printf ("True\n");
  else {
    printf ("False\n");
    return 1;
  }

  //read_data = new char [(int)MAX_DATA_SIZE];
	std::vector<long> data(2);
	data[0] = 0x01234567;
	data[1] = 0x89ABCDEF;
	p->write(DATA_ADDR, data);

  read_data = p->read(DATA_ADDR, DATA_SIZE);
  if (read_data.size() != DATA_SIZE){
    printf ("Error while reading\n");
  }
  else {
    printf ("Read Data from 0x%08X:\n", DATA_ADDR);
    for (int i = 0; i < DATA_SIZE; i++){
      printf ("\t[0x%08X]: %08X\n", DATA_ADDR + i, (uint32_t) read_data[i]);
    }
  }
  printf ("Close\n");


  p->close_pcie();
  //delete (config_data);
  delete(p);
  return 0;
}

