#------------------------------------------------------------------------------

MKDIR_P = mkdir -p

PROJECT_INCLUDES=python_pcie.h

SOURCE=python_pcie.cpp
LIB=pypcie

TEST_PROGRAM=test
SYS_INCLUDES=/usr/include

#Directories
TEST_DIR=test
LIB_DIR=lib
OUT_DIR=build
SOURCE_DIR=src
INC_DIR=include
SYS_INC_DIR=/usr/include
OBJ_DIR=obj


#Flags
CC=g++
CCFLAGS=-I$(INC_DIR) -I$(SYS_INC_DIR)
OFLAGS=-c

LDFLAGS=-L$(LIB_DIR) -l$(LIB)
LIBCCFLAGS=-Wall -Werror -fpic

#------------------------------------------------------------------------------

# $@ = Target
# $^ = All Pre-requisits with duplicates removed

all: directories library ctest

library:$(LIB_DIR)/lib$(LIB).so
ctest:$(OUT_DIR)/$(TEST_PROGRAM)
directories: ${OUT_DIR} ${LIB_DIR} ${OBJ_DIR}

#cpp -> shared object library
$(LIB_DIR)/lib$(LIB).so:$(SOURCE_DIR)/$(SOURCE)
	@echo "Building Library"
	$(CC) -o $@ $(CCFLAGS) $(OFLAGS) $(LIBCCFLAGS) $<


#Test Program Build Instructions
#cpp -> obj
$(OBJ_DIR)/$(TEST_PROGRAM).o:$(TEST_DIR)/$(TEST_PROGRAM).cpp
	@echo "Compiling Test application object"
	$(CC) -o $@ $(CCFLAGS) $(OFLAGS) $<

#obj -> exe
$(OUT_DIR)/$(TEST_PROGRAM):$(OBJ_DIR)/$(TEST_PROGRAM).o
	@echo "Building Test application"
	$(CC) -o $@ $(LDFLAGS) $<

.PHONY: clean directories

clean:
	rm -rf $(OUT_DIR)/*
	rm -rf $(LIB_DIR)/*
	rm -rf $(OBJ_DIR)/*


${OUT_DIR}:
	@echo "Creating output directory"
	@${MKDIR_P} ${OUT_DIR}

${OBJ_DIR}:
	@echo "Creating obj directory"
	@${MKDIR_P} ${OBJ_DIR}

${LIB_DIR}:
	@echo "Creating lib directory"
	@${MKDIR_P} ${LIB_DIR}


