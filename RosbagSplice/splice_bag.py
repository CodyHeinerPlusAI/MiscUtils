#! /usr/bin/python

# Objective:
# Conveniently splice a given bag file from specified start time to start time + duration.
#
# Example usage:
# ./splice_bag.sh input_bag.bag 60 20 output_bag.bag
# saves the segment of the input_bag.bag from 60 seconds to 80 seconds to output_bag.bag
# 
# Note: to update to Python 3, change subprocess.call to subprocess.run.

from __future__ import print_function, division

import subprocess
import sys

def SpliceBag(input_bag_path, start_time_seconds, duration_seconds, output_bag_path):
    # Bag filtering occurs in bag time, so we find the conversion offset with the command:
    # rosbag info -y -k start <bag_path>
    bagtime_offset_command_list = ["rosbag", "info", "-y", "-k", "start", input_bag_path]
    bagtime_offset = float(subprocess.check_output(bagtime_offset_command_list))
    start_time_bagtime = bagtime_offset + start_time_seconds
    end_time_bagtime = start_time_bagtime + duration_seconds
    # Use rosbag filter to splice out desired section of bag
    filter_string = ("(t.secs >= " + str(start_time_bagtime) +
        ") and (t.secs <= " + str(end_time_bagtime) + ")")
    filter_command_list = ["rosbag", "filter", input_bag_path, output_bag_path, filter_string]
    print("Running filter command:", " ".join(filter_command_list), sep="\n")
    subprocess.call(filter_command_list)
    print("Filtered bag written to", output_bag_path)

def main():
    # Parse arguments
    if len(sys.argv) != 5:
        print("Usage:", sys.argv[0],
            "<input_bag> <start_time_seconds> <duration_seconds> <output_bag>")
        sys.exit()
    input_bag_path = sys.argv[1]
    start_time_seconds = float(sys.argv[2])
    duration_seconds = float(sys.argv[3])
    output_bag_path = sys.argv[4]
    SpliceBag(input_bag_path, start_time_seconds, duration_seconds, output_bag_path)
    
    


main()









'''
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <input_bag> <start_time_seconds> <duration_seconds> <output_bag>"
    exit -1
fi

# Parse parameters
input_bag_path="$1"
start_time_seconds="$2"
duration_seconds="$3"
output_bag_path="$4"

bag_start_time=`rosbag info -y -k start "$input_bag_path"`
filter_string="(t.secs >= $bag_start_time) and "
rosbag filter "$input_bag_path" "$output_bag_path"
'''
