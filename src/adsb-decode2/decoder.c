#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "decoder.h"
#include "sample.h"

int decoder_dispatch(SAMPLE_PTR sample)
{
	if (sample->df == 11) {
		printf("downlink format 11\n");
	}
	else if ((sample->df == 17) || (sample->df == 18)) {
		return sample_df_17_18_parser(sample);
	}
	else {
		printf("downlink format default\n");
	}

	return EXIT_SUCCESS;
}

int string_to_decoder(const char *raw_buffer)
{
	SAMPLE_PTR sample = (SAMPLE_PTR)malloc(sizeof(OBSERVATION));
	if (sample == (SAMPLE_PTR)NULL) {
		fprintf(stderr, "failed to allocate memory\n");
		return ALLOC_FAILURE;
	}

	strncpy(sample->raw_sample, raw_buffer, MAX_RAW_SAMPLE_LENGTH);

	int retflag = sample_converter(sample);
	if (retflag != EXIT_SUCCESS) {
		return retflag;
	}

	sample_dumper(sample);

	retflag = decoder_dispatch(sample);
	sample_dumper(sample);

	return retflag;
}
