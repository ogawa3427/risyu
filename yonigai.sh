#!/bin/bash
awk -F, '{
    result = $1;
    for (i = 2; i <= NF; i++) {
        if (i != 4) {
            result = result "," $i
        }
    }
    print result
}' 2023q4.csv
