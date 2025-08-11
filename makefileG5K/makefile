CC = g++
MPICC = mpic++

CPP_VER = -std=c++17
CFLAG = -Wall -c
OFLAG = -O3
OMP = -fopenmp

BOOST = -lboost_mpi -lboost_serialization

SRC_DIR = src
INC_DIR = include

EXEC = qabb qapbb_sp qapbb_mp bound

# OS detection
ifeq ($(OS), Windows_NT) 
    RM = del /Q
    EXEC_EXT = .exe
else
    RM = rm -f
    EXEC_EXT =
endif

all: $(EXEC)

## executables
qabb: main.o node.o matrices.o heuristics.o hungarian.o objective.o utils.o
	$(CC) $(CPP_VER) $(OFLAG) $(OMP) $^ -o $@

qapbb_sp: main_sp.o node.o matrices.o heuristics.o hungarian.o objective.o utils.o
	$(MPICC) $(CPP_VER) $(OFLAG) $(OMP) $^ -o $@ $(BOOST)

qapbb_mp: main_mp.o node.o matrices.o heuristics.o hungarian.o objective.o utils.o
	$(MPICC) $(CPP_VER) $(OFLAG) $(OMP) $^ -o $@ $(BOOST)

bound: main_bound.o node.o matrices.o heuristics.o hungarian.o objective.o utils.o
	$(CC) $(CPP_VER) $(OFLAG) $(OMP) $^ -o $@

## objects
main.o: $(SRC_DIR)/main.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAG) $(OMP) $(CFLAG) $<

main_sp.o: $(SRC_DIR)/main_sp.cpp $(INC_DIR)/*.hpp
	$(MPICC) $(CPP_VER) $(OFLAG) $(OMP) $(CFLAG) $< $(BOOST)

main_mp.o: $(SRC_DIR)/main_mp.cpp $(INC_DIR)/*.hpp
	$(MPICC) $(CPP_VER) $(OFLAG) $(OMP) $(CFLAG) $< $(BOOST)

main_bound.o: $(SRC_DIR)/main_bound.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAG) $(OMP) $(CFLAG) $<

node.o: $(SRC_DIR)/node.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAG) $(OMP) $(CFLAG) $< $(BOOST)

matrices.o: $(SRC_DIR)/matrices.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAG) $(OMP) $(CFLAG) $< $(BOOST)

heuristics.o: $(SRC_DIR)/heuristics.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAG) $(OMP) $(CFLAG) $<

objective.o: $(SRC_DIR)/objective.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAG) $(OMP) $(CFLAG) $<

hungarian.o: $(SRC_DIR)/hungarian.cpp $(INC_DIR)/*.hpp
	$(CC) $(CPP_VER) $(OFLAG) $(OMP) $(CFLAG) $<

utils.o: $(SRC_DIR)/utils.cpp $(INC_DIR)/utils.hpp
	$(CC) $(CPP_VER) $(OFLAG) $(OMP) $(CFLAG) $<


## clean
.PHONY: clean fclean

clean:
	$(RM) *.o

fclean: clean
	$(RM) $(EXEC)$(EXEC_EXT)
