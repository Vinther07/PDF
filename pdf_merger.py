import PyPDF2
import os
import sys # To demonstrate error handling by exiting if dummy files are missing

def merge_pdfs(input_paths: list[str], output_path: str):
    """
    Merges multiple PDF files into a single PDF file using PyPDF2.

    Args:
        input_paths: A list of strings, where each string is the file path
                     to an input PDF file. The files will be merged in the
                     order they appear in the list.
        output_path: A string, the file path where the merged PDF will be saved.

    Raises:
        ValueError: If the input_paths list is empty or not a list of strings.
        FileNotFoundError: If any of the input files do not exist.
        PyPDF2.errors.PdfReadError: If an input file is not a valid PDF
                                    or is encrypted and cannot be read.
        IOError: If there's an error writing the output file (e.g., permission issues).
        Exception: For any other unexpected errors during processing.
    """
    if not isinstance(input_paths, list) or not input_paths:
        raise ValueError("input_paths must be a non-empty list of file paths.")

    if not all(isinstance(p, str) for p in input_paths):
         raise ValueError("All elements in input_paths must be strings (file paths).")

    # Check if all input files exist before starting the merge
    for input_path in input_paths:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        if not os.path.isfile(input_path):
             raise FileNotFoundError(f"Input path is not a file: {input_path}")
        # Optional: Add check for file extension if strictly needed
        # if not input_path.lower().endswith('.pdf'):
        #     print(f"Warning: Input file {input_path} does not have a .pdf extension.")


    pdf_writer = PyPDF2.PdfWriter()

    print(f"Starting PDF merge process...")
    print(f"Input files: {input_paths}")
    print(f"Output file: {output_path}")

    try:
        for i, input_path in enumerate(input_paths):
            print(f"Processing file {i + 1}/{len(input_paths)}: {os.path.basename(input_path)}")
            try:
                # Use 'with' statement for proper file handling
                with open(input_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)

                    # Check if the PDF has pages (optional, but avoids issues with empty files)
                    if len(pdf_reader.pages) == 0:
                        print(f"Warning: Input file '{os.path.basename(input_path)}' is empty or contains no readable pages. Skipping.")
                        continue

                    # Add all pages from the current input file to the writer
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        pdf_writer.add_page(page)
                        # print(f"  - Added page {page_num + 1}") # Too verbose? Keep it simple

            except PyPDF2.errors.PdfReadError as e:
                # Specific error for bad PDF format or encryption
                raise PyPDF2.errors.PdfReadError(f"Error reading PDF file '{os.path.basename(input_path)}': {e}")
            except Exception as e:
                 # Catch any other unexpected error during reading/processing a single file
                 raise Exception(f"An unexpected error occurred while processing '{os.path.basename(input_path)}': {e}")


        # Ensure there is content to write after processing all files
        if len(pdf_writer.pages) == 0:
             print("No pages were added to the output PDF. This might be because all input files were empty or unreadable.")
             # Optionally raise an error here if an empty output file is not desired
             # raise ValueError("No pages could be read from the input files.")
             # Or, proceed to create an empty output file if that's acceptable.

        # Write the merged PDF to the output file
        # Create parent directories if they don't exist (optional, but useful)
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                print(f"Created output directory: {output_dir}")
            except OSError as e:
                raise IOError(f"Error creating output directory {output_dir}: {e}")


        with open(output_path, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

        print(f"Successfully merged {len(input_paths)} files into '{output_path}'")

    except (ValueError, FileNotFoundError, PyPDF2.errors.PdfReadError, IOError) as e:
        # Re-raise specific known errors for calling code to handle
        print(f"Merge failed: {e}")
        raise e # Propagate the specific error
    except Exception as e:
        # Catch any other unexpected error during the final write or other steps
        print(f"An unexpected error occurred during merge: {e}")
        raise e # Propagate the unexpected error


# --- Example Usage (for testing) ---
if __name__ == "__main__":
    # This block only runs when the script is executed directly.
    # In your main program, you would import and call merge_pdfs().

    print("--- PyPDF2 PDF Merge Example ---")

    # --- Instructions for creating dummy PDF files ---
    print("\n--- Setup ---")
    print("Please ensure you have a few small PDF files for testing in the same directory as this script.")
    print("For example, create 'dummy_file_1.pdf', 'dummy_file_2.pdf', 'dummy_file_3.pdf'.")
    print("You can use online tools or a PDF editor to create simple test files.")

    # Define dummy file names
    dummy_file_1 = "dummy_file_1.pdf"
    dummy_file_2 = "dummy_file_2.pdf"
    dummy_file_3 = "dummy_file_3.pdf" # Optional third file
    output_merged_two = "merged_output_two.pdf"
    output_merged_three = "merged_output_three.pdf"
    output_error_dir = "nonexistent_folder/error_output.pdf" # For testing output path error

    # --- Check if dummy files exist before running examples ---
    test_files_exist_two = os.path.exists(dummy_file_1) and os.path.exists(dummy_file_2)
    test_files_exist_three = test_files_exist_two and os.path.exists(dummy_file_3)


    if not test_files_exist_two:
        print("\nSkipping examples: Required test files ('dummy_file_1.pdf', 'dummy_file_2.pdf') not found.")
        print("Please create them to run the examples.")
        # sys.exit(1) # Uncomment to exit if files are missing

    else:
        # --- Example 1: Merge 2 files ---
        print("\n--- Running Example 1: Merging two files ---")
        try:
            input_files_two = [dummy_file_1, dummy_file_2]
            merge_pdfs(input_files_two, output_merged_two)
            print(f"Check your directory for '{output_merged_two}'")
        except Exception as e:
            print(f"Example 1 failed: {e}")

        # --- Example 2: Merge 3 files (if dummy_file_3 exists) ---
        if test_files_exist_three:
            print("\n--- Running Example 2: Merging three files ---")
            try:
                input_files_three = [dummy_file_1, dummy_file_2, dummy_file_3]
                merge_pdfs(input_files_three, output_merged_three)
                print(f"Check your directory for '{output_merged_three}'")
            except Exception as e:
                print(f"Example 2 failed: {e}")
        else:
            print("\nSkipping Example 2: Optional file 'dummy_file_3.pdf' not found.")


        # --- Example 3: Test error handling - non-existent input file ---
        print("\n--- Running Example 3: Testing error handling (non-existent input) ---")
        try:
            merge_pdfs([dummy_file_1, "non_existent_file.pdf"], "error_test_output.pdf")
        except FileNotFoundError as e:
            print(f"Caught expected error: {e}")
        except Exception as e:
            print(f"Caught unexpected error: {e}") # Should not happen for FileNotFoundError

        # --- Example 4: Test error handling - empty input list ---
        print("\n--- Running Example 4: Testing error handling (empty input list) ---")
        try:
            merge_pdfs([], "error_test_empty_input.pdf")
        except ValueError as e:
            print(f"Caught expected error: {e}")
        except Exception as e:
             print(f"Caught unexpected error: {e}") # Should not happen for ValueError

        # --- Example 5: Test error handling - invalid input list type ---
        print("\n--- Running Example 5: Testing error handling (invalid input list type) ---")
        try:
            merge_pdfs("not a list", "error_test_invalid_input_type.pdf") # Pass a string instead of list
        except ValueError as e:
            print(f"Caught expected error: {e}")
        except Exception as e:
             print(f"Caught unexpected error: {e}") # Should not happen for ValueError

        # --- Example 6: Test error handling - unable to write output file (e.g., bad directory) ---
        # Note: This example will create the parent directory "nonexistent_folder" due to os.makedirs
        # If you want to test a true write permission error, you'd need to point to a protected system path.
        print("\n--- Running Example 6: Testing error handling (unable to write output) ---")
        try:
             merge_pdfs([dummy_file_1], output_error_dir)
             # If os.makedirs succeeds, this might actually work, unless there are permission issues *within* the created folder.
             # To force an IOError, one might need to simulate a locked file or permission denial.
             # For this example, let's assume os.makedirs might fail or writing fails.
        except IOError as e:
             print(f"Caught expected error: {e}")
        except Exception as e:
             print(f"Caught unexpected error: {e}")