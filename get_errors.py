

import sys

if len(sys.argv) != 2:
  sys.stderr.write("Usage python check_errors.py <quality_string>")

def calculate_quality_score(quality_string):

    error_probability = 0
    for x in quality_string:
        try:
            phred = ord(x)
            if phred < 33 or phred > 75:
                raise ValueError()
            error_probability += 10**-((phred-33)/10.0)
        except ValueError:
            # If a quality value outside of Illumina1.8 format is detected, exit with an informatice message
            sys.stderr.write("ERROR: Encountered a non-supported quality value - %s\n" % x)
            sys.stderr.write("Only Illumina1.8 format quality values are supported\n")
            sys.stderr.write("Found in the %s input file in read %s - %s\n" % (input_file, item_name, quality_string) )
            sys.exit(1)

    return error_probability

print("Expected Errors: %.4f" % calculate_quality_score(sys.argv[1]))
