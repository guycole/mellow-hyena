#
# Title:makefile
#
# Description: makefile for adsb-decoder
#

#
# Directories.
#
DEVDIR = $(HOME)
INCDIR = $(DEVDIR)/include
LIBDIR = $(DEVDIR)/lib

#
# Header Files.
#
DECODER_H = decoder.h
SAMPLE_H = sample.h
UTILITY_H = utility.h

#
# Libraries.
#

#
# Configurations.
#
CMACS  = -DTRACE=1
CFLAGS = -g -Wall -I$(INCDIR)

#
# Tools.
#
CC = gcc
INDENT = indent

#
# Executable Names.
#
DECODER = decoder

#
# Object Files.
#
OBJS = main.o decoder.o sample.o utility.o

#
# Finally, some work...
#
all: $(DECODER)

$(DECODER): $(OBJS)
	$(CC) -o $(DECODER) $(OBJS)

main.o: main.c $(DECODER_H)
	$(CC) -c $(CFLAGS) $(CMACS) main.c

decoder.o: decoder.c $(DECODER_H) $(SAMPLE_H)
	$(CC) -c $(CFLAGS) $(CMACS) decoder.c

sample.o: sample.c $(SAMPLE_H) $(UTILITY_H)
	$(CC) -c $(CFLAGS) $(CMACS) sample.c

utility.o: $(SAMPLE_H) $(UTILITY_H)
	$(CC) -c $(CFLAGS) $(CMACS) utility.c

#
#
#
indent:
	-$(INDENT) -linux *.c *.h

#
#  Determine the size of source files in this subdirectory. 
#
size:
	-@echo "Size: `pwd`"
	-@wc -l *.c makefile

#
#  Cleanup this subdirectory.
#
clean:
	-rm -f *.o *.BAK core *.aux *.dvi *.log *~

#
#  Nuke all the executables and PostScript
#
ultraclean:
	-rm -f $(DECODER)
