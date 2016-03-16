#------------------------------------------------------------------------------

CC=g++
CCFLAGS=
LDFLAGS=
LIBCCFLAGS=-Wall -Werror -fpic

PROJECT_INCLUDE_DIR=include
PROJECT_INCLUDES=python_pcie.h

SOURCE=python_pcie.cpp
LIB=pypcie

TEST_DIR=test
TEST_PROGRAM=test

SYS_INCLUDES=/usr/include

BUILD_DIR=build
SOURCE_DIR=src
INCLUDE_DIR=-Iinclude -I/usr/include



#------------------------------------------------------------------------------

# $@ = Target
# $^ = All Pre-requisits with duplicates removed



#all: $(MYPROGRAM)
#
#$(MYPROGRAM): $(SOURCE)
#	$(CC) -I$(MYINCLUDES) $(SOURCE) -o$(MYPROGRAM) -l$(MYLIBRARIES)


#all: $(BUILD_DIR)/$(LIB) $(BUILD_DIR)/$(TEST_PROGRAM)
all: LIBRARY

LIBRARY:$(BUILD_DIR)/lib$(LIB)

$(BUILD_DIR)/lib$(LIB):$(SOURCE_DIR)/$(SOURCE)
	@echo "Building Library"
	$(CC) -o $@ $(CCFLAGS) $(INCLUDE_DIR) -c $(LIBCCFLAGS) $<

#$(TEST_PROGRAM):$(BUILD_DIR)/$(TEST_PROGRAM).o
#	$(CC) -I$(PROJECT_INCLUDE_DIR)/$(PROJECT_INCLUDES) -o$(BUILD_DIR)/$(TEST_PROGRAM) $(TEST_DIR)/$(TEST_SOURCE)

#$(BUILD_DIR)/$(TEST_PROGRAM):$(BUILD_DIR)/$(TEST_PROGRAM).o
#	$(CC) -o $@ $(LDFLAGS) $^ 



#$(BUILD_DIR)/$(TEST_PROGRAM).o:$(TEST_DIR)/$(TEST_PROGRAM).cpp
$(BUILD_DIR)/$(TEST_PROGRAM):$(TEST_DIR)/$(TEST_PROGRAM).cpp
	@echo "Building Test application"
	$(CC) -o $@ -c $(CFLAGS) $<

clean:
	rm -rf $(BUILD_DIR)/*


