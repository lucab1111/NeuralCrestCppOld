# Compile NeuralCrest model with clang++ compiler

CC := /opt/homebrew/Cellar/llvm/13.0.1_1/bin/clang++
SRCDIR := src
SRCEXT := cpp
SOURCES := $(shell find $(SRCDIR) -type f -name *.$(SRCEXT))
BUILDDIR := build
OBJECTS := $(patsubst $(SRCDIR)/%,$(BUILDDIR)/%,$(SOURCES:.$(SRCEXT)=.o))
TARGET := NeuralCrest
#CFLAGS := -c -Wall -std=c++11 -g -O0 #Uncomment this line to compile for debugging
CFLAGS := -c -O3 -std=c++11	#Uncomment this line to compile for fast runs
LIB := -larmadillo
INC := -I include armadillo

$(TARGET): $(OBJECTS)
	@echo " Linking..."
	@echo " $(CC) $^ -o $(TARGET) $(LIB)"; $(CC) $^ -o $(TARGET) $(LIB)

$(BUILDDIR)/%.o: $(SRCDIR)/%.$(SRCEXT)
	@mkdir -p $(BUILDDIR)
	@echo " $(CC) $(CFLAGS) $(INC) -c -o $@ $<"; $(CC) $(CFLAGS) $(INC) -c -o $@ $<

clean:
	@echo " Cleaning...";
	@echo " $(RM) -r $(BUILDDIR) $(TARGET)"; $(RM) -r $(BUILDDIR) $(TARGET)
