import sys

def calculate_window_average_depth(depth_file, window_size):
    # Initialize variables
    current_chrom = None
    current_window_start = None
    current_window_end = None
    current_depth_sum = 0
    current_depth_count = 0

    # Open the depth file
    with open(depth_file, 'r') as f:
        for line in f:
            # Skip comment lines or empty lines
            if line.startswith('#') or not line.strip():
                continue

            # Parse the line
            chrom, pos, depth = line.strip().split()
            chrom = chrom
            pos = int(pos)
            depth = int(depth)

            # If we are on a new chromosome or need to start a new window
            if chrom != current_chrom:
                # Print the last window (if any)
                if current_chrom is not None:
                    print_window(current_chrom, current_window_start, current_window_end, current_depth_sum, current_depth_count)

                # Start a new window
                current_chrom = chrom
                current_window_start = pos
                current_window_end = pos + window_size - 1
                current_depth_sum = depth
                current_depth_count = 1
            else:
                # Check if we need to finish the current window
                if pos > current_window_end:
                    # Print the last window
                    print_window(current_chrom, current_window_start, current_window_end, current_depth_sum, current_depth_count)

                    # Start a new window
                    current_window_start = pos
                    current_window_end = pos + window_size - 1
                    current_depth_sum = depth
                    current_depth_count = 1
                else:
                    # Add to the current window
                    current_depth_sum += depth
                    current_depth_count += 1

        # Print the last window after processing all lines
        if current_chrom is not None:
            print_window(current_chrom, current_window_start, current_window_end, current_depth_sum, current_depth_count)

def print_window(chrom, window_start, window_end, depth_sum, depth_count):
    # Adjust the window end position to the last position if it's smaller than the window size
    window_end = min(window_end, window_start + depth_count - 1)
    
    # Calculate mean depth
    mean_depth = depth_sum / depth_count
    
    # Print the results
    print(f"{chrom}\t{window_start}\t{window_end}\t{mean_depth:.2f}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python calculate_depth_window.py <depth_file> <window_size>")
        sys.exit(1)

    depth_file = sys.argv[1]
    window_size = int(sys.argv[2])

    calculate_window_average_depth(depth_file, window_size)
