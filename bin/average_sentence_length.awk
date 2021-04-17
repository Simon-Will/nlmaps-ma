#!/usr/bin/env -S awk -f
BEGIN {
    FS=" ";
    OFS=": "
}
{ SUM += NF }
END {
    print "Tokens", SUM;
    print "Lines", NR;
    print "Avg Tokens/Line", SUM / NR;
}
