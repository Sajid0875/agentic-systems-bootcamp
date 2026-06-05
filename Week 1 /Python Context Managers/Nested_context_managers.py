with open("Source.txt","r") as source_file:
    with open("Destination.txt","w") as destination_file:
        for line in source_file:
            destination_file.write(line)