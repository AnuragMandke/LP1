def pass2(input_file, pass1_output_file, output_file):
    # Parse the Pass-1 output to reconstruct the MNT, MDT, KPTAB, and PNTAB
    mnt = []
    mdt = []
    kptab = {}
    pntab = {}

    # Read the Pass-1 output file
    with open(pass1_output_file, "r") as infile:
        section = None
        for line in infile:
            line = line.strip()
            if line.startswith("Macro Name Table (MNT):"):
                section = "MNT"
                next(infile)  # Skip the header line
                continue
            elif line.startswith("Macro Definition Table (MDT):"):
                section = "MDT"
                continue
            elif line.startswith("Keyword Parameter Table (KPTAB):"):
                section = "KPTAB"
                continue
            elif line.startswith("Parameter Name Table (PNTAB):"):
                section = "PNTAB"
                continue

            if section == "MNT" and line:
                parts = line.split()
                mnt.append({
                    "name": parts[1],
                    "pp_count": int(parts[2]),
                    "kp_count": int(parts[3]),
                    "mdt_pointer": int(parts[4]),
                    "kptab_pointer": int(parts[5]) if len(parts) > 5 else None
                })
            elif section == "MDT" and line:
                mdt.append(line.split(maxsplit=1)[1])  # Store the MDT instructions
            elif section == "KPTAB" and line:
                parts = line.split()
                kptab[parts[1]] = parts[2]  # Store parameter and default value
            elif section == "PNTAB" and line.startswith("Macro:"):
                macro_name = line.split(":")[1].strip()
                pntab[macro_name] = next(infile).split(":")[1].strip().split(", ")

    # Read the source code and process macro expansion
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            line = line.strip()

            # Check if the line is a macro invocation
            macro_call = None
            for macro in mnt:
                if line.startswith(macro["name"]):
                    macro_call = macro
                    break

            if macro_call:
                # Macro expansion logic
                macro_name = macro_call["name"]
                args = line.split()[1:]  # Extract arguments provided in the macro call

                # Replace parameters in the MDT using PNTAB and arguments
                for i in range(macro_call["mdt_pointer"], len(mdt)):
                    if mdt[i] == "MEND":
                        break
                    expanded_line = mdt[i]
                    param_list = pntab[macro_name]

                    # Replace parameters with actual arguments
                    for j, param in enumerate(param_list):
                        if j < len(args):  # Positional parameter
                            expanded_line = expanded_line.replace(param, args[j])
                        else:  # Keyword parameter
                            if param in kptab:
                                expanded_line = expanded_line.replace(param, kptab[param])

                    outfile.write(expanded_line + "\n")
            else:
                # Copy non-macro lines directly to the output file
                outfile.write(line + "\n")

    print(f"Pass-2 complete. Expanded code written to {output_file}.")


# Example usage
input_file = "/home/pict/31452_LP1/Practical-3/Input/source_code.asm"  # Original source code file
pass1_output_file = "/home/pict/31452_LP1/Practical-3/Output/pass1_output2.txt"  # Pass-1 output file
output_file = "/home/pict/31452_LP1/Practical-3/FinalOutput/expanded_output.asm"  # Final expanded assembly code

pass2(input_file, pass1_output_file, output_file)


