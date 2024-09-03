#!/bin/bash

# Configuration
OUTPUT_FILE="project_overview.txt"
INCLUDE_EXTENSIONS=("py" "md")

# Function to check if a file should be included
should_include_file() {
    local file="$1"
    for ext in "${INCLUDE_EXTENSIONS[@]}"; do
        if [[ "$file" == *.$ext ]]; then
            return 0
        fi
    done
    return 1
}

# Clear existing output file
> "$OUTPUT_FILE"

# Process each file in the git repository
git ls-files | while read -r file; do
    if should_include_file "$file"; then
        echo "<document>" >> "$OUTPUT_FILE"
        echo "<source>$file</source>" >> "$OUTPUT_FILE"
        echo "<document_content>" >> "$OUTPUT_FILE"
        cat "$file" >> "$OUTPUT_FILE"
        echo "</document_content>" >> "$OUTPUT_FILE"
        echo "</document>" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"  # Add a blank line between documents
    fi
done

echo "Project overview generated in $OUTPUT_FILE"