# Compilers
CC     = g++
MPICC  = mpic++

# Flags
CPP_VER   = -std=c++17
CFLAGS    = -Wall -c
OFLAGS    = -O3
OMP       = -fopenmp

# Boost paths
BOOST_ROOT = $(HOME)/boost_1_85_0_install
BOOST_INC  = -I$(BOOST_ROOT)/include
BOOST_LIB  = -L$(BOOST_ROOT)/lib
BOOST      = $(BOOST_LIB) -lboost_mpi -lboost_serialization

SRC_DIR   = src
INC_DIR   = include

EXEC      = qabb qapbb_sp qapbb_mp bound

# OS detection
ifeq ($(OS), Windows_NT) 
    RM        = del /Q
    EXEC_EXT  = .exe
else
    RM        = rm -f
    EXEC_EXT  =
endif

all: $(EXEC)


## Executables
qabb: main.o node.o matrices.o heuristics.o hungarian.o objective.o utils.o
	$(CC) $(CPP_VER) $(OFLAGS) $(OMP) $^ -o $@

qapbb_sp: main_sp.o node.o matrices.o heuristics.o hungarian.o objective.o utils.o
	$(MPICC) $(CPP_VER) $(OFLAGS) $(OMP) $^ -o $@ $(BOOST)

qapbb_mp: main_mp.o node.o matrices.o heuristics.o hungarian.o objective.o utils.o
	$(MPICC) $(CPP_VER) $(OFLAGS) $(OMP) $^ -o $@ $(BOOST)

bound: main_bound.o node.o matrices.o heuristics.o hungarian.o objective.o utils.o
	$(CC) $(CPP_VER) $(OFLAGS) $(OMP) $^ -o $@

## Objects
main.o: $(SRC_DIR)/main.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAGS) $(OMP) $(CFLAGS) $(BOOST_INC) $<

main_sp.o: $(SRC_DIR)/main_sp.cpp $(INC_DIR)/*.hpp
	$(MPICC) $(CPP_VER) $(OFLAGS) $(OMP) $(CFLAGS) $(BOOST_INC) $<

main_mp.o: $(SRC_DIR)/main_mp.cpp $(INC_DIR)/*.hpp
	$(MPICC) $(CPP_VER) $(OFLAGS) $(OMP) $(CFLAGS) $(BOOST_INC) $<

main_bound.o: $(SRC_DIR)/main_bound.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAGS) $(OMP) $(CFLAGS) $(BOOST_INC) $<

node.o: $(SRC_DIR)/node.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAGS) $(OMP) $(CFLAGS) $(BOOST_INC) $<

matrices.o: $(SRC_DIR)/matrices.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAGS) $(OMP) $(CFLAGS) $(BOOST_INC) $<

heuristics.o: $(SRC_DIR)/heuristics.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAGS) $(OMP) $(CFLAGS) $(BOOST_INC) $<

objective.o: $(SRC_DIR)/objective.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAGS) $(OMP) $(CFLAGS) $(BOOST_INC) $<

hungarian.o: $(SRC_DIR)/hungarian.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAGS) $(OMP) $(CFLAGS) $(BOOST_INC) $<

utils.o: $(SRC_DIR)/utils.cpp $(INC_DIR)/utils.hpp
	$(CC) $(CPP_VER) $(OFLAGS) $(OMP) $(CFLAGS) $(BOOST_INC) $<

## Clean
.PHONY: clean fclean

clean:
	$(RM) *.o

fclean: clean
	$(RM) $(EXEC)$(EXEC_EXT)
